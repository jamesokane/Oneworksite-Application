# Generated by Django 2.0.6 on 2018-08-07 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timesheet', '0011_timesheet_submitted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timesheet',
            name='submitted',
        ),
        migrations.AddField(
            model_name='timesheet',
            name='status',
            field=models.CharField(choices=[('Open', 'Open'), ('Submitted', 'Submitted'), ('Approved', 'Approved')], default='Open', max_length=20),
        ),
    ]
