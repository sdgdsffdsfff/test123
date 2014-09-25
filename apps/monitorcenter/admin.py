__author__ = 's7eph4ni3'

from django.contrib import admin
from apps.monitorcenter.models import *


class CactiHostAdmin(admin.ModelAdmin):
    list_display = ('name', 'host')


class GraphsGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'cacti_host')


class GraphsIDAdmin(admin.ModelAdmin):
    list_display = ('graph_id', 'graph_group')


class OrdersFailTypeAdmin(admin.ModelAdmin):
    list_display = ('type_id', 'remask')


class OrdersFailNumHourAdmin(admin.ModelAdmin):
    list_display = ('record_time', 'fail_type', 'order_num')

class ShiftTableAdmin(admin.ModelAdmin):
    list_display = ('years', 'month', 'shift_id')
admin.site.register(OrdersFailType, OrdersFailTypeAdmin)
admin.site.register(OrdersFailNumHour, OrdersFailNumHourAdmin)
admin.site.register(CactiHost, CactiHostAdmin)
admin.site.register(ShiftTable, ShiftTableAdmin)
admin.site.register(GraphsGroup, GraphsGroupAdmin)
admin.site.register(GraphsID, GraphsIDAdmin)
