from django.contrib import admin

from .models import FormNew, FormItem

class FormNewAdmin(admin.ModelAdmin):
    list_display = ["form_name", "created_on", "updated_on"]
    list_display_links = ["form_name", "created_on", "updated_on"]
    readonly_fields = ("created_on", "updated_on",)

    class Meta:
        model = FormNew

admin.site.register(FormNew, FormNewAdmin)


class FormItemAdmin(admin.ModelAdmin):
    list_display = ["label", "created_on", "updated_on", "removed"]
    list_display_links = ["label", "created_on", "updated_on"]
    readonly_fields = ("created_on", "updated_on",)

    class Meta:
        model = FormItem

admin.site.register(FormItem, FormItemAdmin)
