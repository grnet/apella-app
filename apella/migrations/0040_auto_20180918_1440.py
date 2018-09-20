# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0039_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='rank',
            field=models.CharField(blank=True, max_length=30, choices=[['Professor', 'Professor'], ['Associate Professor', 'Associate Professor'], ['Assistant Professor', 'Assistant Professor'], ['Lecturer', 'Lecturer']]),
        ),
    ]
