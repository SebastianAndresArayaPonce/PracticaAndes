# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-09 19:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0012_auto_20170209_1415'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workorder',
            old_name='datetime',
            new_name='in_datetime',
        ),
        migrations.AddField(
            model_name='workorder',
            name='out_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]