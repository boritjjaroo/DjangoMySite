from .base import *

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'unsafe-secret-key')

# ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '').split()
ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DJANGO_DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('DJANGO_DB_NAME', 'db.sqlite'),
        'USER': os.environ.get('DJANGO_DB_USER', ''),
        'PASSWORD': os.environ.get('DJANGO_DB_PASSWORD', ''),
        'HOST': os.environ.get('DJANGO_DB_HOST', None),
        'PORT': os.environ.get('DJANGO_DB_PORT', None),
    }
}
