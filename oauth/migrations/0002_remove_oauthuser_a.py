# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-25 17:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='oauthuser',
            name='a',
        ),
    ]
