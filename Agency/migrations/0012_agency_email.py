# Generated by Django 5.0.1 on 2024-05-10 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Agency', '0011_remove_agency_detail_agency_address_agency_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='agency',
            name='email',
            field=models.CharField(default='-', max_length=350, null=True, verbose_name='Email'),
        ),
    ]