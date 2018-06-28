from django.contrib import admin

# Register your models here.
from .models import Contact, Company


class CompanyAdmin(admin.ModelAdmin):
    list_display = ["slug", "company_name", "created_on", "updated_on"]
    list_display_links = ["company_name", "slug"]
    readonly_fields = ("uuid", "created_on", "updated_on" )

    class Meta:
        model = Company

admin.site.register(Company, CompanyAdmin)


class ContactAdmin(admin.ModelAdmin):
    list_display = ["slug", "contact_name", "job_title", "created_on", "updated_on"]
    list_display_links = ["slug", "contact_name", "job_title", "created_on", "updated_on"]
    readonly_fields = ("uuid", "created_on", "updated_on",)

    class Meta:
        model = Contact

admin.site.register(Contact, ContactAdmin)
