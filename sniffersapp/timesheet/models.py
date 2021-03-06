from __future__ import unicode_literals

import datetime

from django.db import models
from django.utils.timezone import now as todays_date
from django.conf import settings

from ..daily_dockets.models import Docket
from ..projects.models import Project
from ..equipment.models import Equipment
from ..connections.models import Company

from .utils import *


class TimesheetManager(models.Manager):
    def for_user(self, user):
        """NOTE: you cannot chain this as it doesn't return a queryset."""
        qs = super().get_queryset()
        if not user.is_staff or not user.is_superuser:
            return [o for o in qs if o.created_user == user]
        return qs.all()


class Timesheet(models.Model):
    shift_options = (
        ('Day', 'Day'),
        ('Night', 'Night'),
    )

    lunch_options = (
        ('0', '0 min'),
        ('5', '5 mins'),
        ('10', '10 mins'),
        ('15', '15 mins'),
        ('20', '20 mins'),
        ('25', '25 mins'),
        ('30', '30 mins'),
        ('35', '35 mins'),
        ('40', '40 mins'),
        ('45', '45 mins'),
        ('50', '50 mins'),
        ('55', '55 mins'),
        ('60', '60 mins'),
    )

    smoko_options = (
        ('0', '0 min'),
        ('5', '5 mins'),
        ('10', '10 mins'),
        ('15', '15 mins'),
        ('20', '20 mins'),
        ('25', '25 mins'),
        ('30', '30 mins'),
        ('35', '35 mins'),
        ('40', '40 mins'),
        ('45', '45 mins'),
        ('50', '50 mins'),
        ('55', '55 mins'),
        ('60', '60 mins'),
    )

    status_options = (
        ('Open', 'Open'),
        ('Submitted', 'Submitted'),
        ('Approved', 'Approved'),
    )


    objects = TimesheetManager()

    created_user = models.ForeignKey(settings.AUTH_USER_MODEL,
            blank=True, null=True, on_delete=models.PROTECT)
    timesheet_num = models.PositiveSmallIntegerField(blank=True, null=True, default=1000)

    # Slug is in format T-{user_id}-{timesheet_num}, e.g. "T-1-1000"
    slug = models.SlugField(blank=True, null=True)

    dockets = models.ManyToManyField(Docket, blank=True)
    docket_num = models.CharField(max_length=80, blank=False)
    #submitted
    status = models.CharField(max_length=20, blank=True, default='Open', choices=status_options)

    # Date
    week_start_date = models.DateField(null=True, blank=True)
    week_end_date = models.DateField( null=True, blank=True)
    timesheet_date = models.DateField(blank=False, null=True, default=todays_date)
    docket_shift = models.CharField(max_length=20, choices=shift_options, default='Day')
    # Equipment
    equipment = models.ForeignKey(Equipment, models.SET_NULL, blank=False, null=True)
    equipment_name = models.CharField(max_length=80) # copied from equipment.id
    equipment_num = models.CharField(max_length=80, blank=False)
    equipment_start_hours = models.CharField(max_length=80, blank=False)
    equipment_finish_hours = models.CharField(max_length=80, blank=False)
    # Attachments
    attachment_1 = models.CharField(max_length=80, blank=True, null=True)
    attachment_hours_1 = models.CharField(max_length=80, blank=True, null=True)
    attachment_2 = models.CharField(max_length=80, blank=True, null=True)
    attachment_hours_2 = models.CharField(max_length=80, blank=True, null=True)
    attachment_3 = models.CharField(max_length=80, blank=True, null=True)
    attachment_hours_3 = models.CharField(max_length=80, blank=True, null=True)
    # Company
    company = models.ForeignKey(Company, models.SET_NULL, blank=False, null=True)
    company_name = models.CharField(max_length=80) # copied from company.name
    # Project
    project = models.ForeignKey(Project, models.SET_NULL, blank=False, null=True)
    project_name = models.CharField(max_length=80) # copied from project.name
    # Time
    start_time = models.TimeField(null=True, blank=False)
    finish_time = models.TimeField(null=True, blank=False)
    lunch = models.CharField(max_length=20, blank=False, default='30', choices=lunch_options)
    smoko = models.CharField(max_length=20, blank=False, default='30', choices=smoko_options)
    # Additional Info
    additional_info = models.TextField(blank=True)
    # Created/Updated
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('created_user', 'timesheet_num')
        ordering = ('created_user__id', '-timesheet_num',)

    def __str__(self):
        return self.slug

    def save(self, **kwargs):
        # Copy over ForeignKey fields
        if self.equipment:
            self.equipment_name = self.equipment.equipment_id
        if self.company:
            self.company_name = self.company.company_name
        if self.project:
            self.project_name = self.project.project_name

        # Pick new timesheet number when creating only - not on update
        if self._state.adding:
            max_timesheet_num = Timesheet.objects.filter(created_user=self.created_user) \
                    .aggregate(models.Max('timesheet_num'))['timesheet_num__max']
            if max_timesheet_num is None:
                self.timesheet_num = 1000
            else:
                self.timesheet_num = max_timesheet_num + 1

        # Always update slug, in case timesheet_num was manually changed
        self.slug = f'T-{self.created_user.id}-{self.timesheet_num}'

        super().save()

    def calender_date(self):
        cal_year = self.docket_date.year
        cal_month = self.docket_date.month - 1
        cal_day = self.docket_date.day
        return cal_year, cal_month, cal_day

    @property
    def total_hours(self):
        return calculate_hours(self, lunch=False)

    @property
    def payable_hours(self):
        return calculate_hours(self)

def timesheet_from_docket(docket):
    ts = Timesheet()
    ts.created_user = docket.created_user
    ts.docket_num = docket.docket_num
    ts.docket_date = docket.docket_date
    ts.docket_shift = docket.docket_shift
    ts.equipment = docket.equipment
    ts.equipment_name = docket.equipment_name
    ts.equipment_num = docket.equipment_num
    ts.equipment_start_hours = docket.equipment_start_hours
    ts.equipment_finish_hours = docket.equipment_finish_hours
    ts.company = docket.company
    ts.company_name = docket.company_name
    ts.project = docket.project
    ts.project_name = docket.project_name
    ts.start_time = docket.start_time
    ts.finish_time = docket.finish_time
    ts.lunch = docket.lunch
    ts.attachment_1 = docket.attachment_1
    ts.attachment_hours_1 = docket.attachment_hours_1
    ts.attachment_2 = docket.attachment_2
    ts.attachment_hours_2 = docket.attachment_hours_2
    ts.attachment_3 = docket.attachment_3
    ts.attachment_hours_3 = docket.attachment_hours_3
    ts.save()
    ts.dockets.add(docket)
