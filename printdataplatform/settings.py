"""
Django settings for printdataplatform project.

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-4s5x+pigol*w)@pps!2@sdh6&vu7qwq%!g#(4=z&qv=3gts-@f'


Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
import sys
from pathlib import Path
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

try:
    PRODUCTION = os.environ['DEBUG']
    DEBUG = False
except KeyError:
    DEBUG = True

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
if not DEBUG:
    SECRET_KEY = os.environ['SECRET_KEY']
else:
    SECRET_KEY = 'django-insecure-4s5x+pigol*w)@pps!2@sdh6&vu7qwq%!g#(4=z&qv=3gts-@f'

ALLOWED_HOSTS = ["localhost",
                 '127.0.0.1', '52.233.175.59', 'localhost',
                 'drukwerkmaatwerk.com', 'www.drukwerkmaatwerk.com',
                 'drukkerijvanhoorn.nl', 'www.drukkerijvanhoorn.nl',
                 'veldhuismedia-online.nl', 'www.veldhuismedia-online.nl',
                 'printdataplatform-h9hvdtgfcpgaevdf.westeurope-01.azurewebsites.net',
                 'printdataplatform-dev-gsascdexakh4d6gq.westeurope-01.azurewebsites.net', ]

CSRF_TRUSTED_ORIGINS = ['https://drukwerkmaatwerk.com', 'https://127.0.0.1',
                        'https://veldhuismedia-online.nl', 'https://drukkerijvanhoorn.nl',
                        'https://printdataplatform-h9hvdtgfcpgaevdf.westeurope-01.azurewebsites.net',
                        'https://printdataplatform-dev-gsascdexakh4d6gq.westeurope-01.azurewebsites.net',
                        'https://*.nl', 'https://*.com'
                        ]

CORS_ALLOWED_ORIGINS = ['https://drukwerkmaatwerk.com', 'https://127.0.0.1', 'https://52.233.175.59',
                        'https://veldhuismedia-online.nl', 'https://drukkerijvanhoorn.nl',
                        'https://printdataplatform-h9hvdtgfcpgaevdf.westeurope-01.azurewebsites.net',
                        'https://printdataplatform-dev-gsascdexakh4d6gq.westeurope-01.azurewebsites.net',
                        'https://*.nl', 'https://*.com'
                        ]
# Models autofield without specifying a primary key
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Application definition
WEBSITE_WEBDEPLOY_USE_SCM = True

LOGIN_URL = 'account_login'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # new
    'profileuseraccount.apps.ProfileuseraccountConfig',
    'allauth',  # new
    'allauth.account',  # new
    'allauth.socialaccount',  # new
    # 'allauth.site-packages',  # new
    # 'allauth.site-packageswidget_tweaks',
    # 'allauth.site-packagesallauth',
    'widget_tweaks',
    'django_filters',
    'api',
    'assets',
    'calculations',
    'downloads',
    'index',
    'materials',
    'members',
    'methods',
    'offers',
    'orders',
    'printprojects',
    'producers',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    # language settings
    'django.middleware.locale.LocaleMiddleware',
    # Add the account middleware:
    "allauth.account.middleware.AccountMiddleware",
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'printdataplatform.urls'

WSGI_APPLICATION = 'printdataplatform.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'printdataplatform_dev',
            'USER': 'postgres',
            'PASSWORD': 'PrintdataClub2025',
            'HOST': '127.0.0.1',
            'PORT': '5432',
        }
    }

# Azure DB for production
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ['DJANGO_DATABASE_NAME'],
            'USER': os.environ['DJANGO_DATABASE_USER'],
            'PASSWORD': os.environ['DJANGO_DATABASE_PASSWORD'],
            'HOST': os.environ['DJANGO_DATABASE_HOST'],
            'PORT': '5432',
            'OPTIONS': {
                'sslmode': 'require',
            }
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

# default language
LANGUAGE_CODE = 'nl'

LANGUAGES = (
    ('nl', _('Dutch')),
    ('en', _('English')),
    ('de', _('German')),
)

TIME_ZONE = 'Europe/Amsterdam'
USE_TZ = False

USE_I18N = True
USE_L10N = False

USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = '.'
NUMBER_GROUPING = 3
DECIMAL_SEPARATOR = ','

# Login redirect
LOGIN_REDIRECT_URL = '/welcome/'

# ALLAUTH User account setup
STORE_TOKENS = True
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = False
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7

# ACCOUNT_RATE_LIMITS['login_failed']
SIGNUP_EMAIL_ENTER_TWICE = True
AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_SESSION_REMEMBER = True

ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login/'

ACCOUNT_FORMS = {'login': 'allauth.account.forms.LoginForm',
                 'signup': 'profileuseraccount.forms.registratie_userprofile.UserProfileCreationForm',
                 'add_email': 'allauth.account.forms.AddEmailForm',
                 'change_password': 'allauth.account.forms.ChangePasswordForm',
                 'set_password': 'allauth.account.forms.SetPasswordForm',
                 'reset_password': 'profileuseraccount.forms.forms.ResetPasswordForm',
                 'reset_password_from_key': 'allauth.account.forms.ResetPasswordKeyForm',
                 'disconnect': 'allauth.socialaccount.forms.DisconnectForm', }
AUTH_USER_MODEL = 'profileuseraccount.UserProfile'  # new

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, 'templates/'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Already defined Django-related contexts here

                # `allauth` needs this from django
                'django.template.context_processors.request',
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",)

# Email settings
if not DEBUG:
    EMAIL_HOST = os.environ['EMAIL_HOST']
    EMAIL_PORT = os.environ['EMAIL_PORT']
    EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
    EMAIL_AANMELDEN = os.environ['EMAIL_AANMELDEN']
    EMAIL_ORDERS = os.environ['EMAIL_ORDERS']
    DEFAULT_FROM_EMAIL = os.environ['EMAIL_HOST_USER']
    EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
    EMAIL_USE_TLS = True
    SERVER_EMAIL = os.environ['EMAIL_HOST']

else:
    EMAIL_HOST = 'mail.antagonist.nl'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = 'info@printdataplatform.nl'  # os.environ['EMAIL_HOST_USER']
    EMAIL_AANMELDEN = 'info@printdataplatform.nl'  # os.environ['EMAIL_AANMELDEN']
    EMAIL_ORDERS = 'info@printdataplatform.nl'  # os.environ['EMAIL_ORDERS']
    DEFAULT_FROM_EMAIL = 'info@printdataplatform.nl'  # os.environ['EMAIL_HOST_USER']
    EMAIL_HOST_PASSWORD = '2025#$269396bv'  # os.environ['EMAIL_HOST_PASSWORD']
    SERVER_EMAIL = 'mail.antagonist.nl'  # os.environ['EMAIL_HOST']

# Admin Error handling
ADMINS = [('Errors', 'info@printdataplatform.nl'), ('Richard', 'info@richardvanhoorn.nl')]

# Site id
SITE_ID = 1

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

if not DEBUG:
    DEFAULT_FILE_STORAGE = 'backend.custom_azure.AzureMediaStorage'
    STATICFILES_STORAGE = 'backend.custom_azure.AzureStaticStorage'

    STATIC_LOCATION = "static"
    MEDIA_LOCATION = "media"

    AZURE_ACCOUNT_NAME = "printdataplatformstorage"
    AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'
    STATIC_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
    MEDIA_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{MEDIA_LOCATION}/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field
