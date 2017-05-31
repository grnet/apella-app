# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0023_userapplication_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='apellauser',
            name='accepted_terms_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='apellauser',
            name='has_accepted_terms',
            field=models.BooleanField(default=False),
        ),
    ]
