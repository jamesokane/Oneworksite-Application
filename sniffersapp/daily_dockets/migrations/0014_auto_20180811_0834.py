# Generated by Django 2.0.6 on 2018-08-10 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daily_dockets', '0013_auto_20180811_0830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docket',
            name='item1',
            field=models.CharField(choices=[('Please select ...', (('No Issues', 'No Issues'), ('Needs Attention', 'Needs Attention'), ('Not Applicable', 'Not Applicable')))], default='Please select ...', max_length=20),
        ),
    ]
