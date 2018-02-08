# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0034_professor_disabled_by_helpdesk'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professor',
            name='rank',
            field=models.CharField(blank=True, max_length=30, choices=[['Professor', 'Professor'], ['Associate Professor', 'Associate Professor'], ['Assistant Professor', 'Assistant Professor'], ['Tenured Assistant Professor', 'Tenured Assistant Professor'], ['Lecturer', 'Lecturer'], ['Research Director', 'Research Director'], ['Principal Researcher', 'Principal Researcher'], ['Affiliated Researcher', 'Affiliated Researcher']]),
        ),
    ]
