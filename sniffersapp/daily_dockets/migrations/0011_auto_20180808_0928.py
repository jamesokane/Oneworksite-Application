# Generated by Django 2.0.6 on 2018-08-07 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daily_dockets', '0010_auto_20180807_2007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docket',
            name='docket_day',
            field=models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], default='Wednesday', max_length=20),
        ),
    ]
