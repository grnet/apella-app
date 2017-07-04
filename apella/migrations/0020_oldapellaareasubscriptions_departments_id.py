# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0019_auto_20170314_0701'),
    ]

    operations = [
        migrations.AddField(
            model_name='oldapellaareasubscriptions',
            name='departments_id',
            field=models.TextField(null=True),
        ),
    ]
