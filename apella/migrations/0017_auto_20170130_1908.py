# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0016_auto_20170130_1243'),
    ]

    operations = [
        migrations.AddField(
            model_name='apellauser',
            name='can_set_academic',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='apellauser',
            name='can_upgrade_role',
            field=models.BooleanField(default=False),
        ),
    ]
