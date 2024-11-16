from django import forms

integer_field = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '  '}),
                                   min_value=0, required=True)

decimal_field = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '  '}),
                                   min_value=0, localize=True, decimal_places=2, required=True)

decimal_field_notreq = forms.DecimalField(
    widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '  '}),
    min_value=0, localize=True, decimal_places=2, required=False)

decimal_field_notreq_negative = forms.DecimalField(
    widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '  '}),
    min_value=-100, localize=True, decimal_places=2, required=False)

integer_field_notreq = forms.IntegerField(
    widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '  '}),
    min_value=0, required=False)

boolean_field = forms.BooleanField(
    widget=forms.CheckboxInput(attrs={'class': 'kt-checkbox', 'type': 'checkbox'}),
    required=False)

boolean_field_check_req = forms.BooleanField(
    widget=forms.CheckboxInput(attrs={'class': 'kt-checkbox', 'type': 'checkbox'}),
    required=True)

char_field_100_true = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '  '}),
                                      max_length=100, required=True)

char_field_200_true = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '  '}),
                                      max_length=200, required=True)

char_field_100_false = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '  '}),
                                       max_length=100, required=False)

char_field_200_false = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '  '}),
                                       max_length=200, required=False)
char_field_1000_true = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '  '}),
                                       max_length=1000, required=True)

char_field_1000_false = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '  '}),
                                        max_length=1000, required=False)

char_field_2500_false = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '  '}),
                                        max_length=2500, required=False)

char_field_2500_req = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '  '}),
                                      max_length=2500, required=True)

date_field = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                             required=False)

textarea = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), max_length=2500, required=False)

url_field_false = forms.URLField(
    widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'url incl https://www.'}),
    required=False)
