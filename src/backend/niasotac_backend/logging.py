import os
from pathlib import Path

# 📍 Répertoire de base du projet
BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR.parent / 'logs'

# 📁 Créer automatiquement le dossier logs/ et les fichiers .log
LOG_DIR.mkdir(exist_ok=True)

for log_file in ['actions.log', 'requests.log', 'errors.log']:
    file_path = LOG_DIR / log_file
    if not file_path.exists():
        file_path.touch()

# ⚙️ Configuration du système de logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} {name} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname}: {message}',
            'style': '{',
        },
    },

    'handlers': {
        'file_actions': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': str(LOG_DIR / 'actions.log'),
            'formatter': 'verbose',
        },
        'file_requests': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': str(LOG_DIR / 'requests.log'),
            'formatter': 'verbose',
        },
        'file_errors': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': str(LOG_DIR / 'errors.log'),
            'formatter': 'verbose',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },

    'loggers': {
        'django': {
            'handlers': ['file_requests', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file_errors'],
            'level': 'ERROR',
            'propagate': False,
        },
        'niasotac.actions': {
            'handlers': ['file_actions'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}
