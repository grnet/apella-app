# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0013_oldapellausermigrationdata_migrated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='apellauser',
            name='remote_data',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='registrationtoken',
            name='remote_data',
            field=models.TextField(blank=True),
        ),
    ]
