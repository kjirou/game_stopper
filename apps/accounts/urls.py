# coding: utf8
from django.conf.urls import patterns, url, include

urlpatterns = patterns('accounts.views',
    url(r'^sign_in$', 'sign_in'),
    url(r'^sign_out$', 'sign_out'),
)
