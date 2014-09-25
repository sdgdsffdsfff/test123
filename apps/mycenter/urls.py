__author__ = 's7eph4ni3'
from django.conf.urls import patterns, include, url

urlpatterns = patterns('apps.mycenter.views',
                        url(r'^$', 'profile',),
                        url(r'^index/?$', 'profile', name="profile"),
                        url(r'^logout?$', 'logout', name="logout"),
                        url(r'^profileedit/?$', 'profileedit', name="profileedit"),
                        url(r'^list.html/?$', 'userlist', name="userlist"),
                        url(r'^useradd/?$', 'useradd', name="useradd"),
                        url(r'^useredit/(?P<id>\d+)$', 'useredit', name="useredit"),
                        url(r'^grouplist.html/?$', 'grouplist', name="grouplist"),
                        url(r'^groupedit/(?P<id>\d+)$', 'groupedit', name="groupedit"),
                        url(r'^groupadd/?$', 'groupadd', name="groupadd"),
                        url(r'^oaquery$', 'oaquery', name="oaquery"),
                        )