import json

from django.shortcuts import render, get_object_or_404, redirect

from django.http import HttpResponse, QueryDict

from django.db.models import F


from .models import FormNew, FormItem
from .forms import FormNewForm, FormItemForm


def form_list(request):
    form_list = FormNew.objects.all()

    context = {
         'form_list': form_list,
     }
    template = 'create_forms/form_list.html'
    return render(request, template, context)


def form_detail(request, slug):
    form = get_object_or_404(FormNew, slug=slug)
    form_list = FormItem.objects.all().filter(form=form).filter(removed=False).order_by(F('order').asc(nulls_last=True))

    form_name = FormNewForm(request.POST or None, instance=form)
    item_form = FormItemForm(request.POST or None)

    if request.method == 'POST':
        # Ajax call for creating new form item
        if 'form_type' in request.POST:
            item_form.label = request.POST.get('label')
            item_form.help_text = request.POST.get('help_text')
            item_form.required = request.POST.get('required')
            item_form.text = request.POST.get('text')
            if item_form.is_valid():
                item_form = item_form.save(commit=False)
                item_form.form = form
                item_form.form_type = request.POST.get('form_type')
                item_form.removed = False
                item_form.save()
                # Update list of form items
                form_list = FormItem.objects.all().filter(form=form).filter(removed=False).order_by(F('order').asc(nulls_last=True))

        # Ajax call for editing form item
        if 'edit' in request.POST:
            slug = request.POST.get('slug')
            item = get_object_or_404(FormItem, slug=slug)
            edit_form = FormItemForm(request.POST or None, instance=item)
            edit_form.label = request.POST.get('label')
            edit_form.help_text = request.POST.get('help_text')
            edit_form.required = request.POST.get('required')
            edit_form.text = request.POST.get('text')
            if edit_form.is_valid():
                edit_form = edit_form.save(commit=False)
                edit_form.form = form
                edit_form.save()
                # Update list of form items
                form_list = FormItem.objects.all().filter(form=form).filter(removed=False).order_by(F('order').asc(nulls_last=True))

        # Ajax call for remove (hide) form item
        if 'remove' in request.POST:
            slug = request.POST.get('slug')
            item = get_object_or_404(FormItem, slug=slug)
            item.removed = True
            item.save()
            form_list = FormItem.objects.all().filter(form=form).filter(removed=False).order_by(F('order').asc(nulls_last=True))


        # Ajax call for form name edit
        if 'form_name' in request.POST:
            form_name.label = request.POST.get('label')
            if form_name.is_valid():
                form_name = form_name.save(commit=False)
                form_name.save()


        # Ajax call for drag and drop list items
        if 'action' in request.POST:
            entries = request.POST['content']
            entries = json.loads(entries)
            for key, value in entries.items():
                entry = FormItem.objects.get(id=key)
                entry.order = value
                entry.save()
            form_list = FormItem.objects.all().filter(form=form).filter(removed=False).order_by(F('order').asc(nulls_last=True))


    edit_item_form = None
    edit_item = None
    help_item = None
    if request.method == 'GET':
        if request.GET.get('name') == "form_edit":
            slug = request.GET.get('content')
            edit_item = get_object_or_404(FormItem, slug=slug)
            edit_item_form = FormItemForm(request.POST or None, instance=edit_item)
        if request.GET.get('name') == "help_info":
            slug = request.GET.get('content')
            help_item = get_object_or_404(FormItem, slug=slug)



    context = {
        'form': form,
        'item_form': item_form,
        'form_list': form_list,
        'form_name': form_name,
        'edit_item_form': edit_item_form,
        'edit_item': edit_item,
        'help_item': help_item,
    }
    template = 'create_forms/form_detail.html'
    return render(request, template, context)
