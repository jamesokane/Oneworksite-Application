# Generated by Django 2.0.6 on 2018-09-02 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daily_dockets', '0023_auto_20180902_1723'),
    ]

    operations = [
        migrations.RenameField(
            model_name='docket',
            old_name='equipment_hours',
            new_name='equipment_start_hours',
        ),
        migrations.AddField(
            model_name='docket',
            name='equipment_finish_hours',
            field=models.CharField(default='TEST', max_length=80),
            preserve_default=False,
        ),
    ]