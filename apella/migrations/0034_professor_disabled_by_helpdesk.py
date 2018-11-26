# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0033_auto_20170919_0954'),
    ]

    operations = [
        migrations.AddField(
            model_name='professor',
            name='disabled_by_helpdesk',
            field=models.BooleanField(default=False),
        ),
    ]
