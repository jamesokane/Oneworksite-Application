# Generated by Django 2.0.6 on 2018-08-06 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timesheet', '0009_remove_timesheet_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='timesheet',
            name='smoko',
            field=models.CharField(choices=[('0', '0 min'), ('5', '5 mins'), ('10', '10 mins'), ('15', '15 mins'), ('20', '20 mins'), ('25', '25 mins'), ('30', '30 mins'), ('35', '35 mins'), ('40', '40 mins'), ('45', '45 mins'), ('50', '50 mins'), ('55', '55 mins'), ('60', '60 mins')], default='30', max_length=20),
        ),
        migrations.AlterField(
            model_name='timesheet',
            name='lunch',
            field=models.CharField(choices=[('0', '0 min'), ('5', '5 mins'), ('10', '10 mins'), ('15', '15 mins'), ('20', '20 mins'), ('25', '25 mins'), ('30', '30 mins'), ('35', '35 mins'), ('40', '40 mins'), ('45', '45 mins'), ('50', '50 mins'), ('55', '55 mins'), ('60', '60 mins')], default='30', max_length=20),
        ),
    ]