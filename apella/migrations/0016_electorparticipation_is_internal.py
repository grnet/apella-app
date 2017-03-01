# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0015_auto_20170223_0943'),
    ]

    operations = [
        migrations.AddField(
            model_name='electorparticipation',
            name='is_internal',
            field=models.BooleanField(default=True),
        ),
    ]
