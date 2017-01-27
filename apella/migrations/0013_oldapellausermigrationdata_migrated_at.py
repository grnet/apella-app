# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0012_auto_20170127_1009'),
    ]

    operations = [
        migrations.AddField(
            model_name='oldapellausermigrationdata',
            name='migrated_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
