# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0020_oldapellaareasubscriptions_departments_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apellauser',
            name='role',
            field=models.CharField(default=b'candidate', max_length=20, choices=[['institutionmanager', 'Institution Manager'], ['candidate', 'Candidate'], ['professor', 'Professor'], ['helpdeskadmin', 'Helpdesk Admin'], ['helpdeskuser', 'Helpdesk User'], ['assistant', 'Assistant'], ['ministry', 'Ministry Administrator']]),
        ),
    ]
