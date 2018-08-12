from django.db import models
from django.conf import settings


from shortuuidfield import ShortUUIDField

from ..connections.models import Company
from ..projects.models import Project

class Equipment(models.Model):
    uuid = ShortUUIDField()
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                     blank=True, null=True, on_delete=models.PROTECT)
    slug = models.CharField(max_length=80, unique=True)
    equipment_id = models.CharField(max_length=20, unique=True)
    year = models.CharField(max_length=12)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    registration = models.CharField(max_length=80)
    additional_info = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Equipment'

    def __str__(self):
        return self.equipment_id

    # Create slug using first 8 characters of uuid
    def save(self, **kwargs):
        super(Equipment, self).save()
        slug = self.uuid
        self.slug = slug[:8]
        super(Equipment, self).save()

class Attachment(models.Model):
    uuid = ShortUUIDField()
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                     blank=True, null=True, on_delete=models.PROTECT)
    slug = models.CharField(max_length=80, unique=True)
    attachment_id = models.CharField(max_length=20, unique=True)
    attachment_type = models.CharField(max_length=50, unique=True)
    additional_info = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Attachment'

    def __str__(self):
        return self.attachment_id

    # Create slug using first 8 characters of uuid
    def save(self, **kwargs):
        super(Attachment, self).save()
        slug = self.uuid
        self.slug = slug[:8]
        super(Attachment, self).save()
