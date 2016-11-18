# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.core.urlresolvers import reverse
from django.conf import settings
from django.apps import apps

from apella.models import Institution, School, Department, ApellaUser, \
        InstitutionManager, Professor, Candidate, MultiLangFields

import sys
reload(sys)
sys.setdefaultencoding('utf8')


MULTI_LANG_APIS = [
    (Institution, reverse('institution-list')),
    (School, reverse('school-list')),
    (Department, reverse('department-list'))
]

NESTED_USER_APIS = [
    (InstitutionManager, reverse('institutionmanager-list')),
    (Professor, reverse('professor-list')),
    (Candidate, reverse('candidate-list'))
]

EXTRA_DATA = {
    Institution: {"category": "Research"},
    School: {"institution": ""},
    Department: {"id": 98, "institution": "", "school": ""},
    InstitutionManager: {
        "authority_full_name": "John Doe",
        "manager_role": "1", "institution": "", "authority": "1"},
    Professor: {
        "discipline_text": "Mathematics", "rank": "Professor",
        "fek": "http://www.google.com"},
    Candidate: {}
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
            'Department': None
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

        for i, (model, url) in enumerate(NESTED_USER_APIS):

            EXTRA_DATA[InstitutionManager]['institution'] = \
                    self.object_urls['Institution']
            self.nested_user_data.update(EXTRA_DATA[model])
            username = 'test' + str(i)
            self.nested_user_data['user']['username'] = username

            response = self.client.post(
                url, self.nested_user_data, format='json')

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
