# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0037_auto_20180529_0952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='electorparticipation',
            name='position',
            field=models.ForeignKey(to='apella.Position', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='electorparticipation',
            name='professor',
            field=models.ForeignKey(to='apella.Professor', on_delete=django.db.models.deletion.PROTECT),
        ),
    ]
