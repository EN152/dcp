# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-27 21:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dcp', '0003_auto_20160627_2239'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post_dangers',
            name='bumps',
        ),
        migrations.RemoveField(
            model_name='post_dangers',
            name='reports',
        ),
        migrations.RemoveField(
            model_name='post_news',
            name='bumps',
        ),
        migrations.RemoveField(
            model_name='post_news',
            name='reports',
        ),
        migrations.RemoveField(
            model_name='post_questions',
            name='bumps',
        ),
        migrations.RemoveField(
            model_name='post_questions',
            name='reports',
        ),
    ]
