"""
Django settings for agrocontrol project.
"""

import os
from pathlib import Path
import dj_database_url

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-wh=0hyc3+_6#ptbj1&zsw2wmt21b_db7i#bz2mu7k5h_4(4yfi'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False  # ← Mantén False para producción

# ✅ CORREGIDO: Agrega el dominio correcto
ALLOWED_HOSTS = [
    'sitiosprueba.tiusr19pl.cuc-carrera-ti.ac.cr',
    'www.sitiosprueba.tiusr19pl.cuc-carrera-ti.ac.cr',
    '127.0.0.1',  # Para pruebas locales
    'localhost',   # Para pruebas locales
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cultivos',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'agrocontrol.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # ✅ Agregado para templates globales
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'agrocontrol.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'es-es'  # ✅ Cambiado a español
TIME_ZONE = 'America/Costa_Rica'  # ✅ Cambiado a tu zona horaria
USE_I18N = True
USE_TZ = True

# ✅ CONFIGURACIÓN DE ARCHIVOS ESTÁTICOS (CORREGIDA)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # ✅ Directorio para collectstatic
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # ✅ Directorio para archivos estáticos manuales
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ✅ Configuración para servir archivos estáticos en producción
# (Opcional: para desarrollo local con DEBUG=False)
#import sys
#if 'runserver' in sys.argv:
    # Si estás ejecutando runserver, sirve archivos estáticos manualmente
 #   DEBUG = True  # Temporal para desarrollo
 #   ALLOWED_HOSTS = ['*']