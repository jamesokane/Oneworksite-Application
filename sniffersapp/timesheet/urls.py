
from __future__ import absolute_import, unicode_literals

# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import timesheet_calender, weekly_timesheet, export_weekly_timesheet_csv, export_timesheet_csv, timesheet_edit

app_name = 'timesheets'

urlpatterns = [
    # Client List, Create, Detail, Edit & Delete

    # URL pattern for the Client List View
    url(r'^$', timesheet_calender, name='timesheet_calender'),


    # URL pattern for the Project Detail View
    url(r'^weekly/(?P<slug>[\w.@+-]+)/$', weekly_timesheet, name='weekly_timesheet'),

    # URL pattern for the Contact Export View
    url(r'^export/csv/(?P<slug>[\w.@+-]+)/$', export_weekly_timesheet_csv, name='export_weekly_timesheet_csv'),

    # URL pattern for the Contact Export View
    url(r'^export/csv/$', export_timesheet_csv, name='export_timesheet_csv'),

    # URL pattern for the Contact Edit View
    url(r'^(?P<slug>[\w.@+-]+)/edit/$', timesheet_edit, name='timesheet_edit'),

]
