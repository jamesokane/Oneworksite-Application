from django.db import models

from shortuuidfield import ShortUUIDField

class FileImport(models.Model):

    csv_import = models.FileField(null=True, blank=True, upload_to='csv_import/')
    uuid = ShortUUIDField()
    slug = models.CharField(max_length=80, unique=True)

    # Create slug using first 8 characters of uuid
    def save(self):
        super(FileImport, self).save()
        slug = self.uuid
        self.slug = slug[:8]
        super(FileImport, self).save()

    def __str__(self):
        return self.slug
