# coding: utf8
from django.conf import settings
from django.db.transaction import commit_on_success
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from locks.models import Lock


def index(request):
    c = {
        'total_saved_hours': Lock.objects.sum_saved_hours(),
        'today_saved_hours': Lock.objects.sum_saved_hours(period=1)
    }
    return render_to_response('core/index.html', c,
        context_instance=RequestContext(request))
