from django.core.management.base import BaseCommand
from showcase.models import Category, Product
from django.core.files.base import ContentFile
import random


class Command(BaseCommand):
    help = 'Peuple la base de données avec des catégories et produits de test'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Début du peuplement des données...'))

        categories_data = [
            {
                'name': 'Ordinateurs',
                'icon': 'laptop',
                'subcategories': [
                    'Ordinateurs portables',
                    'Ordinateurs de bureau',
                    'Mini PC'
                ]
            },
            {
                'name': 'Composants',
                'icon': 'memory',
                'subcategories': [
                    'Processeurs',
                    'Cartes mères',
                    'Mémoire RAM'
                ]
            },
            {
                'name': 'Imprimantes',
                'icon': 'print',
                'subcategories': [
                    'Imprimantes laser',
                    'Imprimantes jet d\'encre',
                    'Imprimantes multifonctions'
                ]
            },
            {
                'name': 'Accessoires',
                'icon': 'devices',
                'subcategories': [
                    'Claviers et souris',
                    'Webcams et microphones',
                    'Casques audio'
                ]
            }
        ]

        products_data = {
            'Ordinateurs portables': [
                {'name': 'HP Pavilion 15', 'brand': 'HP', 'price': 450000, 'desc': 'Ordinateur portable performant avec écran 15.6", Intel Core i5, 8Go RAM, 512Go SSD. Idéal pour le travail et le divertissement.'},
                {'name': 'Dell Latitude 5420', 'brand': 'Dell', 'price': 520000, 'desc': 'PC professionnel robuste, Intel Core i7, 16Go RAM, 1To SSD, parfait pour les professionnels exigeants.'},
                {'name': 'Lenovo ThinkPad E15', 'brand': 'Lenovo', 'price': 380000, 'desc': 'Ordinateur portable fiable pour entreprises, AMD Ryzen 5, 8Go RAM, 256Go SSD.'},
                {'name': 'Asus VivoBook 14', 'brand': 'Asus', 'price': 320000, 'desc': 'Portable léger et élégant, Intel Core i3, 8Go RAM, 512Go SSD, parfait pour la mobilité.'},
            ],
            'Ordinateurs de bureau': [
                {'name': 'HP EliteDesk 800 G6', 'brand': 'HP', 'price': 480000, 'desc': 'PC de bureau compact et puissant, Intel Core i7, 16Go RAM, 512Go SSD, Windows 11 Pro.'},
                {'name': 'Dell OptiPlex 3090', 'brand': 'Dell', 'price': 420000, 'desc': 'PC de bureau professionnel, Intel Core i5, 8Go RAM, 1To HDD, fiable et évolutif.'},
                {'name': 'Lenovo IdeaCentre 3', 'brand': 'Lenovo', 'price': 350000, 'desc': 'PC de bureau tout-en-un, AMD Ryzen 3, 8Go RAM, 256Go SSD, écran 24 pouces intégré.'},
            ],
            'Mini PC': [
                {'name': 'Intel NUC 11', 'brand': 'Intel', 'price': 280000, 'desc': 'Mini PC ultra-compact, Intel Core i5, 8Go RAM, 256Go SSD, parfait pour les espaces réduits.'},
                {'name': 'Asus PN51', 'brand': 'Asus', 'price': 310000, 'desc': 'Mini PC performant, AMD Ryzen 7, 16Go RAM, 512Go SSD, idéal pour le télétravail.'},
            ],
            'Processeurs': [
                {'name': 'Intel Core i5-12400', 'brand': 'Intel', 'price': 95000, 'desc': 'Processeur 6 cœurs, 12 threads, fréquence 2.5GHz, socket LGA1700.'},
                {'name': 'AMD Ryzen 5 5600X', 'brand': 'AMD', 'price': 105000, 'desc': 'Processeur 6 cœurs, 12 threads, fréquence 3.7GHz, socket AM4.'},
                {'name': 'Intel Core i7-12700K', 'brand': 'Intel', 'price': 185000, 'desc': 'Processeur 12 cœurs, 20 threads, fréquence 3.6GHz, haute performance.'},
            ],
            'Cartes mères': [
                {'name': 'Asus Prime B550M-A', 'brand': 'Asus', 'price': 65000, 'desc': 'Carte mère Micro-ATX, socket AM4, chipset B550, support PCIe 4.0.'},
                {'name': 'MSI MPG B560', 'brand': 'MSI', 'price': 72000, 'desc': 'Carte mère ATX, socket LGA1200, chipset B560, RGB Mystic Light.'},
                {'name': 'Gigabyte B660M', 'brand': 'Gigabyte', 'price': 68000, 'desc': 'Carte mère Micro-ATX, socket LGA1700, chipset B660, support DDR4.'},
            ],
            'Mémoire RAM': [
                {'name': 'Corsair Vengeance 16Go', 'brand': 'Corsair', 'price': 35000, 'desc': 'Kit 2x8Go DDR4 3200MHz, compatible Intel et AMD.'},
                {'name': 'Kingston Fury 32Go', 'brand': 'Kingston', 'price': 68000, 'desc': 'Kit 2x16Go DDR4 3600MHz, RGB, haute performance.'},
                {'name': 'G.Skill Ripjaws 8Go', 'brand': 'G.Skill', 'price': 18000, 'desc': 'Barrette 8Go DDR4 2666MHz, fiable et abordable.'},
            ],
            'Imprimantes laser': [
                {'name': 'HP LaserJet Pro M404', 'brand': 'HP', 'price': 185000, 'desc': 'Imprimante laser monochrome, vitesse 38ppm, recto-verso automatique.'},
                {'name': 'Brother HL-L2350DW', 'brand': 'Brother', 'price': 145000, 'desc': 'Imprimante laser compacte, WiFi, vitesse 32ppm, économique.'},
                {'name': 'Canon i-SENSYS LBP223dw', 'brand': 'Canon', 'price': 168000, 'desc': 'Imprimante laser réseau, WiFi, recto-verso, écran tactile.'},
            ],
            'Imprimantes jet d\'encre': [
                {'name': 'Epson EcoTank L3250', 'brand': 'Epson', 'price': 125000, 'desc': 'Imprimante multifonction à réservoirs, économie d\'encre, WiFi.'},
                {'name': 'HP DeskJet 2820', 'brand': 'HP', 'price': 65000, 'desc': 'Imprimante tout-en-un compacte, impression, copie, scan.'},
                {'name': 'Canon PIXMA G3260', 'brand': 'Canon', 'price': 135000, 'desc': 'Imprimante MegaTank sans fil, réservoirs rechargeables.'},
            ],
            'Imprimantes multifonctions': [
                {'name': 'HP OfficeJet Pro 9025e', 'brand': 'HP', 'price': 215000, 'desc': 'Tout-en-un professionnel, couleur, fax, chargeur automatique.'},
                {'name': 'Epson WorkForce WF-2930', 'brand': 'Epson', 'price': 95000, 'desc': 'Imprimante multifonction 4-en-1, WiFi, écran couleur.'},
            ],
            'Claviers et souris': [
                {'name': 'Logitech MK270', 'brand': 'Logitech', 'price': 18000, 'desc': 'Combo clavier et souris sans fil, autonomie longue durée.'},
                {'name': 'Razer DeathAdder V2', 'brand': 'Razer', 'price': 35000, 'desc': 'Souris gaming optique, 20000 DPI, RGB Chroma.'},
                {'name': 'Corsair K55 RGB', 'brand': 'Corsair', 'price': 42000, 'desc': 'Clavier gaming membrane, rétroéclairage RGB, touches multimédia.'},
            ],
            'Webcams et microphones': [
                {'name': 'Logitech C920 HD Pro', 'brand': 'Logitech', 'price': 58000, 'desc': 'Webcam Full HD 1080p, micro stéréo, autofocus.'},
                {'name': 'Blue Yeti', 'brand': 'Blue', 'price': 95000, 'desc': 'Microphone USB professionnel, 4 modes de capture.'},
                {'name': 'Razer Kiyo', 'brand': 'Razer', 'price': 72000, 'desc': 'Webcam streaming 1080p, anneau lumineux intégré.'},
            ],
            'Casques audio': [
                {'name': 'HyperX Cloud II', 'brand': 'HyperX', 'price': 52000, 'desc': 'Casque gaming 7.1, micro antibruit, confortable.'},
                {'name': 'Sony WH-1000XM4', 'brand': 'Sony', 'price': 185000, 'desc': 'Casque sans fil, réduction de bruit active, autonomie 30h.'},
                {'name': 'Logitech G733', 'brand': 'Logitech', 'price': 85000, 'desc': 'Casque gaming sans fil, RGB, micro Blue VO!CE.'},
            ],
        }

        Category.objects.all().delete()
        Product.objects.all().delete()
        self.stdout.write('Anciennes données supprimées.')

        categories_map = {}
        for cat_data in categories_data:
            category = Category.objects.create(
                name=cat_data['name'],
                icon=cat_data['icon']
            )
            categories_map[cat_data['name']] = category
            self.stdout.write(self.style.SUCCESS(f'✓ Catégorie créée: {category.name}'))

            for subcat_name in cat_data['subcategories']:
                subcategory = Category.objects.create(
                    name=subcat_name,
                    parent=category
                )
                categories_map[subcat_name] = subcategory
                self.stdout.write(f'  ✓ Sous-catégorie créée: {subcategory.name}')

        for subcat_name, products in products_data.items():
            subcategory = categories_map.get(subcat_name)
            if not subcategory:
                continue

            main_category = subcategory.parent

            for product_info in products:
                product = Product.objects.create(
                    name=product_info['name'],
                    brand=product_info['brand'],
                    price=product_info['price'],
                    description=product_info['desc'],
                    category=main_category,
                    subcategory=subcategory,
                    in_stock=random.choice([True, True, True, False]),
                    featured=random.choice([True, False, False, False])
                )
                self.stdout.write(f'    ✓ Produit créé: {product.name} ({product.price} FCFA)')

        total_categories = Category.objects.filter(parent__isnull=True).count()
        total_subcategories = Category.objects.filter(parent__isnull=False).count()
        total_products = Product.objects.count()

        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS(f'✓ {total_categories} catégories principales créées'))
        self.stdout.write(self.style.SUCCESS(f'✓ {total_subcategories} sous-catégories créées'))
        self.stdout.write(self.style.SUCCESS(f'✓ {total_products} produits créés'))
        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write(self.style.SUCCESS('\nDonnées de test créées avec succès!'))
