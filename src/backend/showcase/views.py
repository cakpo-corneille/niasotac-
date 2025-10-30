from rest_framework import viewsets, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, NumberFilter, CharFilter
from .models import Category, Product, SiteSettings
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ProductListSerializer,
    SiteSettingsSerializer
)

import logging


# Loggers configurés dans logging.py
action_logger = logging.getLogger('niasotac.actions')
request_logger = logging.getLogger('django')
error_logger = logging.getLogger('django.request')

@api_view(['GET'])
@permission_classes([AllowAny])
def log_test_view(request):
    
    user = request.user if request.user.is_authenticated else "anonyme"
    action_logger.info(f"Visite de log-test par {user}")
    
    action_logger.info("✅ Test d'action métier : log d'activité enregistré.")
    request_logger.info("📥 Test de requête HTTP : log de requête enregistré.")
    try:
        raise ValueError("❌ Test d'erreur : exception simulée.")
    except Exception as e:
        error_logger.error(f"Erreur capturée : {str(e)}")

    return Response({
        "message": "Logs générés avec succès dans actions.log, requests.log et errors.log"
    })


class IsAdminOrReadOnly(IsAuthenticatedOrReadOnly):
    """Permission personnalisée: lecture pour tous, écriture pour admins uniquement"""
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user and request.user.is_staff


# 🔹 Filtres personnalisés pour les produits
class ProductFilter(FilterSet):
    price_min = NumberFilter(field_name='price', lookup_expr='gte')
    price_max = NumberFilter(field_name='price', lookup_expr='lte')
    category = CharFilter(method='filter_by_category_slug')

    class Meta:
        model = Product
        fields = ['category', 'brand', 'in_stock', 'featured', 'price_min', 'price_max']

    def filter_by_category_slug(self, queryset, name, value):
        try:
            cat = Category.objects.get(slug=value)
            descendants = cat.get_descendants()
            return queryset.filter(category__in=[cat] + descendants)
        except Category.DoesNotExist:
            return queryset.none()


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet pour gérer les catégories"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']

    @action(detail=False, methods=['get'])
    def main_categories(self, request):
        """Retourne uniquement les catégories principales"""
        main_cats = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')
        serializer = self.get_serializer(main_cats, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def products(self, request, slug=None):
        """Retourne tous les produits liés à cette catégorie et ses sous-catégories récursives"""
        category = self.get_object()
        descendants = category.get_descendants()
        all_categories = [category] + descendants
        products = Product.objects.filter(category__in=all_categories)
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet pour gérer les produits"""
    queryset = Product.objects.select_related('category').all()
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'brand', 'description']
    ordering_fields = ['name', 'price', 'created_at']

    def get_serializer_class(self):
        return ProductListSerializer if self.action == 'list' else ProductSerializer

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Retourne les produits vedettes"""
        featured_products = self.filter_queryset(self.get_queryset()).filter(featured=True)[:8]
        serializer = ProductListSerializer(featured_products, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Retourne les produits récents"""
        recent_products = self.filter_queryset(self.get_queryset()).order_by('-created_at')[:10]
        serializer = ProductListSerializer(recent_products, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def brands(self, request):
        """Retourne la liste de toutes les marques disponibles"""
        brands = Product.objects.values_list('brand', flat=True).distinct().order_by('brand')
        return Response(list(brands))

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Retourne les statistiques des produits"""
        stats = {
            'total_products': Product.objects.count(),
            'in_stock': Product.objects.filter(in_stock=True).count(),
            'out_of_stock': Product.objects.filter(in_stock=False).count(),
            'featured': Product.objects.filter(featured=True).count(),
            'by_category': list(
                Category.objects.filter(parent__isnull=True).annotate(
                    count=Count('products')
                ).values('name', 'count')
            )
        }
        return Response(stats)


@api_view(['GET'])
@permission_classes([AllowAny])
def site_settings_view(request):
    """GET /api/settings/ - Retourne les paramètres du site (public)"""
    settings = SiteSettings.load()
    serializer = SiteSettingsSerializer(settings, context={'request': request})
    return Response(serializer.data)
