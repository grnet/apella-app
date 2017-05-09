# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0022_auto_20170424_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='userapplication',
            name='department',
            field=models.ForeignKey(default=97, to='apella.Department'),
            preserve_default=False,
        ),
    ]
