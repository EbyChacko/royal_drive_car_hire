# Generated by Django 5.0.4 on 2024-05-29 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0003_booking_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='stripe_pid',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
    ]
