# NIASOTAC TECHNOLOGIE - Application Full-Stack

## Vue d'ensemble
Application complète avec backend Django REST Framework et frontend React/Vite pour NIASOTAC TECHNOLOGIE, un revendeur tech qui vend via WhatsApp.

## État actuel du projet
✅ **Projet full-stack fonctionnel et complet** (Octobre 2025)

### Architecture
- **Backend**: Django REST Framework (port 8000)
- **Frontend**: React + Vite + TypeScript (port 5000)
- **Database**: PostgreSQL (via Replit)
- **Communication**: Proxy Vite pour rediriger /api vers le backend

### Fonctionnalités implémentées

#### Backend API
- API REST complète pour produits et catégories
- Authentification JWT sécurisée (admin uniquement pour modifications)
- Interface admin personnalisée avec branding NIASOTAC
- Génération automatique de liens WhatsApp
- Upload et validation d'images (max 2MB)
- Données de test (4 catégories, 12 sous-catégories, 35 produits)
- Support des sous-catégories imbriquées
- Filtres et recherche avancés
- Slugs SEO-friendly automatiques

#### Frontend React
- Interface utilisateur moderne avec shadcn/ui
- Pages: Home, Products, ProductDetail, Services, Contact
- Intégration React Query pour appels API
- Hooks personnalisés (useProducts, useCategories)
- Composants réutilisables (ProductCard, CategoryCard, etc.)
- Design responsive avec Tailwind CSS
- Hot Module Replacement (HMR) pour développement rapide
- Bouton WhatsApp flottant

### Technologies

#### Backend
- **Framework**: Django 5.2.7
- **API**: Django REST Framework 3.16
- **Auth**: djangorestframework-simplejwt
- **Database**: PostgreSQL (via Replit)
- **Images**: Pillow
- **CORS**: django-cors-headers

#### Frontend
- **Framework**: React 18.3.1
- **Build Tool**: Vite 5.4.19
- **Language**: TypeScript
- **State Management**: TanStack React Query
- **UI Library**: shadcn/ui + Radix UI
- **Styling**: Tailwind CSS
- **Routing**: React Router v6
- **Icons**: Lucide React

## Structure du projet

```
├── niasotac_backend/          # Configuration Django
│   ├── settings.py            # Paramètres (PostgreSQL, JWT, CORS)
│   └── urls.py                # Routes API principales
├── showcase/                   # App Django principale
│   ├── models.py              # Category, Product
│   ├── serializers.py         # DRF serializers
│   ├── views.py               # ViewSets API avec permissions
│   ├── admin.py               # Admin personnalisé NIASOTAC
│   └── management/            # Commandes custom
│       └── commands/
│           └── populate_data.py
├── frontend/                   # Application React/Vite
│   ├── src/
│   │   ├── components/        # Composants UI
│   │   ├── pages/             # Pages de l'application
│   │   ├── hooks/             # Hooks personnalisés
│   │   │   ├── useProducts.ts
│   │   │   └── useCategories.ts
│   │   ├── lib/
│   │   │   └── api.ts         # Configuration API
│   │   └── App.tsx
│   ├── vite.config.ts         # Config Vite avec proxy API
│   └── package.json
├── media/                      # Images uploadées
├── README.md                   # Documentation utilisateur
├── API_DOCUMENTATION.md        # Documentation API complète
└── replit.md                   # Ce fichier
```

## API Endpoints

### Authentification
- `POST /api/token/` - Obtenir token JWT
- `POST /api/token/refresh/` - Rafraîchir token

### Catégories
- `GET /api/categories/` - Liste toutes les catégories
- `GET /api/categories/main_categories/` - Catégories principales
- `GET /api/categories/{slug}/` - Détails catégorie
- `GET /api/categories/{slug}/products/` - Produits d'une catégorie
- `POST/PUT/DELETE /api/categories/` - CRUD (admin uniquement)

### Produits
- `GET /api/products/` - Liste avec filtres et pagination
- `GET /api/products/featured/` - Produits vedettes
- `GET /api/products/recent/` - Produits récents
- `GET /api/products/stats/` - Statistiques
- `GET /api/products/brands/` - Liste marques
- `GET /api/products/{slug}/` - Détails produit
- `POST/PUT/DELETE /api/products/` - CRUD (admin uniquement)

## Workflows Replit

### Django API Backend (port 8000)
```bash
python manage.py runserver 0.0.0.0:8000
```
- Type: Console
- Purpose: API REST backend
- Accès: Interne (via proxy Vite)

### Frontend React (port 5000)
```bash
cd frontend && npm run dev
```
- Type: Webview
- Purpose: Interface utilisateur
- Accès: Public (https://votre-repl.replit.dev)

## Configuration importante

### WhatsApp
⚠️ **À CONFIGURER**: Numéro WhatsApp dans `showcase/models.py`
```python
phone_number = "237XXXXXXXXX"  # Ligne 127
```

### Variables d'environnement
Automatiquement configurées par Replit:
- `DATABASE_URL`, `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`, `PGDATABASE`

Frontend (.env):
- `VITE_API_BASE_URL=/api` (utilise proxy Vite)

### CORS
Backend configuré pour accepter toutes les origines (développement).
Pour production, modifier dans `settings.py`:
```python
CORS_ALLOWED_ORIGINS = ["https://votre-frontend.com"]
```

### Proxy Vite
Le frontend redirige automatiquement `/api/*` vers `http://localhost:8000` grâce au proxy configuré dans `vite.config.ts`.

## Commandes utiles

### Backend
```bash
# Gestion base de données
python manage.py makemigrations
python manage.py migrate
python manage.py populate_data  # Repeupler avec données test

# Administration
python manage.py createsuperuser
python manage.py changepassword admin

# Serveur
python manage.py runserver 0.0.0.0:8000
```

### Frontend
```bash
cd frontend

# Installation
npm install

# Développement
npm run dev

# Build production
npm run build

# Preview build
npm run preview
```

## Admin Panel
- **URL**: http://localhost:8000/admin/
- **Username**: `admin`
- **Password**: `admin123`

## Frontend Pages
- **Home** (`/`): Page d'accueil avec catégories et produits vedettes
- **Products** (`/products`): Liste des produits avec filtres
- **Product Detail** (`/products/:slug`): Détails d'un produit
- **Services** (`/services`): Page des services
- **Contact** (`/contact`): Formulaire de contact

## Hooks React personnalisés

### useProducts
```typescript
const { data, isLoading } = useProducts({ category, subcategory, search });
const { data } = useFeaturedProducts();
const { data } = useRecentProducts();
const { data } = useProduct(slug);
```

### useCategories
```typescript
const { data } = useCategories();
const { data } = useMainCategories();
const { data } = useCategory(slug);
```

## Préférences utilisateur
- **Langue**: Français (FR)
- **Interface**: Tous les textes en français
- **Devise**: FCFA (Franc CFA)
- **Région**: Afrique/Douala

## Changements récents
- 20 Oct 2025: Intégration complète frontend + backend
  - Backend Django REST complet (port 8000)
  - Frontend React/Vite (port 5000)
  - Hooks personnalisés pour API
  - Composants adaptés au format API
  - Proxy Vite pour communication backend
  - Build production fonctionnel

## Notes de développement

### Communication Frontend-Backend
Le frontend utilise un proxy Vite qui redirige tous les appels `/api/*` vers `http://localhost:8000`. Cela évite les problèmes CORS en développement.

### Hot Reload
Les deux serveurs supportent le hot reload:
- Django: StatReloader
- Vite: Hot Module Replacement (HMR)

### Images produits
Actuellement les produits n'ont pas d'images réelles uploadées. Pour ajouter des images:
1. Via API: POST /api/products/ avec multipart/form-data
2. Via Admin: http://localhost:8000/admin/showcase/product/

### Permissions API
- **Lecture** (GET): Publique, pas d'authentification requise
- **Écriture** (POST/PUT/PATCH/DELETE): Admin uniquement (is_staff=True)

## Prochaines étapes potentielles
1. Ajouter vraies images produits
2. Configurer numéro WhatsApp réel
3. Implémenter page ProductDetail complète
4. Ajouter gestion du panier (optionnel)
5. Optimiser images (compression, thumbnails)
6. Ajouter tests frontend (Vitest)
7. Ajouter tests backend (pytest)
8. Configuration production (gunicorn, nginx)
9. Déploiement via Replit Deployments

## Notes importantes
- **Port 5000**: Seul port exposé publiquement sur Replit
- **Port 8000**: Backend accessible uniquement via proxy
- **JWT tokens**: Expirent après 5h (configurable)
- **Database**: PostgreSQL gérée par Replit
- **Build size**: ~522 KB (gzipped: ~161 KB)
