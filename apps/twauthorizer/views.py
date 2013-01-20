# coding: utf8
import tweepy
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth import login
from django.db.transaction import commit_on_success
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import get_template


@commit_on_success
def auth(request):
    return HttpResponse('auth')


@commit_on_success
def auth_callback(request):
    return HttpResponse('auth_callback')
