# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-29 23:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dcp', '0011_auto_20160630_0103'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='catastrophe',
        ),
    ]