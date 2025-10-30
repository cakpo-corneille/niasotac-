from django.db import models
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
import urllib.parse
from datetime import datetime
import pytz  

def validate_image_size(image):
    """Valider que l'image ne dépasse pas 2MB"""
    filesize = image.size
    if filesize > 2 * 1024 * 1024:
        raise ValidationError("La taille maximale du fichier est 2MB")


class Category(models.Model):
    """Modèle pour les catégories et sous-catégories de produits"""
    name = models.CharField(max_length=100, verbose_name="Nom")
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    icon = models.CharField(
        max_length=100,
        blank=False,
        verbose_name="Icône",
        help_text="Classe CSS (ex: fa fa-laptop) ou nom de fichier .ico"
    )
    icon_file = models.FileField(
        upload_to='icons/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['ico'])],
        verbose_name="Fichier .ico"
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories',
        verbose_name="Catégorie parente"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['name']

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_descendants(self):
        """Retourne toutes les sous-catégories récursivement"""
        descendants = []

        def collect(categorie):
            children = Category.objects.filter(parent=categorie)
            for child in children:
                descendants.append(child)
                collect(child)

        collect(self)
        return descendants

    @property
    def is_main_category(self):
        """Vérifie si c'est une catégorie principale"""
        return self.parent is None

    @property
    def product_count(self):
        """Compte le nombre de produits dans cette catégorie"""
        return self.products.count()

    def get_all_products(self):
        """Retourne tous les produits liés à cette catégorie ou ses sous-catégories"""
        return Product.objects.filter(
            models.Q(category=self) | models.Q(category__parent=self)
        )


class Product(models.Model):
    """Modèle pour les produits de la vitrine"""
    name = models.CharField(max_length=200, verbose_name="Nom du produit")
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(verbose_name="Description")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Prix (FCFA)"
    )
    brand = models.CharField(max_length=100, verbose_name="Marque")
    image = models.ImageField(
        upload_to='products/',
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
            validate_image_size
        ],
        verbose_name="Image du produit"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Catégorie"
    )
    in_stock = models.BooleanField(default=True, verbose_name="En stock")
    featured = models.BooleanField(default=False, verbose_name="Produit vedette")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.brand}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.brand}")
        super().save(*args, **kwargs)


    @property
    def whatsapp_link(self):
        """Génère un lien WhatsApp avec message pré-rempli incluant l'image et salutation selon l'heure"""
        settings = SiteSettings.load()
        phone_number = settings.whatsapp_number
        image_url = self.get_image_url()

        # 🕒 Heure locale au Bénin
        benin_tz = pytz.timezone("Africa/Porto-Novo")
        current_hour = datetime.now(benin_tz).hour

        # 👋 Salutation selon l'heure
        salutation = "Bonsoir" if current_hour >= 12 else "Bonjour"

        message = f"""{salutation} {settings.company_name},

        Je suis intéressé(e) par le produit suivant:

        📱 *{self.name}*
        🏷️ Marque: {self.brand}
        💰 Prix: {self.price} FCFA
        🖼️ Image: {image_url}

        Merci de me contacter pour plus d'informations."""

        encoded_message = urllib.parse.quote(message)
        return f"https://wa.me/{phone_number}?text={encoded_message}"

    @property
    def display_price(self):
        """Retourne le prix formaté"""
        return f"{self.price:,.0f} FCFA"

    def get_image_url(self):
        """Retourne l'URL de l'image ou une image par défaut"""
        if self.image:
            return self.image.url
        return '/static/defaults/default_product.png'


class ProductImage(models.Model):
    """Images supplémentaires pour un produit (max 10)"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image de {self.product.name}"

    def save(self, *args, **kwargs):
        if self.product.images.count() >= 10:
            raise ValidationError("Maximum 10 images par produit.")
        super().save(*args, **kwargs)

    def get_image_url(self):
        if self.image:
            return self.image.url
        return '/static/defaults/default_product.png'


class SiteSettings(models.Model):
    """Paramètres globaux du site (Singleton)"""
    whatsapp_number = models.CharField(
        max_length=20,
        default="237XXXXXXXXX",
        verbose_name="Numéro WhatsApp",
        help_text="Format: 237XXXXXXXXX (sans le +)"
    )
    contact_email = models.EmailField(
        default="contact@niasotac.com",
        verbose_name="Email de contact"
    )
    contact_phone = models.CharField(
        max_length=20,
        default="+229 00 00 00 00",
        verbose_name="Téléphone de contact"
    )
    contact_address = models.CharField(
        max_length=200,
        default="Cotonou, Bénin",
        verbose_name="Adresse"
    )
    company_name = models.CharField(
        max_length=100,
        default="NIASOTAC TECHNOLOGIE",
        verbose_name="Nom de l'entreprise"
    )
    company_description = models.TextField(
        default="Votre revendeur tech de confiance au Bénin. Produits de qualité à prix compétitifs.",
        verbose_name="Description de l'entreprise"
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Modifié par"
    )

    class Meta:
        verbose_name = "Paramètres du site"
        verbose_name_plural = "Paramètres du site"

    def __str__(self):
        return "Paramètres du site"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        """Charge ou crée les paramètres du site"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
