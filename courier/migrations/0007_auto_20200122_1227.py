# Generated by Django 2.1.5 on 2020-01-22 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courier', '0006_auto_20200122_1209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='quantity',
            field=models.FloatField(default=1.0),
        ),
    ]