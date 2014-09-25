#coding=utf8
__author__ = 's7eph4ni3'


from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:

urlpatterns = patterns('apps.monitorcenter.views',
    url(r'^$','index',name='monitorindex' ),
    url(r'system$','system',name='monitorsystemindex' ),
    url(r'system/(?P<id>\d+)$','sub_system',name='monitorsystem' ),
    url(r'network$','network',name='monitornetworkindex' ),
    url(r'network/(?P<id>\d+)$','sub_network',name='monitornetwork' ),
    url(r'db$','db',name='monitordbindex' ),
    url(r'db/(?P<id>\d+)$','sub_db',name='monitordb' ),
    url(r'zhiban$','zhiban',name='monitorzhiban' ),
)