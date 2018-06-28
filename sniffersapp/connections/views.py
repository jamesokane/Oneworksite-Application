from __future__ import unicode_literals

import csv

from collections import OrderedDict

from django.contrib import messages
from django.http import HttpResponse
# from django.http import QueryDict
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.html import format_html


from .models import Contact, Company
from .forms import ContactForm, CompanyForm, CompanyContactForm, DeleteContactForm, DeleteCompanyForm

from ..notes.models import Notes

# ----------------------------------------#
# ----- CONTACT & COMPANY LIST VIEW ----- #
# ----------------------------------------#


def connections_list(request):
    contact_list = Contact.objects.order_by('first_name')
    company_list = Company.objects.order_by('company_name')

    if request.method == 'GET':
        slug = request.GET.get('content')
        if slug is None:
            try:
                contact = contact_list[0]
                company = company_list[0]
            except IndexError:
                contact = None
                company = None
        elif 'contact_sum' in request.GET.get('name'):
            contact = get_object_or_404(Contact, slug=slug)
            company = None
        elif 'company_sum' in request.GET.get('name'):
            company = get_object_or_404(Company, slug=slug)
            contact = None

    context = {
         'contact_list': contact_list,
         'company_list': company_list,
         'contact': contact,
         'company': company,
     }
    template = 'connections/connection_list.html'
    return render(request, template, context)


# ----------------------------------------#
# ------------ CONTACT VIEWS ------------ #
# ----------------------------------------#

def contact_detail(request, slug, *args, **kwargs):
    contact = get_object_or_404(Contact, slug=slug)

    context = {
        'contact': contact,
    }
    template = 'connections/contact_detail.html'
    return render(request, template, context)


def contact_new(request, *args, **kwargs):
    contact_list = Contact.objects.all()
    company_list = Company.objects.all()
    company_name_list = list(company_list.values_list('company_name', flat=True))

    if request.method == "POST":
        contact_form = ContactForm(request.POST)
        company_form = CompanyContactForm(request.POST)
        if contact_form.is_valid():
            contact_form = contact_form.save(commit=False)
            # Instead of having the standard dropdown menu for the company ForeignKey an additional field
            # has been setup so that an Autocomplete field can be used instead. ( additional field = "company_name").
            if contact_form.company_name in company_name_list:
                # If the entered company name already exists within the company list than the company ForiegnKey
                # is set to this company name
                contact_form.company = company_list[company_name_list.index(contact_form.company_name)]
                # Check and see if the contact already exists
                for contact in contact_list:
                    # If the first_name, last_name and company already exist show an Alert Message
                    if contact_form.first_name == contact.first_name and contact_form.last_name == \
                     contact.last_name and contact_form.company_id == contact.company_id:
                        contact_form.save()
                        messages.success(request, format_html('New contact added'))
                        messages.warning(request, format_html('A contact with the same details already exists'))
                        return redirect('connections:list')
                contact_form.save()
                messages.success(request, format_html('New contact Added'))
                return redirect('connections:list')
            else:
                # If the entered company name is new save the company name to the company name field within
                # the CompanyForm
                company_form.company_name = contact_form.company_name
                if company_form.is_valid():
                    company_form = company_form.save(commit=False)
                    company = company_form
                    company_form.save()
                    # Set the resource company ForiegnKey as the new company name
                    contact_form.company_id = company.id
                    contact_form.save()
                    # Redirect to new company page so that its information can be completed
                    return redirect('connections:list')
    else:
        contact_form = ContactForm()
        context = {
            'contact_list': contact_list,
            'company_list': company_list,
            'contact_form': contact_form,
        }
        template = 'connections/contact_new.html'
        return render(request, template, context)


def contact_edit(request, slug, *args, **kwargs):
    contact = get_object_or_404(Contact, slug=slug)
    contact_list = Contact.objects.all()
    company_list = Company.objects.all()
    company_name_list = list(Company.objects.all().values_list('company_name', flat=True))

    # Creates a new list with the duplicate items removed so they don't show up in AutoComplete
    contact_location_autocomplete = list(OrderedDict.fromkeys(contact_list.values_list(
                                         'location', flat=True)))

    if request.method == "POST":
        if 'edit_contact' in request.POST:
            contact_form = ContactForm(request.POST, instance=contact)
            company_form = CompanyContactForm(request.POST)
            if contact_form.is_valid():
                contact_form = contact_form.save(commit=False)
                # Check if the entered company name already exists
                if contact_form.company_name in company_name_list:
                    # If the entered company name already exists within the company list than the company ForiegnKey
                    # is set to this company name
                    contact_form.company = company_list[company_name_list.index(contact_form.company_name)]
                    contact_form.save()
                    return redirect('connections:list')
                # If the entered company name is new save the company name to the company name field within
                # the CompanyForm
                else:
                    company_form.company_name = contact_form.company_name
                    if company_form.is_valid():
                        company_form = company_form.save(commit=False)
                        company = company_form
                        company_form.save()
                        # Set the resource company ForiegnKey as the new company name
                        contact_form.company_id = company.id
                        contact_form.save()
                        # Redirect to new company page so that its information can be completed
                        return redirect('connections:list')
        elif 'delete_contact' in request.POST:
            delete_contact_form = DeleteContactForm(request.POST, instance=contact)
            if delete_contact_form.is_valid():
                contact.delete()
                return redirect('connections:list')
    else:
        contact_form = ContactForm(instance=contact)
        delete_contact_form = DeleteContactForm(instance=contact)
        context = {
            'contact': contact,
            'contact_list': contact_list,
            'company_list': company_list,
            'contact_form': contact_form,
            'delete_contact_form': delete_contact_form,
            'contact_location_autocomplete': contact_location_autocomplete,
        }
        template = 'connections/contact_edit.html'
        return render(request, template, context)


def export_contacts_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="contacts.csv"'
    writer = csv.writer(response)
    writer.writerow(['Company',
                     'First Name',
                     'Last Name',
                     'Job Title',
                     'Location',
                     'Email',
                     'Mobile Phone',
                     'Office Phone',
                     'Linkedin',
                     'Facebook',
                     'Twitter',
                     'Additional Info'])
    contact_list = Contact.objects.all().values_list('company_name',
                                                     'first_name',
                                                     'last_name',
                                                     'job_title',
                                                     'location',
                                                     'email_work',
                                                     'phone_mobile',
                                                     'phone_work',
                                                     'linkedin',
                                                     'facebook',
                                                     'twitter',
                                                     'additional_info')
    for contact in contact_list:
        writer.writerow(contact)
    return response

# ----------------------------------------#
# ------------ COMPANY VIEWS ------------ #
# ----------------------------------------#


def company_detail(request, slug, *args, **kwargs):
    company = get_object_or_404(Company, slug=slug)
    contact_list = Contact.objects.all().filter(company=company)
    note_list = Notes.objects.all().filter(company=company)

    if request.method == 'GET':
        slug = request.GET.get('content')
        if slug is None:
            try:
                contact = contact_list[0]
                note = note_list[0]
            except IndexError:
                contact = None
                note = None
        elif 'contact_sum' in request.GET.get('name'):
            contact = get_object_or_404(Contact, slug=slug)
            note = None
        elif 'note_sum' in request.GET.get('name'):
            note = get_object_or_404(Notes, slug=slug)
            print(note.slug)
            contact = contact_list[0]

    context = {
        'company': company,
        'contact': contact,
        'note': note,
        'contact_list': contact_list,
        'note_list': note_list,
    }
    template = 'connections/company_detail.html'
    return render(request, template, context)


def company_new(request, *args, **kwargs):
    contact_list = Contact.objects.all()
    company_list = Company.objects.all()

    if request.method == "POST":
        company_form = CompanyForm(request.POST)
        if company_form.is_valid():
            company_form.save()
            return redirect('connections:list')
    else:
        company_form = CompanyForm()
        context = {
            'contact_list': contact_list,
            'company_list': company_list,
            'company_form': company_form,
        }
        template = 'connections/company_new.html'
        return render(request, template, context)


def export_companies_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="companies.csv"'
    writer = csv.writer(response)
    writer.writerow(['Company Name ',
                     'Website',
                     'Office Email',
                     'Office Phone',
                     'Linkedin',
                     'Facebook',
                     'Twitter',
                     'Additional Info'])
    company_list = Contact.objects.all().values_list('company_name',
                                                     'webaddress_company',
                                                     'company_email',
                                                     'company_phone',
                                                     'linkedin',
                                                     'facebook',
                                                     'twitter',
                                                     'additional_info')
    for company in company_list:
        writer.writerow(company)
    return response


def company_edit(request, slug, *args, **kwargs):
    company = get_object_or_404(Company, slug=slug)
    contact_list = Contact.objects.filter(company=company)

    if request.method == "POST":
        if 'edit_company' in request.POST:
            company_form = CompanyForm(request.POST, instance=company)
            if company_form.is_valid():
                company = company_form.save()
                return redirect('connections:list')
        elif 'delete_company' in request.POST:
            delete_company_form = DeleteCompanyForm(request.POST, instance=company)
            contact_form = ContactForm(request.POST)
            if delete_company_form.is_valid():
                company.delete()
            for contact in contact_list:
                if contact.company is None:
                    contact_form.company_name = None
                    contact = contact_form.save()
            return redirect('connections:list')
    else:
        company_form = CompanyForm(instance=company)
        contact_form = ContactForm(request.POST)
        delete_company_form = DeleteCompanyForm(instance=company)
        context = {
            'company_form': company_form,
            'contact_form': contact_form,
            'delete_company_form': delete_company_form,
            'contact_list': contact_list,
        }
        template = 'connections/company_edit.html'
        return render(request, template, context)
