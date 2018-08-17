from django.urls import path

from .views import *

app_name = 'daily_dockets'

urlpatterns = [
    path('', docket_list, name='list'),

    path('new/', daily_docket_new, name='daily_docket_new'),
    path('new/prestart/', prestart_form, name='prestart_form'),

    # Docket workflow: start/overview -> prestart -> daily -> signature
    path('<slug:slug>/', docket_start, name='docket_start'),
    path('<slug:slug>/prestart/', prestart_form, name='prestart_form'),
    path('<slug:slug>/daily/', docket_form, name='docket_form'),
    path('<slug:slug>/signature/', docket_signature, name='docket_signature'),

    path('<slug:slug>/summary/', docket_summary, name='docket_summary'),
    path('<slug:slug>/summary/pdf/', dockets_pdf, name='dockets_pdf'),
]
