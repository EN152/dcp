# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-26 08:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dcp', '0007_auto_20160626_0214'),
    ]

    operations = [
        migrations.AddField(
            model_name='government',
            name='catastrophe',
            field=models.ManyToManyField(to='dcp.Catastrophe'),
        ),
        migrations.AddField(
            model_name='ngo',
            name='catastrophe',
            field=models.ManyToManyField(to='dcp.Catastrophe'),
        ),
    ]