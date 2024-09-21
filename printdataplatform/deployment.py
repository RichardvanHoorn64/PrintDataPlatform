import os
from .settings import *
from .settings import BASE_DIR

DEBUG = True

WEBSITE_HOSTNAME = 'www.printdataplatform.com'

ALLOWED_HOSTS = ['printdataplatform.com', 'www.printdataplatform.com',
                 'printdata-platform.com', 'www.printdata-platform.com',
                 'drukwerkmaatwerk.com', 'www.drukwerkmaatwerk.com',
                 'drukkerijvanhoorn.nl', 'www.drukkerijvanhoorn.nl',
                 'veldhuismedia-online.nl', 'www.veldhuismedia-online.nl',
                 'printdataplatform-h9hvdtgfcpgaevdf.westeurope-01.azurewebsites.net',
                 'printdataplatform-dev-gsascdexakh4d6gq.westeurope-01.azurewebsites.net',
                 '169.254.130.3']

CSRF_TRUSTED_ORIGINS = ['https://printdataplatform.com', 'https://drukwerkmaatwerk.com',
                        'https://printdata-platform.com',
                        'https://veldhuismedia-online.nl', 'https://drukkerijvanhoorn.nl',
                        'https://printdataplatform-h9hvdtgfcpgaevdf.westeurope-01.azurewebsites.net',
                        'https://printdataplatform-dev-gsascdexakh4d6gq.westeurope-01.azurewebsites.net',
                        ]

CORS_ALLOWED_ORIGINS = ['https://printdataplatform.com', 'https://127.0.0.1', 'https://52.233.175.59',
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

# DEPLOY STATICFILES TO PRODUCTION
# Set the backend to use django-storages
# STATICFILES_STORAGE = 'storages.backends.azure_storage.AzureStorage'

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": 'storages.backends.azure_storage.AzureStorage',
    },
}

# Azure Storage settings
AZURE_ACCOUNT_NAME = 'printdatastorage'  # Replace with your Azure Storage Account Name
AZURE_CONTAINER = 'static'      # Replace with your actual container name
AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'

# Define STATIC_URL to point to the Azure Blob Storage container
STATIC_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{AZURE_CONTAINER}/'

# Ensure your collected static files are saved to the storage container
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]  # Optional: Define the directory where your static files are stored locally


MEDIA_LOCATION = "media"
MEDIA_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{MEDIA_LOCATION}/'

