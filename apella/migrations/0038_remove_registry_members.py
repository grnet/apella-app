# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0037_auto_20180302_1102'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registry',
            name='members',
        ),
    ]
