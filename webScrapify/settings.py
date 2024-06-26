"""
Django settings for webScrapify project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url
load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

DEBUG = False

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')


# allowed_hosts = os.getenv('DJANGO_ALLOWED_HOSTS', '127.0.0.1')
# ALLOWED_HOSTS = allowed_hosts.split(',')
ALLOWED_HOSTS = ["*"]

CRISPY_TEMPLATE_PACK = 'bootstrap5'

CSRF_COOKIE_SECURE = True 

SWEETIFY_SWEETALERT_LIBRARY = 'sweetalert2'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'webscrapify_app',
    'django_celery_results',
    'django_celery_beat',
    'widget_tweaks',
    'corsheaders',
    # "whitenoise.runserver_nostatic"
    # oath
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'crispy_forms',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = 'webScrapify.urls'
BASE_DIRs = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIRs, "templates")],
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

WSGI_APPLICATION = 'webScrapify.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#      'default': {
#          'ENGINE': 'django.db.backends.sqlite3',
#          'NAME': BASE_DIR / 'db.sqlite3',
#      }
#  }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.getenv('POSTGRES_DB'),
#         'USER': os.getenv('POSTGRES_USER'),
#         'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
#         'HOST': 'db',
#         'PORT': 5432,
#     }
# }

# Update DATABASES to use the DATABASE_URL from environment variable
import dj_database_url

DATABASES = {
     'default': dj_database_url.config(
         default=os.getenv('DATABASE_URL')
     )
 }

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
] 
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 

MEDIA_ROOT  = [
    os.path.join(BASE_DIR, 'media'),
] 
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# celery

# CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://redis:6379/0')
# CELERY_RESULT_BACKEND = 'redis://redis:6379/0'



# use redis addons
# Get the Redis URL from the environment variable
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')

CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Africa/Nairobi'
CELERY_CACHE_BACKEND = 'django-cache'


# email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587  # TLS port (TLS encryption is required by Gmail)
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False  # SSL is not supported for Gmail SMTP
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')  
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD') 



# Oath
# Google OAuth Settings
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
# ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_EMAIL_VERIFICATION = "none"
LOGIN_REDIRECT_URL = 'webscrapify_app:home'
ACCOUNT_SIGNUP_REDIRECT_URL = 'webscrapify_app:home'


AUTHENTICATION_BACKENDS = (
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': '1043176860772-5iabn6v6sq7rih4ngv4kq6gn5g751d5v.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

LOGOUT_REDIRECT_URL = '/'


CORS_ALLOWED_ORIGINS = [
    "https://webscrapifyy-1c0f0424e97d.herokuapp.com", "http://127.0.0.1",
]

CSRF_TRUSTED_ORIGINS = ['https://webscrapifyy-1c0f0424e97d.herokuapp.com', "http://127.0.0.1"]

CORS_ALLOW_ALL_HEADERS = True