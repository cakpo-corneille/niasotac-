# NIASOTAC Backend - API Django REST

## Description

API backend pour la vitrine e-commerce NIASOTAC. Construit avec Django 5.2.7 et Django REST Framework, cette API gère les produits, catégories et paramètres du site.

## Technologies Utilisées

- **Django 5.2.7** - Framework web Python
- **Django REST Framework 3.16** - API RESTful
- **Simple JWT** - Authentification par tokens JWT
- **Pillow** - Traitement d'images
- **WhiteNoise** - Service de fichiers statiques
- **Gunicorn** - Serveur WSGI pour la production

## Installation Locale

### Prérequis

- Python 3.11 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'Installation

1. **Cloner le projet et naviguer vers le backend**
   ```bash
   cd backend
   ```

2. **Créer un environnement virtuel**
   ```bash
   python -m venv venv
   ```

3. **Activer l'environnement virtuel**
   - Sur Windows :
     ```bash
     venv\Scripts\activate
     ```
   - Sur macOS/Linux :
     ```bash
     source venv/bin/activate
     ```

4. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configurer les variables d'environnement (optionnel)**
   
   Créer un fichier `.env` dans le dossier `backend/` :
   ```env
   SECRET_KEY=votre-clé-secrète-django
   DEBUG=True
   ```

6. **Exécuter les migrations**
   ```bash
   python manage.py migrate
   ```

7. **Créer un superutilisateur**
   ```bash
   python manage.py createsuperuser
   ```
   
   Suivez les instructions pour créer vos identifiants admin.

8. **Peupler la base de données avec des données de test**
   ```bash
   python manage.py populate_data
   ```

9. **Démarrer le serveur de développement**
   ```bash
   python manage.py runserver
   ```

   Le serveur démarre sur `http://localhost:8000/`

## Structure du Projet

```
backend/
├── niasotac_backend/       # Configuration Django
│   ├── settings.py         # Paramètres du projet
│   ├── urls.py            # Routes principales
│   ├── wsgi.py            # Configuration WSGI
│   └── asgi.py            # Configuration ASGI
│
├── showcase/              # Application principale
│   ├── models.py          # Modèles de données
│   ├── views.py           # Vues/ViewSets API
│   ├── serializers.py     # Sérializers DRF
│   ├── urls.py            # Routes de l'app
│   ├── admin.py           # Configuration admin Django
│   └── management/
│       └── commands/
│           └── populate_data.py  # Commande de peuplement
│
├── media/                 # Fichiers uploadés
├── staticfiles/           # Fichiers statiques collectés
├── manage.py             # Script de gestion Django
└── requirements.txt      # Dépendances Python
```

## Modèles de Données

### Category (Catégorie)
- `name` : Nom de la catégorie
- `slug` : Slug URL (généré automatiquement)
- `icon` : Nom de l'icône
- `image` : Image de la catégorie (optionnel)
- `parent` : Catégorie parente (pour les sous-catégories)

### Product (Produit)
- `name` : Nom du produit
- `slug` : Slug URL (généré automatiquement)
- `description` : Description détaillée
- `price` : Prix en FCFA
- `brand` : Marque
- `image` : Image du produit (**obligatoire**)
- `category` : Catégorie principale
- `subcategory` : Sous-catégorie (optionnel)
- `in_stock` : Disponibilité en stock
- `featured` : Produit vedette

### SiteSettings (Paramètres du Site)
- `whatsapp_number` : Numéro WhatsApp
- `contact_email` : Email de contact
- `contact_phone` : Téléphone
- `contact_address` : Adresse physique
- `company_name` : Nom de l'entreprise
- `company_description` : Description de l'entreprise

## Endpoints API

### Endpoints Publics

#### Catégories
- `GET /api/categories/` - Liste toutes les catégories
- `GET /api/categories/{id}/` - Détails d'une catégorie
- `GET /api/categories/main_categories/` - Liste des catégories principales

#### Produits
- `GET /api/products/` - Liste tous les produits
- `GET /api/products/{id}/` - Détails d'un produit
- `GET /api/products/featured/` - Liste des produits vedettes

**Filtres disponibles :**
- `?category={id}` - Filtrer par catégorie
- `?subcategory={id}` - Filtrer par sous-catégorie
- `?featured=true` - Produits vedettes uniquement
- `?in_stock=true` - Produits en stock uniquement
- `?search={texte}` - Recherche par nom/marque

#### Paramètres du Site
- `GET /api/settings/` - Récupérer les paramètres du site

### Endpoints Authentifiés

#### Authentification JWT
- `POST /api/token/` - Obtenir un token JWT
  ```json
  {
    "username": "admin",
    "password": "votre_mot_de_passe"
  }
  ```
- `POST /api/token/refresh/` - Rafraîchir le token
  ```json
  {
    "refresh": "votre_refresh_token"
  }
  ```

#### Administration
- `POST /api/categories/` - Créer une catégorie (admin uniquement)
- `PUT /api/categories/{id}/` - Modifier une catégorie
- `DELETE /api/categories/{id}/` - Supprimer une catégorie

- `POST /api/products/` - Créer un produit (admin uniquement)
- `PUT /api/products/{id}/` - Modifier un produit
- `DELETE /api/products/{id}/` - Supprimer un produit

## Interface d'Administration Django

Accéder à l'interface admin sur : `http://localhost:8000/admin/`

Identifiants par défaut (après `populate_data`) :
- **Username** : `admin`
- **Password** : `admin123`

L'interface admin permet de :
- Gérer les catégories et sous-catégories
- Ajouter/modifier/supprimer des produits
- Uploader des images de produits
- Configurer les paramètres du site
- Gérer les utilisateurs et permissions

## Commandes de Gestion

### Migration de Base de Données
```bash
# Créer de nouvelles migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Voir l'état des migrations
python manage.py showmigrations
```

### Gestion des Fichiers Statiques
```bash
# Collecter tous les fichiers statiques
python manage.py collectstatic

# Collecter sans demander confirmation
python manage.py collectstatic --noinput
```

### Gestion des Données
```bash
# Peupler la base avec des données de test
python manage.py populate_data

# Créer un superutilisateur
python manage.py createsuperuser

# Ouvrir un shell Python avec le contexte Django
python manage.py shell
```

### Utilitaires
```bash
# Vérifier les problèmes de configuration
python manage.py check

# Démarrer le serveur de développement
python manage.py runserver

# Démarrer sur un port spécifique
python manage.py runserver 8080

# Démarrer en écoutant toutes les interfaces
python manage.py runserver 0.0.0.0:8000
```

## Configuration pour la Production

### Utiliser PostgreSQL

1. Installer psycopg2 (déjà inclus dans requirements.txt)

2. Modifier `settings.py` :
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'niasotac_db',
           'USER': 'votre_user',
           'PASSWORD': 'votre_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

3. Créer la base de données PostgreSQL :
   ```sql
   CREATE DATABASE niasotac_db;
   CREATE USER votre_user WITH PASSWORD 'votre_password';
   GRANT ALL PRIVILEGES ON DATABASE niasotac_db TO votre_user;
   ```

### Variables d'Environnement de Production

Créer un fichier `.env` :
```env
SECRET_KEY=votre-clé-secrète-très-longue-et-aléatoire
DEBUG=False
ALLOWED_HOSTS=votre-domaine.com,www.votre-domaine.com

# PostgreSQL
PGDATABASE=niasotac_db
PGUSER=votre_user
PGPASSWORD=votre_password
PGHOST=localhost
PGPORT=5432
```

### Démarrer avec Gunicorn

```bash
# Production avec 4 workers
gunicorn --bind=0.0.0.0:8000 --workers=4 niasotac_backend.wsgi:application

# Avec threads pour gérer plus de connexions
gunicorn --bind=0.0.0.0:8000 --workers=2 --threads=4 niasotac_backend.wsgi:application
```

## Tests

```bash
# Exécuter tous les tests
python manage.py test

# Tester une application spécifique
python manage.py test showcase

# Tests avec verbosité
python manage.py test --verbosity=2
```

## Dépannage

### Problème : "No module named 'rest_framework'"
```bash
pip install -r requirements.txt
```

### Problème : Erreur de migration
```bash
# Supprimer la base de données et recommencer
rm db.sqlite3
python manage.py migrate
python manage.py populate_data
```

### Problème : Images non affichées
```bash
# Vérifier que MEDIA_ROOT existe
mkdir -p media/products

# Vérifier les permissions
chmod -R 755 media/
```

### Problème : "Secret key not set"
```bash
# Générer une nouvelle clé secrète
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Sécurité

### Bonnes Pratiques

1. **Ne jamais commiter le fichier `.env`** contenant les secrets
2. **Changer la SECRET_KEY** en production
3. **Mettre DEBUG=False** en production
4. **Configurer ALLOWED_HOSTS** correctement
5. **Utiliser HTTPS** en production
6. **Limiter les tailles de fichiers** uploadés (déjà configuré : 2MB max)
7. **Valider les extensions** de fichiers (JPG, JPEG, PNG uniquement)

## Support et Contribution

Pour toute question ou problème, consulter :
- Documentation Django : https://docs.djangoproject.com/
- Documentation DRF : https://www.django-rest-framework.org/
- Code source du projet

## Licence

Ce projet est privé et destiné à un usage interne.
