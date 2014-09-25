# coding=utf-8
__author__ = 's7eph4ni3'

from django.conf.urls import patterns, include, url

urlpatterns = patterns('apps.systemcenter.views',
                       url(r'^$', 'index', name='systemindex'),
                       url(r'^server.html$', 'serverindex', name='serverindex'),
                       url(r'^servertree.html$', 'servertree', name='servertree'),
                       url(r'^server/phy.html$', 'physerver', name='physerver'),
                       url(r'^server/vrt.html$', 'vrtserver', name='vrtserver'),
                       url(r'^servertreelist.html$', 'servertreelist', name='servertreelist'),
                       url(r'^server/detail.html/(?P<id>\d+)$', 'serverdetail', name='serverdetail'),
                       url(r'^serveredit.html/(?P<id>\d+)$', 'serveredit', name='serveredit'),
                       url(r'^servermonitor.html/(?P<id>\d+)$', 'servermonitor', name='servermonitor'),
                       url(r'^server/crtvrt.html/(?P<id>\d+)$', 'crtvrt', name='crtvrt'),
                       url(r'^serverup.html/(?P<id>\d+)$', 'serverup', name='serverup'),
                       url(r'^srvmaintain.html/(?P<id>\d+)$', 'srvmaintain', name='srvmaintain'),)
