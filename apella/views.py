from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.generic.list import ListView

from apella.models import ApellaUser, Position

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

def index(request):
    context = {}
    return render(request, 'apella/index.html', context)

def user_detail(request, user_id):
    context = {}
    return render(request, 'apella/index.html', context)


def position_detail(request, position_id):
    context = {}
    return render(request, 'apella/index.html', context)
