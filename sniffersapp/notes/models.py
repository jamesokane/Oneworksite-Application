from __future__ import unicode_literals

from django.db import models
from ..connections.models import Company, Contact
from ..projects.models import Project

from shortuuidfield import ShortUUIDField


class Notes(models.Model):
    company = models.ForeignKey(Company, blank=True, null=True, on_delete=models.SET_NULL)
    contact = models.ForeignKey(Contact, blank=True, null=True, on_delete=models.SET_NULL)
    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.SET_NULL)
    uuid = ShortUUIDField()
    slug = models.CharField(max_length=80, unique=True)
    note_name = models.CharField(max_length=80, blank=True)
    note_description = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"%s" % (self.created_on)

    # Create slug using first 8 characters of uuid
    def save(self):
        super(Notes, self).save()
        slug = self.uuid
        self.slug = slug[:8]
        super(Notes, self).save()

    # Company Name is shown as blank in NoteAdmin if it is NULL
    def company_name(self):
        if self.company is None:
            return None
        else:
            return self.company.company_name

    # Contact Name is shown as blank in NoteAdmin if it is NULL
    def contact_name(self):
        if self.contact is None:
            return None
        else:
            return u"%s %s" % (self.contact.first_name, self.contact.last_name)

    # Project Name is shown as blank in NoteAdmin if it is NULL
    def project_name(self):
        if self.project is None:
            return None
        else:
            return self.project.project_name

    # Description is limited to 80 characters
    def description_summary(self):
        description = self.note_description
        self.description_summary = description[:60]
        return self.description_summary
