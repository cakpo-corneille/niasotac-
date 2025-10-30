🛍️ NIASOTAC - Vitrine E-Commerce
Plateforme e-commerce moderne pour la vente de matériel informatique, conçue pour les revendeurs tech au Bénin et ailleurs.

🚀 Démarrage Rapide
Environnement de développement local
bash
# Démarrer l'application (backend + frontend)
bash start.sh
Accès à l'application : http://localhost:5000

📚 Documentation
Guides principaux
Frontend README — développement React + Vite

Backend README — API Django REST

Guide de Maintenance — tâches quotidiennes et mensuelles

Guide de Migration BDD — SQLite → PostgreSQL/MySQL

Guide de Déploiement — Replit, VPS, Docker

Architecture Technique — structure du projet

🛠️ Technologies
Frontend
React 18 + TypeScript

Vite

Tailwind CSS + shadcn/ui

TanStack Query

React Router

Backend
Django 5.2.7

Django REST Framework

SQLite (dev) / PostgreSQL (prod)

Simple JWT

WhiteNoise

📦 Installation
Backend Python
bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py populate_data  # Données de test
python manage.py createsuperuser
python manage.py runserver
Frontend Node.js
bash
cd frontend
npm install
npm run dev
🗂️ Structure du Projet
Code
niasotac/
├── frontend/              # Application React
│   ├── src/              # Code source
│   ├── public/           # Fichiers statiques
│   └── README.md         # Docs frontend
│
├── backend/              # API Django
│   ├── niasotac_backend/ # Configuration Django
│   ├── showcase/         # App principale
│   ├── media/            # Uploads (images)
│   ├── staticfiles/      # Fichiers collectés
│   └── README.md         # Docs backend
│
├── start.sh              # Script de démarrage
├── GUIDE_MAINTENANCE.md
├── GUIDE_MIGRATION_BDD.md
├── GUIDE_DEPLOIEMENT.md
└── replit.md
🔑 Fonctionnalités
Côté client
🖼️ Catalogue produits avec images

🧭 Navigation par catégories/sous-catégories

🔍 Recherche et filtres

📄 Détails produit

📱 Intégration WhatsApp

📬 Formulaire de contact

📱 Responsive design

Côté admin
🔐 Interface Django /admin/

🧮 Gestion produits et catégories

📤 Upload d’images (max 2MB)

⚙️ Paramètres du site

👥 Gestion utilisateurs

🌐 API REST
Endpoints publics
Code
GET  /api/categories/              Liste des catégories
GET  /api/products/                Liste des produits
GET  /api/products/{id}/           Détail d’un produit
GET  /api/products/featured/       Produits vedettes
GET  /api/settings/                Paramètres du site
Authentification JWT
Code
POST /api/token/                   Obtenir un token
POST /api/token/refresh/           Rafraîchir le token
📊 Données de Test
Le projet inclut :

4 catégories principales

12 sous-catégories

37 produits avec images

Pour repeupler la base :

bash
cd backend
python manage.py populate_data
🚢 Déploiement
Sur Replit
Déploiement automatique :

Cliquer sur "Deploy"

Sélectionner "Autoscale"

Déployer

Sur VPS
Voir GUIDE_DEPLOIEMENT.md pour :

Configuration Ubuntu/Debian

Nginx + Gunicorn

PostgreSQL

SSL avec Let’s Encrypt

Docker Compose

🔧 Maintenance
Sauvegardes
bash
# Base de données
cp backend/db.sqlite3 ~/backups/db_$(date +%Y%m%d).sqlite3

# Fichiers media
tar -czf ~/backups/media_$(date +%Y%m%d).tar.gz backend/media/
Monitoring
bash
tail -f /var/log/niasotac/django.log
journalctl -u niasotac -f
📱 Personnalisation
Modifier les informations de contact :

Accéder à /admin/

Aller dans “Paramètres du site”

Modifier :

Numéro WhatsApp

Email, téléphone, adresse

Nom et description entreprise

🔒 Sécurité
Bonnes pratiques incluses :

✅ DEBUG=False en production

✅ SECRET_KEY sécurisé

✅ ALLOWED_HOSTS configuré

✅ Validation des images

✅ CORS et HTTPS

✅ Sauvegardes régulières

📈 Performance
Optimisations intégrées :

WhiteNoise pour les fichiers statiques

Gunicorn multi-workers

Images compressées

Cache frontend (TanStack Query)

Code splitting (Vite)

🐛 Dépannage
Site inaccessible
bash
systemctl restart niasotac
Images non affichées
bash
chmod -R 755 backend/media/
df -h
Erreurs 500
bash
tail -f /var/log/niasotac/error.log
🤝 Ressources
Django : https://docs.djangoproject.com/

React : https://react.dev/

Vite : https://vite.dev/

Tailwind : https://tailwindcss.com/

📬 Contact
Email : contact@niasotac.com

Téléphone : +229 XX XX XX XX

📝 Licence
Ce projet est open source. Utilisation libre sous licence MIT (à adapter selon ton choix).

Version : 1.0.0 Dernière mise à jour : Octobre 2025 Déploiement recommandé : Replit Autoscale ou VPS