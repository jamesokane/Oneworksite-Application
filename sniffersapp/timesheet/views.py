from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

import datetime
import calendar
import csv

from .models import Timesheet
from .forms import TimesheetForm

from ..equipment.models import Equipment
from ..connections.models import Company
from ..projects.models import Project


def timesheet_list(request, template='timesheet/timesheet_list.html'):
    week_dates = []
    start_date = datetime.date(2018, 6, 4)
    for x in range(0, 100):
        date = start_date + datetime.timedelta(days=(x*7))
        if date <= datetime.date.today():
            week_dates.append((date, date + datetime.timedelta(days=(4))))
            timesheet_form = TimesheetForm(request.POST)
            if timesheet_form.is_valid():
                timesheet_form = timesheet_form.save(commit=False)
                timesheet_form.docket_date = date
                timesheet_form.created_user = request.user
                timesheet_date_list = list(Timesheet.objects.all().values_list('docket_date', flat=True))
                timesheet_date_list = [str(item) for item in timesheet_date_list]
                if str(timesheet_form.docket_date) not in timesheet_date_list:
                    timesheet_form.save()

    timesheet_list = Timesheet.objects.all()
    weekly_list = []
    week_dates = [str(item[0]) for item in week_dates]
    for item in timesheet_list:
        if str(item.docket_date) in week_dates:
            if item.start_time is None:
                weekly_list.append(item)

    weekly_list = list(dict.fromkeys(weekly_list))


    context = {
         'weekly_list': weekly_list,
     }
    return render(request, template, context)


def timecard_new(request, *args, **kwargs):
    timesheet = Timesheet.objects.all()

    timesheet_form = TimesheetForm(request.POST or None)

    # Create new timecard form
    if request.method == "POST":
        if 'new_timecard' in request.POST:
            if timesheet_form.is_valid():
                timesheet_form = timesheet_form.save(commit=False)
                timesheet_form.created_user = request.user
                timesheet_form.save()
                return redirect('timesheet:weekly_timesheet', timesheet_form.slug)

    context = {
        'timesheet_form': timesheet_form,
    }
    template = 'timesheet/timesheet_new.html'
    return render(request, template, context)


def timesheet_calender(request):
    timesheet_list = Timesheet.objects.all()
    company_list = Company.objects.all()
    company_name_list = list(company_list.values_list('company_name', flat=True))
    project_list = Project.objects.all()
    project_name_list = list(project_list.values_list('project_name', flat=True))
    equipment_list = Equipment.objects.all()
    equipment_name_list = list(equipment_list.values_list('equipment_id', flat=True))

    day_name = '(unset)'

    # AJAX call for item summary modal
    if request.method == 'GET':
        slug = request.GET.get('content')
        if slug is None:
            try:
                timesheet_sum = timesheet_list[0]
                today = timesheet_sum.docket_date
                day_name = calendar.day_name[today.weekday()]
            except IndexError:
                timesheet_sum = None
        elif 'timesheet_sum' in request.GET.get('name'):
            timesheet_sum = get_object_or_404(Timesheet, slug=slug)
            today = timesheet_sum.docket_date
            day_name = calendar.day_name[today.weekday()]

    # Create new timecard form
    if request.method == "POST":
        if 'new_timesheet' in request.POST:
            timesheet_form = TimesheetForm(request.POST)
            if timesheet_form.is_valid():
                timesheet_form = timesheet_form.save(commit=False)
                timesheet_form.equipment = equipment_list[equipment_name_list.index(timesheet_form.equipment_name)]
                timesheet_form.company = company_list[company_name_list.index(timesheet_form.company_name)]
                timesheet_form.project = project_list[project_name_list.index(timesheet_form.project_name)]
                timesheet_form.save()
                return redirect('timesheets:timesheet_calender')
    else:
        timesheet_form = TimesheetForm()
        context = {
            'timesheet_list': timesheet_list,
            'timesheet_form': timesheet_form,
            'equipment_list': equipment_list,
            'company_list': company_list,
            'project_list': project_list,
            'timesheet_sum': timesheet_sum,
            'day_name': day_name,

         }
        template = 'timesheet/timesheet_calender.html'
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
    timesheet_list = Timesheet.objects.all().order_by('start_time')

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
    timesheet_list_weekly = Timesheet.objects.filter(docket_date__range=[week_start, week_end])
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

    context = {
         'timesheet_list_weekly': timesheet_list_weekly,
         'dates': dates,
         'weekly_hours': weekly_hours,
         'weekly_mins': weekly_mins,
         'timesheet_sum': timesheet_sum,
         'timesheet': timesheet,

    }
    template = 'timesheet/timesheet_weekly.html'
    return render(request, template, context)


def timesheet_edit(request, slug, *args, **kwargs):
    timesheet = get_object_or_404(Timesheet, slug=slug)
    company_list = Company.objects.all()
    company_name_list = list(company_list.values_list('company_name', flat=True))
    project_list = Project.objects.all()
    project_name_list = list(project_list.values_list('project_name', flat=True))
    equipment_list = Equipment.objects.all()
    equipment_name_list = list(equipment_list.values_list('name', flat=True))

    # Create new timecard form
    if request.method == "POST":
        if 'edit_timesheet' in request.POST:
            edit_timesheet_form = TimesheetForm(request.POST, instance=timesheet)
            if edit_timesheet_form.is_valid():
                edit_timesheet_form = edit_timesheet_form.save(commit=False)
                edit_timesheet_form.equipment = equipment_list[equipment_name_list.index(edit_timesheet_form.equipment_name)]
                edit_timesheet_form.company = company_list[company_name_list.index(edit_timesheet_form.company_name)]
                edit_timesheet_form.project = project_list[project_name_list.index(edit_timesheet_form.project_name)]
                edit_timesheet_form.save()
                return redirect('timesheets:weekly_timesheet', edit_timesheet_form.slug)
    else:
        edit_timesheet_form = TimesheetForm(instance=timesheet)
        context = {
            'equipment_list': equipment_list,
            'company_list': company_list,
            'project_list': project_list,
            'edit_timesheet_form': edit_timesheet_form,

         }
        template = 'timesheet/timesheet_edit.html'
        return render(request, template, context)
