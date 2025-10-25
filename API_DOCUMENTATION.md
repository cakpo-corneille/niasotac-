# NIASOTAC TECHNOLOGIE - Documentation API

## 🔐 Authentification et Permissions

### Système de permissions
L'API utilise un système de permissions à deux niveaux:

- **👁️ Lecture (GET)**: Accessible à tous (public)
- **✏️ Écriture (POST, PUT, PATCH, DELETE)**: Réservée aux administrateurs uniquement

Les utilisateurs non-administrateurs qui tentent de créer, modifier ou supprimer des produits/catégories recevront une erreur `403 Forbidden`.

### Obtenir un token JWT

**Endpoint**: `POST /api/token/`

**Corps de la requête**:
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Réponse**:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Durée de vie**:
- Access token: 5 heures
- Refresh token: 7 jours

### Rafraîchir un token

**Endpoint**: `POST /api/token/refresh/`

**Corps de la requête**:
```json
{
  "refresh": "votre_refresh_token"
}
```

### Utilisation du token

Incluez le token dans l'en-tête Authorization pour toutes les requêtes protégées:

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

---

## 📦 Catégories

### Lister toutes les catégories
**GET** `/api/categories/`

**Permission**: Public (lecture)

**Réponse**:
```json
[
  {
    "id": 1,
    "name": "Ordinateurs",
    "slug": "ordinateurs",
    "icon": "laptop",
    "image": "http://example.com/media/categories/ordinateurs.png",
    "parent": null,
    "subcategories": [
      {
        "id": 2,
        "name": "Ordinateurs portables",
        "slug": "ordinateurs-portables",
        "icon": null,
        "image": null,
        "product_count": 4
      }
    ],
    "product_count": 9,
    "is_main_category": true,
    "created_at": "2025-10-20T15:30:00Z",
    "updated_at": "2025-10-20T15:30:00Z"
  }
]
```

### Catégories principales uniquement
**GET** `/api/categories/main_categories/`

**Permission**: Public (lecture)

Retourne uniquement les catégories de niveau supérieur (sans parent).

### Détails d'une catégorie
**GET** `/api/categories/{slug}/`

**Permission**: Public (lecture)

**Exemple**: `/api/categories/ordinateurs/`

### Produits d'une catégorie
**GET** `/api/categories/{slug}/products/`

**Permission**: Public (lecture)

**Exemple**: `/api/categories/ordinateurs/products/`

Retourne tous les produits appartenant à cette catégorie ou ses sous-catégories.

### Créer une catégorie
**POST** `/api/categories/`

**Permission**: ⚠️ **Administrateur uniquement**

**Corps de la requête**:
```json
{
  "name": "Tablettes",
  "icon": "tablet",
  "parent": null
}
```

**Image** (optionnel): Envoyez comme `multipart/form-data` avec le champ `image`

### Modifier une catégorie
**PUT/PATCH** `/api/categories/{slug}/`

**Permission**: ⚠️ **Administrateur uniquement**

### Supprimer une catégorie
**DELETE** `/api/categories/{slug}/`

**Permission**: ⚠️ **Administrateur uniquement**

⚠️ **Attention**: La suppression d'une catégorie supprime également toutes ses sous-catégories et produits associés.

---

## 🛍️ Produits

### Lister tous les produits
**GET** `/api/products/`

**Permission**: Public (lecture)

**Paramètres de requête**:
- `category={slug}` - Filtrer par catégorie
- `subcategory={slug}` - Filtrer par sous-catégorie
- `brand={nom}` - Filtrer par marque
- `in_stock=true|false` - Filtrer par disponibilité
- `featured=true|false` - Filtrer produits vedettes
- `search={terme}` - Rechercher dans nom, marque, description
- `ordering={champ}` - Trier (name, price, created_at, -created_at)
- `page={numéro}` - Pagination (20 produits par page)

**Exemples**:
```
/api/products/?category=ordinateurs
/api/products/?brand=HP&in_stock=true
/api/products/?search=laptop&ordering=-price
/api/products/?featured=true&page=2
```

**Réponse**:
```json
{
  "count": 35,
  "next": "http://example.com/api/products/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "HP Pavilion 15",
      "slug": "hp-pavilion-15-hp",
      "price": "450000.00",
      "display_price": "450,000 FCFA",
      "brand": "HP",
      "image": "http://example.com/media/products/hp-pavilion.jpg",
      "category_name": "Ordinateurs",
      "subcategory_name": "Ordinateurs portables",
      "in_stock": true,
      "featured": false,
      "created_at": "2025-10-20T15:30:00Z"
    }
  ]
}
```

### Détails d'un produit
**GET** `/api/products/{slug}/`

**Permission**: Public (lecture)

**Exemple**: `/api/products/hp-pavilion-15-hp/`

**Réponse**:
```json
{
  "id": 1,
  "name": "HP Pavilion 15",
  "slug": "hp-pavilion-15-hp",
  "description": "Ordinateur portable performant avec écran 15.6\"...",
  "price": "450000.00",
  "display_price": "450,000 FCFA",
  "brand": "HP",
  "image": "http://example.com/media/products/hp-pavilion.jpg",
  "category": 1,
  "category_name": "Ordinateurs",
  "subcategory": 2,
  "subcategory_name": "Ordinateurs portables",
  "in_stock": true,
  "featured": false,
  "whatsapp_link": "https://wa.me/237XXXXXXXXX?text=Bonjour%20NIASOTAC...",
  "created_at": "2025-10-20T15:30:00Z",
  "updated_at": "2025-10-20T15:30:00Z"
}
```

### Produits vedettes
**GET** `/api/products/featured/`

**Permission**: Public (lecture)

Retourne les 8 produits marqués comme "vedettes".

### Produits récents
**GET** `/api/products/recent/`

**Permission**: Public (lecture)

Retourne les 10 derniers produits ajoutés.

### Liste des marques
**GET** `/api/products/brands/`

**Permission**: Public (lecture)

**Réponse**:
```json
["Asus", "Brother", "Canon", "Corsair", "Dell", "Epson", ...]
```

### Statistiques
**GET** `/api/products/stats/`

**Permission**: Public (lecture)

**Réponse**:
```json
{
  "total_products": 35,
  "in_stock": 28,
  "out_of_stock": 7,
  "featured": 9,
  "by_category": [
    {"name": "Ordinateurs", "count": 9},
    {"name": "Composants", "count": 9},
    {"name": "Imprimantes", "count": 8},
    {"name": "Accessoires", "count": 9}
  ]
}
```

### Créer un produit
**POST** `/api/products/`

**Permission**: ⚠️ **Administrateur uniquement**

**Content-Type**: `multipart/form-data`

**Champs requis**:
- `name` - Nom du produit
- `brand` - Marque
- `description` - Description
- `price` - Prix (décimal)
- `image` - Fichier image (JPG/PNG, max 2MB)
- `category` - ID de la catégorie principale

**Champs optionnels**:
- `subcategory` - ID de la sous-catégorie
- `in_stock` - Disponibilité (par défaut: true)
- `featured` - Produit vedette (par défaut: false)

**Exemple avec curl**:
```bash
curl -X POST http://localhost:5000/api/products/ \
  -H "Authorization: Bearer votre_token" \
  -F "name=Nouveau produit" \
  -F "brand=HP" \
  -F "description=Description du produit" \
  -F "price=250000" \
  -F "category=1" \
  -F "subcategory=2" \
  -F "image=@/path/to/image.jpg"
```

### Modifier un produit
**PUT/PATCH** `/api/products/{slug}/`

**Permission**: ⚠️ **Administrateur uniquement**

Pour une modification partielle, utilisez PATCH. Pour remplacer complètement, utilisez PUT.

### Supprimer un produit
**DELETE** `/api/products/{slug}/`

**Permission**: ⚠️ **Administrateur uniquement**

---

## 📱 Intégration WhatsApp

Chaque produit inclut un champ `whatsapp_link` généré automatiquement qui contient:
- Numéro WhatsApp de NIASOTAC (à configurer)
- Message pré-rempli avec détails du produit

**Format du message**:
```
Bonjour NIASOTAC TECHNOLOGIE,

Je suis intéressé(e) par le produit suivant:

📱 *{Nom du produit}*
🏷️ Marque: {Marque}
💰 Prix: {Prix} FCFA

Merci de me contacter pour plus d'informations.
```

**⚠️ Configuration requise**:
Modifiez le numéro dans `showcase/models.py` ligne 127:
```python
phone_number = "237XXXXXXXXX"  # Remplacer par votre numéro
```

---

## 🔍 Recherche et Filtrage

### Recherche textuelle
Le paramètre `search` effectue une recherche sur:
- Nom du produit
- Marque
- Description

**Exemple**: `/api/products/?search=portable`

### Tri
Utilisez le paramètre `ordering` pour trier:
- `name` - Par nom (A-Z)
- `-name` - Par nom inversé (Z-A)
- `price` - Par prix croissant
- `-price` - Par prix décroissant
- `created_at` - Plus anciens d'abord
- `-created_at` - Plus récents d'abord (défaut)

**Exemple**: `/api/products/?ordering=-price`

### Filtres combinés
Vous pouvez combiner plusieurs filtres:

**Exemple**: 
```
/api/products/?category=ordinateurs&brand=HP&in_stock=true&ordering=-price
```

---

## ⚠️ Codes d'erreur

### 400 Bad Request
Données de requête invalides (champs manquants, format incorrect, etc.)

### 401 Unauthorized
Token manquant ou invalide

### 403 Forbidden
**Permission refusée - Opération réservée aux administrateurs**

Cette erreur apparaît quand un utilisateur non-administrateur tente:
- Créer un produit/catégorie (POST)
- Modifier un produit/catégorie (PUT/PATCH)
- Supprimer un produit/catégorie (DELETE)

### 404 Not Found
Ressource non trouvée (slug/ID invalide)

### 413 Payload Too Large
Image trop volumineuse (max 2MB)

### 415 Unsupported Media Type
Format d'image non supporté (seuls JPG/PNG acceptés)

---

## 🚀 Exemples d'utilisation

### JavaScript (Fetch API)

**Lister les produits**:
```javascript
fetch('http://localhost:5000/api/products/')
  .then(response => response.json())
  .then(data => console.log(data));
```

**Créer un produit (admin)**:
```javascript
const formData = new FormData();
formData.append('name', 'Nouveau produit');
formData.append('brand', 'HP');
formData.append('description', 'Description');
formData.append('price', '250000');
formData.append('category', '1');
formData.append('image', fileInput.files[0]);

fetch('http://localhost:5000/api/products/', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer ' + token
  },
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

### Python (Requests)

```python
import requests

# Lister les produits
response = requests.get('http://localhost:5000/api/products/')
products = response.json()

# Authentification
auth_response = requests.post(
    'http://localhost:5000/api/token/',
    json={'username': 'admin', 'password': 'admin123'}
)
token = auth_response.json()['access']

# Créer un produit
headers = {'Authorization': f'Bearer {token}'}
files = {'image': open('product.jpg', 'rb')}
data = {
    'name': 'Nouveau produit',
    'brand': 'HP',
    'description': 'Description',
    'price': '250000',
    'category': '1'
}
response = requests.post(
    'http://localhost:5000/api/products/',
    headers=headers,
    files=files,
    data=data
)
```

---

## 📊 Pagination

Toutes les listes sont paginées (20 éléments par page).

**Réponse paginée**:
```json
{
  "count": 35,
  "next": "http://localhost:5000/api/products/?page=2",
  "previous": null,
  "results": [...]
}
```

**Navigation**:
- `count`: Nombre total d'éléments
- `next`: URL de la page suivante (null si dernière page)
- `previous`: URL de la page précédente (null si première page)
- `results`: Tableau des éléments de la page

---

## 🔧 Configuration CORS

L'API accepte actuellement toutes les origines (développement).

Pour la production, configurez les origines autorisées dans `settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "https://votre-frontend.com",
]
```

---

## 📞 Support

Pour toute question concernant l'API, contactez l'équipe NIASOTAC TECHNOLOGIE.
