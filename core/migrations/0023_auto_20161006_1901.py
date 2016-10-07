# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-06 19:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_spreadsheet_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entry',
            options={'verbose_name_plural': 'entries'},
        ),
        migrations.AlterField(
            model_name='transaction',
            name='channel_of_delivery',
            field=models.CharField(blank=True, choices=[('U', 'UN agencies'), ('N', 'NGOs'), ('R', 'RCRC'), ('G', 'Government institutions'), ('P', 'Private sector'), ('O', 'Other channel of delivery')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='loan_or_grant',
            field=models.CharField(blank=True, choices=[('L', 'Loan'), ('G', 'Grant')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='pledge_or_disbursement',
            field=models.CharField(blank=True, choices=[('P', 'Pledged'), ('M', 'Committed'), ('C', 'Contracted'), ('D', 'Disbursed')], max_length=1, null=True),
        ),
    ]