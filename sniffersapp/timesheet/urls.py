from django.urls import path

from .views import *

app_name = 'timesheet'

urlpatterns = [
    path('', timesheet_list, name='timesheet_list'),
    path('<slug:slug>/weekly/', weekly_timesheet, name='weekly_timesheet'),
    path('add_timecard/', timecard_new, name='timecard_new'),
]
