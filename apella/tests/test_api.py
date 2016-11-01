# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse
from django.conf import settings
from django.apps import apps

from apella.models import Institution, InstitutionEl, InstitutionEn,\
    School, SchoolEn, SchoolEl, Department, DepartmentEl, DepartmentEn

import sys
reload(sys)
sys.setdefaultencoding('utf8')


MULTI_LANG_APIS = [
    (Institution, reverse('institution-list')),
    (School, reverse('school-list')),
    (Department, reverse('department-list'))
]

EXTRA_DATA = {
    Institution: {"category": "Research"},
    School: {"institution": ""},
    Department: {"id": 98, "institution": "", "school": ""}
}


class APIMultiLangTest(APITestCase):

    def setUp(self):
        self.data = {
            "title": {
                "el": "ΑΚΑΔΗΜΙΑ ΑΘΗΝΩΝ",
                "en": "ACADEMY OF ATHENS"
            }
        }
        self.institution_url = None
        self.school_url = None

    def test_create_multi_lang(self):

        for model, url in MULTI_LANG_APIS:
            self.data.update(EXTRA_DATA[model])
            response = self.client.post(url, self.data, format='json')

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(model.objects.count(), 1)
            model_name = model.__name__
            for lang in settings.LANGUAGES:
                model_name_lang = model_name + lang.capitalize()
                model_lang = apps.get_model(
                    app_label='apella', model_name=model_name_lang)
                self.assertEqual(model_lang.objects.count(), 1)

            if model == Institution:
                self.institution_url = response.data['url']
                EXTRA_DATA[School]['institution'] = self.institution_url
            elif model == School:
                self.school_url = response.data['url']
                EXTRA_DATA[Department]['institution'] = self.institution_url
                EXTRA_DATA[Department]['school'] = self.school_url
                self.assertEqual(
                    School.objects.get().institution,
                    Institution.objects.get())
            else:
                self.assertEqual(
                    Department.objects.get().institution,
                    Institution.objects.get())
