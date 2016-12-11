# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.test import TestCase

from apella.models import ApellaUser, Institution, School, Department, \
        SubjectArea, Subject, Position, InstitutionManager, Candidacy, \
        MultiLangFields


class CandidacyTest(TestCase):

    start_date = datetime.now() + timedelta(days=10)
    end_date = start_date + timedelta(days=40)

    def setUp(self):
        first_name = MultiLangFields.objects.create(
                el='Λάκης', en='Lakis')
        last_name = MultiLangFields.objects.create(
                el='Λάλακης', en='Lalakis')
        father_name = MultiLangFields.objects.create(
                el='Λούλης', en='Loulis')
        author = ApellaUser.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                father_name=father_name,
                username='manager',
                password='1234',
                role='institutionmanager',
                email='author@gmail.com')
        institution_title = MultiLangFields.objects.create(
            el='Πανεπιστήμιο Κρήτης', en='University of Crete')
        institution = Institution.objects.create(
            category='Institution', title=institution_title)
        self.author = InstitutionManager.objects.create(
                user=author,
                institution=institution,
                authority='1',
                authority_full_name='Κώστας Βουτσάς',
                manager_role='1')
        school_title = MultiLangFields.objects.create(
            el='Σχολή Θετικών Επιστημών', en='School of Sciences')
        school = School.objects.create(
            title=school_title, institution=institution)
        department_title = MultiLangFields.objects.create(
            el='Εφαρμοσμένα Μαθηματικά', en='Applied Mathematics')
        self.department = Department.objects.create(
            title=school_title, school=school,
            institution=institution, dep_number=20)
        subject_area_title = MultiLangFields.objects.create(
            el='Μαθηματικά', en='Mathematics')
        self.subject_area = SubjectArea.objects.create(
            title=subject_area_title)
        subject_title = MultiLangFields.objects.create(
            el='Άλγεβρα', en='Algebra')
        self.subject = Subject.objects.create(
            title=subject_title, area=self.subject_area)

        self.fek_posted_at = datetime.now() - timedelta(days=1)

        cand_first_name = MultiLangFields.objects.create(
                el='Υποψήφιος', en='Candidate')
        cand_last_name = MultiLangFields.objects.create(
                el='Παπαδόπουλος', en='Papadopoulos')
        cand_father_name = MultiLangFields.objects.create(
                el='Νικόλαος', en='Nick')
        candidate = ApellaUser.objects.create_user(
                first_name=cand_first_name,
                last_name=cand_last_name,
                father_name=cand_father_name,
                username='candidate',
                password='1234',
                role='candidate')
        self.candidate = candidate

    def test_create_candidacy(self):
        self.position = Position.objects.create(
                title='New Position',
                description='Description',
                discipline='Discipline',
                author=self.author,
                department=self.department,
                subject_area=self.subject_area,
                subject=self.subject,
                fek='http://www.google.com',
                fek_posted_at=self.fek_posted_at,
                starts_at=self.start_date,
                ends_at=self.end_date,
                department_dep_number=self.department.dep_number)
        self.assertEqual(self.position.state, 'posted')

        self.candidacy = Candidacy.objects.create(
                candidate=self.candidate,
                position=self.position,
                others_can_view=True)
        self.assertEqual(self.candidacy.state, 'posted')
