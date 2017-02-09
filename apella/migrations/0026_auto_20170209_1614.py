# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0025_auto_20170209_1601'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='oldapellacandidacyfilemigrationdata',
            name='status',
        ),
        migrations.AddField(
            model_name='oldapellacandidacyfilemigrationdata',
            name='updated_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='oldapellafilemigrationdata',
            name='updated_at',
            field=models.DateTimeField(null=True),
        ),
    ]
