# Generated by Django 2.0.6 on 2018-08-17 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timesheet', '0015_auto_20180811_0653'),
    ]

    operations = [
        migrations.AddField(
            model_name='timesheet',
            name='docket_date_end',
            field=models.DateField(blank=True, null=True),
        ),
    ]