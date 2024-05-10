# Generated by Django 5.0.4 on 2024-05-10 10:59

import django.db.models.deletion
from django.db import migrations, models


def update_county_to_galway(apps, schema_editor):
    PersonalDetails = apps.get_model('cars', 'PersonalDetails')
    County = apps.get_model('cars', 'County')

    galway_county, _ = County.objects.get_or_create(county="Galway")

    PersonalDetails.objects.update(county=galway_county)

class Migration(migrations.Migration):
    dependencies = [
        ('cars', '0012_alter_booking_country_alter_booking_county'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personaldetails',
            name='county',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cars.county'),
        ),
        migrations.RunPython(update_county_to_galway),

    ]
