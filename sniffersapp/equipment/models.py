from django.db import models
from django.conf import settings
from django.urls import reverse

from ..connections.models import Company
from ..projects.models import Project

class Equipment(models.Model):
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                     blank=True, null=True, on_delete=models.PROTECT)
    equipment_id = models.CharField(max_length=20, unique=True)
    year = models.CharField(max_length=5, blank=True)
    make = models.CharField(max_length=80, blank=True)
    model = models.CharField(max_length=80, blank=True)
    size = models.CharField(max_length=80, blank=True)
    registration = models.CharField(max_length=80, blank=True)
    vin = models.CharField(max_length=80, blank=True)
    engine_no = models.CharField(max_length=80, blank=True)
    purchase_date = models.DateField(blank=True, null=True)
    purchase_amount = models.CharField(max_length=20, blank=True)
    maintenance = models.CharField(max_length=20, blank=True)
    fuel = models.CharField(max_length=20, blank=True)
    rubber_tracks = models.NullBooleanField()
    height_restrictor = models.BooleanField(blank=True, default=0)
    additional_info = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    created_user = models.ForeignKey(settings.AUTH_USER_MODEL,
            blank=True, null=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = 'Equipment'

    def __str__(self):
        return self.equipment_id

    def get_absolute_url(self):
        return reverse('equipment:edit', args=(self.id,))

class Equipment_AdditionalInfo(models.Model):
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                     blank=True, null=True, on_delete=models.PROTECT)

    equipment_id = models.ForeignKey(Equipment, models.SET_NULL, blank=True, null=True)
    card_type = models.CharField(max_length=20, blank=True)
    toll_tag_no = models.CharField(max_length=20, blank=True)
    fuel_card_no = models.CharField(max_length=40, blank=True)
    fuel_card_pin = models.CharField(max_length=8, blank=True)
    odometer_prompt = models.BooleanField(blank=True)
    product_restriction = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.id