# Generated by Django 5.0.4 on 2024-05-14 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0019_alter_booking_booking_number'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Booking',
        ),
    ]
