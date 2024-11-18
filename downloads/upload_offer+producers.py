from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = '<mystorageaccount>'
    account_key = '<mykey>'
    azure_container = 'media'
    expiration_secs = None