# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-26 17:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20160926_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='channel_of_delivery',
            field=models.CharField(choices=[('G', 'Via government institutions in refugee hosting country'), ('U', 'Via UN agencies'), ('N', 'Via NGOs'), ('O', 'Other channel of delivery')], default='O', max_length=1),
        ),
        migrations.AddField(
            model_name='transaction',
            name='outside_london_conference',
            field=models.BooleanField(default=False, help_text='Was/is the above amount pledged outside of the London Conference?'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='refugee_facility_for_turkey',
            field=models.BooleanField(default=False, help_text='Was/is the above amount meant for the Refugee Facility for Turkey?'),
        ),
    ]
