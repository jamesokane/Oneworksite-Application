from django import forms

from crispy_forms.helper import FormHelper
from django_select2.forms import Select2Widget

from .models import Timesheet


class TimesheetForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False

    class Meta:
        model = Timesheet
        fields = ('dockets', 'docket_date', 'docket_shift', 'equipment', 'equipment_hours',
                  'company', 'project', 'start_time', 'finish_time', 'lunch', 'smoko', 'additional_info')

        widgets = {
            'docket': forms.Select(attrs={'id': 'docket_tag',
                                                    'class': 'form_control_timesheet form-control'}),
            'docket_date': forms.DateInput(attrs={'id': 'docket_date_tag',
                                                  'class': 'form_control_timesheet form-control '}),
            'docket_shift': forms.Select(attrs={'id': 'docket_shift_tag',
                                                'class': 'form_control_timesheet form-control '}),
            'equipment': Select2Widget(attrs={'id': 'equipment_name_tag',
                                                   'class': 'form_control_timesheet form-control'}),
            'equipment_hours': forms.TextInput(attrs={'id': 'equipment_hours_tag',
                                                      'class': 'form_control_timesheet form-control '}),
            'company': Select2Widget(attrs={'id': 'company_name_tag',
                                                   'class': 'form_control_timesheet form-control'}),
            'project': Select2Widget(attrs={'id': 'project_name_tag',
                                                   'class': 'form_control_timesheet form-control'}),
            'start_time': forms.TimeInput(attrs={'id': 'start_time_tag',
                                                 'class': 'form_control_timesheet form-control'}),
            'finish_time': forms.TimeInput(attrs={'id': 'finish_time_tag',
                                                  'class': 'form_control_timesheet form-control'}),
            'lunch': forms.Select(attrs={'id': 'lunch_tag',
                                         'class': 'form_control_timesheet form-control '}),
            'smoko': forms.Select(attrs={'id': 'smoko_tag',
                                         'class': 'form_control_timesheet form-control '}),
            'additional_info': forms.Textarea(attrs={'id': 'additional_info_tag',
                                                 'class': 'form_control_timesheet form-control '}),
                                                    }


class ApproveTimesheetForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False

    class Meta:
        model = Timesheet
        fields = ('status',)
