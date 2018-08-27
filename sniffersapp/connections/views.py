from __future__ import unicode_literals

import csv
import os
import glob

from collections import OrderedDict

from django.contrib import messages
from django.http import HttpResponse
# from django.http import QueryDict
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.html import format_html, strip_tags

from .models import Contact, Company
from .forms import ContactForm, CompanyForm, CompanyContactForm, DeleteContactForm, DeleteCompanyForm

from ..notes.models import Notes

from ..csv_import.models import FileImport
from ..csv_import.forms import CSVImportForm

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

    csv_import_form = CSVImportForm(request.POST, request.FILES)
    if request.method == "POST":
        if 'csv_upload' in request.POST:
            if csv_import_form.is_valid():
                csv_import_form = csv_import_form.save(commit=False)
                csv_import = csv_import_form
                csv_import_form.save()
                # Create file path for csv_import file
                filename = "sniffersapp/media/" + str(csv_import.csv_import)
                with open(filename, 'r') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if row[0] != 'First Name' or row[0] != 'FirstName':
                            _, created = Company.objects.get_or_create(
                                company_name=row[2],
                            )
                            company_list = Company.objects.all()
                            company_name_list = list(Company.objects.all().values_list('company_name', flat=True))
                            _, created = Contact.objects.get_or_create(
                                first_name=row[0],
                                last_name=row[1],
                                company=company_list[company_name_list.index(row[2])],
                                company_name=row[2],
                                job_title=row[3],
                                email_work=row[4],
                                phone_mobile=row[5],
                                phone_work=row[6],
                                linkedin=row[7],
                                facebook=row[8],
                                twitter=row[9],
                                location=row[10],
                                additional_info=row[11],
                                contact_status=row[12],
                            )
                # At the end of the import process delete any files in the FileImport model
                FileImport.objects.all().delete()
                # At the end of the import process delete any files in the csv_import folder
                csv_import_files = glob.glob("sniffersapp/media/csv_import/*")
                for files in csv_import_files:
                    os.remove(files)
                return redirect('connections:list')

    context = {
         'contact_list': contact_list,
         'company_list': company_list,
         'contact': contact,
         'company': company,
         'csv_import_form': csv_import_form,
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

    contact_form = ContactForm(request.POST or None)

    if request.method == "POST":
        if 'new_contact' in request.POST:
            if contact_form.is_valid():
                contact_form = contact_form.save(commit=False)
                for contact in contact_list:
                    # If the first_name, last_name and company already exist show an Alert Message
                    if contact_form.first_name == contact.first_name and contact_form.last_name == \
                             contact.last_name and contact_form.job_title == contact.job_title:
                                messages.warning(request, format_html('A contact with the same details already exists'))
                                return redirect('connections:list')

                contact_form.save()
                messages.success(request, format_html('New contact Added'))
                return redirect('connections:list')


    context = {
        'contact_list': contact_list,
        'company_list': company_list,
        'contact_form': contact_form,
        }
    template = 'connections/contact_new.html'
    return render(request, template, context)


def contact_edit(request, slug, *args, **kwargs):
    contact = get_object_or_404(Contact, slug=slug)

    contact_form = ContactForm(request.POST or None, instance=contact)
    delete_contact_form = DeleteContactForm(request.POST or None, instance=contact)

    if request.method == "POST":
        if 'edit_contact' in request.POST:
            if contact_form.is_valid():
                contact_form.save()
                return redirect('connections:list')

        elif 'delete_contact' in request.POST:
            if delete_contact_form.is_valid():
                contact.delete()
                return redirect('connections:list')

    context = {
        'contact': contact,
        'contact_form': contact_form,
        'delete_contact_form': delete_contact_form,
        }
    template = 'connections/contact_edit.html'
    return render(request, template, context)


def export_contacts_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="people.csv"'
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
    company_list = Company.objects.all().values_list('company_name',
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

    company_form = CompanyForm(request.POST or None, instance=company)
    delete_company_form = DeleteCompanyForm(request.POST or None, instance=company)

    if request.method == "POST":
        if 'edit_company' in request.POST:
            if company_form.is_valid():
                company = company_form.save()
                return redirect('connections:list')
        elif 'delete_company' in request.POST:

            contact_form = ContactForm(request.POST)
            if delete_company_form.is_valid():
                company.delete()
            for contact in contact_list:
                if contact.company is None:
                    contact_form.company_name = None
                    contact = contact_form.save()
            return redirect('connections:list')

    context = {
        'company_form': company_form,
        'delete_company_form': delete_company_form,
        }
    template = 'connections/company_edit.html'
    return render(request, template, context)
