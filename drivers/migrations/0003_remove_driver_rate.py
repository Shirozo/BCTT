# Generated by Django 5.0.6 on 2024-08-13 12:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drivers', '0002_driver_rate_alter_driver_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='driver',
            name='rate',
        ),
    ]