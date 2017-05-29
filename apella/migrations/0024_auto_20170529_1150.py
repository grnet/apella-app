# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0023_userapplication_department'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='position',
            name='ranks',
        ),
        migrations.AddField(
            model_name='position',
            name='rank',
            field=models.ForeignKey(blank=True, to='apella.ProfessorRank', null=True),
        ),
    ]
