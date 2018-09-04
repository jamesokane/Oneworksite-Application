# Generated by Django 2.0.6 on 2018-09-03 10:33

from django.db import migrations, models
import django.utils.timezone
import shortuuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20180705_1952'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='slug',
            field=models.CharField(default=self.id, max_length=80, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='uuid',
            field=shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22),
        ),
    ]