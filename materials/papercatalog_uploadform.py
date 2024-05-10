from django import forms
from materials.models import *


class UploadProducerPaperCatalogCSVForm(forms.ModelForm):
    producer_catalog_file = forms.FileField(widget=forms.FileInput(attrs={'class': 'dropzone', }), required=True)

    class Meta:
        model = PaperCatalog
        fields = ('producer_catalog_file',)


