# -*- coding: utf-8 -*-
from django.test import TestCase
from datetime import datetime, timedelta
from apella.models import ApellaUser, Institution, School, Department,\
        SubjectArea, Subject, Position, ApellaUserEl, ApellaUserEn,\
        InstitutionEl, InstitutionEn, SubjectEn, SubjectEl, SubjectAreaEl,\
        SubjectAreaEn, InstitutionManager, Candidacy, SchoolEl, SchoolEn,\
        DepartmentEl, DepartmentEn


class CandidacyTest(TestCase):

    start_date = datetime.now() + timedelta(days=10)
    end_date = start_date + timedelta(days=40)

    def setUp(self):
        user_el = ApellaUserEl.objects.create(
                first_name='Λάκης',
                last_name='Λαλάκης',
                father_name='Λούλης')
        user_en = ApellaUserEn.objects.create(
                first_name='Lakis',
                last_name='Lalakis',
                father_name='Loulis')
        author = ApellaUser.objects.create(
                el=user_el,
                en=user_en,
                username='manager',
                password='1234',
                role='1')
        institution_el = InstitutionEl.objects.create(
            title='Πανεπιστήμιο Κρήτης')
        institution_en = InstitutionEn.objects.create(
            title='University of Crete')
        institution = Institution.objects.create(
                el=institution_el, en=institution_en)
        self.author = InstitutionManager.objects.create(
                user=author,
                institution=institution,
                authority='1',
                authority_full_name='Κώστας Βουτσάς',
                manager_role='1')
        school_el = SchoolEl.objects.create(title='Σχολή Θετικών Επιστημών')
        school_en = SchoolEn.objects.create(title='School of Sciences')
        school = School.objects.create(
            el=school_el, en=school_en, institution=institution)
        department_el = DepartmentEl.objects.create(
            title='Εφαρμοσμένα Μαθηματικά')
        department_en = DepartmentEn.objects.create(
            title='Applied Mathematics')
        self.department = Department.objects.create(
            el=department_el, en=department_en, school=school)
        subject_area_el = SubjectAreaEl.objects.create(title='Μαθηματικά')
        subject_area_en = SubjectAreaEn.objects.create(title='Mathematics')
        subject_area = SubjectArea(el=subject_area_el, en=subject_area_en)
        subject_area.save()
        self.subject_area = subject_area
        subject_el = SubjectEl.objects.create(title='Άλγεβρα')
        subject_en = SubjectEn.objects.create(title='Algebra')
        subject = Subject.objects.create(
                el=subject_el,
                en=subject_en,
                area=self.subject_area)
        subject.save()
        self.subject = subject

        self.fek_posted_at = datetime.now() - timedelta(days=1)

        user_el = ApellaUserEl.objects.create(
                first_name='Υποψήφιος',
                last_name='Παπαδόπουλος',
                father_name='Γεώργιος')
        user_en = ApellaUserEn.objects.create(
                first_name='Candidate',
                last_name='Papadopoulow',
                father_name='George')
        candidate = ApellaUser.objects.create(
                el=user_el,
                en=user_en,
                username='candidate',
                password='1234',
                role='2')
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
                ends_at=self.end_date)
        self.assertEqual(self.position.state, '2')

        self.candidacy = Candidacy.objects.create(
                candidate=self.candidate,
                position=self.position,
                others_can_view=True)
        self.assertEqual(self.candidacy.state, '2')
