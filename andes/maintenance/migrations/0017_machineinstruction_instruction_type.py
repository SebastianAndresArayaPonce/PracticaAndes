# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-17 14:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0016_auto_20170217_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='machineinstruction',
            name='instruction_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='maintenance.InstructionType'),
            preserve_default=False,
        ),
    ]