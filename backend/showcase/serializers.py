from rest_framework import serializers
from .models import Category, Product


class SubcategorySerializer(serializers.ModelSerializer):
    """Serializer pour les sous-catégories"""
    product_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon', 'image', 'product_count']


class CategorySerializer(serializers.ModelSerializer):
    """Serializer pour les catégories principales"""
    subcategories = SubcategorySerializer(many=True, read_only=True)
    product_count = serializers.ReadOnlyField()
    is_main_category = serializers.ReadOnlyField()
    
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'icon', 'image', 'parent',
            'subcategories', 'product_count', 'is_main_category',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']


class ProductSerializer(serializers.ModelSerializer):
    """Serializer pour les produits"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    subcategory_name = serializers.CharField(source='subcategory.name', read_only=True)
    whatsapp_link = serializers.ReadOnlyField()
    display_price = serializers.ReadOnlyField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price', 'display_price',
            'brand', 'image', 'category', 'category_name', 'subcategory',
            'subcategory_name', 'in_stock', 'featured', 'whatsapp_link',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']

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
    subcategory_name = serializers.CharField(source='subcategory.name', read_only=True)
    display_price = serializers.ReadOnlyField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'price', 'display_price', 'brand',
            'image', 'category_name', 'subcategory_name', 'in_stock',
            'featured', 'created_at'
        ]
