# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='oldapellausermigrationdata',
            name='migration_key',
            field=models.TextField(default=None, null=True),
        ),
    ]
