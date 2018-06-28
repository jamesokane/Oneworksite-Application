import csv
import cv2
import base64
import PIL
import numpy as np

from PIL import Image

from io import BytesIO, StringIO
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Frame, Image

from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib import messages

from .forms import PrestartForm, DocketForm, SignForm
from .models import Docket
from .utils import check_docket_locked

from ..connections.models import Company
from ..equipment.models import Equipment
from ..projects.models import Project
from ..timesheet.models import timesheet_from_docket
from ..timesheet.forms import TimesheetForm
from ..utils import get_object_or_404_perms

def docket_list(request, template='daily_dockets/docket_list.html'):
    docket_list = Docket.objects.for_user(user=request.user)
    context = {
         'docket_list': docket_list,
     }
    return render(request, template, context)

def daily_docket_new(request, template='daily_dockets/daily_docket_new.html'):
    return render(request, template, None)

def docket_start(request, slug, template='daily_dockets/docket_start.html'):
    docket = get_object_or_404_perms(Docket, request.user, slug=slug)
    if docket.locked:
        return redirect('daily_dockets:list')
    context = {
        'docket': docket,
    }
    return render(request, template, context)

def prestart_form(request, slug=None, template='daily_dockets/prestart_detail.html'):
    if slug:
        existing_docket = get_object_or_404_perms(Docket, request.user, slug=slug)
        check_docket_locked(existing_docket)
    else:
        existing_docket = None

    prestart_form = PrestartForm(request.POST or None, instance=existing_docket)

    if request.method == 'POST':
        if prestart_form.is_valid():
            docket = prestart_form.save(commit=False)
            if not existing_docket:
                # As this is the first creation of the docket, we need to assign
                # the current user and save
                docket.created_user = request.user
            docket.save()
            messages.success(request, 'Prestart saved successfully.')
            return redirect('daily_dockets:docket_start', docket.slug)

    context = {
        'docket': existing_docket,
        'prestart_form': prestart_form,
        'docket_url': existing_docket.get_absolute_url() if existing_docket else None,
    }
    return render(request, template, context)

def docket_form(request, slug, template='daily_dockets/docket_form.html'):
    docket = get_object_or_404_perms(Docket, request.user, slug=slug)
    check_docket_locked(docket)

    docket_form = DocketForm(request.POST or None, instance=docket)

    if request.method == 'POST':
        if docket_form.is_valid():
            docket_form.save()
            messages.success(request, 'Daily docket saved successfully.')
            return redirect('daily_dockets:docket_start', docket.slug)

    context = {
        'docket_form': docket_form,
        'docket': docket,
    }

    return render(request, template, context)

def docket_signature(request, slug, template='daily_dockets/docket_signature.html'):
    docket = get_object_or_404_perms(Docket, request.user, slug=slug)
    check_docket_locked(docket)

    sign_form = SignForm(request.POST or None, instance=docket)

    if request.method == 'POST':
        if sign_form.is_valid():
            sign_form.save()
            timesheet_from_docket(docket)
            messages.success(request, 'Docket completed and timesheet created.')
            return redirect('daily_dockets:list')

    context = {
        'docket': docket,
        'sign_form': sign_form,
    }
    return render(request, template, context)

def docket_summary(request, slug, template='daily_dockets/daily_docket_sum.html'):
    docket = get_object_or_404_perms(Docket, request.user, slug=slug)
    context = {
        'docket': docket,
    }
    return render(request, template, context)

def export_dockets(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="dockets.csv"'

    writer = csv.writer(response)
    writer.writerow(['Docket Number', 'Created By', 'Docket Date', 'Docket Day', 'Docket Shift',
                     'Start Time', 'Finish Time', 'Smoko', 'Lunch', 'Equipment Name', 'Equipment Number',
                     'Equipment Hours', 'Attachments', 'Client', 'Project Name' ])

    docket_list = Docket.objects.all().values_list('docket_num', 'created_user_name', 'docket_date', 'docket_day', 'docket_shift',
                                                   'start_time', 'finish_time', 'smoko', 'lunch', 'equipment', 'equipment_num',
                                                   'equipment_hours', 'attachments', 'company', 'project')

    for docket in docket_list:
        writer.writerow(docket)
    return response


def dockets_pdf(request, slug):
    docket = get_object_or_404_perms(Docket, request.user, slug=slug)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="docket.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer)


    # data = docket.operator_sign
    # im = PIL.Image.open(BytesIO(base64.b64decode(data.split(',')[1])))
    # im.save("image.png")



    # data = docket.operator_sign
    # f = BytesIO()
    # f.write(base64.b64decode(data.split(',')[1]))
    # f.seek(0)
    # image = PIL.Image.open(f)

    data = docket.operator_sign
    imgdata = base64.b64decode(data.split(',')[1])
    image = PIL.Image.open(BytesIO(imgdata))

    signature = ImageReader(image)

    p.drawImage(signature, 45, 100, width=150, height=75, mask=None, preserveAspectRatio=True, anchor='c')

    logo = ImageReader("sniffersapp/static/images/logo.png")
    p.drawImage(logo, 45, 745, width=150, height=75, mask=None, preserveAspectRatio=True, anchor='c')

    p.setFillColorRGB(0.329, 0.329, 0.329)
    p.setFont('Helvetica-Bold', 16)
    #Docket Number
    p.drawString(400,770,'DOCKET: ')
    p.drawString(480,770,"D-3-1000")

    p.setStrokeColorRGB(0.658, 0.658, 0.658)
    p.setLineWidth(1)
    p.line(40,750,554,750) # Page width 595

    # Customer
    p.setFont('Helvetica-Bold', 10)
    p.drawString(50,720,'docket.operator_sign:')
    p.setFont('Helvetica', 10)
    p.drawString(120,720,"Oneworksite")

    # Date
    p.setFont('Helvetica-Bold', 10)
    p.drawString(50,695,'DATE: ')
    p.setFont('Helvetica', 10)
    p.drawString(90,695,"June 14, 2018")
    # Day
    p.setFont('Helvetica-Bold', 10)
    p.drawString(225,695,'DAY: ')
    p.setFont('Helvetica', 10)
    p.drawString(260,695,"Thursday")
    # Shift
    p.setFont('Helvetica-Bold', 10)
    p.drawString(380,695,'SHIFT: ')
    p.setFont('Helvetica', 10)
    p.drawString(430,695,"Day")

    # Equipment
    p.setFont('Helvetica-Bold', 10)
    p.drawString(50,670,'ITEM OR PLANT: ')
    p.setFont('Helvetica', 10)
    p.drawString(140,670,"20T Excavator")
    # Unit Number
    p.setFont('Helvetica-Bold', 10)
    p.drawString(280,670,'UNIT NO: ')
    p.setFont('Helvetica', 10)
    p.drawString(335,670,"EX120")

    # Operator
    p.setFont('Helvetica-Bold', 10)
    p.drawString(50,645,'OPERATOR: ')
    p.setFont('Helvetica', 10)
    p.drawString(120,645,"James O'Kane")
    # Supervisor
    p.setFont('Helvetica-Bold', 10)
    p.drawString(280,645,'SUPERVISOR: ')
    p.setFont('Helvetica', 10)
    p.drawString(365,645,"Michael Smith")

    # Start time
    p.setFont('Helvetica-Bold', 10)
    p.drawString(50,620,'START TIME: ')
    p.setFont('Helvetica', 10)
    p.drawString(120,620,"05:30")
    # Finish time
    p.setFont('Helvetica-Bold', 10)
    p.drawString(225,620,'FINISH TIME: ')
    p.setFont('Helvetica', 10)
    p.drawString(295,620,"18:00")
    # Total hours
    p.setFont('Helvetica-Bold', 10)
    p.drawString(380,620,'TOTAL HOURS: ')
    p.setFont('Helvetica', 10)
    p.drawString(475,620,"10h 30m")

    # Lunch
    p.setFont('Helvetica-Bold', 10)
    p.drawString(50,595,'LUNCH: ')
    p.setFont('Helvetica', 10)
    p.drawString(100,595,"30mins")
    # Smoko
    p.setFont('Helvetica-Bold', 10)
    p.drawString(225,595,'SMOKO: ')
    p.setFont('Helvetica', 10)
    p.drawString(275,595,"30mins")
    # Payable hours
    p.setFont('Helvetica-Bold', 10)
    p.drawString(380,595,'PAYABLE HOURS: ')
    p.setFont('Helvetica', 10)
    p.drawString(490,595,"10h 30m")

    # Attachments
    p.setFont('Helvetica-Bold', 10)
    p.drawString(50,570,'ATTACHMENTS USED: ')
    p.setFont('Helvetica', 10)
    p.drawString(175,570,"Rock breaker")

    # Prestart
    p.setStrokeColorRGB(0.329, 0.329, 0.329)
    p.setFont('Helvetica-Bold', 11)
    p.drawString(40,520,'PLANT OPERATORS DAILY SAFETY CHECKLIST')
    p.setFont('Helvetica-Bold', 9)
    #Item 1
    p.drawString(50,495,'1. Brakes, steering, gauges, lights, warning devices')
    #check box
    p.rect(515, 495, 10, 10, fill=0, stroke=1)
    p.line(515,495,525,505) #(X-start, Y-start, X-finish, Y-finish )
    p.line(525,495,515,505)
    p.drawString(278,492,'.'*93)
    #Item 2
    p.drawString(50,470,'2. Visibility - windscreen, wipers, washers, demisters, mirrors, windows')
    p.rect(515, 470, 10, 10, fill=0, stroke=1)
    p.line(515,470,525,480) #(X-start, Y-start, X-finish, Y-finish )
    p.line(525,470,515,480)
    p.drawString(365,467,'.'*58)
    #Item 3
    p.drawString(50,445,'3. Cabin - access, seating, seatbelts, loose objects, control levers')
    p.rect(515, 445, 10, 10, fill=0, stroke=1)
    p.line(515,445,525,455) #(X-start, Y-start, X-finish, Y-finish )
    p.line(525,445,515,455)
    p.drawString(340,442,'.'*68)
    #Item 4
    p.drawString(50,420,'4. Wheels, tyres, nutes, damage, wear, pressure')
    p.rect(515, 420, 10, 10, fill=0, stroke=1)
    p.line(515,420,525,430) #(X-start, Y-start, X-finish, Y-finish )
    p.line(525,420,515,430)
    p.drawString(263,417,'.'*99)
    #Item 5
    p.drawString(50,395,'5. Guards - in place, secure, warning signs lights, alarms')
    p.rect(515, 395, 10, 10, fill=0, stroke=1)
    p.line(515,395,525,405) #(X-start, Y-start, X-finish, Y-finish )
    p.line(525,395,515,405)
    p.drawString(302,392,'.'*83)
    #Item 6
    p.drawString(50,370,'6. Hydraulics - rams, hoses, leaks, wear')
    p.rect(515, 370, 10, 10, fill=0, stroke=1)
    p.line(515,370,525,380) #(X-start, Y-start, X-finish, Y-finish )
    p.line(525,370,515,380)
    p.drawString(227,367,'.'*113)
    #Item 7
    p.drawString(50,345,'7. Excessive wear - hooks, chains, pins, pivots, tracks, G.E.T')
    p.rect(515, 345, 10, 10, fill=0, stroke=1)
    p.line(515,345,525,355) #(X-start, Y-start, X-finish, Y-finish )
    p.line(525,345,515,355)
    p.drawString(317,342,'.'*77)
    #Item 8
    p.drawString(50,320,'8. Oils and coolants level')
    p.rect(515, 320, 10, 10, fill=0, stroke=1)
    p.line(515,320,525,330) #(X-start, Y-start, X-finish, Y-finish )
    p.line(525,320,515,330)
    p.drawString(167,317,'.'*137)
    #Item 9
    p.drawString(50,295,'9. Misc, electrical, fire extinguisher, communications')
    p.rect(515, 295, 10, 10, fill=0, stroke=1)
    p.line(515,295,525,305) #(X-start, Y-start, X-finish, Y-finish )
    p.line(525,295,515,305)
    p.drawString(285,292,'.'*90)
    #Item 10
    p.drawString(50,270,'10. Quick hitch attachments')
    p.rect(515, 270, 10, 10, fill=0, stroke=1)
    p.line(515,270,525,280) #(X-start, Y-start, X-finish, Y-finish )
    p.line(525,270,515,280)
    p.drawString(177,267,'.'*133)
    #Item 11
    p.drawString(50,245,'11. You are free from the influences of drugs and alcohol')
    p.rect(515, 245, 10, 10, fill=0, stroke=1)
    p.line(515,245,525,255) #(X-start, Y-start, X-finish, Y-finish )
    p.line(525,245,515,255)
    p.drawString(302,242,'.'*83)
    #Item 12
    p.drawString(50,220,'12. You are physically and mentally fit to operate or drive')
    p.rect(515, 220, 10, 10, fill=0, stroke=1)
    p.line(515,220,525,230) #(X-start, Y-start, X-finish, Y-finish )
    p.line(525,220,515,230)
    p.drawString(302,220,'.'*83)
    # Faults
    p.setFont('Helvetica-Bold', 9)
    p.drawString(50,195,'Details of Fault/Defect: ')
    p.setFont('Helvetica', 9)
    p.drawString(160,195,"Broken windscreen")
    # Reported to
    p.setFont('Helvetica-Bold', 9)
    p.drawString(50,170,'Fault Reported to: ')
    p.setFont('Helvetica', 9)
    p.drawString(140,170,"Adam Morris")





    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
