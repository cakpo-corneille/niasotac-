from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import Category, Product, ProductImage, SiteSettings


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Administration personnalisée pour les catégories"""
    list_display = ['name', 'parent', 'product_count', 'icon', 'icon_preview', 'created_at']
    list_filter = ['parent', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at', 'icon_preview']
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('name', 'slug', 'parent')
        }),
        ('Icône', {
            'fields': ('icon', 'icon_file', 'icon_preview')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def icon_preview(self, obj):
        """Aperçu de l'icône CSS ou fichier .ico"""
        if obj.icon_file:
            return format_html('<img src="{}" style="height:32px;" />', obj.icon_file.url)
        elif obj.icon:
            return format_html('<i class="{}" style="font-size:24px;"></i>', obj.icon)
        return format_html('<i class="fa fa-question-circle" style="font-size:24px;"></i>')
    icon_preview.short_description = "Aperçu"

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


class ProductImageInline(admin.TabularInline):
    """Inline pour images supplémentaires"""
    model = ProductImage
    extra = 1
    max_num = 10
    fields = ['image', 'image_preview']
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:100px;" />', obj.image.url)
        return format_html('<img src="/static/defaults/default_product.png" style="max-height:100px;" />')
    image_preview.short_description = "Aperçu"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Administration personnalisée pour les produits"""
    list_display = [
        'name', 'brand', 'price_display', 'category',
        'in_stock', 'featured', 'image_preview', 'created_at'
    ]
    list_filter = ['category', 'brand', 'in_stock', 'featured', 'created_at']
    search_fields = ['name', 'brand', 'description']
    prepopulated_fields = {'slug': ('name', 'brand')}
    readonly_fields = ['created_at', 'updated_at', 'whatsapp_link', 'image_preview']
    list_editable = ['in_stock', 'featured']
    inlines = [ProductImageInline]
    
    fieldsets = (
        ('Informations produit', {
            'fields': ('name', 'slug', 'brand', 'description')
        }),
        ('Prix et catégorie', {
            'fields': ('price', 'category')
        }),
        ('Image principale', {
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
        url = obj.image.url if obj.image else '/static/defaults/default_product.png'
        return format_html('<img src="{}" style="max-height:100px;" />', url)
    image_preview.short_description = "Aperçu"

    def price_display(self, obj):
        return format_html('<strong>{:,.0f} FCFA</strong>', obj.price)
    price_display.short_description = "Prix"
    price_display.admin_order_field = 'price'


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Administration personnalisée pour les paramètres du site"""
    fieldsets = (
        ('Informations de contact', {
            'fields': ('whatsapp_number', 'contact_phone', 'contact_email', 'contact_address')
        }),
        ('Informations de l\'entreprise', {
            'fields': ('company_name', 'company_description')
        }),
        ('Métadonnées', {
            'fields': ('updated_at', 'updated_by'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['updated_at', 'updated_by']

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


admin.site.site_header = "NIASOTAC TECHNOLOGIE - Administration"
admin.site.site_title = "NIASOTAC Admin"
admin.site.index_title = "Tableau de bord de gestion"
