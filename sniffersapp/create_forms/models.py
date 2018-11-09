import datetime
from django.db import models
from django.conf import settings


from shortuuidfield import ShortUUIDField

class FormNew(models.Model):

    created_user = models.ForeignKey(settings.AUTH_USER_MODEL,
            blank=True, null=True, on_delete=models.PROTECT)

    uuid = ShortUUIDField()
    slug = models.CharField(max_length=80, unique=True)
    # Form Name
    form_name = models.CharField(max_length=80, blank=False,)
    # Form description
    form_description = models.TextField(blank=True)
    # Created/Updated
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.form_name

    # Create slug using first 8 characters of uuid
    def save(self, **kwargs):
        super(FormNew, self).save()
        slug = self.uuid
        self.slug = slug[:8]
        super(FormNew, self).save()


class FormItem(models.Model):

    form_options = (
        ('text', 'text'),
        ('checkbox', 'checkbox'),
        ('textfield', 'textfield'),
    )

    form = models.ForeignKey(FormNew, models.SET_NULL, null=True, blank=True)

    uuid = ShortUUIDField()
    slug = models.CharField(max_length=80, unique=True)

    # General fields in a form field
    text = models.TextField(blank=True)
    label = models.CharField(max_length=80, blank=True)
    help_text = models.CharField(max_length=80, blank=True)
    required = models.BooleanField(blank=True, default=False)

    # Used to remove form items instead of deleting them
    removed = models.BooleanField(blank=True, default=False)

    form_type = models.CharField(max_length=80, blank=False, choices=form_options)

    # Fields used once form has been created
    checkbox = models.BooleanField(blank=True, default=False)
    textfield = models.TextField(blank=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    order = models.IntegerField(blank = True, null = True)

    def __str__(self):
        return self.slug

    # Create slug using first 8 characters of uuid
    def save(self, **kwargs):
        super(FormItem, self).save()
        slug = self.uuid
        self.slug = slug[:8]
        super(FormItem, self).save()
