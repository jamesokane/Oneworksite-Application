from django import forms
from crispy_forms.helper import FormHelper

from .models import Equipment, Attachment


class EquipmentForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False

    class Meta:
        model = Equipment
        fields = ('equipment_id', 'year', 'make', 'model', 'registration', 'additional_info')

        widgets = {
            'equipment_id': forms.TextInput(attrs={'id': 'id',
                                           'class': 'form-control form_control_equipment'}),
            'year': forms.TextInput(attrs={'id': 'year',
                                           'class': 'form-control form_control_equipment'}),
            'make': forms.TextInput(attrs={'id': 'make',
                                           'class': 'form-control form_control_equipment'}),
            'model': forms.TextInput(attrs={'id': 'model',
                                           'class': 'form-control form_control_equipment'}),
            'registration': forms.TextInput(attrs={'id': 'registration',
                                                    'class': 'form-control form_control_equipment'}),
            'additional_info': forms.Textarea(attrs={'id': 'summernote',
                                           'class': 'form-control form_control_equipment'}),
        }

class AttachmentForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False

    class Meta:
        model = Attachment
        fields = ('attachment_id', 'attachment_type', 'additional_info')

        widgets = {
            'attachment_id': forms.TextInput(attrs={'id': 'attachment_id',
                                           'class': 'form-control form_control_attachment'}),
            'attachment_type': forms.TextInput(attrs={'id': 'attachment_type',
                                           'class': 'form-control form_control_attachment'}),
            'additional_info': forms.Textarea(attrs={'id': 'summernote',
                                           'class': 'form-control form_control_attachment'}),
        }
