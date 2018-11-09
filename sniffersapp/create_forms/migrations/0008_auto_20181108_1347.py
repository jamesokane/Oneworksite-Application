# Generated by Django 2.0.6 on 2018-11-08 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('create_forms', '0007_auto_20181108_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formitem',
            name='form_type',
            field=models.CharField(choices=[('text', 'text'), ('checkbox', 'checkbox'), ('textfield', 'textfield')], max_length=80),
        ),
        migrations.AlterField(
            model_name='formitem',
            name='removed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='formitem',
            name='required',
            field=models.BooleanField(default=False),
        ),
    ]