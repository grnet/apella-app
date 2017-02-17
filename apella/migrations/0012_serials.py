# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0011_auto_20170217_0006'),
    ]

    operations = [
        migrations.CreateModel(
            name='Serials',
            fields=[
                ('id', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('value', models.BigIntegerField(default=0)),
            ],
        ),
    ]
