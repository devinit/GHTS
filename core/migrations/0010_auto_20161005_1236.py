# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-05 12:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20160926_1713'),
    ]

    operations = [
        migrations.AddField(
            model_name='sector',
            name='loan_or_grant',
            field=models.CharField(choices=[('L', 'Loan'), ('G', 'Grant')], default='G', max_length=1),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='channel_of_delivery',
            field=models.CharField(choices=[('U', 'UN agencies'), ('N', 'NGOs'), ('R', 'RCRC'), ('G', 'Government institutions'), ('P', 'Private sector'), ('O', 'Other channel of delivery')], default='O', max_length=1),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='pledge_or_disbursement',
            field=models.CharField(choices=[('P', 'Committed'), ('C', 'Contracted'), ('D', 'Disbursed')], default='P', max_length=1),
        ),
    ]