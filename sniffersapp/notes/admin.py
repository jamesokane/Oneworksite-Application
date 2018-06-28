from django.contrib import admin

# Register your models here.
from .models import Notes


class NoteAdmin(admin.ModelAdmin):
    list_display = ["company_name", "contact_name", "project_name", "created_on", "updated_on"]
    list_display_links = ["company_name", "contact_name", "project_name", "created_on", "updated_on"]
    readonly_fields = ("created_on", "updated_on")

    class Meta:
        model = Notes

admin.site.register(Notes, NoteAdmin)
