from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import loader
from django.views.generic.list import ListView

from apella.models import ApellaUser, Position, Candidacy
from apella.forms import ApellaUserForm, PositionForm

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

def index(request):
    context = {}
    return render(request, 'apella/index.html', context)

def user_detail(request, user_id):
    context = {}
    return render(request, 'apella/index.html', context)


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
