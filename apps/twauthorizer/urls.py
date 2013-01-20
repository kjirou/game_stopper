# coding: utf8
from django.conf.urls import patterns, url, include

urlpatterns = patterns('twauthorizer.views',
    url(r'^auth/$', 'auth', name='auth'),
    url(r'^auth_callback/$', 'auth_callback', name='auth_callback'),
    #url(r'^sign_up/$', 'sign_up', name='sign_up'),
)
