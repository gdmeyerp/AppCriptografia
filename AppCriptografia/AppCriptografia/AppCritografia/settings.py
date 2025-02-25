"""
Django settings for AppCritografia project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-5wgri8muq^--cxl_d)-@z3s1_pqcu=5u(m1el*y)n+tke)$ml8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['gdmeyerp.pythonanywhere.com','localhost','127.0.0.1','jrodriguezru.pythonanywhere.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',  # Módulo de usuarios
    'dashboard',  # Módulo del dashboard
    'vigenere',
    'rsa_p',
    'sustitucion',
    'multiplicativo',
    'hill',
    'permutacion',
    'indiceCoincidencia',
    'AnalisisBrauer',
    'afin',
    'desplazamiento',
    'cifrado_musical',
    'firmaDocumentos',
    'elGamal',
    'des',
    'aes'
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

ROOT_URLCONF = 'AppCritografia.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'AppCritografia.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'

# Define STATIC_ROOT for collectstatic
STATIC_ROOT = BASE_DIR / "staticfiles"

# Define where Django should look for additional static files (if needed)
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # Carpeta global para archivos estáticos

    os.path.join(BASE_DIR, "dashboard/static"),
    os.path.join(BASE_DIR, "vigenere/static"),
    os.path.join(BASE_DIR, "cifrado_musical/static"),
    os.path.join(BASE_DIR, "des/static"),
    os.path.join(BASE_DIR, "aes/static")
]

MEDIA_URL = '/media/'  # URL for accessing media files in the browser

MEDIA_ROOT = BASE_DIR / 'media'

MEDIAFILES_DIRS = [
    os.path.join(BASE_DIR, "media/cifrados"),
    os.path.join(BASE_DIR, "media/descifrados"),
]




# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL = '/dashboard/'  # Redirige al dashboard después de iniciar sesión
LOGOUT_REDIRECT_URL = '/'          # Redirige a la página principal después de cerrar sesión
LOGIN_URL = '/login/'              # Ruta para la página de inicio de sesión