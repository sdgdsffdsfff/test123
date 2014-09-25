#coding=utf-8
__author__ = 's7eph4ni3'

from django.contrib import admin
from apps.networkcenter.models import IDC, IpSection, DeviceLevel, DeviceTag, Device, DeviceNIC


class IDCAdmin(admin.ModelAdmin):
    list_display = ('name', 'remark')


class IPNetAdmin(admin.ModelAdmin):
    list_display = ('name', 'remark')


class DeviceLevelAdmin(admin.ModelAdmin):
    list_display = ("level", "remask")


class DeviceTagAdmin(admin.ModelAdmin):
    list_display = ('tag', 'level', 'remask')


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('sn', 'remark')


class DeviceNICAdmin(admin.ModelAdmin):
    list_display = ('device', 'name')


admin.site.register(IDC, IDCAdmin)
admin.site.register(IpSection, IPNetAdmin)
admin.site.register(DeviceLevel, DeviceLevelAdmin)
admin.site.register(DeviceTag, DeviceTagAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(DeviceNIC, DeviceNICAdmin)