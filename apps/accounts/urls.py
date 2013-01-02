# coding: utf8
from django.conf.urls import patterns, url, include
from accounts.forms import ProfiledUserOnlyAuthenticationForm

urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login',
        { 'authentication_form': ProfiledUserOnlyAuthenticationForm }, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
)

urlpatterns += patterns('accounts.views',
    url(r'^sign_up/$', 'sign_up', name='sign_up'),
)
