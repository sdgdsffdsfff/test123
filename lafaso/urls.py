from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'apps.mycenter.views.profile',),
                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),

                       # monitor url
                       url(r'^monitor/', include('apps.monitorcenter.urls')),

                       #networkcenter manager url
                       url(r'^network/', include('apps.networkcenter.urls')),

                       # systemcenter manager url
                       url(r'^system/', include('apps.systemcenter.urls')),

                       #account manager url
                       url(r'^account/', include('apps.mycenter.urls')),
                       url(r'^login$', 'apps.mycenter.views.login', name='login'),
                       )
#if settings.DEBUG is False:
#    urlpatterns += patterns('',
#        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
#            'document_root': settings.STATIC_ROOT,
#        }),
#   )