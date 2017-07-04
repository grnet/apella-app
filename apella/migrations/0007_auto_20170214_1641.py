# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0006_auto_20170214_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professor',
            name='discipline_text',
            field=models.TextField(blank=True),
        ),
    ]
