# Generated by Django 5.0.6 on 2024-07-05 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='driverscan',
            name='show',
            field=models.BooleanField(default=True),
        ),
    ]
