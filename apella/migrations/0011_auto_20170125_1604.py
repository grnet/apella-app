# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0010_registry_registry_set_decision_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apellafile',
            name='file_kind',
            field=models.CharField(max_length=40, choices=[['cv', 'CV'], ['cv_professor', 'CV'], ['diploma', 'Diploma'], ['publication', 'Publication'], ['id_passport', 'ID Passport'], ['electors_set_file', 'Electors Set File'], ['committee_set_file', 'Committee Set File'], ['committee_proposal', 'Committee Proposal'], ['committee_note', 'Committee Note'], ['electors_meeting_proposal', 'Electors Meeting Proposal'], ['nomination_proceedings', 'Nomination Proceedings'], ['proceedings_cover_letter', 'Proceedings Cover Letter'], ['nomination_act', 'Nomination Act'], ['revocation_decision', 'Revocation Decision'], ['failed_election_decision', 'Failed Election Decision'], ['assistant_file', 'Assistant File'], ['self_evaluation_report', 'Self Evaluation Report'], ['attachment_file', 'Attachment File'], ['registry_set_decision_file', 'Registry Set Decision File']]),
        ),
        migrations.AlterField(
            model_name='professor',
            name='rank',
            field=models.CharField(blank=True, max_length=30, choices=[['Professor', 'Professor'], ['Associate Professor', 'Associate Professor'], ['Assistant Professor', 'Assistant Professor'], ['Research Director', 'Research Director'], ['Principal Researcher', 'Principal Researcher'], ['Affiliated Researcher', 'Affiliated Researcher']]),
        ),
    ]
