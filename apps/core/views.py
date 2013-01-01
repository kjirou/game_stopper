# coding: utf8
from django.conf import settings
from django.db.transaction import commit_on_success
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render_to_response('core/index.html', {},
        context_instance=RequestContext(request))
