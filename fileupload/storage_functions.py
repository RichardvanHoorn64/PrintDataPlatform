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
        credential = ManagedIdentityCredential(account_url=account_url)
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
    try:
        account_url = "https://printdatastorage.blob.core.windows.net"
        credential = ManagedIdentityCredential(account_url=account_url)
        blob_service_client = BlobServiceClient(account_url=account_url, credential=credential)
        container_client = blob_service_client.get_container_client(container_name)
        container_client.upload_blob(name=blob_name, data=file, overwrite=True)
        print(f"Bestand {blob_name} succesvol geüpload naar container {container_name}.")
    except Exception as e:
        print('Can not get blob_service_client error: ', str(e))
        raise RuntimeError(f"Can not upload pdf to Blob Storage: {e}")



