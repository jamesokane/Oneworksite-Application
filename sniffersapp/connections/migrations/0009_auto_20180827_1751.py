# Generated by Django 2.0.6 on 2018-08-27 07:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('connections', '0008_remove_contact_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='job_title',
            field=models.CharField(max_length=80),
        ),
        migrations.AlterField(
            model_name='contact',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.Project'),
        ),
    ]
