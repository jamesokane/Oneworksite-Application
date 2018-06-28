from django import forms
from crispy_forms.helper import FormHelper
from .models import FileImport

class CSVImportForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False

    class Meta:
        model = FileImport
        fields = ('csv_import',)
