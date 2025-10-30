# Guide de Migration de Base de Données - NIASOTAC

Ce guide explique comment migrer l'application NIASOTAC d'une base de données SQLite vers PostgreSQL, MySQL ou toute autre base de données supportée par Django.

## Table des Matières

1. [Migration SQLite → PostgreSQL](#migration-sqlite--postgresql)
2. [Migration SQLite → MySQL](#migration-sqlite--mysql)
3. [Sauvegarde Avant Migration](#sauvegarde-avant-migration)
4. [Vérification Post-Migration](#vérification-post-migration)
5. [Rollback en Cas de Problème](#rollback-en-cas-de-problème)

---

## Migration SQLite → PostgreSQL

PostgreSQL est recommandé pour la production car il offre de meilleures performances, concurrent users, et fonctionnalités avancées.

### Étape 1 : Installer PostgreSQL

#### Sur Ubuntu/Debian
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

#### Sur macOS
```bash
brew install postgresql
brew services start postgresql
```

#### Sur Windows
Télécharger et installer depuis : https://www.postgresql.org/download/windows/

### Étape 2 : Créer la Base de Données PostgreSQL

```bash
# Se connecter à PostgreSQL
sudo -u postgres psql

# Dans le shell PostgreSQL
CREATE DATABASE niasotac_db;
CREATE USER niasotac_user WITH PASSWORD 'VotreMotDePasseSecurise123!';

# Accorder les privilèges
GRANT ALL PRIVILEGES ON DATABASE niasotac_db TO niasotac_user;

# PostgreSQL 15+ requiert aussi ces permissions
\c niasotac_db
GRANT ALL ON SCHEMA public TO niasotac_user;
GRANT CREATE ON SCHEMA public TO niasotac_user;

# Quitter
\q
```

### Étape 3 : Installer le Pilote PostgreSQL pour Python

```bash
cd backend
pip install psycopg2-binary
# Mettre à jour requirements.txt
pip freeze > requirements.txt
```

### Étape 4 : Sauvegarder les Données de SQLite

```bash
# Créer un dump des données en JSON
cd backend
python manage.py dumpdata --natural-foreign --natural-primary \
    --exclude auth.permission --exclude contenttypes \
    -o datadump.json
```

**Important** : Cette sauvegarde contient toutes vos données (produits, catégories, utilisateurs, etc.)

### Étape 5 : Configurer Django pour PostgreSQL

Éditer `backend/niasotac_backend/settings.py` :

```python
# Remplacer la configuration SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'niasotac_db',
        'USER': 'niasotac_user',
        'PASSWORD': 'VotreMotDePasseSecurise123!',
        'HOST': 'localhost',  # ou l'adresse de votre serveur PostgreSQL
        'PORT': '5432',
    }
}
```

**Avec variables d'environnement (recommandé)** :

Créer/modifier `.env` :
```env
PGDATABASE=niasotac_db
PGUSER=niasotac_user
PGPASSWORD=VotreMotDePasseSecurise123!
PGHOST=localhost
PGPORT=5432
```

Dans `settings.py` :
```python
from decouple import config

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('PGDATABASE'),
        'USER': config('PGUSER'),
        'PASSWORD': config('PGPASSWORD'),
        'HOST': config('PGHOST'),
        'PORT': config('PGPORT'),
    }
}
```

### Étape 6 : Migrer la Structure

```bash
cd backend

# Créer les tables dans PostgreSQL
python manage.py migrate

# Vérifier que les tables ont été créées
python manage.py dbshell
# Dans psql :
\dt
\q
```

### Étape 7 : Importer les Données

```bash
# Charger les données depuis le dump JSON
python manage.py loaddata datadump.json
```

Si vous rencontrez des erreurs, essayez :
```bash
# Charger les données par étapes
python manage.py loaddata datadump.json --ignorenonexistent
```

### Étape 8 : Copier les Fichiers Media

Les fichiers media (images des produits) ne sont pas dans la base de données.

```bash
# Ils sont déjà dans backend/media/, rien à faire
# Juste vérifier les permissions
chmod -R 755 backend/media/
```

### Étape 9 : Vérifier la Migration

```bash
# Vérifier le nombre de produits
python manage.py shell
>>> from showcase.models import Product, Category
>>> print(f"Produits : {Product.objects.count()}")
>>> print(f"Catégories : {Category.objects.count()}")
>>> exit()

# Tester le serveur
python manage.py runserver

# Visiter http://localhost:8000/api/products/
# Vérifier que tous les produits sont présents
```

### Étape 10 : Optimiser PostgreSQL

Créer des index pour améliorer les performances :

```bash
python manage.py dbshell
```

```sql
-- Créer des index sur les champs fréquemment recherchés
CREATE INDEX idx_product_slug ON showcase_product(slug);
CREATE INDEX idx_product_category ON showcase_product(category_id);
CREATE INDEX idx_product_subcategory ON showcase_product(subcategory_id);
CREATE INDEX idx_product_featured ON showcase_product(featured);
CREATE INDEX idx_product_in_stock ON showcase_product(in_stock);
CREATE INDEX idx_category_slug ON showcase_category(slug);
CREATE INDEX idx_category_parent ON showcase_category(parent_id);

-- Analyser les tables
ANALYZE;
```

### Étape 11 : Configurer les Sauvegardes Automatiques

Créer un script de sauvegarde PostgreSQL :

```bash
#!/bin/bash
# /home/user/scripts/backup_postgres.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR=~/backups/niasotac

mkdir -p $BACKUP_DIR

pg_dump -U niasotac_user -h localhost niasotac_db > $BACKUP_DIR/db_backup_$DATE.sql
gzip $BACKUP_DIR/db_backup_$DATE.sql

# Garder les 30 dernières sauvegardes
cd $BACKUP_DIR
ls -t db_backup_*.sql.gz | tail -n +31 | xargs -r rm

echo "Sauvegarde PostgreSQL terminée : $DATE"
```

Automatiser avec cron :
```bash
chmod +x ~/scripts/backup_postgres.sh
crontab -e

# Ajouter :
0 2 * * * ~/scripts/backup_postgres.sh >> ~/backups/niasotac/backup.log 2>&1
```

---

## Migration SQLite → MySQL

### Étape 1 : Installer MySQL

```bash
# Ubuntu/Debian
sudo apt install mysql-server

# macOS
brew install mysql
brew services start mysql
```

### Étape 2 : Créer la Base de Données MySQL

```bash
# Se connecter à MySQL
sudo mysql

# Créer la base et l'utilisateur
CREATE DATABASE niasotac_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'niasotac_user'@'localhost' IDENTIFIED BY 'VotreMotDePasse123!';
GRANT ALL PRIVILEGES ON niasotac_db.* TO 'niasotac_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Étape 3 : Installer le Pilote MySQL

```bash
cd backend
pip install mysqlclient
pip freeze > requirements.txt
```

### Étape 4 : Configurer Django pour MySQL

Dans `settings.py` :

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'niasotac_db',
        'USER': 'niasotac_user',
        'PASSWORD': 'VotreMotDePasse123!',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

### Étape 5 : Suivre les Étapes PostgreSQL

Les étapes 4 à 10 de la migration PostgreSQL s'appliquent également pour MySQL :
- Dump des données SQLite
- Migrations Django
- Import des données
- Vérification

### Sauvegarde MySQL

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
mysqldump -u niasotac_user -p niasotac_db > ~/backups/niasotac/db_backup_$DATE.sql
gzip ~/backups/niasotac/db_backup_$DATE.sql
```

---

## Sauvegarde Avant Migration

**CRUCIAL** : Toujours sauvegarder avant de migrer !

```bash
#!/bin/bash
# Script de sauvegarde pré-migration
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR=~/backups/niasotac/pre_migration_$DATE

mkdir -p $BACKUP_DIR

# Base de données SQLite
cp backend/db.sqlite3 $BACKUP_DIR/

# Dump JSON des données
cd backend
python manage.py dumpdata --natural-foreign --natural-primary \
    --exclude auth.permission --exclude contenttypes \
    -o $BACKUP_DIR/datadump.json

# Fichiers media
cp -r backend/media $BACKUP_DIR/

# Configuration
cp backend/niasotac_backend/settings.py $BACKUP_DIR/
cp .env $BACKUP_DIR/ 2>/dev/null || true

# Compresser
cd ~/backups/niasotac
tar -czf pre_migration_$DATE.tar.gz pre_migration_$DATE/
rm -rf pre_migration_$DATE/

echo "Sauvegarde pré-migration créée : pre_migration_$DATE.tar.gz"
echo "Emplacement : ~/backups/niasotac/pre_migration_$DATE.tar.gz"
```

---

## Vérification Post-Migration

### Checklist de Vérification

```bash
# 1. Vérifier le nombre d'enregistrements
cd backend
python manage.py shell <<EOF
from showcase.models import Product, Category
from django.contrib.auth.models import User

print("=== VÉRIFICATION POST-MIGRATION ===")
print(f"Produits : {Product.objects.count()}")
print(f"Catégories : {Category.objects.count()}")
print(f"Utilisateurs : {User.objects.count()}")
print("===================================")
EOF
```

**Comparer avec SQLite** :
```bash
# Dans une autre terminal, avec l'ancienne base SQLite
sqlite3 backend/db.sqlite3
SELECT COUNT(*) FROM showcase_product;
SELECT COUNT(*) FROM showcase_category;
SELECT COUNT(*) FROM auth_user;
.quit
```

### Tests Fonctionnels

```bash
# 2. Tester les requêtes API
curl http://localhost:8000/api/products/ | jq '.results | length'
curl http://localhost:8000/api/categories/ | jq '. | length'
curl http://localhost:8000/api/settings/ | jq '.'

# 3. Tester l'admin Django
# Visiter http://localhost:8000/admin/
# Se connecter et vérifier les produits/catégories

# 4. Tester la recherche
curl "http://localhost:8000/api/products/?search=HP" | jq '.results | length'

# 5. Tester les filtres
curl "http://localhost:8000/api/products/?in_stock=true" | jq '.results | length'
curl "http://localhost:8000/api/products/?featured=true" | jq '.results | length'
```

### Tests d'Intégrité

```bash
python manage.py shell

# Vérifier l'intégrité des relations
from showcase.models import Product

# Tous les produits doivent avoir une catégorie
products_without_category = Product.objects.filter(category__isnull=True)
print(f"Produits sans catégorie : {products_without_category.count()}")

# Tous les produits doivent avoir une image
products_without_image = Product.objects.filter(image='')
print(f"Produits sans image : {products_without_image.count()}")

# Vérifier que les images existent physiquement
import os
for product in Product.objects.all():
    if not os.path.exists(product.image.path):
        print(f"Image manquante pour : {product.name}")
```

---

## Rollback en Cas de Problème

Si la migration échoue, voici comment revenir à SQLite :

### Méthode 1 : Restauration Rapide

```bash
# 1. Arrêter le serveur
# Ctrl+C

# 2. Restaurer settings.py
cp ~/backups/niasotac/pre_migration_*/settings.py backend/niasotac_backend/

# Ou modifier manuellement pour remettre SQLite :
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# 3. Restaurer la base SQLite
cp ~/backups/niasotac/pre_migration_*/db.sqlite3 backend/

# 4. Redémarrer
cd backend
python manage.py runserver
```

### Méthode 2 : Restauration Complète

```bash
# Décompresser la sauvegarde complète
cd ~/backups/niasotac
tar -xzf pre_migration_YYYYMMDD_HHMMSS.tar.gz

# Restaurer tous les fichiers
cp pre_migration_*/db.sqlite3 /chemin/vers/backend/
cp pre_migration_*/settings.py /chemin/vers/backend/niasotac_backend/
rm -rf /chemin/vers/backend/media
cp -r pre_migration_*/media /chemin/vers/backend/

# Redémarrer l'application
```

---

## Cas Spéciaux

### Migration avec beaucoup de Données (> 10 000 produits)

Pour de grandes bases de données, utilisez une approche par lots :

```bash
# Dumper par application
python manage.py dumpdata auth.user --indent 2 > users.json
python manage.py dumpdata showcase.category --indent 2 > categories.json
python manage.py dumpdata showcase.product --indent 2 > products.json

# Charger dans l'ordre
python manage.py loaddata users.json
python manage.py loaddata categories.json
python manage.py loaddata products.json
```

### Migration vers une Base de Données Distante

Si PostgreSQL/MySQL est sur un serveur distant :

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'niasotac_db',
        'USER': 'niasotac_user',
        'PASSWORD': 'VotreMotDePasse',
        'HOST': '192.168.1.100',  # IP du serveur
        'PORT': '5432',
        'OPTIONS': {
            'connect_timeout': 10,
        },
    }
}
```

**Sécurité** : Utiliser SSL pour les connexions distantes :

```python
'OPTIONS': {
    'sslmode': 'require',
    'sslrootcert': '/path/to/ca-cert.pem',
},
```

---

## Performance : SQLite vs PostgreSQL

### Quand utiliser SQLite ?
- ✅ Développement local
- ✅ Petite application (< 100 utilisateurs simultanés)
- ✅ Pas de traffic concurrent élevé
- ✅ Simplicité de déploiement

### Quand utiliser PostgreSQL ?
- ✅ Production
- ✅ Trafic élevé (> 100 utilisateurs simultanés)
- ✅ Écriture concurrente
- ✅ Fonctionnalités avancées (full-text search, JSON, etc.)
- ✅ Scaling horizontal

### Benchmark Simple

```bash
# Test de performance basique
python manage.py shell

import time
from showcase.models import Product

# Test de lecture
start = time.time()
products = list(Product.objects.all())
print(f"Temps lecture {len(products)} produits : {time.time() - start:.3f}s")

# Test de filtrage
start = time.time()
featured = list(Product.objects.filter(featured=True))
print(f"Temps filtrage produits vedettes : {time.time() - start:.3f}s")
```

---

## Ressources Additionnelles

- **Django Database Documentation** : https://docs.djangoproject.com/en/5.2/ref/databases/
- **PostgreSQL Documentation** : https://www.postgresql.org/docs/
- **MySQL Documentation** : https://dev.mysql.com/doc/

## Support

En cas de problème lors de la migration, contacter le support technique avec :
- Les logs d'erreur complets
- La version de Django et de la base de données
- Les étapes déjà effectuées
