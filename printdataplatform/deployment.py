import os
from .settings import *

DEBUG = False

WEBSITE_HOSTNAME = 'www.printdataplatform.com'

ALLOWED_HOSTS = ['printdataplatform.com', 'www.printdataplatform.com',
                 'printdata-platform.com', 'www.printdata-platform.com',
                 'printdata-platform.org',
                 'drukwerkmaatwerk.com', 'www.drukwerkmaatwerk.com',
                 'drukkerijvanhoorn.nl', 'www.drukkerijvanhoorn.nl',
                 'veldhuismedia-online.nl', 'www.veldhuismedia-online.nl',
                 'printdataplatform-h9hvdtgfcpgaevdf.westeurope-01.azurewebsites.net',
                 'printdataplatform-dev-gsascdexakh4d6gq.westeurope-01.azurewebsites.net',
                 '169.254.130.3', '169.254.129.3', '169.254.130.6', '169.254.129.4', '169.254.132.3', '169.254.129.2',
                 '169.254.129.5', '169.254.129.5', '*'
                 ]

CSRF_TRUSTED_ORIGINS = ['https://printdataplatform.com', 'https://www.printdataplatform.com',
                        'https://printdata-platform.com', 'https://printdata-platform.org'
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


# Email settings

