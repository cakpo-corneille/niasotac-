from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
from django.db.models import Count, Q
from .models import Category, Product
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ProductListSerializer
)


class IsAdminOrReadOnly(IsAuthenticatedOrReadOnly):
    """
    Permission personnalisée: lecture pour tous, écriture pour admins uniquement
    """
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user and request.user.is_staff


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les catégories et sous-catégories
    GET /api/categories/ - Liste toutes les catégories (public)
    POST /api/categories/ - Créer une nouvelle catégorie (admin uniquement)
    GET /api/categories/{id}/ - Détails d'une catégorie (public)
    PUT/PATCH /api/categories/{id}/ - Modifier une catégorie (admin uniquement)
    DELETE /api/categories/{id}/ - Supprimer une catégorie (admin uniquement)
    """
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
        """Retourne tous les produits d'une catégorie"""
        category = self.get_object()
        products = Product.objects.filter(
            Q(category=category) | Q(subcategory=category)
        )
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les produits
    GET /api/products/ - Liste tous les produits (public)
    POST /api/products/ - Créer un nouveau produit (admin uniquement)
    GET /api/products/{id}/ - Détails d'un produit (public)
    PUT/PATCH /api/products/{id}/ - Modifier un produit (admin uniquement)
    DELETE /api/products/{id}/ - Supprimer un produit (admin uniquement)
    """
    queryset = Product.objects.select_related('category', 'subcategory').all()
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'brand', 'description']
    ordering_fields = ['name', 'price', 'created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        
        category_slug = self.request.query_params.get('category', None)
        subcategory_slug = self.request.query_params.get('subcategory', None)
        brand = self.request.query_params.get('brand', None)
        in_stock = self.request.query_params.get('in_stock', None)
        featured = self.request.query_params.get('featured', None)
        
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        if subcategory_slug:
            queryset = queryset.filter(subcategory__slug=subcategory_slug)
        
        if brand:
            queryset = queryset.filter(brand__icontains=brand)
        
        if in_stock is not None:
            queryset = queryset.filter(in_stock=in_stock.lower() == 'true')
        
        if featured is not None:
            queryset = queryset.filter(featured=featured.lower() == 'true')
        
        return queryset

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Retourne les produits vedettes"""
        featured_products = self.get_queryset().filter(featured=True)[:8]
        serializer = ProductListSerializer(featured_products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Retourne les produits récents"""
        recent_products = self.get_queryset().order_by('-created_at')[:10]
        serializer = ProductListSerializer(recent_products, many=True)
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
