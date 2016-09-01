from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import loader
from django.views.generic.list import ListView

from apella.models import ApellaUser, Position, Candidacy, Institution
from apella.forms import ApellaUserForm, PositionForm, CandidacyForm,\
        InstitutionForm

class UserListView(ListView):

    model = ApellaUser

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        return context

class PositionListView(ListView):

    model = Position

    def get_context_data(self, **kwargs):
        context = super(PositionListView, self).get_context_data(**kwargs)
        return context

class CandidacyListView(ListView):

    model = Candidacy

    def get_context_data(self, **kwargs):
        context = super(CandidacyListView, self).get_context_data(**kwargs)
        return context

class InstitutionListView(ListView):

    model = Institution

    def get_context_data(self, **kwargs):
        context = super(InstitutionListView, self).get_context_data(**kwargs)
        return context

def index(request):
    context = {}
    return render(request, 'apella/index.html', context)


def user_edit(request, user_id=None):
    if user_id:
        user = get_object_or_404(ApellaUser, pk=user_id)
    else:
        user = ApellaUser()
    form = ApellaUserForm(request.POST or None, instance=user)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            user.save()
            return redirect('user-list')
    else:
        form = ApellaUserForm(instance=user)
    return render(request, 'apella/apellauser_detail.html', {'form' : form})

def position_edit(request, position_id=None):
    if position_id:
        position = get_object_or_404(Position, pk=position_id)
    else:
        position = Position()
    form = PositionForm(request.POST or None, instance=position)
    if request.method == 'POST':
        if form.is_valid():
            position = form.save()
            position.save()
            return redirect('position-list')
    else:
        form = PositionForm(instance=position)
    return render(request, 'apella/position_detail.html', {'form' : form})

def candidacy_edit(request, candidacy_id=None, position_id=None):
    if candidacy_id:
        candidacy = get_object_or_404(Candidacy, pk=candidacy_id)
    elif position_id:
        position = get_object_or_404(Position, pk=position_id)
        candidacy = Candidacy(position=position)
    else:
        candidacy = Candidacy()
    form = CandidacyForm(request.POST or None, instance=candidacy)
    if request.method == 'POST':
        if form.is_valid():
            candidacy = form.save()
            candidacy.save()
            return redirect('candidacy-list')
    else:
        form = CandidacyForm(instance=candidacy)
    return render(request, 'apella/candidacy_detail.html', {'form' : form})


def institution_edit(request, institution_id=None):
    if institution_id:
        institution = get_object_or_404(Institution, pk=institution_id)
    else:
        institution = Institution()
    form = InstitutionForm(request.POST or None, instance=institution)
    if request.method == 'POST':
        if form.is_valid():
            institution = form.save()
            institution.save()
            return redirect('institution-list')
    else:
        form = InstitutionForm(instance=institution)
    return render(request, 'apella/institution_detail.html', {'form' : form})
