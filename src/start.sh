#!/bin/bash

# Démarrer le backend Django sur localhost:8000
cd backend
python manage.py runserver localhost:8000 &
BACKEND_PID=$!

# Attendre que le backend démarre
sleep 3

# Retourner au répertoire racine et démarrer le frontend
cd ../frontend
npm run dev

# Si le frontend s'arrête, arrêter aussi le backend
kill $BACKEND_PID 2>/dev/null
