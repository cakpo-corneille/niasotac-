# 🚀 Guide de démarrage rapide - NIASOTAC TECHNOLOGIE

## ✅ Votre application est prête!

Votre application full-stack est maintenant **complètement fonctionnelle** avec:
- ✅ **Backend Django REST** (35 produits pré-chargés)
- ✅ **Frontend React moderne**
- ✅ **Communication API fonctionnelle**
- ✅ **Interface en français**

## 🎯 Accès rapide

### 🌐 Frontend (Interface publique)
**URL**: https://votre-repl.replit.dev (port 5000)

L'interface utilisateur est accessible à cette adresse. Les visiteurs peuvent:
- Parcourir les catégories et produits
- Voir les détails des produits
- Commander via WhatsApp

### 🔧 Admin Django (Gestion)
**URL**: http://localhost:8000/admin/

**Identifiants**:
- Username: `admin`
- Password: `admin123`

Vous pouvez:
- Gérer les produits et catégories
- Upload des images
- Modifier les prix et descriptions
- Voir les statistiques

### 📊 API REST
**Base URL**: http://localhost:8000/api/

Documentation complète dans `API_DOCUMENTATION.md`

## 📱 Configuration WhatsApp

⚠️ **IMPORTANT**: Configurez votre numéro WhatsApp!

**Fichier**: `showcase/models.py` (ligne 127)

```python
phone_number = "237XXXXXXXXX"  # Remplacez par votre numéro
```

Format: Code pays + numéro (ex: 237698765432)

## 🔄 Workflows actifs

Deux serveurs fonctionnent simultanément:

### 1. Django API Backend (port 8000)
```bash
python manage.py runserver 0.0.0.0:8000
```
- API REST interne
- Admin panel
- Gestion base de données

### 2. Frontend React (port 5000)
```bash
cd frontend && npm run dev
```
- Interface utilisateur
- Accessible publiquement

## 📦 Données incluses

### Catégories (4 principales)
1. **Ordinateurs** 
   - Ordinateurs portables (4 produits)
   - Ordinateurs de bureau (3 produits)
   - Mini PC (2 produits)

2. **Composants**
   - Processeurs (3 produits)
   - Cartes mères (3 produits)
   - Mémoire RAM (3 produits)

3. **Imprimantes**
   - Imprimantes laser (3 produits)
   - Imprimantes jet d'encre (3 produits)
   - Imprimantes multifonctions (2 produits)

4. **Accessoires**
   - Claviers et souris (3 produits)
   - Webcams et microphones (3 produits)
   - Casques audio (3 produits)

**Total**: 35 produits avec descriptions en français

## 🛠️ Commandes utiles

### Repeupler la base de données
```bash
python manage.py populate_data
```
Efface et recrée toutes les données de test.

### Ajouter un produit (via API)
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Utilisez le token reçu:
curl -X POST http://localhost:8000/api/products/ \
  -H "Authorization: Bearer VOTRE_TOKEN" \
  -F "name=Nouveau Produit" \
  -F "brand=HP" \
  -F "description=Description du produit" \
  -F "price=250000" \
  -F "category=1" \
  -F "image=@/chemin/vers/image.jpg"
```

### Build production du frontend
```bash
cd frontend
npm run build
```
Le build sera dans `frontend/dist/`

## 🎨 Personnalisation

### Changer les couleurs
**Fichier**: `frontend/src/index.css`

### Ajouter des produits
1. Via Admin: http://localhost:8000/admin/showcase/product/add/
2. Via API: POST /api/products/ (avec authentification)

### Modifier les catégories
1. Via Admin: http://localhost:8000/admin/showcase/category/
2. Via API: POST /api/categories/ (avec authentification)

## 🔒 Sécurité

### Permissions API
- **Lecture** (GET): Publique ✅
- **Écriture** (POST/PUT/DELETE): Admin uniquement 🔒

### Pour production
1. Changez le `SECRET_KEY` dans `settings.py`
2. Configurez `ALLOWED_HOSTS`
3. Restreignez `CORS_ALLOWED_ORIGINS`
4. Utilisez gunicorn au lieu de runserver

## 📞 Fonctionnalités WhatsApp

Chaque produit génère automatiquement:
- Lien WhatsApp cliquable
- Message pré-rempli avec:
  - Nom du produit
  - Marque
  - Prix en FCFA

## 🐛 Dépannage

### Le frontend ne charge pas les produits
1. Vérifiez que le backend tourne (port 8000)
2. Vérifiez les logs Django: Workflow "Django API Backend"
3. Testez l'API: http://localhost:8000/api/products/

### Erreur 403 lors de l'ajout de produit
Vous devez être authentifié comme admin. Utilisez:
```bash
POST /api/token/ avec {"username":"admin","password":"admin123"}
```

### Les images ne s'affichent pas
1. Vérifiez que `MEDIA_URL` et `MEDIA_ROOT` sont configurés
2. Assurez-vous que le serveur Django sert les fichiers media en dev

## 📚 Documentation complète

- **README.md**: Guide complet d'installation
- **API_DOCUMENTATION.md**: Documentation API détaillée
- **replit.md**: Architecture technique

## ✨ Prochaines étapes

### Obligatoire
1. ⚠️ **Configurer le numéro WhatsApp** (showcase/models.py)
2. 📸 **Ajouter de vraies images** pour les produits

### Optionnel
3. 🎨 Personnaliser les couleurs et le design
4. 📝 Compléter la page Services
5. 📧 Configurer le formulaire Contact
6. 🚀 Déployer en production via Replit Deployments

## 💡 Astuces

### Hot Reload
Les modifications sont détectées automatiquement:
- **Frontend**: Rechargement instantané (HMR)
- **Backend**: Redémarrage automatique

### Tester l'API avec le navigateur
Visitez: http://localhost:8000/api/products/
Django REST Framework affiche une interface navigable!

### Ajouter des filtres
```
/api/products/?category=ordinateurs
/api/products/?brand=HP&in_stock=true
/api/products/?search=laptop&ordering=-price
```

---

## 🆘 Support

Pour toute question:
1. Consultez `API_DOCUMENTATION.md`
2. Vérifiez les logs des workflows
3. Testez l'API via http://localhost:8000/api/

**Bon développement avec NIASOTAC TECHNOLOGIE!** 🚀
