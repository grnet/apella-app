#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import logging
import xlsxwriter
import StringIO
from datetime import datetime, date, time
from time import strftime, gmtime

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import detail_route, list_route
from rest_framework.serializers import ValidationError
from rest_framework.exceptions import PermissionDenied

from django.db.models import ProtectedError, Min, Q, Max
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404, \
    StreamingHttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.servers.basehttp import FileWrapper

from apimas.drf.mixins import HookMixin

from apella.models import InstitutionManager, Position, Department, \
    Candidacy, ApellaFile, ElectorParticipation, Candidate, \
    Professor as ProfessorModel, UserApplication, ApellaUser, \
    Registry
from apella.loader import adapter
from apella.common import FILE_KIND_TO_FIELD, RANKS_EL, POSITION_STATES_EL
from apella import auth_hooks
from apella.serializers.position import link_files, \
    upgrade_candidate_to_professor, upgrade_candidates_to_professors
from apella.emails import send_user_email, send_emails_file, \
    send_emails_members_change, send_disable_professor_emails, \
    send_release_shibboleth_email
from apella.util import urljoin, safe_path_join, otz, move_to_timezone, \
    write_row
from apella.serials import get_serial
from apella.helpers import position_is_latest
from apella.validators import validate_candidate_files


logger = logging.getLogger(__name__)


class DestroyProtectedObject(viewsets.ModelViewSet):
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProtectedError:
            return Response(status=status.HTTP_403_FORBIDDEN)


class Professor(object):
    @list_route()
    def report(self, request, pk=None):
        response = HttpResponse(content_type='application/ms-excel')
        filename = "professors_export_" + \
            strftime("%Y_%m_%d", gmtime()) + ".xlsx"
        response['Content-Disposition'] = 'attachment; filename=' + filename

        output = StringIO.StringIO()
        wb = xlsxwriter.Workbook(
            output, {'constant_memory': True})
        ws = wb.add_worksheet('Professors')

        user = request.user
        if user.is_manager() or user.is_ministry():
            report_type = '1'
        elif user.is_helpdeskadmin():
            report_type = '2'
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


        if report_type == '1':
            fields = ['Κωδικός Χρήστη', 'Όνομα', 'Επώνυμο',
                'Ίδρυμα', 'Σχολή', 'Τμήμα', 'Βαθμίδα', 'Γνωστικό Αντικείμενο',
                'Κατηγορία Χρήστη']
        elif report_type == '2':
            fields = ['Κωδικός Χρήστη', 'Παλιός Κωδικός Χρήστη', 'Όνομα (el)',
                'Επώνυμο (el)', 'Πατρώνυμο (el)', 'Όνομα (en)', 'Επώνυμο (en)',
                'Πατρώνυμο (en)', 'Email', 'Κινητό Τηλέφωνο',
                'Σταθερό Τηλέφωνο', 'Αρ. Ταυτότητας',
                'Ημ/νία Δημιουργίας Λογαριασμού', 'login',
                'Ενεργός', 'Ενεργοποιήθηκε στις', 'Ενεργοποίηση Email',
                'Ενεργοποίηση Email στις',
                'Κατάσταση Προφίλ',
                'Ημ/νία Τελευταίας Αλλαγής Κατάστασης Προφίλ',
                'Κατηγορία Χρήστη', 'Ίδρυμα', 'Κωδικός Ιδρύματος',
                'Τμήμα', 'Κωδικός Τμήματος', 'Βαθμίδα',
                'Υπάρχει URL Βιογραφικού', 'URL Βιογραφικού',
                'Γνωστικό Αντικείμενο', 'Υπάρχει Γνωστικό Αντικείμενο στο ΦΕΚ',
                'ΦΕΚ Διορισμού', 'Ομιλεί Ελληνικά',
                'Έχει αποδεχτεί τους όρους συμμετοχής',
                'Συμμετοχές']

        k = 0
        for field in fields:
            ws.write(0, k, field.decode('utf-8'))
            k += 1

        queryset = self.get_queryset().select_related(
                'user__first_name__el', 'user__last_name__el',
                'user__father_name__el', 'user', 'institution',
                'institution__title__el', 'department__title__el',
                'department', 'department__school__title__el')

        if report_type == '1':
            queryset = queryset.filter(is_verified=True)

        i = 1
        for p in queryset:
            institution_id = '-'
            try:
                institution = p.institution.title.el
                institution_id = p.institution.id
            except AttributeError:
                institution = p.institution_freetext

            department_id = '-'
            try:
                department = p.department.title.el
                department_id = p.department.id
            except AttributeError:
                department = ''

            try:
                school = p.department.school.title.el
            except AttributeError:
                school = ''

            category = ''
            if p.is_professor and not p.is_foreign:
                category = 'Καθηγητής Ημεδαπής'
            elif p.is_professor and p.is_foreign:
                category = 'Καθηγητής Αλλοδαπής'
            elif not p.is_professor and not p.is_foreign:
                category = 'Ερευνητής Ημεδαπής'
            else:
                category = 'Ερευνητής Αλλοδαπής'

            rank_el = ""
            if p.rank:
                rank_el = RANKS_EL.get(p.rank)

            if report_type == '1':
                row = [
                    p.user.id,
                    p.user.first_name.el,
                    p.user.last_name.el,
                    institution,
                    school,
                    department,
                    rank_el and rank_el.decode('utf-8'),
                    p.discipline_text,
                    category.decode('utf-8')
                ]
            elif report_type == '2':
                profile_state = ''
                profile_last_changed_at = '-'
                if p.is_verified:
                    profile_state = 'Πιστοποιημένος'
                    profile_last_changed_at = \
                        move_to_timezone(p.verified_at, otz)
                elif p.is_rejected:
                    profile_state = 'Απορριφθείς'
                elif p.verification_pending:
                    profile_state = 'Αναμονή Πιστοποίησης'
                    profile_last_changed_at = \
                        move_to_timezone(p.verification_request, otz)
                elif not p.verification_pending and not p.is_rejected \
                        and not p.is_verified and p.changes_request:
                    profile_state = 'Ζητήθηκαν αλλαγές'
                    profile_last_changed_at = \
                        move_to_timezone(p.changes_request, otz)

                row = [
                    p.user.id,
                    p.user.old_user_id,
                    p.user.first_name.el,
                    p.user.last_name.el,
                    p.user.father_name.el,
                    p.user.first_name.en,
                    p.user.last_name.en,
                    p.user.father_name.en,
                    p.user.email,
                    p.user.mobile_phone_number,
                    p.user.home_phone_number,
                    p.user.id_passport,
                    str(move_to_timezone(p.user.date_joined, otz)),
                    p.user.login_method,
                    p.user.is_active,
                    str(move_to_timezone(p.user.activated_at, otz)),
                    p.user.email_verified,
                    str(move_to_timezone(p.user.email_verified_at, otz)),
                    profile_state.decode('utf-8'),
                    str(profile_last_changed_at),
                    'Καθηγητής Αλλοδαπής'.decode('utf-8') \
                        if p.is_foreign \
                        else 'Καθηγητής Ημεδαπής'.decode('utf-8'),
                    institution,
                    institution_id,
                    department,
                    department_id,
                    rank_el and rank_el.decode('utf-8'),
                    'ΝΑΙ'.decode('utf-8') \
                        if p.cv_url else 'ΟΧΙ'.decode('utf-8'),
                    p.cv_url,
                    p.discipline_text,
                    'ΝΑΙ'.decode('utf-8') \
                        if p.discipline_in_fek else 'ΟΧΙ'.decode('utf-8'),
                    p.fek,
                    'ΝΑΙ'.decode('utf-8') \
                        if p.speaks_greek else 'ΟΧΙ'.decode('utf-8'),
                    'ΝΑΙ'.decode('utf-8') \
                        if p.user.has_accepted_terms \
                        else 'ΟΧΙ'.decode('utf-8'),
                    #p.active_elections
                ]
            write_row(ws, row, i)
            i += 1

        wb.close()
        xlsx_data = output.getvalue()
        response.write(xlsx_data)
        return response

    def get_queryset(self):
        queryset = self.queryset
        leave_query = self.request.GET.get('on_leave')
        if leave_query:
            now = datetime.utcnow()
            queryset = queryset.filter(Q(leave_starts_at__lte=now) &
                                       Q(leave_ends_at__gt=now))
        if 'ordering' not in self.request.query_params:
            queryset = self.queryset.order_by('user__last_name__el')
        create_registry = self.request.query_params.get(
            'create_registry', None)
        if create_registry:
            queryset = queryset.exclude(rank='Lecturer'). \
                exclude(rank='Tenured Assistant Professor'). \
                exclude(is_disabled=True)
            registry_id = self.request.query_params.get(
                'registry_id', None)
            if registry_id:
                try:
                    registry = Registry.objects.get(id=registry_id)
                    queryset = queryset.exclude(
                        registrymembership__registry=registry)
                    other_type = 'internal' if registry.type == 'external' \
                        else 'external'
                    other_registry = Registry.objects.get(
                        department=registry.department,
                        type=other_type)
                    queryset = queryset.exclude(
                        registrymembership__registry=other_registry)
                except Registry.DoesNotExist:
                    pass
        return queryset

    def set_professor_is_disabled(self, is_disabled, request):
        professor = self.get_object()
        if professor.is_disabled is is_disabled:
            return
        professor.is_disabled = is_disabled
        if is_disabled:
            professor.disabled_at = datetime.utcnow()
            professor.disabled_by_helpdesk = request.user.is_helpdesk()
        professor.save()
        logger.info(
            'user %s %s professor %r' %
            (request.user.username,
            'disabled' if is_disabled else 'enabled',
            professor.id))
        if is_disabled:
            send_disable_professor_emails(professor, is_disabled)

    @detail_route(methods=['post'])
    def disable_professor(self, request, pk=None):
        professor = self.get_object()
        try:
            self.set_professor_is_disabled(True, request)
        except ValidationError as ve:
            return Response(ve.detail, status=status.HTTP_400_BAD_REQUEST)
        return Response(request.data, status=status.HTTP_200_OK)

    @detail_route(methods=['post'])
    def enable_professor(self, request, pk=None):
        professor = self.get_object()
        try:
            self.set_professor_is_disabled(False, request)
        except ValidationError as ve:
            return Response(ve.detail, status=status.HTTP_400_BAD_REQUEST)
        return Response(request.data, status=status.HTTP_200_OK)


class AssistantList(generics.ListAPIView):
    def get_queryset(self):
        user = self.request.user
        if user.is_manager():
            institution_id = user.institutionmanager.institution_id
            return InstitutionManager.objects.filter(
                manager_role='assistant',
                institution__id=institution_id)
        else:
            return InstitutionManager.objects.filter(
                manager_role='assistant')

elector_sets = {
    'electors_regular_internal': True,
    'electors_regular_external': True,
    'electors_sub_internal': False,
    'electors_sub_external': False
}

committee_sets = ['committee_internal', 'committee_external']


class PositionHookMixin(HookMixin):
    def preprocess_update(self):
        obj = self.unstash()
        position = obj.instance

        curr_position = Position.objects.get(id=position.id)
        if position.state == 'electing' and curr_position.state != 'revoked':
            eps = ElectorParticipation.objects.filter(position=position)
            old_participations = [old_el_pa for old_el_pa in eps.all()]
            eps.all().delete()

            new_participations = []
            for elector_set_key, is_regular in elector_sets.items():
                if elector_set_key in obj.validated_data:
                    for elector in obj.validated_data[elector_set_key]:
                        ep = ElectorParticipation.objects.create(
                            professor=elector,
                            position=position,
                            is_regular=is_regular,
                            is_internal=elector_set_key.endswith('internal'))
                        new_participations.append(ep)

            send_emails_members_change(
                position, 'electors', {'e': old_participations},
                {'e': new_participations})

            c = {'committee': []}
            for com_set in committee_sets:
                if obj.validated_data and com_set in obj.validated_data:
                    committee = obj.validated_data[com_set]
                    if committee:
                        for professor in committee:
                            c['committee'].append(professor)
            self.stash(extra=c)

class PositionMixin(object):
    @list_route()
    def report(self, request, pk=None):
        response = HttpResponse(content_type='application/ms-excel')
        filename = "positions_export_" + \
            strftime("%Y_%m_%d", gmtime()) + ".xlsx"
        response['Content-Disposition'] = 'attachment; filename=' + filename

        output = StringIO.StringIO()
        wb = xlsxwriter.Workbook(
            output, {'constant_memory': True})
        ws = wb.add_worksheet('Positions')

        fields = ['Κωδικός Θέσης', 'Παλιός Κωδικός Θέσης',
            'Τίτλος Θέσης', 'Ίδρυμα', 'Σχολή', 'Τμήμα', 'Βαθμίδα',
            'Περιγραφή', 'Γνωστικό Αντικείμενο', 'Θεματική Περιοχή',
            'Θέμα', 'Σχετιζόμενες Θέσεις', 'Φ.Ε.Κ.', 'Ημ/νία Φ.Ε.Κ.',
            'Κατάσταση Θέσης', 'Ημ/νία Έναρξης Υποβολών',
            'Ημ/νία Λήξης Υποβολών',
            'Ημ/νία Σύγκλησης του Εκλεκτορικού Σώματος για τον ορισμό της Εισηγητικής Επιτροπής',
            'Ημ/νία Σύγκλησης του Εκλεκτορικού Σώματος για Επιλογή',
            'Εκλεγείς', 'Δεύτερος Καταλληλότερος Υποψήφιος',
            'Φ.Ε.Κ. Διορισμού']

        k = 0
        for field in fields:
            ws.write(0, k, field.decode('utf-8'))
            k += 1

        i = 1
        queryset = self.get_queryset().select_related(
            'elected__first_name__el', 'elected__last_name__el',
            'second_best__first_name__el', 'second_best__last_name__el',
            'department__title__el', 'department__school__title__el',
            'department__institution__title__el', 'subject__title__el',
            'subject_area__title__el')

        for p in queryset:
            elected_full_name = ''
            if p.elected:
                elected_full_name = \
                    p.elected.first_name.el + ' ' + \
                    p.elected.last_name.el

            second_best_full_name = ''
            if p.second_best:
                second_best_full_name = \
                    p.second_best.first_name.el + ' ' + \
                    p.second_best.last_name.el

            rank_el = ""
            if p.rank:
                rank_el = RANKS_EL.get(p.rank)

            if p.state == 'posted' and p.starts_at \
                    and p.starts_at > datetime.utcnow():
                p_state = 'Ενταγμένη'
            elif p.state == 'posted' and p.ends_at \
                    and p.ends_at < datetime.utcnow():
                p_state = 'Κλειστή'
            elif p.state == 'posted':
                p_state = 'Ανοιχτή'
            else:
                p_state = POSITION_STATES_EL.get(p.state)

            p_related = ""
            if p.related_positions.count() > 0:
                p_related = ','.join(str(rp.code) for rp in
                        p.related_positions.all())

            row = [
                p.code,
                p.old_code,
                p.title,
                p.department.institution.title.el,
                p.department.school and p.department.school.title.el,
                p.department.title.el,
                rank_el and rank_el.decode('utf-8'),
                p.description,
                p.discipline,
                p.subject_area.title.el,
                p.subject.title.el,
                p_related,
                p.fek,
                p.fek_posted_at,
                p_state and p_state.decode('utf-8'),
                p.starts_at and str(move_to_timezone(p.starts_at, otz).date()),
                p.ends_at and str(move_to_timezone(p.ends_at, otz).date()),
                p.electors_meeting_to_set_committee_date,
                p.electors_meeting_date,
                elected_full_name,
                second_best_full_name,
                p.nomination_act_fek
            ]
            write_row(ws, row, i)
            i += 1

        wb.close()
        xlsx_data = output.getvalue()
        response.write(xlsx_data)
        return response

    @detail_route()
    def history(self, request, pk=None):
        position = self.get_object()
        position_states = Position.objects.filter(code=position.code). \
            order_by('-updated_at')
        serializer = self.get_serializer(position_states, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        now = datetime.utcnow()
        queryset = self.queryset
        user = self.request.user

        if 'pk' in self.kwargs:
            queryset = queryset.filter(id=self.kwargs['pk'])
        else:
            ids = queryset.values('code').annotate(Min('id')). \
                values('id__min')
            queryset = queryset.filter(id__in=ids)

        if user.is_authenticated():
            if user.is_institutionmanager():
                queryset = queryset.filter(
                    department__in=user.institutionmanager.
                    institution.department_set.all())
            elif user.is_assistant():
                queryset = queryset.filter(
                    department__in=user.institutionmanager.
                    departments.all())
            elif user.is_professor():
                position_codes = list(Candidacy.objects.filter(
                    candidate=user).values_list('position__code', flat=True))
                if user.professor.department:
                    department_position_codes = list(Position.objects.filter(
                        department=user.professor.department).
                        values_list('code', flat=True))
                    position_codes += department_position_codes

                position_codes += list(
                    user.userapplication_set.values_list(
                    'position__code', flat=True))
                queryset = queryset.filter(
                    Q(state='posted', ends_at__gte=now) |
                    Q(code__in=position_codes) |
                    Q(committee=user.professor.id) |
                    Q(electors=user.professor.id))
            elif user.is_candidate():
                position_codes = Candidacy.objects.filter(
                    candidate=user).values_list('position__code', flat=True)
                queryset = queryset.filter(
                    Q(state='posted', ends_at__gte=now) |
                    Q(code__in=position_codes))

            state_query = self.request.GET.get('state_expanded')
            if state_query:
                now = datetime.utcnow()
                if state_query in ('electing', 'successful',
                                   'failed', 'cancelled', 'revoked'):
                    queryset = queryset.filter(Q(state=state_query))

                elif state_query == 'posted':
                    queryset = queryset.filter(Q(state='posted') &
                                               Q(starts_at__gte=now))

                elif state_query == 'open':
                    queryset = queryset.filter(Q(state='posted') &
                                               Q(starts_at__lte=now) &
                                               Q(ends_at__gt=now))
                elif state_query == 'closed':
                    queryset = queryset.filter(Q(state='posted') &
                                               Q(ends_at__lte=now))

                elif state_query == 'before_closed':
                    queryset = queryset.filter(
                        (Q(state='posted') &
                        Q(ends_at__gt=now)) |
                        Q(ends_at=None))

            queryset = queryset.distinct()
        return queryset

    def update(self, request, *args, **kwargs):
        position = self.get_object()
        code = position.code
        if code.split(settings.POSITION_CODE_PREFIX)[1] != \
                str(position.id):
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super(PositionMixin, self).update(request, *args, **kwargs)


class CandidacyList(object):

    @detail_route()
    def history(self, request, pk=None):
        candidacy = self.get_object()
        candidacy_states = Candidacy.objects.filter(code=candidacy.code)
        serializer = self.get_serializer(candidacy_states, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        if user.is_institutionmanager():
            institution_ids = InstitutionManager.objects.filter(user=user). \
                values_list('institution', flat=True)
            departments = Department.objects.filter(
                institution_id__in=institution_ids)
            positions = Position.objects.filter(department__in=departments)
            queryset = queryset.filter(position__in=positions)
        elif user.is_assistant():
            departments = user.institutionmanager.departments.all()
            positions = Position.objects.filter(department__in=departments)
            queryset = queryset.filter(position__in=positions)
        if 'pk' in self.kwargs:
            queryset = queryset.filter(id=self.kwargs['pk'])
        else:
            ids = queryset.values('code').annotate(Min('id')). \
                values_list('id__min', flat=True)
            queryset = queryset.filter(id__in=ids)
            if 'latest' in self.request.query_params:
                q2 = queryset.values('candidate', 'position'). \
                    annotate(Max('id')).values_list('id__max', flat=True)
                queryset = queryset.filter(id__in=q2)
        if not user.is_helpdesk():
            queryset = queryset.exclude(state='draft')

        queryset = queryset.distinct()
        return queryset

    def update(self, request, pk=None):
        candidacy = self.get_object()
        code = candidacy.code
        if code != str(candidacy.id):
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super(CandidacyList, self).update(request, pk=None)

    @list_route(methods=['POST'])
    def upgrade_role(self, request, pk=None):

        file_upload = request.FILES.get('file_upload', None)
        if not file_upload:
            return Response('no.csv.file', status=status.HTTP_400_BAD_REQUEST)

        owner = request.user
        try:
            errors, success = \
                upgrade_candidates_to_professors(file_upload, owner)
        except ValidationError as ve:
            return Response(
                {'errors': ve.detail}, status=status.HTTP_400_BAD_REQUEST)

        if not errors:
            return Response(
                {'success': success}, status=status.HTTP_200_OK)
        else:
            return Response(
                {'errors': errors, 'success': success},
                    status=status.HTTP_409_CONFLICT)


class RegistriesList(viewsets.GenericViewSet):
    @list_route()
    def report(self, request, pk=None):
        response = HttpResponse(content_type='application/ms-excel')
        filename = "registries_export_" + \
            strftime("%Y_%m_%d", gmtime()) + ".xlsx"
        response['Content-Disposition'] = 'attachment; filename=' + filename

        output = StringIO.StringIO()
        wb = xlsxwriter.Workbook(
            output, {'constant_memory': True})
        ws = wb.add_worksheet('Registries')

        fields = ['Κωδικός Χρήστη', 'Όνομα', 'Επώνυμο', 'Κατηγορία Χρήστη',
            'Ίδρυμα Χρήστη', 'Τμήμα Χρήστη', 'Κωδικός Μητρώου',
            'Ίδρυμα Μητρώου', 'Τμήμα Μητρώου', 'Είδος Μητρώου']

        k = 0
        for field in fields:
            ws.write(0, k, field.decode('utf-8'))
            k += 1

        i = 1
        queryset = self.get_queryset()
        for r in queryset:
            members = r.members.select_related(
                'institution__title__el', 'department__title__el',
                'user__first_name__el', 'user__last_name__el',
                'institution', 'department').all()
            for p in members:
                try:
                    institution = p.institution.title.el
                except AttributeError:
                    institution = p.institution_freetext

                try:
                    department = p.department.title.el
                except AttributeError:
                    department = ''

                row = [
                    p.user.id,
                    p.user.first_name.el,
                    p.user.last_name.el,
                    'Αλλοδαπής'.decode('utf-8') \
                        if p.is_foreign else 'Ημεδαπής'.decode('utf-8'),
                    institution,
                    department,
                    r.id,
                    r.department.institution.title.el,
                    r.department.title.el,
                    'Εσωτερικό'.decode('utf-8') \
                        if r.type == 'internal' \
                        else 'Εξωτερικό'.decode('utf-8')
                ]
                write_row(ws, row, i)
                i += 1

        wb.close()
        xlsx_data = output.getvalue()
        response.write(xlsx_data)
        return response

    def get_queryset(self):
        queryset = self.queryset
        if 'ordering' not in self.request.query_params:
            queryset = queryset.order_by('department')
        else:
            ordering = self.request.query_params['ordering']
            queryset = queryset.order_by(ordering)
        return queryset

    @detail_route()
    def members(self, request, pk=None):
        registry = self.get_object()
        query_params = self.request.query_params
        members = registry.members
        if 'user_id' in query_params:
            try:
                user_id = int(query_params['user_id'])
            except ValueError:
                user_id = 0
            members = members.filter(user_id=user_id)
        if 'institution' in query_params:
            members = members.filter(institution=query_params['institution'])
        if 'members_department' in query_params:
            members = members.filter(
                department=query_params['members_department'])
        if 'rank' in query_params:
            members = members.filter(rank=query_params['rank'])
        if 'is_disabled' in query_params:
            members = members.filter(
                is_disabled=query_params['is_disabled'] == 'True')
        if 'search' in query_params:
            search = query_params['search']
            members = members.filter(
                Q(user__last_name__en__icontains=search) |
                Q(user__first_name__en__icontains=search) |
                Q(user__last_name__el__icontains=search) |
                Q(user__first_name__el__icontains=search) |
                Q(user__email__icontains=search) |
                Q(user__old_user_id__icontains=search) |
                Q(user__id__icontains=search) |
                Q(discipline_text__icontains=search))
        if 'ordering' not in query_params:
            ordering = 'user__last_name__el'
        else:
            ordering = query_params['ordering']
        members = members.order_by(ordering)

        ser = adapter.get_serializer(settings.API_ENDPOINT, 'professors')
        page = self.paginate_queryset(members)
        if page is not None:
            return self.get_paginated_response(
                ser(page, many=True, context={'request': request}).data)
        return Response(
            ser(members, many=True, context={'request': request}).data)


USE_X_SEND_FILE = getattr(settings, 'USE_X_SEND_FILE', False)


class FilesViewSet(viewsets.ModelViewSet):

    @detail_route(methods=['head'], url_path='download')
    def download_head(self, request, pk=None):
        response = HttpResponse(content_type='application/force-download')
        assert request.method == 'HEAD'
        user = request.user
        file = self.get_object()
        token = auth_hooks.generate_file_token(user, file)
        url = urljoin(settings.BASE_URL or '/',
                      reverse('api_apella-files-downloadfile', args=(pk,)))
        response['X-File-Location'] = "%s?token=%s" % (url, token)
        return response

    @detail_route(methods=['get'], url_path='downloadfile')
    def download_get(self, request, pk=None):
        token = request.GET.get('token', None)
        if token is None:
            raise PermissionDenied("no.token")
            # url = reverse('apella-files-download', args=(pk,))
            # ui_url = getattr(settings, 'DOWNLOAD_FILE_URL', '')
            # ui_download_url = '%s?#download=%s' % (ui_url, url)
            # return HttpResponseRedirect(ui_download_url)

        file_id = auth_hooks.consume_file_token(token)
        if not file_id == int(pk):
            raise Http404

        file = get_object_or_404(ApellaFile, id=file_id)
        filename = file.file_name
        if isinstance(filename, unicode):
            filename = filename.encode('utf-8')
        filename = filename.replace('"', '')
        disp = 'attachment; filename="%s"' % filename
        if USE_X_SEND_FILE:
            response['X-Sendfile'] = file.file_content.path
        else:
            chunk_size = 8192
            response = StreamingHttpResponse(
                           FileWrapper(
                               open(file.file_content.path, 'rb'), chunk_size),
                                  content_type="application/force-download")
        response['Content-Disposition'] = disp
        return response

    def destroy(self, request, pk=None):
        obj = self.get_object()
        try:
            f = safe_path_join(settings.MEDIA_ROOT, obj.file_content.name)
            os.remove(f)
            logger.info(
                'user %s removed file: %s, path: %s source: %s, source_id: %s' %
                (request.user.username,
                obj.file_name,
                obj.file_content.path,
                obj.source,
                obj.source_id,))
        except OSError:
            pass
        return super(FilesViewSet, self).destroy(request, pk)


class UploadFilesViewSet(viewsets.ModelViewSet):

    FILE_SOURCE = {
        "Professor": "profile",
        "Candidate": "profile",
        "Candidacy": "candidacy",
        "Position": "position",
        "Registry": "registry"
    }

    @detail_route(methods=['post'])
    def upload(self, request, pk=None):
        obj = self.get_object()
        if 'file_upload' not in request.FILES:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        file_upload = request.FILES.get('file_upload', None)
        file_kind = request.data.get('file_kind', None)
        file_description = request.data.get('file_description', None)

        if file_kind not in FILE_KIND_TO_FIELD:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if not file_upload:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        field_name, many = FILE_KIND_TO_FIELD[file_kind].values()
        if field_name not in obj._meta.get_all_field_names():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        owner = request.user
        if request.user.is_helpdesk():
            if isinstance(obj, ProfessorModel) or isinstance(obj, Candidate):
                owner = obj.user
            elif isinstance(obj, Candidacy):
                owner = obj.candidate
            elif isinstance(obj, Position):
                owner = obj.author.user

        uploaded_file = ApellaFile.objects.create(
                id=get_serial('apella_file'),
                owner=owner,
                file_kind=file_kind,
                source=self.FILE_SOURCE[obj.__class__.__name__],
                source_id=obj.id,
                file_content=file_upload,
                file_name=file_upload.name,
                description=file_description,
                updated_at=datetime.utcnow())

        if not many:
            setattr(obj, field_name, uploaded_file)
        else:
            many_attr = getattr(obj, field_name)
            many_attr.add(uploaded_file)
        if isinstance(obj, Candidacy):
            obj.updated_at = datetime.utcnow()
        obj.save()
        send_emails_file(obj, file_kind)

        return Response(status=status.HTTP_200_OK)


class SyncCandidacies(object):
    @detail_route(methods=['post'])
    def sync_candidacies(self, request, pk=None):
        now = datetime.utcnow()
        candidate_user = self.get_object()
        try:
            validate_candidate_files(candidate_user.user)
        except DjangoValidationError as ve:
            return Response(ve.message, status=status.HTTP_400_BAD_REQUEST)

        active_candidacies = Candidacy.objects.filter(
            candidate=candidate_user.user,
            state='posted',
            position__state='posted',
            position__ends_at__gt=now)
        for candidacy in active_candidacies:
            link_files(candidacy, candidate_user.user)
            candidacy.updated_at = now
            candidacy.save()
        return Response(request.data, status=status.HTTP_200_OK)


class CandidateProfile(object):
    @detail_route(methods=['post'])
    def request_verification(self, request, pk=None):
        candidate_user = self.get_object()
        try:
            auth_hooks.request_user_verify(candidate_user)
            candidate_user.save()
        except ValidationError as ve:
            return Response(ve.detail, status=status.HTTP_400_BAD_REQUEST)
        return Response(request.data, status=status.HTTP_200_OK)

    @detail_route(methods=['post'])
    def request_changes(self, request, pk=None):
        candidate_user = self.get_object()
        try:
            auth_hooks.request_user_changes(candidate_user)
            candidate_user.save()
            send_user_email(
                candidate_user.user,
                'apella/emails/user_profile_request_changes_subject.txt',
                'apella/emails/user_profile_request_changes_body.txt')
        except ValidationError as ve:
            return Response(ve.detail, status=status.HTTP_400_BAD_REQUEST)
        return Response(request.data, status=status.HTTP_200_OK)

    @detail_route(methods=['post'])
    def verify_user(self, request, pk=None):
        candidate_user = self.get_object()
        try:
            auth_hooks.verify_user(candidate_user)
            if isinstance(candidate_user, ProfessorModel) and not\
                candidate_user.user.shibboleth_id and \
                candidate_user.institution and \
                candidate_user.institution.has_shibboleth:
                    candidate_user.user.can_set_academic = True
                    candidate_user.user.save()
            candidate_user.save()
            logger.info(
                'user %s verified profile %r' %
                (request.user.username, candidate_user.id))
            send_user_email(
                candidate_user.user,
                'apella/emails/user_verified_profile_subject.txt',
                'apella/emails/user_verified_profile_body.txt')
        except ValidationError as ve:
            return Response(ve.detail, status=status.HTTP_400_BAD_REQUEST)
        return Response(request.data, status=status.HTTP_200_OK)

    @detail_route(methods=['post'])
    def reject_user(self, request, pk=None):
        candidate_user = self.get_object()
        try:
            reason = None
            if 'rejected_reason' in request.data:
                reason = request.data['rejected_reason']
            auth_hooks.reject_user(candidate_user, reason=reason)
            candidate_user.save()
            logger.info(
                'user %s rejected profile %r' %
                (request.user.username, candidate_user.id))
            send_user_email(
                candidate_user.user,
                'apella/emails/user_rejected_profile_subject.txt',
                'apella/emails/user_rejected_profile_body.txt')
        except ValidationError as ve:
            return Response(ve.detail, status=status.HTTP_400_BAD_REQUEST)
        return Response(request.data, status=status.HTTP_200_OK)

    @detail_route(methods=['post'])
    def upgrade_to_professor(self, request, pk=None):
        candidate_user = self.get_object()
        if not candidate_user.is_candidate():
            return Response(
                'not.a.candidate', status=status.HTTP_400_BAD_REQUEST)

        department = request.data.get('department', None)
        rank = request.data.get('rank', None)
        fek = request.data.get('fek', None)
        discipline_text = request.data.get('discipline_text', None)
        discipline_in_fek = request.data.get('discipline_in_fek', None)

        try:
            upgrade_candidate_to_professor(
                candidate_user.user,
                department=department,
                rank=rank,
                fek=fek,
                discipline_text=discipline_text,
                discipline_in_fek=discipline_in_fek)
        except ValidationError as ve:
            return Response(ve.detail, status=status.HTTP_400_BAD_REQUEST)
        return Response(request.data, status=status.HTTP_200_OK)


class PositionsPortal(object):
    def get_queryset(self):
        now = datetime.utcnow()
        queryset = self.queryset
        ids = queryset.values('code').annotate(Min('id')). \
            values('id__min')
        queryset = queryset.filter(id__in=ids)
        return queryset.filter(state='posted', ends_at__gte=now)


class UserApplicationMixin(object):
    def _can_accept_application(self):
        application = self.get_object()
        apps = UserApplication.objects.filter(
                user=application.user,
                app_type=application.app_type,
                state='approved')
        if not apps:
            return True
        for app in apps:
            positions = app.position_set.all()
            for p in positions:
                if p.state != 'cancelled' and position_is_latest(p):
                    return False
        return True

    @detail_route(methods=['post'])
    def accept_application(self, request, pk=None):
        application = self.get_object()
        if not self._can_accept_application():
            return Response(
                'cannot.accept.application', status=status.HTTP_400_BAD_REQUEST)
        try:
            application.state = 'approved'
            application.updated_at = datetime.utcnow()
            application.save()
        except ValidationError as ve:
            return Response(ve.detail, status=status.HTTP_400_BAD_REQUEST)
        send_user_email(
            application.user,
            'apella/emails/user_application_accepted_subject.txt',
            'apella/emails/user_application_accepted_body.txt',
            {'application': application})
        return Response(request.data, status=status.HTTP_200_OK)

    @detail_route(methods=['post'])
    def reject_application(self, request, pk=None):
        application = self.get_object()
        try:
            application.state = 'rejected'
            application.updated_at = datetime.utcnow()
            application.save()
        except ValidationError as ve:
            return Response(ve.detail, status=status.HTTP_400_BAD_REQUEST)
        send_user_email(
            application.user,
            'apella/emails/user_application_accepted_subject.txt',
            'apella/emails/user_application_rejected_body.txt',
            {'application': application})
        return Response(request.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        if user.is_institutionmanager():
            departments = Department.objects.filter(
                institution=user.institutionmanager.institution)
            queryset = queryset.filter(
                Q(department__in=departments) |
                Q(receiving_department__in=departments))
        elif user.is_assistant():
            departments = user.institutionmanager.departments.all()
            queryset = queryset.filter(
                Q(department__in=departments) |
                Q(receiving_department__in=departments))
        elif user.is_professor():
            ua_ids = Position.objects.filter(
                Q(electors=user.professor) | Q(committee=user.professor)). \
                    values_list('user_application', flat=True)
            ua_ids = [ua_id for ua_id in ua_ids if ua_id]

            if user.professor.department:
                queryset = queryset.filter(
                    Q(user=user) |
                    Q(department=user.professor.department) |
                    Q(receiving_department=user.professor.department) |
                    Q(id__in=ua_ids))
            else:
                queryset = queryset.filter(Q(user=user) | Q(id__in=ua_ids))

        queryset = queryset.order_by('-id')
        return queryset


class ApellaUsers(object):
    @detail_route(methods=['post'])
    def accept_terms(self, request, pk=None):
        user = self.get_object()
        user.accepted_terms_at = datetime.utcnow()
        user.has_accepted_terms = True
        user.save()
        return Response(request.data, status=status.HTTP_200_OK)

    @detail_route(methods=['post'])
    def release_shibboleth(self, request, pk=None):
        user = self.get_object()
        if user.login_method == 'password':
            msg = 'no.shibboleth'
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        user.login_method = 'password'
        user.shibboleth_id = None
        user.shibboleth_idp = ''
        user.shibboleth_schac_home_organization = ''
        password = ApellaUser.objects.make_random_password(length=15)
        user.set_password(password)
        user.can_set_academic = True
        user.save()
        send_release_shibboleth_email(user, request)

        logger.info('User %s released shibboleth for %s' %
            (request.user.username, user.username))
        return Response(request.data, status=status.HTTP_200_OK)



class JiraIssues(object):
    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        if not user.is_helpdesk():
            queryset = queryset.filter(reporter_id=user.id)
        queryset = queryset.order_by('-updated_at')
        return queryset
