# Generated by Django 5.0.6 on 2024-05-13 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drivers', '0008_rename_address_operator_op_address_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='operator',
            old_name='op_address',
            new_name='operator_address',
        ),
        migrations.RenameField(
            model_name='operator',
            old_name='op_first_name',
            new_name='operator_first_name',
        ),
        migrations.RenameField(
            model_name='operator',
            old_name='op_last_name',
            new_name='operator_last_name',
        ),
    ]