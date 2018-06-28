from django.urls import path

from .views import *

app_name = 'connections'

urlpatterns = [
    path('', connections_list, name='list'),
    path('add_person/', contact_new, name='contact_new'),
    path('add_company/', company_new, name='company_new'),
    path('contact/<slug:slug>/', contact_detail, name='contact_detail'),
    path('company/<slug:slug>/', company_detail, name='company_detail'),
    path('contact/<slug:slug>/edit/', contact_edit, name='contact_edit'),
    path('company/<slug:slug>/edit/', company_edit, name='company_edit'),
]
