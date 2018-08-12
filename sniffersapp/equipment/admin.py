from django.contrib import admin

from .models import Equipment, Attachment


class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('equipment_id', 'year', 'make', 'model', 'registration')
    readonly_fields = ('created_on', 'updated_on', 'created_user')

admin.site.register(Equipment, EquipmentAdmin)

class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('attachment_id', 'attachment_type')
    readonly_fields = ('created_on', 'updated_on', 'created_user')

admin.site.register(Attachment, AttachmentAdmin)
