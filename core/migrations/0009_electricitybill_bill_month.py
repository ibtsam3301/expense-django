# Generated by Django 4.1.2 on 2022-10-10 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_internetbill_alter_khata_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='electricitybill',
            name='bill_month',
            field=models.CharField(help_text='bill month', max_length=10, null=True),
        ),
    ]
