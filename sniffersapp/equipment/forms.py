from django import forms
from crispy_forms.helper import FormHelper
from django_select2.forms import Select2Widget

from .models import Equipment, EquipmentBooking

class EquipmentForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False

    class Meta:
        model = Equipment
        exclude = ['created_on', 'updated_on', 'created_user']

        widgets = {
            'name': forms.TextInput(attrs={'id': 'name',
                                           'class': 'form-control'}),
            'make': forms.TextInput(attrs={'id': 'name',
                                           'class': 'form-control'}),
            'model': forms.TextInput(attrs={'id': 'model',
                                           'class': 'form-control'}),
            'equipment_type': forms.TextInput(attrs={'id': 'type',
                                           'class': 'form-control'}),
            'purchase_date': forms.TextInput(attrs={'id': 'purchase_date',
                                           'class': 'form-control'}),
            'purchase_amount': forms.TextInput(attrs={'id': 'purchaee_amount',
                                           'class': 'form-control'}),
            'base_rate': forms.TextInput(attrs={'id': 'base_rate',
                                           'class': 'form-control'}),
            'service_lag': forms.TextInput(attrs={'id': 'base_rate',
                                           'class': 'form-control'}),
            'additional_info': forms.TextInput(attrs={'id': 'base_rate',
                                           'class': 'form-control'}),
        }


class EquipmentBookingForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False

    class Meta:
        model = EquipmentBooking
        exclude = ['equipment', 'created_on', 'updated_on', 'created_user']

        widgets = {
            'equipment': Select2Widget(attrs={'id': 'id_equipment',
                                             'class': 'form-control'}),
            'project': Select2Widget(attrs={'id': 'id_project',
                                             'class': 'form-control'}),
            'company': Select2Widget(attrs={'id': 'company_name',
                                             'class': 'form-control'}),
            'start_date': forms.TextInput(attrs={'id': 'start_date',
                                             'class': 'form-control'}),
            'end_date': forms.TextInput(attrs={'id': 'end_date',
                                             'class': 'form-control'}),
            'bookings_days': forms.TextInput(attrs={'id': 'booking_days',
                                             'class': 'form-control'}),
            'booking_cost': forms.TextInput(attrs={'id': 'booking_cost',
                                             'class': 'form-control'}),
            'additional_info': forms.Textarea(attrs={'id': 'additional_info',
                                             'class': 'form-control'}),
        }
