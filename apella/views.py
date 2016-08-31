from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.generic.list import ListView

from apella.models import ApellaUser


def index(request):
    context = {}
    return render(request, 'apella/index.html', context)

def user_list(request):
    context = {}
    return render(request, 'apella/index.html', context)

def user_detail(request, user_id):
    context = {}
    return render(request, 'apella/index.html', context)

def position_list(request):
    context = {}
    return render(request, 'apella/index.html', context)

def position_detail(request, position_id):
    context = {}
    return render(request, 'apella/index.html', context)
