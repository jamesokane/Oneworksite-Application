from __future__ import unicode_literals

from django.db import models

from shortuuidfield import ShortUUIDField



class Company(models.Model):

    uuid = ShortUUIDField()
    slug = models.CharField(max_length=80, unique=True)
    # Name
    company_name = models.CharField(max_length=80, blank=True)
    # WebAddress
    webaddress_company = models.CharField(max_length=120, blank=True)
    # Emails
    company_email = models.EmailField(max_length=80, blank=True)
    # Phone
    company_phone = models.CharField(max_length=20, blank=True)
    # Social
    linkedin = models.CharField(max_length=120, blank=True)
    facebook = models.CharField(max_length=120, blank=True)
    twitter = models.CharField(max_length=120, blank=True)
    # Additional Info
    additional_info = models.TextField(blank=True)
    # Created/Updated
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.company_name

    # Create slug using first 8 characters of uuid
    def save(self, **kwargs):
        super(Company, self).save()
        slug = self.uuid
        self.slug = slug[:8]
        super(Company, self).save()


from ..projects.models import Project

class Contact(models.Model):

    uuid = ShortUUIDField()
    slug = models.CharField(max_length=80, unique=True)
    # Company
    company = models.ForeignKey(Company, models.SET_NULL, null=True, blank=True)
    company_name = models.CharField(max_length=80, blank=True)
    # Name
    first_name = models.CharField(max_length=80, blank=False)
    last_name = models.CharField(max_length=80, blank=False)
    # Job Title
    job_title = models.CharField(max_length=80, blank=False)
    project = models.ForeignKey(Project, models.SET_NULL, null=True, blank=True)
    # Emails
    email_work = models.EmailField(max_length=80, blank=True)
    # Phone
    phone_mobile = models.CharField(max_length=20, blank=True)
    phone_work = models.CharField(max_length=20, blank=True)
    # Social
    linkedin = models.CharField(max_length=120, blank=True)
    facebook = models.CharField(max_length=120, blank=True)
    twitter = models.CharField(max_length=120, blank=True)
    # location
    # location = models.CharField(max_length=80, blank=True)
    # Additional Info
    additional_info = models.TextField(blank=True)
    # Created/Updated
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    # Contact List Order
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return u"%s %s - %s" % (self.first_name, self.last_name, self.slug)

    def contact_name(self):
        return u"%s %s" % (self.first_name, self.last_name)

    # Create slug using first 8 characters of uuid
    def save(self, **kwargs):
        super(Contact, self).save()
        slug = self.uuid
        self.slug = slug[:8]
        super(Contact, self).save()
