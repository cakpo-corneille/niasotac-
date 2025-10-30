from rest_framework import serializers
from .models import Category, Product, ProductImage, SiteSettings


class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer pour les images supplémentaires d'un produit"""
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['id', 'image']

    def get_image(self, obj):
        request = self.context.get('request')
        url = obj.get_image_url()
        return request.build_absolute_uri(url) if request else url


class ProductSerializer(serializers.ModelSerializer):
    """Serializer complet pour les produits"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    whatsapp_link = serializers.ReadOnlyField()
    display_price = serializers.ReadOnlyField()
    image = serializers.SerializerMethodField()
    gallery = ProductImageSerializer(source='images', many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price', 'display_price',
            'brand', 'image', 'category', 'category_name',
            'in_stock', 'featured', 'whatsapp_link',
            'gallery', 'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']

    def get_image(self, obj):
        request = self.context.get('request')
        url = obj.get_image_url()
        return request.build_absolute_uri(url) if request else url

    def validate_image(self, value):
        """Valider la taille et le type de l'image"""
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError("La taille de l'image ne doit pas dépasser 2MB")
        allowed_extensions = ['jpg', 'jpeg', 'png']
        ext = value.name.split('.')[-1].lower()
        if ext not in allowed_extensions:
            raise serializers.ValidationError(
                f"Format non supporté. Utilisez: {', '.join(allowed_extensions)}"
            )
        return value


class ProductListSerializer(serializers.ModelSerializer):
    """Serializer simplifié pour les listes de produits"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    display_price = serializers.ReadOnlyField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'price', 'display_price', 'brand',
            'image', 'category_name', 'in_stock',
            'featured', 'created_at'
        ]

    def get_image(self, obj):
        request = self.context.get('request')
        url = obj.get_image_url()
        return request.build_absolute_uri(url) if request else url


class CategorySerializer(serializers.ModelSerializer):
    """Serializer pour les catégories avec sous-catégories"""
    subcategories = serializers.SerializerMethodField()
    product_count = serializers.ReadOnlyField()
    is_main_category = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'icon', 'icon_file', 'parent',
            'subcategories', 'product_count', 'is_main_category',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']

    def get_subcategories(self, obj):
        subs = obj.subcategories.all()
        return SubcategorySerializer(subs, many=True, context=self.context).data


class SubcategorySerializer(serializers.ModelSerializer):
    """Serializer pour les sous-catégories"""
    product_count = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon', 'icon_file', 'product_count']


class SiteSettingsSerializer(serializers.ModelSerializer):
    """Serializer pour les paramètres du site"""

    class Meta:
        model = SiteSettings
        fields = [
            'whatsapp_number', 'contact_email', 'contact_phone',
            'contact_address', 'company_name', 'company_description',
            'updated_at'
        ]
        read_only_fields = ['updated_at']
