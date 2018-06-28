from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import *

from .models import Equipment, EquipmentBooking
from .forms import EquipmentForm, EquipmentBookingForm

class EquipmentListView(ListView):
    model = Equipment

class EquipmentCreateView(SuccessMessageMixin, CreateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'equipment/equipment_form.html'
    success_url = reverse_lazy('equipment:list')
    success_message = 'Equipment created succesfully.'

    def form_valid(self, form):
        form.instance.created_user = self.request.user
        return super().form_valid(form)

class EquipmentUpdateView(SuccessMessageMixin, UpdateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'equipment/equipment_form.html'
    success_url = reverse_lazy('equipment:list')
    success_message = 'Equipment updated successfully.'

class EquipmentBookingListView(ListView):
    model = EquipmentBooking
    template_name = 'equipment/bookings.html'

class EquipmentBookingCreateView(SuccessMessageMixin, CreateView):
    model = EquipmentBooking
    form_class = EquipmentBookingForm
    template_name = 'equipment/booking_form.html'
    success_url = reverse_lazy('equipment:bookings')
    success_message = 'Booking created successfully.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        e = get_object_or_404(Equipment, pk=self.kwargs['equipment_id'])
        context['equipment'] = e
        return context

    def form_valid(self, form):
        form.instance.created_user = self.request.user
        return super().form_valid(form)

class EquipmentBookingUpdateView(SuccessMessageMixin, UpdateView):
    model = EquipmentBooking
    form_class = EquipmentBookingForm
    template_name = 'equipment/booking_form.html'
    success_url = reverse_lazy('equipment:list')
    success_message = 'Booking updated successfully.'
