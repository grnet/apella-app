# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0037_auto_20180302_1102'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='registrymembership',
            unique_together=set([('registry', 'professor')]),
        ),
    ]
