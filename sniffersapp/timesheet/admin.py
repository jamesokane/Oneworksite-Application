from django.contrib import admin

from .models import Timesheet

class TimesheetAdmin(admin.ModelAdmin):
    list_display = ('slug',)
    list_display_links = ('slug',)
    readonly_fields = ('slug', 'created_on', 'updated_on')

    class Meta:
        model = Timesheet

admin.site.register(Timesheet, TimesheetAdmin)
