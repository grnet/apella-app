# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0013_auto_20170222_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='electors_meeting_to_set_committee_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
