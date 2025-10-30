# Guide de Maintenance - NIASOTAC

Ce document décrit les procédures de maintenance courantes pour l'application NIASOTAC (frontend React + backend Django).

## Table des Matières

1. [Maintenance Quotidienne](#maintenance-quotidienne)
2. [Maintenance Hebdomadaire](#maintenance-hebdomadaire)
3. [Maintenance Mensuelle](#maintenance-mensuelle)
4. [Gestion des Produits](#gestion-des-produits)
5. [Gestion des Images](#gestion-des-images)
6. [Sauvegarde et Restauration](#sauvegarde-et-restauration)
7. [Mise à Jour des Dépendances](#mise-à-jour-des-dépendances)
8. [Surveillance et Logs](#surveillance-et-logs)
9. [Résolution de Problèmes Courants](#résolution-de-problèmes-courants)

---

## Maintenance Quotidienne

### 1. Vérifier le Fonctionnement de l'Application

**Fréquence** : Tous les jours

```bash
# Vérifier que les serveurs sont actifs
ps aux | grep "python manage.py runserver"  # Backend
ps aux | grep "vite"                        # Frontend (dev)
ps aux | grep "gunicorn"                    # Backend (production)
```

**Actions** :
- Visiter le site web et vérifier que toutes les pages se chargent
- Tester la recherche de produits
- Vérifier que les images s'affichent correctement
- Tester le bouton WhatsApp

### 2. Vérifier les Logs d'Erreur

```bash
# Logs Django
cd backend
tail -f /var/log/niasotac/django.log  # ou le chemin de vos logs

# Logs système
tail -f /var/log/syslog | grep niasotac
```

**Actions** :
- Rechercher les erreurs 500 ou 404 inhabituelles
- Noter les erreurs répétitives pour investigation
- Vérifier les tentatives de connexion admin suspectes

### 3. Surveiller l'Espace Disque

```bash
# Vérifier l'espace disque disponible
df -h

# Vérifier la taille du dossier media
du -sh backend/media/

# Vérifier la taille de la base de données
ls -lh backend/db.sqlite3  # ou pour PostgreSQL
```

**Seuils d'alerte** :
- Espace disque < 20% : Nettoyer les fichiers inutiles
- Dossier media > 5GB : Optimiser les images
- Base de données > 2GB : Considérer l'archivage

---

## Maintenance Hebdomadaire

### 1. Sauvegarde de la Base de Données

**Fréquence** : Tous les dimanches à 2h00 du matin (ou via cron)

#### SQLite
```bash
#!/bin/bash
# Créer le dossier de sauvegarde
mkdir -p ~/backups/niasotac

# Créer une sauvegarde avec horodatage
DATE=$(date +%Y%m%d_%H%M%S)
cp backend/db.sqlite3 ~/backups/niasotac/db_backup_$DATE.sqlite3

# Compresser la sauvegarde
gzip ~/backups/niasotac/db_backup_$DATE.sqlite3

# Garder seulement les 30 dernières sauvegardes
cd ~/backups/niasotac
ls -t | tail -n +31 | xargs -r rm

echo "Sauvegarde terminée : db_backup_$DATE.sqlite3.gz"
```

#### PostgreSQL
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -U niasotac_user niasotac_db > ~/backups/niasotac/db_backup_$DATE.sql
gzip ~/backups/niasotac/db_backup_$DATE.sql
```

**Automatiser avec cron** :
```bash
# Éditer le crontab
crontab -e

# Ajouter cette ligne pour sauvegarde le dimanche à 2h
0 2 * * 0 /chemin/vers/script/backup.sh
```

### 2. Sauvegarde des Fichiers Media

```bash
#!/bin/bash
DATE=$(date +%Y%m%d)
tar -czf ~/backups/niasotac/media_backup_$DATE.tar.gz backend/media/

# Garder 15 dernières sauvegardes media
cd ~/backups/niasotac
ls -t media_backup_*.tar.gz | tail -n +16 | xargs -r rm
```

### 3. Nettoyer les Fichiers Temporaires

```bash
# Backend
cd backend
python manage.py clearsessions  # Supprimer les sessions expirées

# Logs anciens
find /var/log/niasotac/ -name "*.log" -mtime +30 -delete
```

### 4. Vérifier les Mises à Jour de Sécurité

```bash
# Backend Python
cd backend
pip list --outdated | grep -i security

# Frontend Node.js
cd frontend
npm audit

# Corriger les vulnérabilités automatiquement
npm audit fix
```

---

## Maintenance Mensuelle

### 1. Optimiser la Base de Données

#### SQLite
```bash
# Reconstruire la base pour optimiser l'espace
cd backend
sqlite3 db.sqlite3 "VACUUM;"

# Analyser et optimiser les requêtes
sqlite3 db.sqlite3 "ANALYZE;"
```

#### PostgreSQL
```bash
# Optimiser et nettoyer
psql -U niasotac_user -d niasotac_db -c "VACUUM ANALYZE;"

# Réindexer
psql -U niasotac_user -d niasotac_db -c "REINDEX DATABASE niasotac_db;"
```

### 2. Optimiser les Images

```bash
# Installer les outils d'optimisation
sudo apt install optipng jpegoptim

# Optimiser toutes les images JPEG
find backend/media/products/ -name "*.jpg" -o -name "*.jpeg" | xargs jpegoptim --strip-all --max=85

# Optimiser toutes les images PNG
find backend/media/products/ -name "*.png" | xargs optipng -o2
```

### 3. Analyser les Statistiques

```bash
# Nombre de produits
cd backend
python manage.py shell <<EOF
from showcase.models import Product, Category
print(f"Total produits: {Product.objects.count()}")
print(f"Produits en stock: {Product.objects.filter(in_stock=True).count()}")
print(f"Produits vedettes: {Product.objects.filter(featured=True).count()}")
print(f"Total catégories: {Category.objects.count()}")
EOF
```

### 4. Mettre à Jour la Documentation

- Documenter les nouveaux produits ajoutés
- Mettre à jour les procédures si changements
- Archiver les anciennes versions des guides

---

## Gestion des Produits

### Ajouter un Nouveau Produit

#### Via l'Interface Admin Django

1. Se connecter à `/admin/`
2. Aller dans "Showcase" > "Produits" > "Ajouter produit"
3. Remplir tous les champs :
   - Nom du produit
   - Marque
   - Prix (en FCFA)
   - Description détaillée
   - **Image** (OBLIGATOIRE, max 2MB, JPG/PNG)
   - Catégorie principale
   - Sous-catégorie (optionnel)
   - En stock (coché si disponible)
   - Produit vedette (coché pour affichage sur page d'accueil)
4. Cliquer sur "Enregistrer"

#### Via Commande Django

```bash
cd backend
python manage.py shell

from showcase.models import Product, Category
from django.core.files import File

# Récupérer la catégorie
category = Category.objects.get(name="Ordinateurs")
subcategory = Category.objects.get(name="Ordinateurs portables")

# Créer le produit
product = Product(
    name="Dell XPS 15",
    brand="Dell",
    price=850000,
    description="Ordinateur portable haute performance...",
    category=category,
    subcategory=subcategory,
    in_stock=True,
    featured=True
)

# Attacher l'image
with open('/chemin/vers/image.jpg', 'rb') as f:
    product.image.save('dell-xps-15.jpg', File(f))

product.save()
print(f"Produit créé: {product.name}")
```

### Modifier un Produit Existant

```bash
python manage.py shell

from showcase.models import Product

# Trouver le produit
product = Product.objects.get(slug="hp-pavilion-15-hp")

# Modifier les champs
product.price = 425000  # Nouveau prix
product.in_stock = False  # Plus en stock
product.save()

print(f"Produit mis à jour: {product.name}")
```

### Supprimer un Produit

```bash
python manage.py shell

from showcase.models import Product

# Supprimer un produit (l'image sera aussi supprimée)
Product.objects.get(slug="ancien-produit").delete()
```

### Marquer des Produits comme Rupture de Stock

```bash
python manage.py shell

from showcase.models import Product

# Marquer plusieurs produits en rupture
products_to_update = ["hp-pavilion-15-hp", "dell-latitude-5420-dell"]
Product.objects.filter(slug__in=products_to_update).update(in_stock=False)
```

---

## Gestion des Images

### Taille et Format des Images

**Règles** :
- **Formats acceptés** : JPG, JPEG, PNG
- **Taille maximale** : 2 MB par image
- **Résolution recommandée** : 800x600 pixels minimum
- **Ratio recommandé** : 4:3 ou 16:9

### Ajouter une Image à un Produit

```bash
cd backend
python manage.py shell

from showcase.models import Product
from django.core.files import File

product = Product.objects.get(slug="mon-produit")

with open('/chemin/vers/nouvelle-image.jpg', 'rb') as f:
    product.image.save('nouvelle-image.jpg', File(f))

print(f"Image mise à jour pour: {product.name}")
```

### Remplacer Toutes les Images d'une Catégorie

```bash
python manage.py shell

from showcase.models import Product
from django.core.files import File
from pathlib import Path

# Dossier contenant les nouvelles images
images_dir = Path('/chemin/vers/nouvelles/images')

# Produits de la catégorie
products = Product.objects.filter(category__name="Ordinateurs")

for product in products:
    image_path = images_dir / f"{product.slug}.jpg"
    if image_path.exists():
        with open(image_path, 'rb') as f:
            product.image.save(f"{product.slug}.jpg", File(f))
        print(f"✓ Image mise à jour: {product.name}")
```

### Nettoyer les Images Orphelines

```bash
# Trouver les images qui ne sont plus utilisées
python manage.py shell

from showcase.models import Product
from pathlib import Path

media_dir = Path('backend/media/products')
used_images = set(Product.objects.values_list('image', flat=True))

for image_file in media_dir.glob('*.jpg'):
    if f'products/{image_file.name}' not in used_images:
        print(f"Image orpheline: {image_file}")
        # image_file.unlink()  # Décommenter pour supprimer
```

---

## Sauvegarde et Restauration

### Créer une Sauvegarde Complète

```bash
#!/bin/bash
# Script de sauvegarde complète
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR=~/backups/niasotac/$DATE

mkdir -p $BACKUP_DIR

# Base de données
cp backend/db.sqlite3 $BACKUP_DIR/

# Fichiers media
cp -r backend/media $BACKUP_DIR/

# Configuration
cp backend/niasotac_backend/settings.py $BACKUP_DIR/
cp .env $BACKUP_DIR/ 2>/dev/null || true

# Compresser
cd ~/backups/niasotac
tar -czf backup_complet_$DATE.tar.gz $DATE/
rm -rf $DATE/

echo "Sauvegarde complète créée: backup_complet_$DATE.tar.gz"
```

### Restaurer une Sauvegarde

```bash
#!/bin/bash
# Script de restauration
BACKUP_FILE=$1

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: ./restore.sh backup_complet_YYYYMMDD_HHMMSS.tar.gz"
    exit 1
fi

# Arrêter les serveurs
systemctl stop niasotac-backend  # ou votre méthode d'arrêt

# Décompresser
tar -xzf $BACKUP_FILE -C /tmp/

# Restaurer la base de données
cp /tmp/*/db.sqlite3 backend/

# Restaurer les media
rm -rf backend/media
cp -r /tmp/*/media backend/

# Redémarrer
systemctl start niasotac-backend

echo "Restauration terminée"
```

---

## Mise à Jour des Dépendances

### Backend Python

```bash
cd backend

# Vérifier les mises à jour disponibles
pip list --outdated

# Mettre à jour une dépendance spécifique
pip install --upgrade django

# Mettre à jour toutes les dépendances (ATTENTION : tester d'abord)
pip install --upgrade -r requirements.txt

# Générer le nouveau requirements.txt
pip freeze > requirements.txt
```

### Frontend Node.js

```bash
cd frontend

# Vérifier les mises à jour
npm outdated

# Mettre à jour une dépendance
npm update react

# Mettre à jour toutes les dépendances mineures
npm update

# Mettre à jour les dépendances majeures (avec npm-check-updates)
npx npm-check-updates -u
npm install
```

### Tester Après Mise à Jour

```bash
# Backend
cd backend
python manage.py check
python manage.py test

# Frontend
cd frontend
npm run build
npm run lint
```

---

## Surveillance et Logs

### Configurer les Logs Django

Dans `backend/niasotac_backend/settings.py` :

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/niasotac/django.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### Analyser les Logs

```bash
# Erreurs récentes
tail -n 100 /var/log/niasotac/django.log | grep ERROR

# Requêtes lentes
grep "slow query" /var/log/niasotac/django.log

# Tentatives de connexion admin
grep "admin" /var/log/niasotac/django.log | grep "login"

# Statistiques des erreurs
awk '/ERROR/ {print $3}' /var/log/niasotac/django.log | sort | uniq -c | sort -rn
```

---

## Résolution de Problèmes Courants

### Problème : Site web inaccessible

**Diagnostic** :
```bash
# Vérifier si les serveurs tournent
ps aux | grep python
ps aux | grep gunicorn

# Vérifier les ports
netstat -tulpn | grep :5000
netstat -tulpn | grep :8000

# Vérifier les logs
tail -f /var/log/niasotac/django.log
```

**Solution** :
```bash
# Redémarrer les serveurs
systemctl restart niasotac-backend
systemctl restart niasotac-frontend  # si applicable
```

### Problème : Images ne s'affichent pas

**Diagnostic** :
```bash
# Vérifier les permissions
ls -la backend/media/products/

# Vérifier l'espace disque
df -h
```

**Solution** :
```bash
# Corriger les permissions
chmod -R 755 backend/media/

# Vérifier que les images existent
ls backend/media/products/ | wc -l
```

### Problème : Base de données corrompue

**Solution** :
```bash
# Restaurer depuis sauvegarde
./restore.sh ~/backups/niasotac/backup_complet_latest.tar.gz

# Ou reconstruire depuis zéro
cd backend
rm db.sqlite3
python manage.py migrate
python manage.py populate_data
python manage.py createsuperuser
```

### Problème : Erreurs 500 fréquentes

**Diagnostic** :
```bash
# Activer DEBUG temporairement dans settings.py
DEBUG = True

# Redémarrer et reproduire l'erreur
# Consulter le traceback complet dans les logs

# IMPORTANT : Remettre DEBUG = False après diagnostic
```

### Problème : Performance dégradée

**Solutions** :
1. **Optimiser la base de données** (voir Maintenance Mensuelle)
2. **Optimiser les images** (compression)
3. **Activer le cache Django** :
   ```python
   # settings.py
   CACHES = {
       'default': {
           'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
           'LOCATION': 'cache_table',
       }
   }
   ```
4. **Vérifier les ressources serveur** :
   ```bash
   top
   htop
   free -h
   ```

---

## Checklist de Maintenance

### Quotidienne
- [ ] Vérifier fonctionnement site
- [ ] Consulter logs erreurs
- [ ] Vérifier espace disque

### Hebdomadaire
- [ ] Sauvegarde base de données
- [ ] Sauvegarde fichiers media
- [ ] Nettoyer fichiers temporaires
- [ ] Vérifier mises à jour sécurité

### Mensuelle
- [ ] Optimiser base de données
- [ ] Optimiser images
- [ ] Analyser statistiques
- [ ] Mettre à jour documentation
- [ ] Tester procédures de restauration

### Trimestrielle
- [ ] Audit sécurité complet
- [ ] Revue performances
- [ ] Mise à jour dépendances majeures
- [ ] Formation équipe sur nouvelles fonctionnalités

---

## Contact Support

Pour toute question ou problème non résolu, contacter :
- **Email** : support@niasotac.com
- **Téléphone** : +229 XX XX XX XX

## Ressources Supplémentaires

- Documentation Django : https://docs.djangoproject.com/
- Documentation React : https://react.dev/
- Guide PostgreSQL : https://www.postgresql.org/docs/
- Best Practices : Consulter le fichier BEST_PRACTICES.md
