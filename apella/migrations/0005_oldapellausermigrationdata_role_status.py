# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0004_auto_20170123_1009'),
    ]

    operations = [
        migrations.AddField(
            model_name='oldapellausermigrationdata',
            name='role_status',
            field=models.TextField(default=b'UNAPPROVED'),
        ),
    ]
