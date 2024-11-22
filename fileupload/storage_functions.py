from printdataplatform.settings import *
from azure.storage.blob import BlobServiceClient
from azure.identity import ManagedIdentityCredential
from django.core.exceptions import ValidationError


def validate_pdf(file):
    if not file.name.endswith('.pdf'):
        raise ValidationError('Het bestand moet een PDF zijn.')


def get_blob_service_client_azure():
    try:
        account_url = "https://printdatastorage.blob.core.windows.net"
        credential = ManagedIdentityCredential
        return BlobServiceClient(account_url=account_url, credential=credential)
    except Exception as e:
        print('Can not connect to Blob Storage production error: ', str(e))
        raise RuntimeError(f"Can not connect to Blob Storage with ManagedIdentityCredential: {e}")


def get_blob_service_client_local():
    try:
        return BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
    except Exception as e:
        print('Can not connect to Blob Storage production error: ', str(e))
        raise RuntimeError(f"Can not connect to Blob Storage Local: {e}")


def upload_pdf_to_azure(file, blob_name, container_name):
    # Maak een verbinding met de blob-service
    try:
        # if DEBUG:
        #     blob_service_client = get_blob_service_client_local()
        # else:
        blob_service_client = get_blob_service_client_azure()
    except Exception as e:
        print('Can not get blob_service_client error: ', str(e))
        raise RuntimeError(f"Can not upload pdf to Blob Storage: {e}")

    # Krijg een referentie naar de container
    try:
        container_client = blob_service_client.get_container_client(container_name)
    except Exception as e:
        print('container_client error: ', str(e))
        raise RuntimeError(f"container_client error: {e}")

    # Upload het bestand
    try:
        container_client.upload_blob(name=blob_name, data=file, overwrite=True)
    except Exception as e:
        print('Upload blob error: ', str(e))
        raise RuntimeError(f"Upload blob error: {e}")


