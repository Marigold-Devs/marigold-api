# Generated by Django 3.2.9 on 2021-11-24 14:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("deliveries", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="delivery",
            old_name="delivered_out_by",
            new_name="delivered_by",
        ),
    ]
