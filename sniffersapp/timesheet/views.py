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


def timesheet_calender(request):
    timesheet_list = Timesheet.objects.all()
    company_list = Company.objects.all()
    company_name_list = list(company_list.values_list('company_name', flat=True))
    project_list = Project.objects.all()
    project_name_list = list(project_list.values_list('project_name', flat=True))
    equipment_list = Equipment.objects.all()
    equipment_name_list = list(equipment_list.values_list('name', flat=True))

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
    timesheet_date_list = list(timesheet_list.values_list('docket_date', flat=True))
    company_list = Company.objects.all()
    company_name_list = list(company_list.values_list('company_name', flat=True))
    project_list = Project.objects.all()
    project_name_list = list(project_list.values_list('project_name', flat=True))
    equipment_list = Equipment.objects.all()
    equipment_name_list = list(equipment_list.values_list('name', flat=True))

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
    timesheet_list_weekly = timesheet_list_weekly.order_by('docket_date').order_by('start_time')

    # AJAX call for item summary modal
    if request.method == 'GET':
        slug = request.GET.get('content')
        if slug is None:
            try:
                timesheet_sum = timesheet_list_weekly[0]
                timesheet_ed = timesheet_list_weekly[0]
            except IndexError:
                timesheet_sum = None
                timesheet_ed = None
        elif 'timesheet_sum' in request.GET.get('name'):
            timesheet_sum = get_object_or_404(Timesheet, slug=slug)
            timesheet_ed = timesheet_list_weekly[0]
        elif 'timesheet_ed' in request.GET.get('name'):
            timesheet_ed = get_object_or_404(Timesheet, slug=slug)
            timesheet_sum = timesheet_list_weekly[0]


    # Determine the total hours worked each day of the week.
    # Monday
    # Creates a list of all the hours worked in a day
    monday_hours = []
    for item in timesheet_list.filter(docket_date=dates[0][0]):
        total_hours = datetime.datetime.combine(item.docket_date, item.finish_time) - datetime.datetime.combine(item.docket_date, item.start_time)
        payable_hours = total_hours - datetime.timedelta(minutes=int(item.lunch))
        monday_hours.append(payable_hours)
    # Determines the total hours worked in a day
    monday_total_hours = datetime.timedelta(hours=0, minutes=0, seconds=0)
    for item in monday_hours:
        monday_total_hours += item
    # Allows the total hours worked to be displayed in Hrs Mins
    if len(str(monday_total_hours)) == 7:
        monday_total_hours_hours = str(monday_total_hours)[:1]
        monday_total_hours_mins = str(monday_total_hours)[2:4]
    elif len(str(monday_total_hours)) == 8:
        monday_total_hours_hours = str(monday_total_hours)[:2]
        monday_total_hours_mins = str(monday_total_hours)[3:5]

    # Tuesday
    # Creates a list of all the hours worked in a day
    tuesday_hours = []
    for item in timesheet_list.filter(docket_date=dates[1][0]):
        total_hours = datetime.datetime.combine(item.docket_date, item.finish_time) - datetime.datetime.combine(item.docket_date, item.start_time)
        payable_hours = total_hours - datetime.timedelta(minutes=int(item.lunch))
        tuesday_hours.append(payable_hours)
    # Determines the total hours worked in a day
    tuesday_total_hours = datetime.timedelta(hours=0, minutes=0, seconds=0)
    for item in tuesday_hours:
        tuesday_total_hours += item
    # Allows the total hours worked to be displayed in Hrs Mins
    if len(str(tuesday_total_hours)) == 7:
        tuesday_total_hours_hours = str(tuesday_total_hours)[:1]
        tuesday_total_hours_mins = str(tuesday_total_hours)[2:4]
    elif len(str(tuesday_total_hours)) == 8:
        tuesday_total_hours_hours = str(tuesday_total_hours)[:2]
        tuesday_total_hours_mins = str(tuesday_total_hours)[3:5]

    # Wednesday
    # Creates a list of all the hours worked in a day
    wednesday_hours = []
    for item in timesheet_list.filter(docket_date=dates[2][0]):
        total_hours = datetime.datetime.combine(item.docket_date, item.finish_time) - datetime.datetime.combine(item.docket_date, item.start_time)
        payable_hours = total_hours - datetime.timedelta(minutes=int(item.lunch))
        wednesday_hours.append(payable_hours)
    # Determines the total hours worked in a day
    wednesday_total_hours = datetime.timedelta(hours=0, minutes=0, seconds=0)
    for item in wednesday_hours:
        wednesday_total_hours += item
    # Allows the total hours worked to be displayed in Hrs Mins
    if len(str(wednesday_total_hours)) == 7:
        wednesday_total_hours_hours = str(wednesday_total_hours)[:1]
        wednesday_total_hours_mins = str(wednesday_total_hours)[2:4]
    elif len(str(wednesday_total_hours)) == 8:
        wednesday_total_hours_hours = str(wednesday_total_hours)[:2]
        wednesday_total_hours_mins = str(wednesday_total_hours)[3:5]

    # Thursday
    # Creates a list of all the hours worked in a day
    thursday_hours = []
    for item in timesheet_list.filter(docket_date=dates[3][0]):
        total_hours = datetime.datetime.combine(item.docket_date, item.finish_time) - datetime.datetime.combine(item.docket_date, item.start_time)
        payable_hours = total_hours - datetime.timedelta(minutes=int(item.lunch))
        thursday_hours.append(payable_hours)
    # Determines the total hours worked in a day
    thursday_total_hours = datetime.timedelta(hours=0, minutes=0, seconds=0)
    for item in thursday_hours:
        thursday_total_hours += item
    # Allows the total hours worked to be displayed in Hrs Mins
    if len(str(thursday_total_hours)) == 7:
        thursday_total_hours_hours = str(thursday_total_hours)[:1]
        thursday_total_hours_mins = str(thursday_total_hours)[2:4]
    elif len(str(thursday_total_hours)) == 8:
        thursday_total_hours_hours = str(thursday_total_hours)[:2]
        thursday_total_hours_mins = str(thursday_total_hours)[3:5]

    # Friday
    # Creates a list of all the hours worked in a day
    friday_hours = []
    for item in timesheet_list.filter(docket_date=dates[4][0]):
        total_hours = datetime.datetime.combine(item.docket_date, item.finish_time) - datetime.datetime.combine(item.docket_date, item.start_time)
        payable_hours = total_hours - datetime.timedelta(minutes=int(item.lunch))
        friday_hours.append(payable_hours)
    # Determines the total hours worked in a day
    friday_total_hours = datetime.timedelta(hours=0, minutes=0, seconds=0)
    for item in friday_hours:
        friday_total_hours += item
    # Allows the total hours worked to be displayed in Hrs Mins
    if len(str(friday_total_hours)) == 7:
        friday_total_hours_hours = str(friday_total_hours)[:1]
        friday_total_hours_mins = str(friday_total_hours)[2:4]
    elif len(str(friday_total_hours)) == 8:
        friday_total_hours_hours = str(friday_total_hours)[:2]
        friday_total_hours_mins = str(friday_total_hours)[3:5]

    # Saturday
    # Creates a list of all the hours worked in a day
    saturday_hours = []
    for item in timesheet_list.filter(docket_date=dates[5][0]):
        total_hours = datetime.datetime.combine(item.docket_date, item.finish_time) - datetime.datetime.combine(item.docket_date, item.start_time)
        payable_hours = total_hours - datetime.timedelta(minutes=int(item.lunch))
        saturday_hours.append(payable_hours)
    # Determines the total hours worked in a day
    saturday_total_hours = datetime.timedelta(hours=0, minutes=0, seconds=0)
    for item in saturday_hours:
        saturday_total_hours += item
    # Allows the total hours worked to be displayed in Hrs Mins
    if len(str(saturday_total_hours)) == 7:
        saturday_total_hours_hours = str(saturday_total_hours)[:1]
        saturday_total_hours_mins = str(saturday_total_hours)[2:4]
    elif len(str(saturday_total_hours)) == 8:
        saturday_total_hours_hours = str(saturday_total_hours)[:2]
        saturday_total_hours_mins = str(saturday_total_hours)[3:5]

    # Sunday
    # Creates a list of all the hours worked in a day
    sunday_hours = []
    for item in timesheet_list.filter(docket_date=dates[6][0]):
        total_hours = datetime.datetime.combine(item.docket_date, item.finish_time) - datetime.datetime.combine(item.docket_date, item.start_time)
        payable_hours = total_hours - datetime.timedelta(minutes=int(item.lunch))
        sunday_hours.append(payable_hours)
    # Determines the total hours worked in a day
    sunday_total_hours = datetime.timedelta(hours=0, minutes=0, seconds=0)
    for item in sunday_hours:
        sunday_total_hours += item
    # Allows the total hours worked to be displayed in Hrs Mins
    if len(str(sunday_total_hours)) == 7:
        sunday_total_hours_hours = str(sunday_total_hours)[:1]
        sunday_total_hours_mins = str(sunday_total_hours)[2:4]
    elif len(str(sunday_total_hours)) == 8:
        sunday_total_hours_hours = str(sunday_total_hours)[:2]
        sunday_total_hours_mins = str(sunday_total_hours)[3:5]

    # Adds the total hours worked in a week
    weekly_total_hours = monday_total_hours + tuesday_total_hours + wednesday_total_hours + thursday_total_hours + friday_total_hours + saturday_total_hours + sunday_total_hours
    # Allows the total hours worked to be displayed in Hrs Mins
    if len(str(weekly_total_hours)) == 7:
        weekly_total_hours_hours = str(weekly_total_hours)[:1]
        weekly_total_hours_mins = str(weekly_total_hours)[2:4]
    elif len(str(weekly_total_hours)) == 8:
        weekly_total_hours_hours = str(weekly_total_hours)[:2]
        weekly_total_hours_mins = str(weekly_total_hours)[3:5]
    elif len(str(weekly_total_hours)) == 14:
        day_to_hours = int(str(weekly_total_hours)[:1]) * 24
        weekly_total_hours_hours = int(str(weekly_total_hours)[7:8]) + day_to_hours
        weekly_total_hours_hours = str(weekly_total_hours_hours)
        weekly_total_hours_mins = str(weekly_total_hours)[9:11]
    elif len(str(weekly_total_hours)) == 15:
        day_to_hours = int(str(weekly_total_hours)[:1]) * 24
        weekly_total_hours_hours = int(str(weekly_total_hours)[8:9]) + day_to_hours
        weekly_total_hours_hours = str(weekly_total_hours_hours)
        weekly_total_hours_mins = str(weekly_total_hours)[10:12]
    elif len(str(weekly_total_hours)) == 16:
        day_to_hours = int(str(weekly_total_hours)[:1]) * 24
        weekly_total_hours_hours = int(str(weekly_total_hours)[8:10]) + day_to_hours
        weekly_total_hours_hours = str(weekly_total_hours_hours)
        weekly_total_hours_mins = str(weekly_total_hours)[11:13]

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
                return redirect('timesheets:weekly_timesheet', timesheet_form.slug)
        elif 'edit_timesheet' in request.POST:
            edit_timesheet_form = TimesheetForm(request.POST)
            if edit_timesheet_form.is_valid():
                edit_timesheet_form = edit_timesheet_form.save(commit=False)
                edit_timesheet_form.equipment = equipment_list[equipment_name_list.index(edit_timesheet_form.equipment_name)]
                edit_timesheet_form.company = company_list[company_name_list.index(edit_timesheet_form.company_name)]
                edit_timesheet_form.project = project_list[project_name_list.index(edit_timesheet_form.project_name)]
                edit_timesheet_form.save()
                return redirect('timesheets:weekly_timesheet', edit_timesheet_form.slug)
    else:
        timesheet_form = TimesheetForm()
        edit_timesheet_form = TimesheetForm()
        context = {
            'timesheet': timesheet,
            'timesheet_date_list': timesheet_date_list,
            'timesheet_list_weekly': timesheet_list_weekly,
            'dates': dates,
            'day_name': day_name,
            'timesheet_sum': timesheet_sum,
            'timesheet_ed': timesheet_ed,
            'timesheet_list': timesheet_list,
            'monday_total_hours_hours': monday_total_hours_hours,
            'monday_total_hours_mins': monday_total_hours_mins,
            'tuesday_total_hours_hours': tuesday_total_hours_hours,
            'tuesday_total_hours_mins': tuesday_total_hours_mins,
            'wednesday_total_hours_hours': wednesday_total_hours_hours,
            'wednesday_total_hours_mins': wednesday_total_hours_mins,
            'thursday_total_hours_hours': thursday_total_hours_hours,
            'thursday_total_hours_mins': thursday_total_hours_mins,
            'friday_total_hours_hours': friday_total_hours_hours,
            'friday_total_hours_mins': friday_total_hours_mins,
            'saturday_total_hours_hours': saturday_total_hours_hours,
            'saturday_total_hours_mins': saturday_total_hours_mins,
            'sunday_total_hours_hours': sunday_total_hours_hours,
            'sunday_total_hours_mins': sunday_total_hours_mins,
            'weekly_total_hours_hours': weekly_total_hours_hours,
            'weekly_total_hours_mins': weekly_total_hours_mins,
            'timesheet_form': timesheet_form,
            'edit_timesheet_form': edit_timesheet_form,
            'equipment_list': equipment_list,
            'company_list': company_list,
            'project_list': project_list,
            'today': today,
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
