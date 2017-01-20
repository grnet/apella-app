# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professor',
            name='fek',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
