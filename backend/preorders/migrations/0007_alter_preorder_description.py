# Generated by Django 3.2.9 on 2022-04-22 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preorders', '0006_preorder_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preorder',
            name='description',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]