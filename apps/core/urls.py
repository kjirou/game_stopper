# coding: utf8
from django.conf.urls import patterns, url, include

urlpatterns = patterns('core.views',
    url(r'^$', 'index'),
)
