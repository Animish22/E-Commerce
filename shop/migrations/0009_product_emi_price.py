# Generated by Django 4.1.4 on 2022-12-18 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_rename_timestap_orderupdate_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='emi_price',
            field=models.IntegerField(default=0),
        ),
    ]
