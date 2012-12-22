# coding: utf8
from django.conf import settings
from django.http import HttpResponse
from django.db.transaction import commit_on_success
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return HttpResponse('index page')
