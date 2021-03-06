# Generated by Django 2.0.6 on 2018-08-10 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daily_dockets', '0011_auto_20180808_0928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docket',
            name='docket_day',
            field=models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], default='Saturday', max_length=20),
        ),
        migrations.AlterField(
            model_name='docket',
            name='item1',
            field=models.CharField(choices=[('No Issues', 'No Issues'), ('Needs Attention', 'Needs Attention'), ('Not Applicable', 'Not Applicable')], default='No Issues', max_length=20),
        ),
        migrations.AlterField(
            model_name='docket',
            name='item10',
            field=models.CharField(choices=[('No Issues', 'No Issues'), ('Needs Attention', 'Needs Attention'), ('Not Applicable', 'Not Applicable')], default='No Issues', max_length=20),
        ),
        migrations.AlterField(
            model_name='docket',
            name='item11',
            field=models.CharField(choices=[('No Issues', 'No Issues'), ('Needs Attention', 'Needs Attention'), ('Not Applicable', 'Not Applicable')], default='No Issues', max_length=20),
        ),
        migrations.AlterField(
            model_name='docket',
            name='item12',
            field=models.CharField(choices=[('No Issues', 'No Issues'), ('Needs Attention', 'Needs Attention'), ('Not Applicable', 'Not Applicable')], default='No Issues', max_length=20),
        ),
        migrations.AlterField(
            model_name='docket',
            name='item2',
            field=models.CharField(choices=[('No Issues', 'No Issues'), ('Needs Attention', 'Needs Attention'), ('Not Applicable', 'Not Applicable')], default='No Issues', max_length=20),
        ),
        migrations.AlterField(
            model_name='docket',
            name='item3',
            field=models.CharField(choices=[('No Issues', 'No Issues'), ('Needs Attention', 'Needs Attention'), ('Not Applicable', 'Not Applicable')], default='No Issues', max_length=20),
        ),
        migrations.AlterField(
            model_name='docket',
            name='item4',
            field=models.CharField(choices=[('No Issues', 'No Issues'), ('Needs Attention', 'Needs Attention'), ('Not Applicable', 'Not Applicable')], default='No Issues', max_length=20),
        ),
        migrations.AlterField(
            model_name='docket',
            name='item5',
            field=models.CharField(choices=[('No Issues', 'No Issues'), ('Needs Attention', 'Needs Attention'), ('Not Applicable', 'Not Applicable')], default='No Issues', max_length=20),
        ),
        migrations.AlterField(
            model_name='docket',
            name='item6',
            field=models.CharField(choices=[('No Issues', 'No Issues'), ('Needs Attention', 'Needs Attention'), ('Not Applicable', 'Not Applicable')], default='No Issues', max_length=20),
        ),
        migrations.AlterField(
            model_name='docket',
            name='item7',
            field=models.CharField(choices=[('No Issues', 'No Issues'), ('Needs Attention', 'Needs Attention'), ('Not Applicable', 'Not Applicable')], default='No Issues', max_length=20),
        ),
        migrations.AlterField(
            model_name='docket',
            name='item8',
            field=models.CharField(choices=[('No Issues', 'No Issues'), ('Needs Attention', 'Needs Attention'), ('Not Applicable', 'Not Applicable')], default='No Issues', max_length=20),
        ),
        migrations.AlterField(
            model_name='docket',
            name='item9',
            field=models.CharField(choices=[('No Issues', 'No Issues'), ('Needs Attention', 'Needs Attention'), ('Not Applicable', 'Not Applicable')], default='No Issues', max_length=20),
        ),
    ]
