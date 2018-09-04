from django.urls import path

from .views import *

app_name = 'projects'

urlpatterns = [
    path('', project_list, name='list'),
    path('new/', project_form, name='project_new'),
    path('<slug:slug>/', project_detail, name='project_detail'),
    path('<slug:slug>/edit/', project_form, name='project_edit'),
]
