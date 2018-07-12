from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from .models import Equipment, Equipment_AdditionalInfo
from .forms import EquipmentForm, EquipmentExtendedForm

def equipment_list(request, template='equipment/equipment_list.html'):
    context = {
         'equipment_list': Equipment.objects.all(),
     }
    return render(request, template, context)

def equipment_detail(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    equipment_additional = Equipment_AdditionalInfo
    context = {
        'equipment': equipment,
        'equipment_additional': equipment_additional,
    }
    template = 'equipment/equipment_detail.html'
    return render(request, template, context)

def equipment_form(request, template='equipment/equipment_form.html'):

    if request.method == 'POST':
        equipment_form = EquipmentForm(request.POST)
        if equipment_form.is_valid():
            equipment_form.save(commit=False)
            if request.user.is_authenticated:
                equipment_form.created_user = request.user
            equipment_form.save()
        messages.success(request, 'equipment saved successfully.')
        return redirect('equipment:list')

    else:
        equipment_form = EquipmentForm

    context = {
        'form': equipment_form,
    }

    return render(request, template, context)

def equipment_edit(request, pk, template='equipment/equipment_form.html'):
    equipment = get_object_or_404(Equipment, pk=pk)
    if request.method == 'POST':
        equipment_form = EquipmentForm(request.POST, instance=equipment)

        if equipment_form.is_valid():
            equipment_form.save(commit=False)
            if request.user.is_authenticated:
                equipment_form.created_user = request.user
            equipment_form.save()
        messages.success(request, 'equipment updated successfully.')
        return redirect('equipment:list')

    else:
        equipment_form = EquipmentForm(instance=equipment)


    context = {
        'form': equipment_form,
    }

    return render(request, template, context)

# from django.contrib.messages.views import SuccessMessageMixin
# from django.shortcuts import get_object_or_404
# from django.urls import reverse_lazy
# from django.views.generic import *
#
# from .models import Equipment
# from .forms import EquipmentForm
#
#
# class EquipmentListView(ListView):
#     model = Equipment
#
#
# class EquipmentCreateView(SuccessMessageMixin, CreateView):
#     model = Equipment
#     form_class = EquipmentForm
#     template_name = 'equipment/equipment_form.html'
#     success_url = reverse_lazy('equipment:list')
#     success_message = 'Equipment created succesfully.'
#
#     def form_valid(self, form):
#         form.instance.created_user = self.request.user
#         return super().form_valid(form)
#
#
# class EquipmentUpdateView(SuccessMessageMixin, UpdateView):
#     model = Equipment
#     form_class = EquipmentForm
#     template_name = 'equipment/equipment_form.html'
#     success_url = reverse_lazy('equipment:list')
#     success_message = 'Equipment updated successfully.'