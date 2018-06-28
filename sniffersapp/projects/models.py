import datetime
from django.db import models
from django.conf import settings

from ..connections.models import Company

class Project(models.Model):
    status_options = (
        ('Open', 'Project Open'),
        ('Closed', 'Project Closed'),
    )

    created_user = models.ForeignKey(settings.AUTH_USER_MODEL,
            blank=True, null=True, on_delete=models.PROTECT)

    # Company
    company = models.ForeignKey(Company, models.SET_NULL, blank=True, null=True)
    # Project Name
    project_name = models.CharField(max_length=80, blank=True)
    # Address Info
    project_address = models.CharField(max_length=200, blank=True, null=True)
    # Project Status
    project_status = models.CharField(max_length=20, blank=False, default='Open', choices=status_options)
    # Project Start/End Date
    project_start_date = models.DateField(auto_now=False, blank=True, null=True)
    project_end_date = models.DateField(auto_now=False, blank=True, null=True)
    # Additional Info
    additional_info = models.TextField(blank=True)
    # Created/Updated
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('project_name',)

    def __str__(self):
        return self.project_name

    @property
    def duration(self):
        if self.project_end_date:
            end = self.project_end_date
        else:
            end = datetime.date.today()
        return (end - self.project_start_date).days
