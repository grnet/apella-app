# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0017_oldapellaareasubscriptions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professor',
            name='rank',
            field=models.CharField(blank=True, max_length=30, choices=[['Professor', 'Professor'], ['Associate Professor', 'Associate Professor'], ['Assistant Professor', 'Assistant Professor'], ['Lecturer', 'Lecturer'], ['Research Director', 'Research Director'], ['Principal Researcher', 'Principal Researcher'], ['Affiliated Researcher', 'Affiliated Researcher']]),
        ),
    ]
