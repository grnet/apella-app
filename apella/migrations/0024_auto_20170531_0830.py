# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0023_userapplication_department'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='professorrank',
            name='rank',
        ),
        migrations.RemoveField(
            model_name='position',
            name='ranks',
        ),
        migrations.AddField(
            model_name='position',
            name='rank',
            field=models.CharField(blank=True, max_length=30, choices=[['Professor', 'Professor'], ['Associate Professor', 'Associate Professor'], ['Assistant Professor', 'Assistant Professor']]),
        ),
        migrations.AddField(
            model_name='position',
            name='related_positions',
            field=models.ManyToManyField(related_name='_position_related_positions_+', to='apella.Position', blank=True),
        ),
        migrations.DeleteModel(
            name='ProfessorRank',
        ),
    ]
