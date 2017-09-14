# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0030_jiraissue_issue_call'),
    ]

    operations = [
        migrations.AddField(
            model_name='jiraissue',
            name='helpdesk_response',
            field=models.TextField(null=True, blank=True),
        ),
    ]
