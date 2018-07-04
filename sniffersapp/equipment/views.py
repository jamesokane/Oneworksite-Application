from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from .models import Equipment
from .forms import EquipmentForm, EquipmentExtendedForm

def equipment_list(request, template='equipment/equipment_list.html'):
    context = {
         'equipment_list': Equipment.objects.all(),
     }
    return render(request, template, context)

def equipment_detail(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    context = {
        'equipment': equipment,
    }
    template = 'equipment/equipment_detail.html'
    return render(request, template, context)

def equipment_form(request, pk, template='equipment/equipment_form.html'):
    if id:
        existing_equipment = get_object_or_404(Equipment, pk=pk)
    else:
        existing_equipment= None

    equipment_form = EquipmentForm(request.POST or None, instance=existing_equipment)
    if request.method == 'POST':
        if equipment_form.is_valid():
            equipment = equipment_form.save(commit=False)
            if not existing_equipment:
                equipment.created_user = request.user
                equipment.save()
            messages.success(request, 'equipment saved successfully.')
            return redirect('equipment:list')

    context = {
        'form': equipment_form,
        'title': str(existing_equipment) if existing_equipment else 'New Equipment',
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