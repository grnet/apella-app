# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='verification_pending',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='candidate',
            name='verification_request',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='institutionmanager',
            name='verification_pending',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='institutionmanager',
            name='verification_request',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='professor',
            name='verification_pending',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='professor',
            name='verification_request',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='apellafile',
            name='file_kind',
            field=models.CharField(max_length=40, choices=[['cv', 'CV'], ['diploma', 'Diploma'], ['publication', 'Publication'], ['id_passport', 'ID Passport'], ['application_form', 'Application Form'], ['electors_set_file', 'Electors Set File'], ['committee_set_file', 'Committee Set File'], ['committee_proposal', 'Committee Proposal'], ['committee_note', 'Committee Note'], ['electors_meeting_proposal', 'Electors Meeting Proposal'], ['nomination_proceedings', 'Nomination Proceedings'], ['proceedings_cover_letter', 'Proceedings Cover Letter'], ['nomination_act', 'Nomination Act'], ['revocation_decision', 'Revocation Decision'], ['failed_election_decision', 'Failed Election Decision'], ['assistant_file', 'Assistant Files']]),
        ),
    ]
