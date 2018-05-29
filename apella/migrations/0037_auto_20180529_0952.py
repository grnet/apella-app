# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0036_auto_20180523_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='position_type',
            field=models.CharField(default=b'election', max_length=30, choices=[['election', 'Election'], ['tenure', 'Tenure'], ['renewal', 'Renewal'], ['move', 'Move']]),
        ),
    ]
