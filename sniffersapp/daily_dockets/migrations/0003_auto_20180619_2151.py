# Generated by Django 2.0.6 on 2018-06-19 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daily_dockets', '0002_auto_20180618_2121'),
    ]

    operations = [
        migrations.AddField(
            model_name='docket',
            name='created_user_name',
            field=models.CharField(default='James', max_length=80),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='docket',
            name='docket_day',
            field=models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], default='Tuesday', max_length=20),
        ),
    ]
