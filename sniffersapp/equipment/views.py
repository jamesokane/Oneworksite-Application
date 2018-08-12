from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from .models import Equipment, Attachment
from .forms import EquipmentForm, AttachmentForm

def equipment_list(request, template='equipment/equipment_list.html'):
    equipment_list = Equipment.objects.order_by('equipment_id')
    attachment_list = Attachment.objects.order_by('attachment_id')

    if request.method == 'GET':
        slug = request.GET.get('content')
        if slug is None:
            try:
                equipment = equipment_list[0]
                attachment = attachment_list[0]
            except IndexError:
                equipment = None
                attachment = None
        elif 'equipment_sum' in request.GET.get('name'):
            equipment = get_object_or_404(Equipment, slug=slug)
            attachment = None
        elif 'attachment_sum' in request.GET.get('name'):
            attachment = get_object_or_404(Attachment, slug=slug)
            equipment = None

    context = {
         'attachment_list': attachment_list,
         'equipment_list': equipment_list,
         'attachment': attachment,
         'equipment': equipment,

     }
    return render(request, template, context)

def equipment_form(request, template='equipment/equipment_form.html'):

    equipment_form = EquipmentForm(request.POST or None)

    if request.method == 'POST':
        if 'new_equipment' in request.POST:
            if equipment_form.is_valid():
                equipment_form.save(commit=False)
                equipment_form.created_user = request.user
                equipment_form.save()
                messages.success(request, 'Equipment saved successfully.')
                return redirect('equipment:list')

    context = {
        'equipment_form': equipment_form,
    }
    return render(request, template, context)

def attachment_form(request, template='equipment/attachment_form.html'):

    attachment_form = AttachmentForm(request.POST or None)

    if request.method == 'POST':
        if 'new_attachment' in request.POST:
            if attachment_form.is_valid():
                attachment_form.save(commit=False)
                attachment_form.created_user = request.user
                attachment_form.save()
                messages.success(request, 'Attachment saved successfully.')
                return redirect('equipment:list')

    context = {
        'attachment_form': attachment_form,
    }
    return render(request, template, context)

def equipment_edit(request, slug, template='equipment/equipment_edit_form.html'):
    equipment = get_object_or_404(Equipment, slug=slug)

    edit_equipment_form = EquipmentForm(request.POST or None, instance=equipment)

    if request.method == 'POST':
        if 'edit_equipment' in request.POST:
            if edit_equipment_form.is_valid():
                edit_equipment_form.save(commit=False)
                edit_equipment_form.save()
                messages.success(request, 'Equipment updated successfully.')
                return redirect('equipment:list')

    context = {
        'edit_equipment_form': edit_equipment_form,
    }
    return render(request, template, context)

def attachment_edit(request, slug, template='equipment/attachment_edit_form.html'):
    attachment = get_object_or_404(Attachment, slug=slug)

    edit_attachment_form = AttachmentForm(request.POST or None, instance=attachment)

    if request.method == 'POST':
        if 'edit_attachment' in request.POST:
            if edit_attachment_form.is_valid():
                edit_attachment_form.save(commit=False)
                edit_attachment_form.save()
                messages.success(request, 'Attachment updated successfully.')
                return redirect('equipment:list')

    context = {
        'edit_attachment_form': edit_attachment_form,
    }
    return render(request, template, context)
