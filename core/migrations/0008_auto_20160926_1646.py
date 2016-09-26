# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-26 16:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20160926_1628'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='sector',
        ),
        migrations.AddField(
            model_name='transaction',
            name='sector',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Sector'),
        ),
    ]
