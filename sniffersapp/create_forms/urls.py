from django.urls import path

from .views import *

app_name = 'create_forms'

urlpatterns = [
    path('', form_list, name='list'),
    path('<slug:slug>/', form_detail, name='detail'),
]
