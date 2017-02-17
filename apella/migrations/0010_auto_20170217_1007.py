# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0009_subject_old_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='electors_meeting_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
