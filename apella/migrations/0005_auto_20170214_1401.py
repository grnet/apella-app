# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0004_auto_20170214_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professor',
            name='discipline_text',
            field=models.CharField(max_length=1024, blank=True),
        ),
    ]
