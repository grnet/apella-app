# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0011_auto_20170125_1604'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='position',
            name='assistants',
        ),
        migrations.AddField(
            model_name='institutionmanager',
            name='departments',
            field=models.ManyToManyField(to='apella.Department', blank=True),
        ),
    ]