from django import forms

from crispy_forms.helper import FormHelper
from django_select2.forms import Select2Widget, ModelSelect2Widget

from .models import Docket

from ..connections.models import Company
from ..equipment.models import Equipment
from ..projects.models import Project

class PrestartForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False

    class Meta:
        model = Docket
        exclude = ('slug', 'docket_num', 'created_on', 'created_on', 'docket_number', 'company_name', 'company', 'project',
                   'project_name', 'start_time', 'finish_time', 'supervisor', 'lunch', 'smoko', 'supervisor_sign', 'operator_sign', 'docket_day',
                   'equipment_name', 'created_user', 'created_user_name', 'attachment_1', 'attachment_hours_1', 'attachment_2', 'attachment_hours_2',
                   'attachment_3', 'attachment_hours_3', 'daily_notes')

        labels = {
            'item1': "1. Brakes, steering, gauges, lights, warning devices",
            'item2': "2. Visibility - windscreen, wipers, washers, demisters, mirrors, windows",
            'item3': "3. Cabin - access, seating, seatbelts, loose objects, control levers",
            'item4': "4. Wheels, tyres, nutes, damage, wear, pressure",
            'item5': "5. Guards - in place, secure, warning signs lights, alarms",
            'item6': "6. Hydraulics - rams, hoses, leaks, wear",
            'item7': "7. Excessive wear - hooks, chains, pins, pivots, tracks, G.E.T.",
            'item8': "8. Oils and coolants level",
            'item9': "9. Misc, electrical, fire extinguisher, communications",
            'item10': "10. Quick hitch attachments",
            'item11': "11. You are free from the influences of drugs and alcohol",
            'item12': "12. You are physically and mentally fit to operate or drive",
            'fault': "Details of Fault/defect:",
            'reported_to': "Fault Reported to:",
            'docket_date': "Select Date",
            'docket_shift': "Select Shift",
            'equipment': "Item or Plant",
            'equipment_num': "Unit No.",
            'equipment_hours': "Plant Hours",
        }

        widgets = {
            'item1': forms.Select(attrs={'id': 'item1_tag',
                                                'class': 'form_control_prestart form-control item_option '}),
            'item2': forms.Select(attrs={'id': 'item2_tag',
                                                'class': 'form_control_prestart form-control item_option'}),
            'item3': forms.Select(attrs={'id': 'item3_tag',
                                                'class': 'form_control_prestart form-control item_option'}),
            'item4': forms.Select(attrs={'id': 'item4_tag',
                                                'class': 'form_control_prestart form-control item_option'}),
            'item5': forms.Select(attrs={'id': 'item5_tag',
                                                'class': 'form_control_prestart form-control item_option'}),
            'item6': forms.Select(attrs={'id': 'item6_tag',
                                                'class': 'form_control_prestart form-control item_option'}),
            'item7': forms.Select(attrs={'id': 'item7_tag',
                                                'class': 'form_control_prestart form-control item_option'}),
            'item8': forms.Select(attrs={'id': 'item8_tag',
                                                'class': 'form_control_prestart form-control item_option'}),
            'item9': forms.Select(attrs={'id': 'item9_tag',
                                                'class': 'form_control_prestart form-control item_option'}),
            'item10': forms.Select(attrs={'id': 'item10_tag',
                                                 'class': 'form_control_prestart form-control item_option'}),
            'item11': forms.Select(attrs={'id': 'item11_tag',
                                                 'class': 'form_control_prestart form-control item_option'}),
            'item12': forms.Select(attrs={'id': 'item12_tag',
                                                 'class': 'form_control_prestart form-control item_option'}),
            'fault': forms.Textarea(attrs={'id': 'fault_tag',
                                                 'class': 'form_control_prestart form-control ',
                                                 'placeholder': 'Details of Fault/Defect:'}),
            'reported_to': forms.Textarea(attrs={'id': 'reported_to_tag',
                                                 'class': 'form_control_prestart form-control ',
                                                 'placeholder': 'Fault Reported to:'}),
            'docket_date': forms.DateInput(attrs={'id': 'docket_date_tag',
                                                  'class': 'form_control_prestart form-control '}),
            'docket_shift': forms.Select(attrs={'id': 'docket_shift_tag',
                                                'class': 'form_control_prestart form-control '}),
            'equipment': Select2Widget(attrs={'id': 'equipment_tag',
                                                     'class': 'form_control_prestart form-control '}),
            'equipment_num': forms.TextInput(attrs={'id': 'equipment_num_tag',
                                                    'class': 'form_control_prestart form-control '}),
            'equipment_hours': forms.TextInput(attrs={'id': 'equipment_hours_tag',
                                                      'class': 'form_control_prestart form-control '}),
            }



class DocketForm(forms.ModelForm):
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
        model = Docket
        fields = ( 'company', 'project', 'start_time', 'finish_time', 'lunch', 'smoko',
                  'attachment_1', 'attachment_hours_1', 'attachment_2', 'attachment_hours_2',
                  'attachment_3', 'attachment_hours_3', 'daily_notes')
        labels = {
            'start_time': "Start Time",
            'finish_time': "Finish Time",
            'lunch': "Lunch",
            'smoko': "Smoko",
            'attachment_1': "Attachment",
            'attachment_hours_1': "Attachment Hours",
            'attachment_2': "Attachment",
            'attachment_hours_2': "Attachment Hours",
            'attachment_3': "Attachment",
            'attachment_hours_3': "Attachment Hours",
            'daily_notes': "Daily Notes",
        }

        widgets = {
            'start_time': forms.TimeInput(attrs={'id': 'start_time_tag',
                                                 'class': 'form_control_prestart form-control'}),
            'finish_time': forms.TimeInput(attrs={'id': 'finish_time_tag',
                                                  'class': 'form_control_prestart form-control'}),
            'lunch': forms.Select(attrs={'id': 'lunch_tag',
                                         'class': 'form_control_prestart form-control '}),
            'smoko': forms.Select(attrs={'id': 'smoko_tag',
                                         'class': 'form_control_prestart form-control '}),
            'attachment_1': Select2Widget(attrs={'id': 'attachment_tag_1',
                                               'class': 'form_control_prestart form-control '}),
            'attachment_hours_1': forms.TextInput(attrs={'id': 'attachment_hours_1',
                                                       'class': 'form_control_prestart form-control'}),
            'attachment_2': Select2Widget(attrs={'id': 'attachment_tag_2',
                                               'class': 'form_control_prestart form-control '}),
            'attachment_hours_2': forms.TextInput(attrs={'id': 'attachment_hours_2',
                                                       'class': 'form_control_prestart form-control'}),
            'attachment_3': Select2Widget(attrs={'id': 'attachment_tag_3',
                                               'class': 'form_control_prestart form-control '}),
            'attachment_hours_3': forms.TextInput(attrs={'id': 'attachment_hours_3',
                                                       'class': 'form_control_prestart form-control'}),
            'daily_notes': forms.Textarea(attrs={'id': 'daily_notes',
                                                     'class': 'form_control_prestart form-control'}),
            }


class SignForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False

    class Meta:
        model = Docket
        fields = ('supervisor_sign', 'operator_sign', 'supervisor')
        labels = {
            'operator_sign': "Operator's Signature:",
            'supervisor_sign': "Supervisor's Signature:",
            'supervisor': "Supervisor Name",
        }

        widgets = {
            'operator_sign': forms.TextInput(attrs={'id': 'operator_sign_tag',
                                                    'class': 'form_control_prestart form-control'}),
            'supervisor_sign': forms.TextInput(attrs={'id': 'supervisor_sign_tag',
                                                      'class': 'form_control_prestart form-control'}),
            'supervisor': forms.TextInput(attrs={'id': 'supervisor_tag',
                                                 'class': 'form_control_prestart form-control'}),
            }
