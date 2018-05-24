# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0035_auto_20180202_1017'),
    ]

    operations = [
        migrations.AddField(
            model_name='userapplication',
            name='receiving_department',
            field=models.ForeignKey(related_name='receiving_department', to='apella.Department', null=True),
        ),
        migrations.AlterField(
            model_name='userapplication',
            name='app_type',
            field=models.CharField(default=b'tenure', max_length=30, choices=[['tenure', 'Tenure'], ['renewal', 'Renewal'], ['move', 'Change Department']]),
        ),
        migrations.AlterField(
            model_name='userapplication',
            name='department',
            field=models.ForeignKey(related_name='init_department', to='apella.Department'),
        ),
    ]
