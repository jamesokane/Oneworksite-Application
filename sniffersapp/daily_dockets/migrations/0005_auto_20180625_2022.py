# Generated by Django 2.0.6 on 2018-06-25 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daily_dockets', '0004_docket_smoko'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docket',
            name='docket_day',
            field=models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], default='Monday', max_length=20),
        ),
    ]
