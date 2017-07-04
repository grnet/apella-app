# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0018_auto_20170311_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professor',
            name='rank',
            field=models.CharField(blank=True, max_length=30, choices=[['Professor', 'Professor'], ['Associate Professor', 'Associate Professor'], ['Assistant Professor', 'Assistant Professor'], ['Lecturer', 'Lecturer'], ['Tenured Assistant Professor', 'Tenured Assistant Professor'], ['Research Director', 'Research Director'], ['Principal Researcher', 'Principal Researcher'], ['Affiliated Researcher', 'Affiliated Researcher']]),
        ),
    ]
