# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0002_auto_20170213_2040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institution',
            name='organization',
            field=models.URLField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='institution',
            name='regulatory_framework',
            field=models.URLField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='position',
            name='fek',
            field=models.URLField(max_length=255),
        ),
        migrations.AlterField(
            model_name='position',
            name='nomination_act_fek',
            field=models.URLField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='professor',
            name='cv_url',
            field=models.URLField(max_length=255, blank=True),
        ),
    ]
