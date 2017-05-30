# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0024_auto_20170529_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='related',
            field=models.ManyToManyField(related_name='_position_related_+', to='apella.Position', blank=True),
        ),
    ]
