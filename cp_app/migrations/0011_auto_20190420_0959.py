# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-20 09:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cp_app', '0010_partner_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='partner',
            old_name='modified_at',
            new_name='modify_at',
        ),
    ]