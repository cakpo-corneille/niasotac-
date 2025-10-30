# Guide de Déploiement - NIASOTAC

Ce guide explique comment déployer l'application NIASOTAC (frontend React + backend Django) en production sur différentes plateformes.

## Table des Matières

1. [Déploiement sur Replit](#déploiement-sur-replit)
2. [Déploiement sur VPS (Ubuntu/Debian)](#déploiement-sur-vps-ubuntudebian)
3. [Déploiement avec Docker](#déploiement-avec-docker)
4. [Configuration DNS et Domaine](#configuration-dns-et-domaine)
5. [SSL/HTTPS Configuration](#sslhttps-configuration)
6. [Checklist Pré-Déploiement](#checklist-pré-déploiement)
7. [Monitoring et Maintenance Post-Déploiement](#monitoring-et-maintenance-post-déploiement)

---

## Déploiement sur Replit

### Étape 1 : Configuration Actuelle

Le projet est déjà configuré pour Replit avec :
- **Workflow "App"** : Lance backend Django + frontend Vite
- **Configuration de déploiement** : Mode autoscale configuré

### Étape 2 : Vérifier la Configuration

Le fichier `.replit` devrait contenir :

```toml
[deployment]
run = ["bash", "-c", "cd backend && gunicorn --bind=0.0.0.0:5000 --workers=2 --worker-class=gthread --threads=4 niasotac_backend.wsgi:application"]
deploymentTarget = "autoscale"

[[deployment.build]]
command = ["bash", "-c", "cd frontend && npm install && npm run build && cd ../backend && python manage.py collectstatic --noinput"]
```

### Étape 3 : Build du Frontend

Avant de déployer, construire le frontend :

```bash
cd frontend
npm run build
```

Cela crée le dossier `frontend/dist/` avec les fichiers optimisés.

### Étape 4 : Collecter les Fichiers Statiques

```bash
cd backend
python manage.py collectstatic --noinput
```

### Étape 5 : Tester en Mode Production Localement

```bash
cd backend
DEBUG=False python manage.py runserver
```

Vérifier que :
- L'API fonctionne : http://localhost:8000/api/products/
- L'admin fonctionne : http://localhost:8000/admin/
- Les fichiers statiques se chargent

### Étape 6 : Déployer sur Replit

1. Dans l'interface Replit, cliquer sur **"Deploy"**
2. Sélectionner **"Autoscale Deployment"**
3. Vérifier la configuration de build et run
4. Cliquer sur **"Deploy"**

Replit va :
- Installer les dépendances (npm install, pip install)
- Builder le frontend (npm run build)
- Collecter les statiques
- Démarrer Gunicorn

### Étape 7 : Variables d'Environnement Replit

Dans les "Secrets" Replit, ajouter :

```
SECRET_KEY=votre-clé-secrète-très-longue-et-aléatoire
DEBUG=False
```

### Étape 8 : Accéder à l'Application Déployée

Après déploiement, Replit fournit une URL comme :
```
https://niasotac-votre-username.replit.app
```

---

## Déploiement sur VPS (Ubuntu/Debian)

Déploiement complet sur un serveur privé virtuel.

### Prérequis

- Serveur Ubuntu 22.04 LTS ou Debian 12
- Accès root ou sudo
- Nom de domaine pointant vers votre serveur

### Étape 1 : Préparer le Serveur

```bash
# Mettre à jour le système
sudo apt update && sudo apt upgrade -y

# Installer les dépendances système
sudo apt install -y python3.11 python3.11-venv python3-pip \
    nodejs npm nginx postgresql postgresql-contrib \
    git curl build-essential libpq-dev
```

### Étape 2 : Créer un Utilisateur pour l'Application

```bash
# Créer l'utilisateur
sudo adduser niasotac --disabled-password --gecos ""

# Ajouter aux groupes nécessaires
sudo usermod -aG www-data niasotac

# Passer à l'utilisateur
sudo su - niasotac
```

### Étape 3 : Cloner le Projet

```bash
cd /home/niasotac
git clone https://github.com/votre-username/niasotac.git
cd niasotac
```

### Étape 4 : Configurer le Backend

```bash
cd backend

# Créer un environnement virtuel
python3.11 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
pip install gunicorn
```

### Étape 5 : Configurer PostgreSQL

```bash
# Revenir en root
exit

# Créer la base de données
sudo -u postgres psql <<EOF
CREATE DATABASE niasotac_production;
CREATE USER niasotac_user WITH PASSWORD 'MotDePasseSecurise123!';
ALTER ROLE niasotac_user SET client_encoding TO 'utf8';
ALTER ROLE niasotac_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE niasotac_user SET timezone TO 'Africa/Douala';
GRANT ALL PRIVILEGES ON DATABASE niasotac_production TO niasotac_user;
\c niasotac_production
GRANT ALL ON SCHEMA public TO niasotac_user;
EOF
```

### Étape 6 : Configurer les Variables d'Environnement

```bash
sudo su - niasotac
cd /home/niasotac/niasotac/backend

# Créer le fichier .env
cat > .env <<EOF
SECRET_KEY=$(python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
DEBUG=False
ALLOWED_HOSTS=votre-domaine.com,www.votre-domaine.com

PGDATABASE=niasotac_production
PGUSER=niasotac_user
PGPASSWORD=MotDePasseSecurise123!
PGHOST=localhost
PGPORT=5432
EOF

chmod 600 .env
```

### Étape 7 : Modifier settings.py pour Production

Éditer `backend/niasotac_backend/settings.py` :

```python
from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# Utiliser la configuration PostgreSQL (déjà faite dans votre projet)
```

### Étape 8 : Migrations et Collecte des Statiques

```bash
source venv/bin/activate

# Migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Peupler la base (optionnel)
python manage.py populate_data

# Collecter les statiques
python manage.py collectstatic --noinput
```

### Étape 9 : Builder le Frontend

```bash
cd /home/niasotac/niasotac/frontend

# Installer les dépendances
npm install

# Builder pour production
npm run build
```

### Étape 10 : Configurer Gunicorn

```bash
exit  # Revenir en root

# Créer le fichier de service systemd
sudo nano /etc/systemd/system/niasotac.service
```

Contenu :

```ini
[Unit]
Description=NIASOTAC Gunicorn daemon
After=network.target

[Service]
User=niasotac
Group=www-data
WorkingDirectory=/home/niasotac/niasotac/backend
EnvironmentFile=/home/niasotac/niasotac/backend/.env
ExecStart=/home/niasotac/niasotac/backend/venv/bin/gunicorn \
          --bind unix:/run/niasotac.sock \
          --workers 4 \
          --worker-class gthread \
          --threads 2 \
          --timeout 60 \
          --access-logfile /var/log/niasotac/access.log \
          --error-logfile /var/log/niasotac/error.log \
          niasotac_backend.wsgi:application

[Install]
WantedBy=multi-user.target
```

Créer le dossier des logs :

```bash
sudo mkdir -p /var/log/niasotac
sudo chown niasotac:www-data /var/log/niasotac
```

Activer et démarrer le service :

```bash
sudo systemctl daemon-reload
sudo systemctl enable niasotac
sudo systemctl start niasotac
sudo systemctl status niasotac
```

### Étape 11 : Configurer Nginx

```bash
sudo nano /etc/nginx/sites-available/niasotac
```

Contenu :

```nginx
server {
    listen 80;
    server_name votre-domaine.com www.votre-domaine.com;

    client_max_body_size 2M;

    # Logs
    access_log /var/log/nginx/niasotac_access.log;
    error_log /var/log/nginx/niasotac_error.log;

    # Fichiers statiques Django
    location /static/ {
        alias /home/niasotac/niasotac/backend/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Fichiers media (images produits)
    location /media/ {
        alias /home/niasotac/niasotac/backend/media/;
        expires 7d;
    }

    # API Django et Admin
    location / {
        proxy_pass http://unix:/run/niasotac.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

Activer le site :

```bash
sudo ln -s /etc/nginx/sites-available/niasotac /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Étape 12 : Configurer SSL avec Let's Encrypt

```bash
# Installer Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtenir un certificat SSL
sudo certbot --nginx -d votre-domaine.com -d www.votre-domaine.com

# Le renouvellement automatique est configuré par défaut
# Tester le renouvellement :
sudo certbot renew --dry-run
```

Nginx sera automatiquement configuré pour HTTPS.

### Étape 13 : Configurer le Firewall

```bash
# Activer UFW
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
sudo ufw status
```

---

## Déploiement avec Docker

### Étape 1 : Créer le Dockerfile Backend

`backend/Dockerfile` :

```dockerfile
FROM python:3.11-slim

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Dossier de travail
WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copier et installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code
COPY . .

# Collecter les statiques
RUN python manage.py collectstatic --noinput || true

# Exposer le port
EXPOSE 8000

# Commande de démarrage
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "niasotac_backend.wsgi:application"]
```

### Étape 2 : Créer le Dockerfile Frontend

`frontend/Dockerfile` :

```dockerfile
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Image finale nginx
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

`frontend/nginx.conf` :

```nginx
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    server {
        listen 80;
        server_name _;
        root /usr/share/nginx/html;
        index index.html;

        location / {
            try_files $uri $uri/ /index.html;
        }

        location /api/ {
            proxy_pass http://backend:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
```

### Étape 3 : Créer docker-compose.yml

`docker-compose.yml` :

```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: niasotac_db
      POSTGRES_USER: niasotac_user
      POSTGRES_PASSWORD: VotreMotDePasse123
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - niasotac-network

  backend:
    build: ./backend
    command: gunicorn --bind 0.0.0.0:8000 --workers 4 niasotac_backend.wsgi:application
    volumes:
      - ./backend:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    environment:
      - DEBUG=False
      - SECRET_KEY=votre-clé-secrète
      - PGDATABASE=niasotac_db
      - PGUSER=niasotac_user
      - PGPASSWORD=VotreMotDePasse123
      - PGHOST=db
      - PGPORT=5432
    depends_on:
      - db
    networks:
      - niasotac-network

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    networks:
      - niasotac-network

volumes:
  postgres_data:
  static_volume:
  media_volume:

networks:
  niasotac-network:
    driver: bridge
```

### Étape 4 : Lancer avec Docker Compose

```bash
# Construire et démarrer
docker-compose up -d --build

# Exécuter les migrations
docker-compose exec backend python manage.py migrate

# Créer un superutilisateur
docker-compose exec backend python manage.py createsuperuser

# Peupler la base
docker-compose exec backend python manage.py populate_data

# Voir les logs
docker-compose logs -f

# Arrêter
docker-compose down

# Arrêter et supprimer les volumes
docker-compose down -v
```

---

## Configuration DNS et Domaine

### Étape 1 : Acheter un Nom de Domaine

Fournisseurs recommandés :
- **Namecheap** : https://www.namecheap.com/
- **OVH** : https://www.ovhcloud.com/
- **Cloudflare Registrar** : https://www.cloudflare.com/

### Étape 2 : Configurer les DNS

Dans le panneau de votre registrar, créer ces enregistrements :

```
Type    Nom                 Valeur                  TTL
A       @                   VOTRE.IP.SERVEUR.VPS    3600
A       www                 VOTRE.IP.SERVEUR.VPS    3600
AAAA    @                   VOTRE:IPV6::SI:DISPO    3600
```

### Étape 3 : Vérifier la Propagation DNS

```bash
# Vérifier les enregistrements A
dig votre-domaine.com
dig www.votre-domaine.com

# Ou en ligne
https://dnschecker.org
```

La propagation peut prendre 24-48 heures.

---

## SSL/HTTPS Configuration

### Avec Certbot (Recommandé)

Voir [Étape 12 du déploiement VPS](#étape-12--configurer-ssl-avec-lets-encrypt)

### Avec Cloudflare (Alternative)

1. Créer un compte sur https://www.cloudflare.com/
2. Ajouter votre domaine
3. Modifier les nameservers chez votre registrar vers ceux de Cloudflare
4. Dans Cloudflare : SSL/TLS > Chiffrement > Flexible
5. Cloudflare gère automatiquement SSL

**Avantages** :
- SSL gratuit
- CDN global intégré
- Protection DDoS
- Mise en cache automatique

---

## Checklist Pré-Déploiement

### Sécurité

- [ ] DEBUG=False dans settings.py
- [ ] SECRET_KEY changée et sécurisée
- [ ] ALLOWED_HOSTS configuré correctement
- [ ] Mots de passe base de données forts
- [ ] Fichiers .env dans .gitignore
- [ ] CSRF et CORS configurés
- [ ] Validation des uploads (taille, types)

### Performance

- [ ] Fichiers statiques collectés
- [ ] Frontend buildé et optimisé
- [ ] Images produits optimisées
- [ ] Gunicorn avec workers multiples
- [ ] Cache configuré (optionnel)
- [ ] CDN pour fichiers statiques (optionnel)

### Base de Données

- [ ] Migrations appliquées
- [ ] Sauvegardes automatiques configurées
- [ ] Index créés sur champs critiques
- [ ] Contraintes d'intégrité vérifiées

### Monitoring

- [ ] Logs configurés
- [ ] Erreurs 500 loguées
- [ ] Espace disque surveillé
- [ ] Uptime monitoring (UptimeRobot, etc.)

---

## Monitoring et Maintenance Post-Déploiement

### Surveiller les Logs

```bash
# Logs Gunicorn
tail -f /var/log/niasotac/error.log
tail -f /var/log/niasotac/access.log

# Logs Nginx
tail -f /var/log/nginx/niasotac_error.log

# Logs Systemd
journalctl -u niasotac -f
```

### Métriques à Surveiller

1. **Uptime** : Utiliser UptimeRobot ou StatusCake
2. **Temps de réponse** : Doit être < 500ms
3. **Erreurs 5xx** : Doivent être = 0
4. **Espace disque** : Alerter si < 20%
5. **CPU/RAM** : Alerter si > 80%

### Outils Recommandés

- **Sentry** : Tracking d'erreurs - https://sentry.io/
- **Google Analytics** : Analytics visiteurs
- **UptimeRobot** : Monitoring uptime - https://uptimerobot.com/

### Sauvegardes Automatiques

Voir [GUIDE_MAINTENANCE.md](GUIDE_MAINTENANCE.md) section Sauvegardes.

---

## Dépannage Déploiement

### Problème : Erreur 502 Bad Gateway

```bash
# Vérifier que Gunicorn tourne
sudo systemctl status niasotac

# Vérifier les logs
sudo journalctl -u niasotac -n 50

# Redémarrer
sudo systemctl restart niasotac
```

### Problème : Fichiers statiques non trouvés

```bash
# Re-collecter les statiques
cd /home/niasotac/niasotac/backend
source venv/bin/activate
python manage.py collectstatic --noinput

# Vérifier les permissions
sudo chown -R niasotac:www-data staticfiles/
sudo chmod -R 755 staticfiles/
```

### Problème : Base de données non accessible

```bash
# Vérifier PostgreSQL
sudo systemctl status postgresql

# Tester la connexion
psql -U niasotac_user -d niasotac_production -h localhost
```

---

## Ressources

- **Documentation Django Deployment** : https://docs.djangoproject.com/en/5.2/howto/deployment/
- **Gunicorn Documentation** : https://docs.gunicorn.org/
- **Nginx Documentation** : https://nginx.org/en/docs/
- **Docker Documentation** : https://docs.docker.com/

---

## Support

Pour toute assistance au déploiement :
- Vérifier les logs d'erreur
- Consulter la documentation officielle
- Contacter le support technique avec les détails du problème
