# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-25 00:49
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dcp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='catastrophe',
            name='location_x',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='catastrophe',
            name='location_y',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='catastrophe',
            name='radius',
            field=models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1000)]),
        ),
        migrations.AddField(
            model_name='governmentarea',
            name='canCreateNgoArea',
            field=models.BooleanField(default=False),
        ),
    ]
