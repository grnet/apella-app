# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0002_auto_20170120_1420'),
    ]

    operations = [
        migrations.AddField(
            model_name='oldapellausermigrationdata',
            name='permanent_auth_token',
            field=models.TextField(unique=True, null=True),
        ),
    ]
