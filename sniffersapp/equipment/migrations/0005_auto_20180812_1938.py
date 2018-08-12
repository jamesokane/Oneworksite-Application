# Generated by Django 2.0.6 on 2018-08-12 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0004_auto_20180703_2320'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipment_additionalinfo',
            name='created_user',
        ),
        migrations.RemoveField(
            model_name='equipment_additionalinfo',
            name='equipment_id',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='fuel',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='height_restrictor',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='maintenance',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='make',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='model',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='purchase_amount',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='purchase_date',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='rubber_tracks',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='size',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='year',
        ),
        migrations.AddField(
            model_name='equipment',
            name='description',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.DeleteModel(
            name='Equipment_AdditionalInfo',
        ),
    ]