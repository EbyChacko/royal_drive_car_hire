# Generated by Django 5.0.4 on 2024-05-28 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0002_booking_stripe_pid'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='status',
            field=models.CharField(default='', max_length=50),
        ),
    ]
