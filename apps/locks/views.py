# coding: utf8
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.transaction import commit_on_success
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import get_template
from locks.models import Lock


def index(request):
    c = {}
    return render_to_response('locks/index.html', c,
        context_instance=RequestContext(request))
