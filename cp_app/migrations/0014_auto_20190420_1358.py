# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-20 13:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cp_app', '0013_auto_20190420_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
