# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0016_auto_20170130_1243'),
    ]

    operations = [
        migrations.AddField(
            model_name='institutionmanager',
            name='is_secretary',
            field=models.BooleanField(default=False),
        ),
    ]
