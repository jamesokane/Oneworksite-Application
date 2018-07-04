from django import forms
from crispy_forms.helper import FormHelper
from django_select2.forms import Select2Widget

from .models import Equipment


class EquipmentForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False

    class Meta:
        model = Equipment
        exclude = ['created_on', 'updated_on', 'created_user', 'purchase_date', 'purchase_amount',
                   'maintenance', 'fuel', 'rubber_tracks', 'height_restrictor']

        widgets = {
            'equipment_id': forms.TextInput(attrs={'id': 'id',
                                           'class': 'form-control'}),
            'year': forms.TextInput(attrs={'id': 'year',
                                           'class': 'form-control'}),
            'make': forms.TextInput(attrs={'id': 'make',
                                           'class': 'form-control'}),
            'model': forms.TextInput(attrs={'id': 'model',
                                           'class': 'form-control'}),
            'size': forms.TextInput(attrs={'id': 'size',
                                           'class': 'form-control'}),
            'registration': forms.TextInput(attrs={'id': 'registration',
                                                    'class': 'form-control'}),
            'vin': forms.TextInput(attrs={'id': 'vin',
                                                    'class': 'form-control'}),
            'engine_no': forms.TextInput(attrs={'id': 'engine_no',
                                                    'class': 'form-control'}),
            'additional_info': forms.TextInput(attrs={'id': 'base_rate',
                                           'class': 'form-control'}),
        }


class EquipmentExtendedForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False

    class Meta:
        model = Equipment
        exclude = ['created_on', 'updated_on', 'created_user',]

        widgets = {
            'equipment_id': forms.TextInput(attrs={'id': 'id',
                                           'class': 'form-control'}),
            'year': forms.TextInput(attrs={'id': 'year',
                                           'class': 'form-control'}),
            'make': forms.TextInput(attrs={'id': 'make',
                                           'class': 'form-control'}),
            'model': forms.TextInput(attrs={'id': 'model',
                                           'class': 'form-control'}),
            'size': forms.TextInput(attrs={'id': 'size',
                                           'class': 'form-control'}),
            'registration': forms.TextInput(attrs={'id': 'registration',
                                                    'class': 'form-control'}),
            'vin': forms.TextInput(attrs={'id': 'vin',
                                                    'class': 'form-control'}),
            'engine_no': forms.TextInput(attrs={'id': 'engine_no',
                                                    'class': 'form-control'}),
            'purchase_date': forms.TextInput(attrs={'id': 'purchase_date',
                                           'class': 'form-control'}),
            'purchase_amount': forms.TextInput(attrs={'id': 'purchase_amount',
                                                    'class': 'form-control'}),
            'maintenance': forms.TextInput(attrs={'id': 'maintenance',
                                                    'class': 'form-control'}),
            'fuel': forms.TextInput(attrs={'id': 'fuel',
                                                    'class': 'form-control'}),
            'rubber_tracks': forms.TextInput(attrs={'id': 'purchase_date',
                                                    'class': 'form-control'}),
            'height_restrictor': forms.TextInput(attrs={'id': 'purchase_date',
                                                    'class': 'form-control'}),
            'additional_info': forms.TextInput(attrs={'id': 'base_rate',
                                           'class': 'form-control'}),
        }
