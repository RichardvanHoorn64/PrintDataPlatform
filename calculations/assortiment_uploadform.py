from django import forms
from calculations.models import *


class UploadAssortimentCSVForm(forms.ModelForm):
    assortiment_file = forms.FileField(widget=forms.FileInput(attrs={'class': 'dropzone', }), required=True)

    class Meta:
        model = Calculations
        fields = ('assortiment_file',)


