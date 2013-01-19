# coding: utf8
from django.conf.urls import patterns, url, include

urlpatterns = patterns('locks.views',
    url(r'^$', 'index', name='index'),
    url(r'^create/$', 'create', name='create'),
    url(r'^delete_file/(\d+)/$', 'delete_file', name='delete_file'),
    url(r'^unlock_file/(\d+)/$', 'unlock_file', name='unlock_file'),
)
