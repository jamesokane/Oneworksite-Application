from django.contrib import admin

from .models import Docket

class DocketAdmin(admin.ModelAdmin):
    list_display = ('slug',)
    list_display_links = ('slug',)
    readonly_fields = ('slug', 'created_on', 'updated_on')

    class Meta:
        model = Docket

admin.site.register(Docket, DocketAdmin)
