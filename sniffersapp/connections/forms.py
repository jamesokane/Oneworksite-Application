from django import forms

from crispy_forms.helper import FormHelper

from .models import Contact, Company


class ContactForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False

    class Meta:
        model = Contact
        exclude = ('uuid', 'slug', 'created_on', 'updated_on', 'order')

        widgets = {
            'company_name': forms.TextInput(attrs={'id': 'contact_company_tag',
                                                   'class': 'form_control_contact form-control'}),
            'first_name': forms.TextInput(attrs={'id': 'contact_first_name_tag',
                                                 'class': 'form_control_contact form-control'}),
            'last_name': forms.TextInput(attrs={'id': 'contact_last_name_tag',
                                                'class': 'form_control_contact form-control'}),
            'job_title': forms.TextInput(attrs={'id': 'contact_job_title_tag',
                                                'class': 'form_control_contact form-control'}),
            'email_work': forms.EmailInput(attrs={'id': 'contact_email_work_tag',
                                                  'class': 'form_control_contact form-control'}),
            'phone_mobile': forms.TextInput(attrs={'id': 'contact_phone_mobile_tag',
                                                   'class': 'form_control_contact form-control'}),
            'phone_work': forms.TextInput(attrs={'id': 'contact_phone_work_tag',
                                                 'class': 'form_control_contact form-control'}),
            'linkedin': forms.TextInput(attrs={'id': 'contact_linkedin_tag',
                                               'class': 'form_control_contact form-control'}),
            'facebook': forms.TextInput(attrs={'id': 'contact_facebook_tag',
                                               'class': 'form_control_contact form-control'}),
            'twitter': forms.TextInput(attrs={'id': 'contact_twitter_tag',
                                              'class': 'form_control_contact form-control'}),
            'location': forms.TextInput(attrs={'id': 'autocomplete',
                                               'class': 'form_control_project form-control',
                                               'onFocus': "geolocate()"}),
            'additional_info': forms.Textarea(attrs={'id': 'summernote',
                                                     'class': 'form_control_contact form-control'}),
            'contact_status': forms.Select(attrs={'id': 'project_status_tag',
                                                  'class': 'form_control_project form-control'}),
                    }


class CompanyForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False

    class Meta:
        model = Company
        exclude = ('uuid', 'slug', 'created_on', 'updated_on')
        widgets = {
            'company_name': forms.TextInput(attrs={'id': 'company_company_name_tag',
                                                   'class': 'form_control_company form-control'}),
            'webaddress_company': forms.TextInput(attrs={'id': 'company_webaddress_company_tag',
                                                         'class': 'form_control_company form-control'}),
            'company_email': forms.EmailInput(attrs={'id': 'company_company_email_tag',
                                                     'class': 'form_control_company form-control'}),
            'company_phone': forms.TextInput(attrs={'id': 'company_company_phone_tag',
                                                    'class': 'form_control_company form-control'}),
            'linkedin': forms.TextInput(attrs={'id': 'company_linkedin_tag',
                                               'class': 'form_control_company form-control'}),
            'facebook': forms.TextInput(attrs={'id': 'company_facebook_tag',
                                               'class': 'form_control_company form-control'}),
            'twitter': forms.TextInput(attrs={'id': 'company_twitter_tag',
                                              'class': 'form_control_company form-control'}),
            'additional_info': forms.Textarea(attrs={'id': 'company_info_tag',
                                                     'class': 'form_control_company form-control'}),
            'company_status': forms.Select(attrs={'id': 'company_status_tag',
                                                  'class': 'form_control_project form-control'}),
                                                  }

class CompanyContactForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False

    class Meta:
        model = Company
        fields = ('company_name',)


class DeleteContactForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False

    class Meta:
        model = Contact
        fields = []


class DeleteCompanyForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False

    class Meta:
        model = Company
        fields = []
