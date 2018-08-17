from django import forms

from crispy_forms.helper import FormHelper
from django_select2.forms import Select2Widget, ModelSelect2Widget

from .models import Timesheet

from ..connections.models import Company
from ..equipment.models import Equipment
from ..projects.models import Project


class WeeklyStartTimesheetForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False

    class Meta:
        model = Timesheet
        fields = ('week_start_date', 'week_end_date', 'created_user')


class TimesheetForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False

    company = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        label=u"Company",
        widget=ModelSelect2Widget(
            model=Company,
            search_fields=['company_name__icontains'],
        )
    )

    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        label=u"Project",
        widget=ModelSelect2Widget(
            model=Project,
            search_fields=['project_name__icontains'],
            dependent_fields={'company': 'company'},
            max_results=500,
        )
    )


    class Meta:
        model = Timesheet
        fields = ('dockets', 'timesheet_date', 'week_start_date', 'week_end_date', 'docket_shift', 'equipment', 'equipment_num',
                  'company', 'project', 'start_time', 'finish_time', 'lunch', 'smoko', 'additional_info')

        widgets = {
            'docket': forms.Select(attrs={'id': 'docket_tag',
                                                    'class': 'form_control_timesheet form-control'}),
            'timesheet_date': forms.DateInput(attrs={'id': 'docket_date_tag',
                                                  'class': 'form_control_timesheet form-control '}),
            'docket_shift': forms.Select(attrs={'id': 'docket_shift_tag',
                                                'class': 'form_control_timesheet form-control '}),
            'equipment': Select2Widget(attrs={'id': 'equipment_name_tag',
                                                   'class': 'form_control_timesheet form-control'}),
            'equipment_num': forms.TextInput(attrs={'id': 'equipment_num_tag',
                                                      'class': 'form_control_timesheet form-control '}),
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
