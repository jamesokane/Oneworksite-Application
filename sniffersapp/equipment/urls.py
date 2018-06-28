from django.urls import path

from .views import *

app_name = 'equipment'

urlpatterns = [
    path('', EquipmentListView.as_view(), name='list'),
    path('add/', EquipmentCreateView.as_view(), name='add'),
    path('<int:pk>/edit/', EquipmentUpdateView.as_view(), name='edit'),
    path('<int:equipment_id>/book/', EquipmentBookingCreateView.as_view(), name='book'),
    path('<int:equipment_id>/book/<int:pk>/edit/', EquipmentBookingUpdateView.as_view(), name='book_edit'),
    path('bookings/', EquipmentBookingListView.as_view(), name='bookings'),
]
