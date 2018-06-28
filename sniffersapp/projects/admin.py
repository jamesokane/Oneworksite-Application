from django.contrib import admin

from .models import Project

class ProjectAdmin(admin.ModelAdmin):
    list_display = ["project_name", "created_on", "updated_on"]
    list_display_links = ["project_name", "created_on", "updated_on"]
    readonly_fields = ("created_on", "updated_on",)

    class Meta:
        model = Project

admin.site.register(Project, ProjectAdmin)
