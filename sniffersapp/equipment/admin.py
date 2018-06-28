from django.contrib import admin

from .models import Equipment, EquipmentBooking

class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'make', 'model', 'equipment_type')
    readonly_fields = ('created_on', 'updated_on', 'created_user')

admin.site.register(Equipment, EquipmentAdmin)

class EquipmentBookingAdmin(admin.ModelAdmin):
    list_display = ('equipment', 'project', 'company', 'start_date', 'end_date')
    readonly_fields = ('created_on', 'updated_on', 'created_user')

admin.site.register(EquipmentBooking, EquipmentBookingAdmin)
