# Generated by Django 2.0.6 on 2018-07-05 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daily_dockets', '0005_auto_20180625_2022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docket',
            name='docket_day',
            field=models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], default='Thursday', max_length=20),
        ),
    ]