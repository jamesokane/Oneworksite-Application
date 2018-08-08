from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

import datetime
import calendar
import csv
import pytz

from .models import Timesheet
from .forms import TimesheetForm, ApproveTimesheetForm

from ..equipment.models import Equipment
from ..connections.models import Company
from ..projects.models import Project


def timesheet_list(request, template='timesheet/timesheet_list.html'):
    timesheet_list = Timesheet.objects.for_user(user=request.user)
    # Create a string list of dates within timesheet_list
    timesheet_date_list = []
    for item in timesheet_list:
        timesheet_date_list.append(str(item.docket_date))

    # #Create list of Mondays and Fridays
    week_dates = []
    start_date = request.user.date_joined
    start_date = start_date - datetime.timedelta(days=start_date.weekday())
    for x in range(0, 100):
        date = start_date + datetime.timedelta(days=(x*7))
        if date <= datetime.datetime.utcnow().replace(tzinfo=pytz.UTC):
            week_dates.append((date, date + datetime.timedelta(days=(4))))
            # Create a dummy entry for the monday of each week
            timesheet_form = TimesheetForm(request.POST)
            if timesheet_form.is_valid():
                timesheet_form = timesheet_form.save(commit=False)
                timesheet_form.docket_date = date
                timesheet_form.created_user = request.user
                test = datetime.datetime.strptime(str(date)[:10], '%Y-%m-%d')
                test = test.date()
                if str(test) not in timesheet_date_list:
                    timesheet_form.save()


    timesheet_list = Timesheet.objects.for_user(user=request.user)
    weekly_list = []
    week_dates_2 = []
    for item in week_dates:
        item = datetime.datetime.strptime(str(item[0])[:10], '%Y-%m-%d')
        week_dates_2.append(str(item.date()))

    for item in timesheet_list:
        if str(item.docket_date) in week_dates_2 and item.start_time is None:
            weekly_list.append(item)
    weekly_list = list(dict.fromkeys(weekly_list))


    context = {
         'weekly_list': weekly_list,
         'timesheet_date_list': timesheet_date_list,
     }
    return render(request, template, context)

def timecard_new(request, slug, *args, **kwargs):
    timesheet = get_object_or_404(Timesheet, slug=slug)

    timesheet_form = TimesheetForm(request.POST or None)

    # Create new timecard form
    if request.method == "POST":
        if 'new_timecard' in request.POST:
            if timesheet_form.is_valid():
                timesheet_form = timesheet_form.save(commit=False)
                timesheet_form.created_user = timesheet.created_user
                timesheet_form.save()
                return redirect('timesheet:weekly_timesheet', timesheet_form.slug)

    # Determine the week range any selected date sits within
    today = timesheet.docket_date
    dates = []
    for i in range(0 - today.weekday(), 7 - today.weekday()):
        week_date = today + datetime.timedelta(days=i)
        week_day = calendar.day_name[week_date.weekday()]
        month_day = calendar.month_name[week_date.month]
        dates.append([week_date, week_day, month_day])

    context = {
        'timesheet_form': timesheet_form,
        'timesheet': timesheet,
        'dates': dates,
    }
    template = 'timesheet/timesheet_new.html'
    return render(request, template, context)

def timecard_edit(request, slug, *args, **kwargs):
    timesheet = get_object_or_404(Timesheet, slug=slug)

    edit_timesheet_form = TimesheetForm(request.POST or None, instance=timesheet)

    # Create new timecard form
    if request.method == "POST":
        if 'edit_timecard' in request.POST:
            if edit_timesheet_form.is_valid():
                edit_timesheet_form = edit_timesheet_form.save(commit=False)
                edit_timesheet_form.save()
                return redirect('timesheet:weekly_timesheet', edit_timesheet_form.slug)

    # Determine the week range any selected date sits within
    today = timesheet.docket_date
    dates = []
    for i in range(0 - today.weekday(), 7 - today.weekday()):
        week_date = today + datetime.timedelta(days=i)
        week_day = calendar.day_name[week_date.weekday()]
        month_day = calendar.month_name[week_date.month]
        dates.append([week_date, week_day, month_day])

    context = {
        'edit_timesheet_form': edit_timesheet_form,
        'timesheet': timesheet,
        'dates': dates,
    }
    template = 'timesheet/timesheet_edit.html'
    return render(request, template, context)

def export_weekly_timesheet_csv(request, slug, *args, **kwargs):
    timesheet = get_object_or_404(Timesheet, slug=slug)
    # Determine the week range any selected date sits within
    today = timesheet.docket_date
    dates = []
    for i in range(0 - today.weekday(), 7 - today.weekday()):
        week_date = today + datetime.timedelta(days=i)
        week_day = calendar.day_name[week_date.weekday()]
        month_day = calendar.month_name[week_date.month]
        dates.append([week_date, week_day, month_day])
    # Creates a specific list of all the timesheet items that fall within a given week
    week_start = dates[0][0]
    week_end = dates[6][0]
    timesheet_list_weekly = Timesheet.objects.filter(docket_date__range=[week_start, week_end])

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="weekly_timesheet.csv"'

    writer = csv.writer(response)
    writer.writerow(['Operator Name', 'Date', 'Shift', 'Equipment', 'Equipment Number', 'Equipment Hours',
                     'Docket Number', 'Customer', 'Project', 'Start Time', 'Finish Time', 'Lunch'])

    timesheet_list_weekly = timesheet_list_weekly.values_list('', 'docket_date', 'docket_shift', 'equipment_name',
                                                              'equipment_num', 'equipment_hours', 'docket_number',
                                                              'company_name', 'project_name', 'start_time', 'finish_time',
                                                              'lunch')
    for item in timesheet_list_weekly:
        writer.writerow(item)
    return response


def export_timesheet_csv(request):
    timesheet_list = Timesheet.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="monthly_timesheet.csv"'

    writer = csv.writer(response)
    writer.writerow(['Operator Name', 'Date', 'Shift', 'Equipment', 'Equipment Number', 'Equipment Hours',
                     'Docket Number', 'Customer', 'Project', 'Start Time', 'Finish Time', 'Lunch'])

    timesheet_list = timesheet_list.values_list('user_name', 'docket_date', 'docket_shift', 'equipment_name',
                                                              'equipment_num', 'equipment_hours', 'docket_number',
                                                              'company_name', 'project_name', 'start_time', 'finish_time',
                                                              'lunch')
    for item in timesheet_list:
        writer.writerow(item)
    return response



def weekly_timesheet(request, slug, *args, **kwargs):
    timesheet = get_object_or_404(Timesheet, slug=slug)


    # Determine the week range any selected date sits within
    today = timesheet.docket_date
    day_name = calendar.day_name[today.weekday()]
    dates = []
    for i in range(0 - today.weekday(), 7 - today.weekday()):
        week_date = today + datetime.timedelta(days=i)
        week_day = calendar.day_name[week_date.weekday()]
        month_day = calendar.month_name[week_date.month]
        dates.append([week_date, week_day, month_day])
    # Creates a specific list of all the timesheet items that fall within a given week
    week_start = dates[0][0]
    week_end = dates[6][0]
    timesheet_list_weekly = Timesheet.objects.filter(docket_date__range=[week_start, week_end]).filter(created_user__id = timesheet.created_user.id)
    timesheet_list_weekly = timesheet_list_weekly.order_by('docket_date')

    weekly_hours = 0
    weekly_mins = 0
    for item in timesheet_list_weekly:
        weekly_hours += item.payable_hours[0]
        weekly_mins += item.payable_hours[1]
        while weekly_mins > 60:
            weekly_hours += 1
            weekly_mins = weekly_mins - 60

    # AJAX call for item summary modal
    if request.method == 'GET':
        slug = request.GET.get('content')
        if slug is None:
            try:
                timesheet_sum = timesheet_list_weekly[0]
            except IndexError:
                timesheet_sum = None
        elif 'timesheet_sum' in request.GET.get('name'):
            timesheet_sum = get_object_or_404(Timesheet, slug=slug)

    # Submit timesheet form
    if request.method == "POST":
        if 'submit_timesheet' in request.POST:
            for timesheet in timesheet_list_weekly:
                approve_timesheet_form = ApproveTimesheetForm(request.POST, instance=timesheet)
                if approve_timesheet_form.is_valid():
                    approve_timesheet_form = approve_timesheet_form.save(commit=False)
                    approve_timesheet_form.status = "Submitted"
                    approve_timesheet_form.save()
            return redirect('timesheet:timesheet_list')
        elif 'approve_timesheet' in request.POST:
            for timesheet in timesheet_list_weekly:
                approve_timesheet_form = ApproveTimesheetForm(request.POST, instance=timesheet)
                if approve_timesheet_form.is_valid():
                    approve_timesheet_form = approve_timesheet_form.save(commit=False)
                    approve_timesheet_form.status = "Approved"
                    approve_timesheet_form.save()
            return redirect('timesheet:timesheet_list')

    else:
        approve_timesheet_form = ApproveTimesheetForm()
        context = {
            'timesheet_list_weekly': timesheet_list_weekly,
            'dates': dates,
            'weekly_hours': weekly_hours,
            'weekly_mins': weekly_mins,
            'timesheet_sum': timesheet_sum,
            'timesheet': timesheet,
            'approve_timesheet_form': approve_timesheet_form,
        }
        template = 'timesheet/timesheet_weekly.html'
        return render(request, template, context)
