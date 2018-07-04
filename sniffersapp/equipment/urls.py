from django.urls import path

from .views import *

app_name = 'equipment'

urlpatterns = [
    path('', equipment_list, name='list'),
    path('new/', equipment_form, name='equipment_new'),
    path('<int:pk>/', equipment_detail, name='equipment_detail'),
    path('<int:pk>/edit/', equipment_edit, name='equipment_edit'),
]