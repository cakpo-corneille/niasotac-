from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Category, Product, SiteSettings
from .serializers import (
    ProductSerializer,
    ProductListSerializer,
    CategorySerializer,
    SubcategorySerializer,
    SiteSettingsSerializer,
    ProductImageSerializer
)
from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile
from PIL import Image


# 🔹 Utilitaires
def generate_image_file():
    image = Image.new('RGB', (100, 100))
    tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
    image.save(tmp_file, format='JPEG')
    tmp_file.seek(0)
    return SimpleUploadedFile("test.jpg", tmp_file.read(), content_type="image/jpeg")


# 🔹 Tests des modèles
class ModelTests(TestCase):
    def test_category_slug_and_hierarchy(self):
        parent = Category.objects.create(name="Électronique")
        child = Category.objects.create(name="Audio", parent=parent)
        self.assertEqual(parent.slug, "electronique")
        self.assertFalse(child.is_main_category)
        self.assertTrue(parent.is_main_category)

    def test_product_slug_and_whatsapp_link(self):
        SiteSettings.objects.create(pk=1, whatsapp_number="22900000000")
        category = Category.objects.create(name="Audio")
        image = generate_image_file()
        product = Product.objects.create(
            name="AirPods Pro",
            brand="Apple",
            category=category,
            price=299.99,
            description="Casque haut de gamme",
            image=image
        )
        self.assertEqual(product.slug, "airpods-pro-apple")
        self.assertIn("https://wa.me/22900000000", product.whatsapp_link)

    def test_site_settings_singleton(self):
        settings = SiteSettings.load()
        self.assertEqual(settings.pk, 1)
        self.assertEqual(str(settings), "Paramètres du site")


# 🔹 Tests des serializers
class SerializerTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Audio")
        self.image = generate_image_file()
        self.product = Product.objects.create(
            name="AirPods Pro",
            brand="Apple",
            category=self.category,
            price=299.99,
            description="Casque haut de gamme",
            image=self.image
        )

    def test_product_serializer_fields(self):
        serializer = ProductSerializer(instance=self.product, context={'request': None})
        self.assertIn('whatsapp_link', serializer.data)
        self.assertEqual(serializer.data['category_name'], "Audio")

    def test_product_list_serializer(self):
        serializer = ProductListSerializer(instance=self.product, context={'request': None})
        self.assertIn('display_price', serializer.data)
        self.assertEqual(serializer.data['brand'], "Apple")

    def test_category_serializer(self):
        serializer = CategorySerializer(instance=self.category)
        self.assertEqual(serializer.data['name'], "Audio")
        self.assertEqual(serializer.data['product_count'], 1)

    def test_site_settings_serializer(self):
        settings = SiteSettings.load()
        serializer = SiteSettingsSerializer(instance=settings)
        self.assertIn('company_name', serializer.data)


# 🔹 Tests des vues et endpoints
class ViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(username='admin', password='pass')
        self.user = User.objects.create_user(username='user', password='pass')
        self.category = Category.objects.create(name="Audio", slug="audio")
        self.image = generate_image_file()
        self.product = Product.objects.create(
            name="AirPods Pro",
            brand="Apple",
            category=self.category,
            price=299.99,
            description="Casque haut de gamme",
            image=self.image,
            featured=True
        )

    def test_main_categories(self):
        url = reverse('category-main-categories')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_category_products(self):
        url = reverse('category-products', args=[self.category.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_featured_products(self):
        url = reverse('product-featured')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], "AirPods Pro")

    def test_recent_products(self):
        url = reverse('product-recent')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_stats_endpoint(self):
        url = reverse('product-stats')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('total_products', response.data)

    def test_site_settings_view(self):
        url = reverse('site-settings')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('company_name', response.data)

    def test_admin_can_create_category(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('category-list')
        response = self.client.post(url, {'name': 'Test'})
        self.assertEqual(response.status_code, 201)

    def test_user_cannot_create_category(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('category-list')
        response = self.client.post(url, {'name': 'Test'})
        self.assertEqual(response.status_code, 403)
