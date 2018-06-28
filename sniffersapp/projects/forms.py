from django import forms

from crispy_forms.helper import FormHelper
from django_select2.forms import Select2Widget

from .models import Project

class ProjectForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False

    class Meta:
        model = Project
        exclude = ('created_user', 'created_on', 'updated_on')

        widgets = {
            'company': Select2Widget(attrs={'id': 'company_name_tag',
                                                   'class': 'form_control_project form-control'}),
            'project_name': forms.TextInput(attrs={'id': 'projecy_name_tag',
                                                   'class': 'form_control_project form-control'}),
            'project_address': forms.TextInput(attrs={'id': 'autocomplete',
                                                      'class': 'form_control_project form-control',
                                                      'onFocus': "geolocate()"}),
            'project_status': forms.Select(attrs={'id': 'project_status_tag',
                                                        'class': 'form_control_project form-control'}),
            'project_forecast_cost': forms.TextInput(attrs={'id': 'project_forecast_cost_tag',
                                                            'class': 'form_control_project form-control'}),
            'project_start_date': forms.DateInput(attrs={'id': 'project_start_date_tag',
                                                               'class': 'form_control_project form-control'}),
            'project_end_date': forms.DateInput(attrs={'id': 'project_end_date_tag',
                                                       'class': 'form_control_project form-control'}),
            'additional_info': forms.Textarea(attrs={'id': "summernote",
                                                     'class': 'form_control_project form-control'}), }
