from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Administration personnalisée pour les catégories"""
    list_display = ['name', 'parent', 'product_count', 'icon', 'image_preview', 'created_at']
    list_filter = ['parent', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at', 'image_preview']
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('name', 'slug', 'parent')
        }),
        ('Médias', {
            'fields': ('icon', 'image', 'image_preview')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        """Affiche un aperçu de l'image"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 150px;" />',
                obj.image.url
            )
        return "Pas d'image"
    image_preview.short_description = "Aperçu"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _product_count=Count('products', distinct=True)
        )
        return queryset

    def product_count(self, obj):
        """Affiche le nombre de produits"""
        return obj._product_count
    product_count.short_description = "Nombre de produits"
    product_count.admin_order_field = '_product_count'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Administration personnalisée pour les produits"""
    list_display = [
        'name', 'brand', 'price_display', 'category', 'subcategory',
        'in_stock', 'featured', 'image_preview', 'created_at'
    ]
    list_filter = ['category', 'subcategory', 'brand', 'in_stock', 'featured', 'created_at']
    search_fields = ['name', 'brand', 'description']
    prepopulated_fields = {'slug': ('name', 'brand')}
    readonly_fields = ['created_at', 'updated_at', 'whatsapp_link', 'image_preview']
    list_editable = ['in_stock', 'featured']
    
    fieldsets = (
        ('Informations produit', {
            'fields': ('name', 'slug', 'brand', 'description')
        }),
        ('Prix et catégories', {
            'fields': ('price', 'category', 'subcategory')
        }),
        ('Médias', {
            'fields': ('image', 'image_preview')
        }),
        ('Options', {
            'fields': ('in_stock', 'featured')
        }),
        ('WhatsApp', {
            'fields': ('whatsapp_link',),
            'classes': ('collapse',)
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        """Affiche un aperçu de l'image du produit"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 150px;" />',
                obj.image.url
            )
        return "Pas d'image"
    image_preview.short_description = "Aperçu"

    def price_display(self, obj):
        """Affiche le prix formaté"""
        return format_html(
            '<strong>{:,.0f} FCFA</strong>',
            obj.price
        )
    price_display.short_description = "Prix"
    price_display.admin_order_field = 'price'


admin.site.site_header = "NIASOTAC TECHNOLOGIE - Administration"
admin.site.site_title = "NIASOTAC Admin"
admin.site.index_title = "Tableau de bord de gestion"
