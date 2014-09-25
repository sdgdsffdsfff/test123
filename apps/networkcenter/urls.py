# coding=utf-8
__author__ = 's7eph4ni3'

from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:

urlpatterns = patterns('apps.networkcenter.views',
    url(r'^$','networkindex',name='networkindex' ),
    url(r'^idcindex.html$','idcindex',name='idcindex' ),
    url(r'^racklist.html$','racklist',name='racklist' ),
    url(r'^racklist.html/(?P<id>\d+)$','rackdetail',name='rackdetail' ),
    url(r'^iplist.html$','iplist',name='iplist' ),
    url(r'^rackedit/(?P<id>\d+)$','rackedit',name='rackedit' ),
    url(r'^rackdel/(?P<id>\d+)$','rackdel',name='rackdel' ),
    url(r'^ipnet.html$','ipsection',name='ipsection' ),
    url(r'^deviceindex.html$','deviceindex',name='deviceindex' ),
    url(r'^devicetree$','devicetree',name='devicetree' ),
    url(r'^devicelist.html$','devicelist',name='devicelist' ),
    url(r'^devicetreelist.html$','devicetreelist',name='devicetreelist' ),
    url(r'^devicelist.html/(?P<id>\d+)$','devicedetail',name='devicedetail' ),
    url(r'^deviceedit.html/(?P<id>\d+)$','deviceedit',name='deviceedit' ),
    url(r'^deviceint.html/(?P<id>\d+)$','deviceint',name='deviceint' ),
    url(r'^deviceint.html/(?P<id>\d+)/edit$','deviceintedit',name='deviceintedit' ),
    url(r'^importdevice$','importdevice',name='importdevice' ),
    url(r'^exportdevice$','exportdevice',name='exportdevice' ),
    url(r'^apigetrack$','getrack',name='getchrack' ),
    url(r'^apigetposition$','getposition',name='getposition' ),
    url(r'^osinstall.html$','osinstall',name='osinstall' ),
    url(r'^osinstall.html/pool$','srvpool',name='srvpool' ),
    url(r'^osinstall.html/complete$','osinstallcomplete',name='osinstallcomplete' ),
    url(r'^osinstalltask/refresh/(?P<id>\d+)$','osinstallrefresh',name='osinstallrefresh' ),
    url(r'^osinstalltask/submit/(?P<id>\d+)$','osinstallsubmit',name='osinstallsubmit' ),
    url(r'^osinstalltask/deliver/(?P<id>\d+)$','osinstalldeliver',name='osinstalldeliver' ),
)