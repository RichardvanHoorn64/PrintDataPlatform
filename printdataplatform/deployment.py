import os
from .settings import *
from .settings import BASE_DIR

DEBUG = False

WEBSITE_HOSTNAME = 'www.printdataplatform.com'

ALLOWED_HOSTS = ['printdataplatform.com', 'www.printdataplatform.com',
                 'printdataplatform.com', 'www.printdataplatform.com',
                 'drukwerkmaatwerk.com', 'www.drukwerkmaatwerk.com',
                 'drukkerijvanhoorn.nl', 'www.drukkerijvanhoorn.nl',
                 'veldhuismedia-online.nl', 'www.veldhuismedia-online.nl',
                 'printdataplatform-h9hvdtgfcpgaevdf.westeurope-01.azurewebsites.net',
                 'printdataplatform-dev-gsascdexakh4d6gq.westeurope-01.azurewebsites.net',
                 '169.254.130.3']

CSRF_TRUSTED_ORIGINS = ['https://127.0.0.1',
                        'https://printdataplatform.com', 'https://drukwerkmaatwerk.com',
                        'https://printdata-platform.com', 'https://printdata-platform.org',
                        'https://veldhuismedia-online.nl', 'https://drukkerijvanhoorn.nl',
                        'https://printdataplatform-h9hvdtgfcpgaevdf.westeurope-01.azurewebsites.net',
                        'https://printdataplatform-dev-gsascdexakh4d6gq.westeurope-01.azurewebsites.net',
                        ]

CORS_ALLOWED_ORIGINS = ['https://drukwerkmaatwerk.com',
                        'https://printdataplatform.com', 'https://127.0.0.1', 'https://52.233.175.59',
                        'https://printdata-platform.com', 'https://printdata-platform.org',
                        'https://veldhuismedia-online.nl', 'https://drukkerijvanhoorn.nl',
                        'https://printdataplatform-h9hvdtgfcpgaevdf.westeurope-01.azurewebsites.net',
                        'https://printdataplatform-dev-gsascdexakh4d6gq.westeurope-01.azurewebsites.net',
                        ]

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ['DJANGO_DATABASE_NAME'],
            'USER': os.environ['DJANGO_DATABASE_USER'],
            'PASSWORD': os.environ['DJANGO_DATABASE_PASSWORD'],
            'HOST': os.environ['DJANGO_DATABASE_HOST'],
            'PORT': os.environ['DJANGO_DATABASE_PORT'],
            'OPTIONS': {
                'sslmode': 'require',
            }
        }
    }

# email
EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_PORT = os.environ['EMAIL_PORT']
MAIL_USE_TLS = True
EMAIL_TO_USERS = os.environ['EMAIL_TO_USERS']
EMAIL_USERS_PASSWORD = os.environ['EMAIL_USERS_PASSWORD']
EMAIL_TO_ADMIN = os.environ['EMAIL_TO_ADMIN']
EMAIL_ADMIN_PASSWORD = os.environ['EMAIL_ADMIN_PASSWORD']
DEFAULT_FROM_EMAIL = os.environ['DEFAULT_FROM_EMAIL']


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# STORAGES = {
#     "staticfiles": {
#         "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
#     },
# }

DEFAULT_FILE_STORAGE = 'backend.custom_azure.AzureMediaStorage'
STATICFILES_STORAGE = 'backend.custom_azure.AzureStaticStorage'

STATIC_LOCATION = "static"
MEDIA_LOCATION = "media"

AZURE_ACCOUNT_NAME = "printdataplatformstorage"
AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'
STATIC_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
MEDIA_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{MEDIA_LOCATION}/'
