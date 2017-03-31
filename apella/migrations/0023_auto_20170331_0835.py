# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0022_auto_20170330_1410'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='position_type',
            field=models.CharField(default=b'election', max_length=30, choices=[['election', 'Election'], ['tenure', 'Tenure'], ['renewal', 'Renewal']]),
        ),
        migrations.AddField(
            model_name='position',
            name='user_application',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='apella.UserApplication', null=True),
        ),
    ]
