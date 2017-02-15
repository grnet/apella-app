# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0008_auto_20170215_1007'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='old_code',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
