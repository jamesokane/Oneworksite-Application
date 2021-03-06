# Generated by Django 2.0.6 on 2018-10-24 09:12

from django.db import migrations, models
import django.db.models.deletion
import shortuuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('create_forms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22)),
                ('slug', models.CharField(max_length=80, unique=True)),
                ('textfield_name', models.CharField(max_length=80)),
                ('textfield_input', models.TextField(blank=True)),
                ('checkbox_name', models.CharField(max_length=80)),
                ('checkboxinput', models.BooleanField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('form', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='create_forms.FormNew')),
            ],
        ),
    ]
