# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0032_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='professor',
            name='disabled_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='professor',
            name='is_disabled',
            field=models.BooleanField(default=False),
        ),
    ]
