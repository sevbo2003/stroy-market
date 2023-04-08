import os

from corsheaders.defaults import default_headers, default_methods
# from smart_getenv import getenv
from datetime import timedelta


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/0.1.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', '(@s5no*3@a7s-h5rb+*sy0e(#zwdhliu96zo@22qmn)utsc9y8')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG") == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',') if os.getenv('ALLOWED_HOSTS') else []

# If the app is running behind a proxy, this variable must be set with the proxy path
# See https://docs.djangoproject.com/en/0.1.0/ref/settings/#force-script-name



# Application definition

INSTALLED_APPS = [
    'modeltranslation',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party apps
    'corsheaders',
    'django_extensions',
    'django_filters',
    'drf_yasg',
    'rest_framework',

    # Local apps
    'apps.authentication',
    'apps.stroy',
    'apps.stroy.shipping',
    'apps.advertisement',
    'apps.recommendation'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Local middleware
    'core.middleware.RevisionMiddleware',
]

ROOT_URLCONF = 'config.urls'

AUTH_USER_MODEL = 'authentication.User'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.application_info',
            ]
        },
    }
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/0.1.0/ref/settings/#databases

DATABASES_ENGINE_MAP = {
    'mysql': 'django.db.backends.mysql',
    'oracle': 'django.db.backends.oracle',
    'postgresql': 'django.db.backends.postgresql',
    'postgresql_psycopg2': 'django.db.backends.postgresql_pycopg2',
    'sqlite3': 'django.db.backends.sqlite3',
}

DATABASES = {
    'default': {
        'ENGINE': DATABASES_ENGINE_MAP.get(os.getenv('DB_ENGINE')),
        'NAME': os.getenv('DB_NAME', os.path.join(BASE_DIR, 'db.sqlite3')),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'CONN_MAX_AGE': os.getenv('DB_CONN_MAX_AGE', 0),
    }
}

if os.environ.get('DB_ENGINE') == 'oracle':
    DATABASES['default']['OPTIONS'] = {'threaded': True, 'use_returning_into': False}

# Password validation
# https://docs.djangoproject.com/en/0.1.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/0.1.0/topics/i18n/

LANGUAGE_CODE = 'uz-uz'

TIME_ZONE = os.getenv('TIME_ZONE', 'Asia/Tashkent')

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/0.1.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'staticfiles')]

MEDIA_URL = '/media/'
BASE_URL = os.getenv('BASE_URL', 'http://localhost:8000')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# django-cors-headers
# https://pypi.org/project/django-cors-headers/

CORS_ORIGIN_ALLOW_ALL = os.getenv('CORS_ORIGIN_ALLOW_ALL') == 'True'
CORS_ORIGIN_WHITELIST = os.getenv('CORS_ORIGIN_WHITELIST').split(',') if os.getenv('CORS_ORIGIN_WHITELIST') else []

# CORS_ALLOW_HEADERS = getenv(
#     'CORS_ALLOW_HEADERS', type=list, default=list(default_headers)
# )
# CORS_ALLOW_METHODS = getenv(
#     'CORS_ALLOW_METHODS', type=list, default=list(default_methods)
# )

# Django REST framework
# http://www.django-rest-framework.org/api-guide/settings/

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        # 'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'core.paginations.CustomPagination',
    'PAGE_SIZE': 100,
}

REST_USE_JWT = True

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=14),
}

# Celery settings
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


gettext = lambda s: s
LANGUAGES = (
    ('uz', gettext('Uzbek')),
    ('ru', gettext('Russian'))
)
MODELTRANSLATION_DEFAULT_LANGUAGE = 'uz'
MODELTRANSLATION_LANGUAGES = ('uz', 'ru')

DELIVERY_COST = os.getenv('DELIVERY_COST', 0)

ESKIZ_EMAIL=os.getenv('ESKIZ_EMAIL')
ESKIZ_PASSWORD=os.getenv('ESKIZ_PASSWORD')


# Application definitions

APP_VERSION = '1.0.0'
APP_NAME = 'Stroy market'
APP_DESCRIPTION = 'A RESTfull API for project Stroy market'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://localhost:6379/0',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
# SAVE SESSION IN PRODUCTION
# SESSION_COOKIE_DOMAIN = 'backend.stroymarkets.uz'
SESSION_SAVE_EVERY_REQUEST = True