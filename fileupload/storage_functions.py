from printdataplatform.settings import *
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
from django.core.exceptions import ValidationError


def validate_pdf(file):
    if not file.name.endswith('.pdf'):
        raise ValidationError('Het bestand moet een PDF zijn.')


def get_blob_service_client():
    try:
        try:
            account_url = "https://printdatastorage.blob.core.windows.net"
            credential = DefaultAzureCredential()
            return BlobServiceClient(account_url=account_url, credential=credential)
        except Exception as e:
            print('Can not connect to Blob Storage production error: ', str(e))
            raise RuntimeError(f"Can not connect to production Blob Storage,  DefaultAzureCredential: {e}")

        #         return BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
        #     except Exception as e:
        #         print('Can not connect using connection string debug error: ', str(e))
        #         raise RuntimeError(f"Can not connect to lokal Blob Storage, connection string: {e}")
        # else:
        #     try:
        #         account_url = "https://printdatastorage.blob.core.windows.net"
        #         credential = DefaultAzureCredential()
        #         return BlobServiceClient(account_url=account_url, credential=credential)
        #     except Exception as e:
        #         print('Can not connect to Blob Storage production error: ', str(e))
        #         raise RuntimeError(f"Can not connect to production Blob Storage,  DefaultAzureCredential: {e}")
    except Exception as e:
        print('Can not connect to Blob Storage production error: ', str(e))
        raise RuntimeError(f"Can not connect to Blob Storage: {e}")


def upload_pdf_to_azure(file, blob_name, container_name):
    """
    Upload een PDF-bestand naar Azure Blob Storage.

    :param container_name:
    :param file: Bestand (InMemoryUploadedFile of bestandspad)
    :param blob_name: De naam waarmee het bestand wordt opgeslagen in de container
    """
    # Maak een verbinding met de blob-service
    blob_service_client = get_blob_service_client()
    print("Verbinding gemaakt met Blob Storage!")

    # Krijg een referentie naar de container
    container_client = blob_service_client.get_container_client(container_name)

    # Upload het bestand
    container_client.upload_blob(name=blob_name, data=file, overwrite=True)
