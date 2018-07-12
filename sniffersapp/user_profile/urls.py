from django.urls import path

from . import views
from .views import *

app_name = 'users'

urlpatterns = [
    path('', user_list , name='list'),
    path('~update/', views.UserEditView.as_view(), name='update'),
    path('pending-invites/', views.PendingInvites.as_view(), name='pending-invites'),
    path('resend-invite/<int:pk>/', views.resend_invitation, name='resend-invite'),
    path('~adminupdate/<int:pk>/', views.AdminUpdateView.as_view(), name='adminupdate'),
    path('<str:username>/', views.UserDetailView.as_view(), name='detail'),
]
