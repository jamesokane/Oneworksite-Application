from django import forms

from crispy_forms.helper import FormHelper

from .models import Timesheet


class TimesheetForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False

    class Meta:
        model = Timesheet
        fields = ('dockets', 'docket_date', 'docket_shift', 'equipment_name', 'equipment_num', 'equipment_hours',
                  'company_name', 'project_name', 'start_time', 'finish_time', 'lunch')

        widgets = {
            'docket': forms.Select(attrs={'id': 'docket_tag',
                                                    'class': 'form_control_timesheet form-control'}),
            'docket_date': forms.DateInput(attrs={'id': 'docket_date_tag',
                                                  'class': 'form_control_timesheet form-control '}),
            'docket_shift': forms.Select(attrs={'id': 'docket_shift_tag',
                                                'class': 'form_control_timesheet form-control '}),
            'equipment_id': forms.TextInput(attrs={'id': 'equipment_name_tag',
                                                     'class': 'form_control_timesheet form-control '}),
            'equipment_num': forms.TextInput(attrs={'id': 'equipment_num_tag',
                                                    'class': 'form_control_timesheet form-control '}),
            'equipment_hours': forms.TextInput(attrs={'id': 'equipment_hours_tag',
                                                      'class': 'form_control_timesheet form-control '}),
            'company_name': forms.TextInput(attrs={'id': 'company_name_tag',
                                                   'class': 'form_control_timesheet form-control'}),
            'project_name': forms.TextInput(attrs={'id': 'project_name_tag',
                                                   'class': 'form_control_timesheet form-control'}),
            'start_time': forms.TimeInput(attrs={'id': 'start_time_tag',
                                                 'class': 'form_control_timesheet form-control'}),
            'finish_time': forms.TimeInput(attrs={'id': 'finish_time_tag',
                                                  'class': 'form_control_timesheet form-control'}),
            'lunch': forms.Select(attrs={'id': 'lunch_tag',
                                         'class': 'form_control_timesheet form-control '}),
                                                    }
