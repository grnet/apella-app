# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0009_auto_20170125_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='registry',
            name='registry_set_decision_file',
            field=models.ForeignKey(related_name='registry_set_decision_files', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='apella.ApellaFile', null=True),
        ),
    ]
