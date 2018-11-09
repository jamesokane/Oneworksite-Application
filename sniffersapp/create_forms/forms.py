from django import forms

from crispy_forms.helper import FormHelper
from django_select2.forms import Select2Widget

from .models import FormNew, FormItem

class FormNewForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False

    class Meta:
        model = FormNew
        fields = ('form_name', 'form_description')

        widgets = {
            'form_name': forms.TextInput(attrs={'id': 'form_name_tag',
                                                   'class': 'form-control',}),
            'form_description': forms.Textarea(attrs={'id': "form_description_tag",
                                                     'class': 'form-control'}),
            }


class FormItemForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False

    class Meta:
        model = FormItem
        fields = ('label', 'help_text', 'required', 'text')

        widgets = {
            'label': forms.TextInput(attrs={'id': 'label_tag',
                                                   'class': 'form-control'}),
            'help_text': forms.TextInput(attrs={'id': "help_text_tag",
                                                     'class': 'form-control'}),
            'required': forms.CheckboxInput(attrs={'id': "required_tag",
                                                     'class': 'form-control'}),
            'text': forms.Textarea(attrs={'id': "text_tag",
                                                     'class': 'form-control'}),
            }
