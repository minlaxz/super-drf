"""
Django settings for superduperdrf project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os
import dj_database_url
from datetime import timedelta
from rest_framework.settings import api_settings


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

try:
    IS_CONTAINER = int(os.environ.get('IS_CONTAINER', 0))
except ValueError:
    IS_CONTAINER = False

try:
    IS_SAAS = int(os.environ.get("IS_SAAS", 0))
except ValueError:
    IS_SAAS = False


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-$b)zc9%&djhxe_$12$^5*ykiss&3#*r*a447cmfc%p=8va5uza")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.environ.get('DEBUG', default=1))


ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "*").split(",")


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
    # third party
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'django_fsm',
    'django_prometheus',

    # authentication
    'knox',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    'api.apps.ApiConfig',
    'upload.apps.UploadConfig',
    'superauth.apps.SuperauthConfig',
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

# All Auth
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
# we are turning off email verification for now
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_EMAIL_REQUIRED = False

SITE_ID = 1  # https://dj-rest-auth.readthedocs.io/en/latest/installation.html#registration-optional
REST_USE_JWT = True # use JSON Web Tokens
# JWT_AUTH_COOKIE = "nextjsdrf-access-token"
# JWT_AUTH_REFRESH_COOKIE = "nextjsdrf-refresh-token"
# JWT_AUTH_SAMESITE = "none"

# custom user model, because we do not want to use the Django provided user model
AUTH_USER_MODEL = "superauth.CustomUserModel"

# We need to specify the exact serializer as well for dj-rest-auth, otherwise it will end up shooting itself
REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'superauth.serializers.CustomUserModelSerializer'
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        "knox.auth.TokenAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "dj_rest_auth.utils.JWTCookieAuthentication",
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DATETIME_FORMAT': "iso-8601",
}

REST_KNOX = {
  'SECURE_HASH_ALGORITHM': 'cryptography.hazmat.primitives.hashes.SHA512',
  'AUTH_TOKEN_CHARACTER_LENGTH': 64,
  'TOKEN_TTL': timedelta(hours=10),
  'USER_SERIALIZER': 'knox.serializers.UserSerializer',
  'TOKEN_LIMIT_PER_USER': None,
  'AUTO_REFRESH': False,
  'EXPIRY_DATETIME_FORMAT': api_settings.DATETIME_FORMAT,
}

# OAUTH2_PROVIDER = {
#     'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'groups': 'Access to your groups'}
# }
# H2J3bHlJNH4MlXAYviLWW4hquotHGFB3IWOxz7kl
# YsN2Km9opyWmVZAdvguANc3YYsUkoHhtrdtmLvzTSFzRTxIh3eL33M3YQ6u39ZDXcFDebW6uesnBFqfp5xTze8SoUM5B8bONI1zTv36SW6GlRdWRtpBUNSvHIYf0E80F


MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'superduperdrf.middlewares.RequestResponseMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=3),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True, 
    'UPDATE_LAST_LOGIN': True,
    # "USER_ID_FIELD": "user_id",  # for the custom user model
    # "USER_ID_CLAIM": "user_id",
    "SIGNING_KEY": SECRET_KEY
}

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'https://minlaxz.me',
    'https://minlaxz.vercel.app',
    'https://minlaxz.github.io',
]
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'superduperdrf.urls'

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

WSGI_APPLICATION = 'superduperdrf.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases


DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", BASE_DIR / "db.sqlite3"),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
} if IS_CONTAINER else {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Deploying to fly.io
IS_SAAS = True
if IS_SAAS:
    DATABASE_URL = os.environ.get('DATABASE_URL')
    db_from_env = dj_database_url.config(default=DATABASE_URL, conn_max_age=500, ssl_require=False)
    DATABASES['default'].update(db_from_env)

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "mediafiles"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
