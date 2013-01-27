# coding: utf-8
from django.conf.urls import patterns, url, include

urlpatterns = patterns('twauthorizer.views',
    url(r'^auth/$', 'auth', name='auth'),
    url(r'^auth_callback/$', 'auth_callback', name='auth_callback'),
)
