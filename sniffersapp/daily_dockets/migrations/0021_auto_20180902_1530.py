# Generated by Django 2.0.6 on 2018-09-02 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daily_dockets', '0020_auto_20180827_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docket',
            name='docket_day',
            field=models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], default='Sunday', max_length=20),
        ),
        migrations.AlterField(
            model_name='docket',
            name='item1',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='docket',
            name='item10',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='docket',
            name='item11',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='docket',
            name='item12',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='docket',
            name='item2',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='docket',
            name='item3',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='docket',
            name='item4',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='docket',
            name='item5',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='docket',
            name='item6',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='docket',
            name='item7',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='docket',
            name='item8',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='docket',
            name='item9',
            field=models.BooleanField(),
        ),
    ]
