# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0026_auto_20170703_1242'),
    ]

    operations = [
        migrations.AddField(
            model_name='professor',
            name='leave_ends_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='professor',
            name='leave_file',
            field=models.ForeignKey(related_name='professor_leave_file', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='apella.ApellaFile', null=True),
        ),
        migrations.AddField(
            model_name='professor',
            name='leave_starts_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='apellafile',
            name='file_kind',
            field=models.CharField(max_length=40, choices=[['cv', 'CV'], ['cv_professor', 'CV'], ['diploma', 'Diploma'], ['publication', 'Publication'], ['id_passport', 'ID Passport'], ['electors_set_file', 'Electors Set File'], ['committee_set_file', 'Committee Set File'], ['committee_proposal', 'Committee Proposal'], ['committee_note', 'Committee Note'], ['electors_meeting_proposal', 'Electors Meeting Proposal'], ['nomination_proceedings', 'Nomination Proceedings'], ['proceedings_cover_letter', 'Proceedings Cover Letter'], ['nomination_act', 'Nomination Act'], ['revocation_decision', 'Revocation Decision'], ['failed_election_decision', 'Failed Election Decision'], ['assistant_file', 'Assistant File'], ['self_evaluation_report', 'Self Evaluation Report'], ['statement_file', 'Statement File'], ['attachment_file', 'Attachment File'], ['registry_set_decision_file', 'Registry Set Decision File'], ['leave_file', 'Leave File']]),
        ),
    ]
