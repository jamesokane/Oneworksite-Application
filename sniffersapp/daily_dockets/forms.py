from django import forms

from crispy_forms.helper import FormHelper
from django_select2.forms import Select2Widget

from .models import Docket

class PrestartForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False

    class Meta:
        model = Docket
        exclude = ('slug', 'docket_num', 'created_on', 'created_on', 'docket_number', 'company_name',
                   'project_name', 'start_time', 'finish_time', 'supervisor', 'lunch', 'smoko', 'supervisor_sign', 'operator_sign', 'docket_day',
                   'equipment_name', 'created_user', 'created_user_name')

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
            'attachments': "Attachments used"
        }

        widgets = {
            'item1': forms.CheckboxInput(attrs={'id': 'item1_tag',
                                                'class': 'form_control_prestart form-control '}),
            'item2': forms.CheckboxInput(attrs={'id': 'item2_tag',
                                                'class': 'form_control_prestart form-control '}),
            'item3': forms.CheckboxInput(attrs={'id': 'item3_tag',
                                                'class': 'form_control_prestart form-control '}),
            'item4': forms.CheckboxInput(attrs={'id': 'item4_tag',
                                                'class': 'form_control_prestart form-control '}),
            'item5': forms.CheckboxInput(attrs={'id': 'item5_tag',
                                                'class': 'form_control_prestart form-control '}),
            'item6': forms.CheckboxInput(attrs={'id': 'item6_tag',
                                                'class': 'form_control_prestart form-control '}),
            'item7': forms.CheckboxInput(attrs={'id': 'item7_tag',
                                                'class': 'form_control_prestart form-control '}),
            'item8': forms.CheckboxInput(attrs={'id': 'item8_tag',
                                                'class': 'form_control_prestart form-control '}),
            'item9': forms.CheckboxInput(attrs={'id': 'item9_tag',
                                                'class': 'form_control_prestart form-control '}),
            'item10': forms.CheckboxInput(attrs={'id': 'item10_tag',
                                                 'class': 'form_control_prestart form-control '}),
            'item11': forms.CheckboxInput(attrs={'id': 'item11_tag',
                                                 'class': 'form_control_prestart form-control '}),
            'item12': forms.CheckboxInput(attrs={'id': 'item12_tag',
                                                 'class': 'form_control_prestart form-control '}),
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
            'attachments': forms.TextInput(attrs={'id': 'attachments_tag',
                                                  'class': 'form_control_prestart form-control ',
                                                  'placeholder': 'Attachments used:'}),
                                                    }

class DocketForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False

    class Meta:
        model = Docket
        fields = ('company', 'project', 'start_time', 'finish_time', 'supervisor', 'lunch', 'smoko')
        labels = {
            'company': "Customer",
            'project': "Project",
            'start_time': "Start Time",
            'finish_time': "Finish Time",
            'supervisor': "Supervisor",
            'lunch': "Lunch",
            'smoko': "Smoko"
        }

        widgets = {
            'company': Select2Widget(attrs={'id': 'company_name_tag',
                                                   'class': 'form_control_prestart form-control'}),
            'project': Select2Widget(attrs={'id': 'project_name_tag',
                                                   'class': 'form_control_prestart form-control'}),
            'start_time': forms.TimeInput(attrs={'id': 'start_time_tag',
                                                 'class': 'form_control_prestart form-control'}),
            'finish_time': forms.TimeInput(attrs={'id': 'finish_time_tag',
                                                  'class': 'form_control_prestart form-control'}),
            'supervisor': forms.TextInput(attrs={'id': 'supervisor_tag',
                                                 'class': 'form_control_prestart form-control'}),
            'lunch': forms.Select(attrs={'id': 'lunch_tag',
                                         'class': 'form_control_prestart form-control '}),
            'smoko': forms.Select(attrs={'id': 'smoko_tag',
                                         'class': 'form_control_prestart form-control '}),
            }


class SignForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False

    class Meta:
        model = Docket
        fields = ('supervisor_sign', 'operator_sign')
        labels = {
            'operator_sign': "Operator's Signature:",
            'supervisor_sign': "Supervisor's Signature:",
        }

        widgets = {
            'operator_sign': forms.TextInput(attrs={'id': 'operator_sign_tag',
                                                    'class': 'form_control_prestart form-control'}),
            'supervisor_sign': forms.TextInput(attrs={'id': 'supervisor_sign_tag',
                                                      'class': 'form_control_prestart form-control'}),
            }
