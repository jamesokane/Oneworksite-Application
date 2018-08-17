from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from django.utils.timezone import now as todays_date
from django.conf import settings

import datetime
import calendar

from ..projects.models import Project
from ..equipment.models import Equipment, Attachment
from ..connections.models import Company

from ..timesheet.utils import calculate_hours

class DocketManager(models.Manager):
    def for_user(self, user):
        """NOTE: you cannot chain this as it doesn't return a queryset."""
        qs = super().get_queryset()
        if not user.is_staff or not user.is_superuser:
            return [o for o in qs if o.created_user == user]
        return qs.all()

class Docket(models.Model):
    shift_options = (
        ('Day', 'Day'),
        ('Night', 'Night'),
    )

    day_options = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
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

    item_options = (
        ('No Issues', 'No Issues'),
        ('Needs Attention', 'Needs Attention'),
        ('Not Applicable', 'Not Applicable'),
    )


    objects = DocketManager()

    week_day = calendar.day_name[datetime.date.today().weekday()]

    created_user = models.ForeignKey(settings.AUTH_USER_MODEL,
            blank=True, null=True, on_delete=models.PROTECT)
    created_user_name = models.CharField(max_length=80) # copied from created_user.name
    docket_num = models.PositiveSmallIntegerField(blank=True, null=True, default=1000)

    # Slug is populated off (created_user, docket_num) pair
    slug = models.SlugField(blank=True, null=True)

    # Signatures - base64 encoded image/png
    operator_sign = models.TextField(blank=False, null=True)
    supervisor_sign = models.TextField(blank=False, null=True)

    # Date
    docket_date = models.DateField(blank=False, null=True, default=todays_date)
    docket_day = models.CharField(max_length=20, blank=False, default=week_day, choices=day_options)
    docket_shift = models.CharField(max_length=20, blank=False, default='Day', choices=shift_options)
    # Attachments
    attachment_1 = models.ForeignKey(Attachment, models.SET_NULL, blank=True, null=True, related_name='attachment_1', )
    attachment_hours_1 = models.CharField(max_length=80, blank=True)
    attachment_2 = models.ForeignKey(Attachment, models.SET_NULL, blank=True, null=True, related_name='attachment_2')
    attachment_hours_2 = models.CharField(max_length=80, blank=True)
    attachment_3 = models.ForeignKey(Attachment, models.SET_NULL, blank=True, null=True, related_name='attachment_3')
    attachment_hours_3 = models.CharField(max_length=80, blank=True)
    # Equipment
    equipment = models.ForeignKey(Equipment, models.SET_NULL, blank=False, null=True)
    equipment_name = models.CharField(max_length=80) # copied from equipment.id
    equipment_num = models.CharField(max_length=80, blank=False)
    equipment_hours = models.CharField(max_length=80, blank=False)
    # Company
    company = models.ForeignKey(Company, models.SET_NULL, blank=False, null=True)
    company_name = models.CharField(max_length=80) # copied from company.name
    # Project
    project = models.ForeignKey(Project, models.SET_NULL, blank=False, null=True)
    project_name = models.CharField(max_length=80) # copied from project.name
    # Supervisor
    supervisor = models.CharField(max_length=80, blank=False, null=True)
    # Time
    start_time = models.TimeField(null=True, blank=False)
    finish_time = models.TimeField(null=True, blank=False)
    lunch = models.CharField(max_length=20, blank=False, default='30', choices=lunch_options)
    smoko = models.CharField(max_length=20, blank=False, default='30', choices=smoko_options)
    # Items
    item1 = models.CharField(max_length=20, blank=False, choices=item_options)
    item2 = models.CharField(max_length=20, blank=False, choices=item_options)
    item3 = models.CharField(max_length=20, blank=False, choices=item_options)
    item4 = models.CharField(max_length=20, blank=False, choices=item_options)
    item5 = models.CharField(max_length=20, blank=False, choices=item_options)
    item6 = models.CharField(max_length=20, blank=False, choices=item_options)
    item7 = models.CharField(max_length=20, blank=False, choices=item_options)
    item8 = models.CharField(max_length=20, blank=False, choices=item_options)
    item9 = models.CharField(max_length=20, blank=False, choices=item_options)
    item10 = models.CharField(max_length=20, blank=False, choices=item_options)
    item11 = models.CharField(max_length=20, blank=False, choices=item_options)
    item12 = models.CharField(max_length=20, blank=False, choices=item_options)
    # Details of faults
    fault = models.TextField(blank=True)
    # Fault reported to
    reported_to = models.TextField(blank=True)
    # Daily notes
    daily_notes = models.TextField(blank=True)
    # Created/Updated
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('created_user', 'docket_num')
        ordering = ('created_user__id', '-docket_num',)

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('daily_dockets:docket_start', kwargs={'slug': self.slug})

    def save(self, **kwargs):
        # Copy over ForeignKey fields
        if self.equipment:
            self.equipment_name = self.equipment.equipment_id
        if self.company:
            self.company_name = self.company.company_name
        if self.project:
            self.project_name = self.project.project_name


        # Pick new docket number when creating only - not on update
        if self._state.adding:
            max_docket_num = Docket.objects.filter(created_user=self.created_user) \
                    .aggregate(models.Max('docket_num'))['docket_num__max']
            if max_docket_num is None:
                self.docket_num = 1000
            else:
                self.docket_num = max_docket_num + 1

        # Always update slug, in case docket_num was manually changed
        self.slug = f'D-{self.created_user.id}-{self.docket_num}'

        super().save()

    @property
    def locked(self):
        return self.operator_sign and self.supervisor_sign

    @property
    def total_hours(self):
        return calculate_hours(self, lunch=False, smoko=False)

    @property
    def payable_hours(self):
        return calculate_hours(self)
