from django.urls import path

from .views import *

app_name = 'equipment'

urlpatterns = [
    path('', equipment_list, name='list'),
    path('new_attachment', attachment_form, name='attachment_new'),
    path('new_equipment', equipment_form, name='equipment_new'),
    path('<slug:slug>/edit/attachment/', attachment_edit, name='attachment_edit'),
    path('<slug:slug>/edit/equipment/', equipment_edit, name='equipment_edit'),
]
