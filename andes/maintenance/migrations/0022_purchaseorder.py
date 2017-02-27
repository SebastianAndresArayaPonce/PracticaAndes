# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-27 16:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0021_auto_20170224_1551'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estimate', models.FileField(upload_to=b'')),
                ('work_order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='maintenance.WorkOrder')),
            ],
        ),
    ]
