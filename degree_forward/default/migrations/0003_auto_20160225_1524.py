# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-25 21:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('default', '0002_auto_20160225_1518'),
    ]

    operations = [
        migrations.RenameField(
            model_name='semester',
            old_name='Year',
            new_name='Number',
        ),
        migrations.RemoveField(
            model_name='degreeplan',
            name='Type',
        ),
        migrations.AddField(
            model_name='degreeplan',
            name='Entry',
            field=models.CharField(choices=[('F', 'Fall'), ('S', 'Spring')], default='F"', max_length=1),
        ),
    ]
