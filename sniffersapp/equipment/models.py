from django.db import models
from django.conf import settings
from django.urls import reverse

from ..connections.models import Company
from ..projects.models import Project

class Equipment(models.Model):
    name = models.CharField(max_length=80)
    make = models.CharField(max_length=80, blank=True)
    model = models.CharField(max_length=80, blank=True)
    equipment_type = models.CharField(max_length=80, blank=True)
    purchase_date = models.DateField(blank=True, null=True)
    purchase_amount = models.CharField(max_length=20, blank=True)
    base_rate = models.CharField(max_length=5, blank=True)
    service_lag = models.CharField(max_length=5)
    additional_info = models.TextField(blank=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    created_user = models.ForeignKey(settings.AUTH_USER_MODEL,
            blank=True, null=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = 'Equipment'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('equipment:edit', args=(self.id,))

class EquipmentBooking(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.PROTECT, null=True)
    project = models.ForeignKey(Project, on_delete=models.PROTECT, null=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    bookings_days = models.SmallIntegerField(blank=True, null=True)
    booking_cost = models.CharField(max_length=6, blank=True, null=True)
    additional_info = models.TextField(blank=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    created_user = models.ForeignKey(settings.AUTH_USER_MODEL,
            blank=True, null=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Equipment booking'

    def __str__(self):
        return f'Booking of {self.equipment} for {self.company}'

    def edit_url(self):
        if not self.equipment:
            return '#'
        d = {'equipment_id': self.equipment.id,
             'pk': self.id,
        }
        return reverse('equipment:book_edit', kwargs=d)
