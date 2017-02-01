# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0017_auto_20170130_1908'),
    ]

    operations = [
        migrations.AddField(
            model_name='apellauser',
            name='shibboleth_enabled_at',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
