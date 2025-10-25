# NIASOTAC TECHNOLOGIE - Backend API

Backend Django REST Framework pour le site vitrine de NIASOTAC TECHNOLOGIE, un revendeur de produits technologiques qui photographie les produits dans les magasins partenaires et les vend directement aux clients via WhatsApp.

## 🚀 Fonctionnalités

### API REST complète
- **CRUD Produits** : Gestion complète des produits avec images
- **CRUD Catégories** : Support des catégories et sous-catégories imbriquées
- **Authentification JWT** : Sécurisation des endpoints administratifs
- **Génération liens WhatsApp** : Liens pré-remplis pour chaque produit
- **Upload d'images** : Validation automatique (max 2MB, JPG/PNG)
- **URLs SEO-friendly** : Slugs automatiques pour produits et catégories
- **Filtres avancés** : Par catégorie, sous-catégorie, marque, stock, etc.

### Interface d'administration
- Panel Django Admin personnalisé avec branding NIASOTAC
- Dashboard avec statistiques
- Gestion visuelle des produits et catégories
- Aperçu des images
- Liens WhatsApp pré-générés

### Données de test
- 4 catégories principales (Ordinateurs, Composants, Imprimantes, Accessoires)
- 12 sous-catégories
- 35 produits avec descriptions détaillées

## 📋 Modèles de données

### Category (Catégorie)
```python
- name: Nom de la catégorie
- slug: URL SEO-friendly (auto-généré)
- icon: Nom de l'icône
- image: Image de la catégorie
- parent: Catégorie parente (null pour catégories principales)
```

### Product (Produit)
```python
- name: Nom du produit
- slug: URL SEO-friendly (auto-généré)
- description: Description détaillée
- price: Prix en FCFA
- brand: Marque
- image: Image du produit
- category: Catégorie principale
- subcategory: Sous-catégorie
- in_stock: Disponibilité
- featured: Produit vedette
```

## 🔌 Endpoints API

### Authentification
```
POST /api/token/              # Obtenir token JWT
POST /api/token/refresh/      # Rafraîchir token
```

### Catégories
```
GET    /api/categories/                    # Liste toutes les catégories
GET    /api/categories/main_categories/    # Catégories principales uniquement
GET    /api/categories/{slug}/             # Détails d'une catégorie
GET    /api/categories/{slug}/products/    # Produits d'une catégorie
POST   /api/categories/                    # Créer catégorie (auth requis)
PUT    /api/categories/{slug}/             # Modifier catégorie (auth requis)
DELETE /api/categories/{slug}/             # Supprimer catégorie (auth requis)
```

### Produits
```
GET    /api/products/                  # Liste tous les produits
GET    /api/products/featured/         # Produits vedettes
GET    /api/products/recent/           # Produits récents
GET    /api/products/brands/           # Liste des marques
GET    /api/products/stats/            # Statistiques produits
GET    /api/products/{slug}/           # Détails d'un produit
POST   /api/products/                  # Créer produit (auth requis)
PUT    /api/products/{slug}/           # Modifier produit (auth requis)
DELETE /api/products/{slug}/           # Supprimer produit (auth requis)
```

### Filtres disponibles
```
GET /api/products/?category={slug}       # Filtrer par catégorie
GET /api/products/?subcategory={slug}    # Filtrer par sous-catégorie
GET /api/products/?brand={nom}           # Filtrer par marque
GET /api/products/?in_stock=true         # Filtrer par disponibilité
GET /api/products/?featured=true         # Filtrer produits vedettes
GET /api/products/?search={terme}        # Rechercher
```

## 🔑 Authentification

### Obtenir un token
```bash
curl -X POST http://localhost:5000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### Utiliser le token
```bash
curl -X GET http://localhost:5000/api/products/ \
  -H "Authorization: Bearer {votre_token}"
```

## 👤 Compte administrateur

- **Username**: `admin`
- **Email**: `admin@niasotac.com`
- **Password**: `admin123`
- **Panel admin**: `http://localhost:5000/admin/`

## 🛠️ Installation et exécution locale

### Prérequis
- Python 3.11+
- PostgreSQL
- Variables d'environnement configurées

### Installation
```bash
# Les dépendances sont déjà installées via uv
# Si besoin de réinstaller :
uv sync
```

### Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Créer un superuser
```bash
python manage.py createsuperuser
```

### Peupler avec données de test
```bash
python manage.py populate_data
```

### Lancer le serveur
```bash
python manage.py runserver 0.0.0.0:5000
```

L'API sera accessible sur : `http://localhost:5000/api/`
Le panel admin sur : `http://localhost:5000/admin/`

## 📱 Intégration WhatsApp

Chaque produit génère automatiquement un lien WhatsApp avec message pré-rempli :

```
https://wa.me/237XXXXXXXXX?text=Bonjour NIASOTAC TECHNOLOGIE...
```

**⚠️ N'oubliez pas de remplacer le numéro de téléphone** dans `showcase/models.py` :
```python
phone_number = "237XXXXXXXXX"  # Remplacer par votre numéro
```

## 🌐 Configuration CORS

CORS est configuré pour accepter toutes les origines en développement. Pour la production, modifiez dans `settings.py` :

```python
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "https://votre-frontend.com",
]
```

## 📦 Structure du projet

```
niasotac_backend/
├── niasotac_backend/          # Configuration Django
│   ├── settings.py           # Paramètres (DB, CORS, JWT, etc.)
│   ├── urls.py               # URLs principales
│   └── wsgi.py              
├── showcase/                  # Application principale
│   ├── models.py             # Modèles Category et Product
│   ├── serializers.py        # Serializers DRF
│   ├── views.py              # ViewSets API
│   ├── admin.py              # Configuration admin Django
│   ├── urls.py               # Routes API
│   └── management/
│       └── commands/
│           └── populate_data.py  # Commande peuplement données
├── media/                     # Fichiers uploadés
├── manage.py
└── requirements (via uv)
```

## 🔒 Sécurité

- Authentification JWT avec tokens refresh
- Validation des uploads d'images (taille et format)
- CORS configuré
- Protection CSRF activée
- Permissions REST Framework (lecture publique, écriture authentifiée)

## 📝 Prochaines étapes recommandées

1. **Configuration WhatsApp** : Remplacer le numéro de téléphone par le vôtre
2. **Images** : Ajouter de vraies images pour les produits et catégories
3. **Production** : 
   - Configurer ALLOWED_HOSTS
   - Restreindre CORS_ALLOWED_ORIGINS
   - Utiliser gunicorn/uwsgi au lieu de runserver
   - Configurer le stockage des médias (S3, etc.)
4. **Monitoring** : Ajouter Sentry ou équivalent
5. **Documentation API** : Ajouter Swagger/OpenAPI avec drf-spectacular

## 🆘 Support

Pour toute question ou assistance, contactez l'équipe NIASOTAC TECHNOLOGIE.

---

**Développé avec ❤️ pour NIASOTAC TECHNOLOGIE**
