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

    created_user = models.ForeignKey(settings.AUTH_USER_MODEL,
            blank=True, null=True, on_delete=models.PROTECT)
    timesheet_num = models.PositiveSmallIntegerField(blank=True, null=True, default=1000)

    # Slug is in format T-{user_id}-{timesheet_num}, e.g. "T-1-1000"
    slug = models.SlugField(blank=True, null=True)

    dockets = models.ManyToManyField(Docket, blank=True)

    # Date
    docket_date = models.DateField(blank=True, null=True, default=todays_date)
    docket_shift = models.CharField(max_length=20, blank=True, choices=shift_options)
    # Equipment
    equipment = models.ForeignKey(Equipment, models.SET_NULL, blank=True, null=True)
    equipment_name = models.CharField(max_length=80, blank=True)
    equipment_num = models.CharField(max_length=80, blank=True)
    equipment_hours = models.CharField(max_length=80, blank=True)
    # Company
    company = models.ForeignKey(Company, models.SET_NULL, blank=True, null=True)
    company_name = models.CharField(max_length=80, blank=True)
    # Project
    project = models.ForeignKey(Project, models.SET_NULL, blank=True, null=True)
    project_name = models.CharField(max_length=80, blank=True)
    # Time
    start_time = models.TimeField(blank=True, null=True)
    finish_time = models.TimeField(blank=True, null=True)
    lunch = models.CharField(max_length=20, blank=True, choices=lunch_options)
    # Created/Updated
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('created_user', 'timesheet_num')
        ordering = ('created_user__id', '-timesheet_num',)

    def __str__(self):
        return self.slug

    def save(self, **kwargs):
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
    ts.docket_date = docket.docket_date
    ts.docket_shift = docket.docket_shift
    ts.equipment = docket.equipment
    ts.equipment_name = docket.equipment_name
    ts.equipment_num = docket.equipment_num
    ts.equipment_hours = docket.equipment_hours
    ts.company = docket.company
    ts.company_name = docket.company_name
    ts.project = docket.project
    ts.project_name = docket.project_name
    ts.start_time = docket.start_time
    ts.finish_time = docket.finish_time
    ts.lunch = docket.lunch
    ts.save()
    ts.dockets.add(docket)
