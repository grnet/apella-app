# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0003_auto_20170214_0938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apellauser',
            name='home_phone_number',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='apellauser',
            name='id_passport',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='apellauser',
            name='mobile_phone_number',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
