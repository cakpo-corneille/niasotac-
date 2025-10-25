from django.db import models
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
import urllib.parse


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
        max_length=50, 
        blank=True, 
        null=True,
        verbose_name="Icône",
        help_text="Nom de l'icône (ex: laptop, printer, etc.)"
    )
    image = models.ImageField(
        upload_to='categories/',
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
            validate_image_size
        ],
        verbose_name="Image"
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

    @property
    def is_main_category(self):
        """Vérifie si c'est une catégorie principale"""
        return self.parent is None

    @property
    def product_count(self):
        """Compte le nombre de produits dans cette catégorie"""
        return self.products.count()


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
        limit_choices_to={'parent__isnull': True},
        verbose_name="Catégorie principale"
    )
    subcategory = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subcategory_products',
        verbose_name="Sous-catégorie"
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
        """Génère un lien WhatsApp avec message pré-rempli"""
        phone_number = "237XXXXXXXXX"
        message = f"""Bonjour NIASOTAC TECHNOLOGIE,

Je suis intéressé(e) par le produit suivant:

📱 *{self.name}*
🏷️ Marque: {self.brand}
💰 Prix: {self.price} FCFA

Merci de me contacter pour plus d'informations."""
        
        encoded_message = urllib.parse.quote(message)
        return f"https://wa.me/{phone_number}?text={encoded_message}"

    @property
    def display_price(self):
        """Retourne le prix formaté"""
        return f"{self.price:,.0f} FCFA"
