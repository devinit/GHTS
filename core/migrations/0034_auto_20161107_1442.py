# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-07 14:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_auto_20161103_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='recipient',
            field=models.CharField(choices=[('S', 'Syria'), ('J', 'Jordan'), ('L', 'Lebanon'), ('T', 'Turkey'), ('I', 'Iraq'), ('E', 'Egypt'), ('M', 'Multi-country'), ('R', 'Region'), ('N', 'Not defined')], default='N', max_length=1),
        ),
    ]