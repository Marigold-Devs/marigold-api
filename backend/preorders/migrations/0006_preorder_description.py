# Generated by Django 3.2.9 on 2022-04-22 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preorders', '0005_preordertransaction_datetime_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='preorder',
            name='description',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
