from django.test import TestCase
from datetime import datetime, timedelta
from apella.models import ApellaUser, Institution, School, Department,\
        SubjectArea, Subject, Position


class PositionTest(TestCase):

    start_date = datetime.now() + timedelta(days=10)
    end_date = start_date + timedelta(days=40)

    def setUp(self):
        self.author = ApellaUser.objects.create(
            username='manager', password='1234', role='1')
        institution = Institution.objects.create(title='University of Crete')
        school = School.objects.create(
            title='School of Mathematics', institution=institution)
        self.department = Department.objects.create(
            title='Applied Mathematics', school=school)
        self.subject_area = SubjectArea.objects.create(title='Mathematics')
        self.subject = Subject.objects.create(
            title='Algebra', area=self.subject_area)

        self.fek_posted_at = datetime.now() - timedelta(days=1)

    def test_create_position(self):
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
