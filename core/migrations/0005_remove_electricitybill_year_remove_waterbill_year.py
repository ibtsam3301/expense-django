# Generated by Django 4.1.2 on 2022-10-09 01:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_electricitybill_monthlyrent_waterbill'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='electricitybill',
            name='year',
        ),
        migrations.RemoveField(
            model_name='waterbill',
            name='year',
        ),
    ]
