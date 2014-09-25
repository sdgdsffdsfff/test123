#!/usr/bin/python
#coding=utf-8
__author__ = 's7eph4ni3'

from django.contrib import admin
from apps.systemcenter.models import SystemLevel, SystemTag, ServerPool, SoftWare, ServerSoftVersion, ServerSLA,\
    ServerMonitor


class SystemLevelAdmin(admin.ModelAdmin):
    list_display = ('level', 'remask')


class SystemTagAdmin(admin.ModelAdmin):
    list_display = ('tag', 'level', 'remask')


class ServerPoolAdmin(admin.ModelAdmin):
    list_display = ('sn', 'hostname')


class ServerMonitorAdmin(admin.ModelAdmin):
    list_display = ("server", "graph_id")


admin.site.register(SystemLevel, SystemLevelAdmin)
admin.site.register(SystemTag, SystemTagAdmin)
admin.site.register(ServerPool, ServerPoolAdmin)
admin.site.register(ServerMonitor, ServerMonitorAdmin)