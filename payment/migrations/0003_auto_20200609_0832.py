# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2020-06-09 08:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_auto_20200608_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Телефон'),
        ),
    ]