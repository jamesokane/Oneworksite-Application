from django.contrib import admin

from .models import FileImport

class FileImportAdmin(admin.ModelAdmin):
    list_display = ['csv_import', 'slug']
    list_display_links = ['csv_import', 'slug']

    class Meta:
        model = FileImport

admin.site.register(FileImport, FileImportAdmin)    
