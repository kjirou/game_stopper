from django.conf import settings
import re
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^locks/', include('locks.urls', namespace='locks')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('core.urls', namespace='core')),
)

if settings.WEB_SERVER == 'development':
    urlpatterns += patterns('',
        (
            ur'^%s(?P<path>.*)$' % re.sub(ur'^/', u'', settings.MEDIA_URL),
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}
        ),
    )
