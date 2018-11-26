# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0027_jiraissue_issue_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jiraissue',
            name='resolution',
            field=models.CharField(default=b'', max_length=30, blank=True, choices=[['', ''], ['fixed', 'Fixed'], ['wont_fix', "Won't Fix"], ['duplicate', 'Duplicate'], ['incomplete', 'Incomplete'], ['cannot_reproduce', 'Cannot Reproduce'], ['fixed_workaround', 'Fixed Workaround']]),
        ),
    ]
