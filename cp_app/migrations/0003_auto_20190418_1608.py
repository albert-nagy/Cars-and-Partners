# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-18 16:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cp_app', '0002_auto_20190418_1446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=32),
        ),
    ]
