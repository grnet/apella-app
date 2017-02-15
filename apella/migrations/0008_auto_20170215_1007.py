# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0007_auto_20170214_1641'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='oldapellacandidateassistantprofessormigrationdata',
            name='account_status',
        ),
        migrations.RemoveField(
            model_name='oldapellacandidateassistantprofessormigrationdata',
            name='rank',
        ),
    ]
