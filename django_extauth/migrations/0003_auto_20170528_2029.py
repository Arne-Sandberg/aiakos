# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-28 20:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_extauth', '0002_auto_20170311_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='externalidentity',
            name='userinfo_yaml',
            field=models.TextField(blank=True, verbose_name='User information'),
        ),
    ]