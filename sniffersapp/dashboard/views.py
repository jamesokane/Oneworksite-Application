from django.shortcuts import render

from sniffersapp.equipment.models import Equipment


def dashboard(request):
    equipment_list = Equipment.objects.all().order_by('created_on')
    equipment_count = Equipment.objects.all().count

    # sum example for later if needed
    #av_coverage_latest = AV.objects.all().aggregate(total=Sum('healthy'))
    #av_coverage_latest = AV.objects.all().aggregate(total=Sum('healthy') + Sum('attention'))

    #Author.objects.annotate(total_pages=Sum('book__pages'))

    context = {
        'equipment_list': equipment_list,
        'equipment_count': equipment_count,
        }
    template = 'dashboard/dashboard.html'
    return render(request, template, context)