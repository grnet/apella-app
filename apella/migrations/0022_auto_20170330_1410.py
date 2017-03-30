# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0021_userapplication'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='ends_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='position',
            name='fek',
            field=models.URLField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='position',
            name='fek_posted_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='position',
            name='starts_at',
            field=models.DateTimeField(null=True),
        ),
    ]
