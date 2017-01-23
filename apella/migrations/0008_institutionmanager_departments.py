# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0007_auto_20170124_0946'),
    ]

    operations = [
        migrations.AddField(
            model_name='institutionmanager',
            name='departments',
            field=models.ManyToManyField(to='apella.Department', blank=True),
        ),
    ]
