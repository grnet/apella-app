# -*- coding: utf-8 -*-
from datetime import timedelta, datetime
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.core.urlresolvers import reverse
from django.conf import settings
from django.apps import apps

from apella.models import Institution, School, Department, ApellaUser, \
        InstitutionManager, Professor, Candidate, MultiLangFields, \
        SubjectArea, Subject, ProfessorRank

import sys
reload(sys)
sys.setdefaultencoding('utf8')


MULTI_LANG_APIS = [
    (Institution, reverse('institutions-list')),
    (School, reverse('schools-list')),
    (Department, reverse('departments-list')),
    (SubjectArea, reverse('subject-areas-list')),
    (Subject, reverse('subjects-list'))
]

NESTED_USER_APIS = [
    (InstitutionManager, reverse('institution-managers-list')),
    (Professor, reverse('professors-list')),
    (Candidate, reverse('candidates-list'))
]

EXTRA_DATA = {
    Institution: {
        "category": "Research", "organization": "http://www.in.gr",
        "regulatory_framework": "http://www.in.gr"},
    School: {"institution": ""},
    Department: {"id": 98, "institution": "", "school": "", "dep_number": 20},
    InstitutionManager: {
        "authority_full_name": "John Doe",
        "manager_role": "institutionmanager", "institution": "",
        "authority": "1", "sub_home_phone_number": "", "sub_last_name":
        {"el": "", "en": ""}, "sub_mobile_phone_number": "",
        "sub_father_name": {"el": "", "en": ""},
        "sub_first_name": {"el": "", "en": ""}, "sub_email": ""},
    Professor: {
        "discipline_text": "Mathematics", "rank": "Professor",
        "fek": "http://www.google.com", "speaks_greek": True,
        "discipline_in_fek": True, "cv_url": "http://www.in.gr",
        "institution": "", "is_foreign": False},
    Candidate: {},
    SubjectArea: {},
    Subject: {}
}


class APIMultiLangTest(APITestCase):

    def setUp(self):

        first_name = MultiLangFields.objects.create(
                el='Γιάννης', en='John')
        last_name = MultiLangFields.objects.create(
                el='Γιαννάκης', en='John')
        father_name = MultiLangFields.objects.create(
                el='Πέτρος', en='Peter')
        self.user = ApellaUser.objects.create_user(
                username='test',
                password='test',
                role='helpdeskadmin',
                first_name=first_name,
                last_name=last_name,
                father_name=father_name
        )
        self.user.save()
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.client.force_authenticate(user=self.user, token=token)

        self.data = {
            "title": {
                "el": "ΑΚΑΔΗΜΙΑ ΑΘΗΝΩΝ",
                "en": "ACADEMY OF ATHENS"
            }
        }
        self.update_data = {
            'title': {
                'el': 'New',
                'en': 'Title'
            }
        }

        self.object_urls = {
            'Institution': None,
            'School': None,
            'Department': None,
            'SubjectArea': None,
            'Subject': None,
            'InstitutionManager': None
        }

        self.nested_user_data = {
            "user": {
                "username": "candidate",
                "first_name": {
                    "el": "Μαρία",
                    "en": "Maria"
                },
                "last_name": {
                    "el": "Παπαδοπούλου",
                    "en": "Papadopoulou"
                },
                "home_phone_number": "2104567890",
                "id_passport": "AZ12345",
                "mobile_phone_number": "2102345678",
                "email": "maria@gmail.com",
                "father_name": {
                    "el": "Πέτρος",
                    "en": "Peter"
                },
                "password": "12345"
            }
        }
        self.update_user_data = {
            'user': {
                'first_name': {'en': 'Helen'}
            }
        }

        self.position_data = {
            'description': 'Description',
            'discipline': 'Discipline',
            'title': 'Title',
            'state': 'posted',
            'fek': 'http://www.google.com',
            'fek_posted_at': datetime.now() + timedelta(days=-3),
            'starts_at': datetime.now() + timedelta(days=3),
            'ends_at': datetime.now() + timedelta(days=40)
        }

    def test_multi_lang(self):
        for model, url in MULTI_LANG_APIS:
            self.data.update(EXTRA_DATA[model])
            response = self.client.post(url, self.data, format='json')

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(model.objects.count(), 1)
            model_name = model.__name__

            self.object_urls[model.__name__] = response.data['url']
            EXTRA_DATA[School]['institution'] = self.object_urls['Institution']
            EXTRA_DATA[Department]['institution'] = self.object_urls[
                'Institution']
            EXTRA_DATA[Department]['school'] = self.object_urls['School']
            EXTRA_DATA[Subject]['area'] = self.object_urls['SubjectArea']

            if 'institution' in model._meta.get_all_field_names():
                self.assertEqual(
                    model.objects.get().institution,
                    Institution.objects.get())

            response = self.client.patch(
                response.data['url'], self.update_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            obj = response.data
            self.assertEqual(
                obj['title']['el'], self.update_data['title']['el'])

        EXTRA_DATA[Professor]['institution'] = self.object_urls[
            'Institution']
        EXTRA_DATA[InstitutionManager]['institution'] = \
            self.object_urls['Institution']

        for i, (model, url) in enumerate(NESTED_USER_APIS):
            self.nested_user_data.update(EXTRA_DATA[model])
            username = 'test' + str(i)
            self.nested_user_data['user']['username'] = username
            email = str(i) + self.nested_user_data['user']['email']
            self.nested_user_data['user']['email'] = email

            response = self.client.post(
                url, self.nested_user_data, format='json')

            self.object_urls[model.__name__] = response.data['url']
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(
                model.objects.get().user,
                ApellaUser.objects.get(username=username))

            response = self.client.patch(
                response.data['url'], self.update_user_data, format='json')

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            obj = response.data
            self.assertEqual(
                obj['user']['first_name']['en'],
                self.update_user_data['user']['first_name']['en'])

        # Test assistants
        assistants_url = reverse('assistants-list')
        username = 'test100' + str(i)
        self.nested_user_data['user']['username'] = username
        email = str(i) + '100' + self.nested_user_data['user']['email']
        self.nested_user_data['user']['email'] = email
        self.nested_user_data['can_create_registries'] = True
        self.nested_user_data['can_create_positions'] = False
        self.nested_user_data['manager_role'] = 'assistant'

        manager = InstitutionManager.objects.get()
        manager.user.role = 'institutionmanager'
        manager.save()
        token = Token.objects.create(user=manager.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.client.force_authenticate(user=manager.user, token=token)
        response = self.client.post(
            assistants_url, self.nested_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test positions
        positions_url = reverse('positions-list')
        self.position_data['subject_area'] = self.object_urls['SubjectArea']
        self.position_data['subject'] = self.object_urls['Subject']
        self.position_data['department'] = self.object_urls['Department']

        professor_rank = MultiLangFields.objects.create(
            el='Καθηγητής', en='Professor')
        rank = ProfessorRank.objects.create(rank=professor_rank)
        rank_detail_url = reverse('professor-ranks-detail', args=[rank.id])
        self.position_data['ranks'] = [rank_detail_url]

        response = self.client.post(
            positions_url, self.position_data, format='json')

        position = response.data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(position['state'], 'posted')
        self.assertEqual(
            position['author'], self.object_urls['InstitutionManager'])
        self.assertEqual(
            position['department_dep_number'],
            Department.objects.get().dep_number)
