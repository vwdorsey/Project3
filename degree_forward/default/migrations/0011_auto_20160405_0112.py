# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-05 06:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('default', '0010_auto_20160404_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersemester',
            name='Number',
            field=models.IntegerField(null=True),
        ),
    ]
