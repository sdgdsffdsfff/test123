#!/usr/bin/env python
#coding=utf8
from django.db import models


class CactiHost(models.Model):
    name = models.CharField(max_length=50, unique=True, error_messages={'unique': u'名称已经使用'})
    host = models.CharField(max_length=511, blank=True, null=True)

    def __unicode__(self):
        return self.name


class GraphsGroup(models.Model):
    name = models.CharField(max_length=50, unique=True, error_messages={'unique': u'名称已经使用'})
    cacti_host = models.ForeignKey(CactiHost)

    def __unicode__(self):
        return self.name


class GraphsID(models.Model):
    graph_id = models.CharField(max_length=20, unique=True, error_messages={'unique': u'名称已经使用'})
    graph_group = models.ForeignKey(GraphsGroup)

    def __unicode__(self):
        return self.name

#失败订单数据结构定义"


class OrdersFailType(models.Model):
    """订单失败分类"""
    type_id = models.IntegerField(unique=True, error_messages={'unique': u'分类已经存在'})
    remask = models.CharField(max_length=511, blank=True, null=True)

    def __unicode__(self):
        return unicode(self.type_id)


class OrdersFailNumHour(models.Model):
    """订单失败数量/小时"""
    record_time = models.DateTimeField()
    fail_type = models.ForeignKey(OrdersFailType)
    order_num = models.IntegerField()

    class Meta:
        unique_together = (("record_time", "fail_type"),)

    def __unicode__(self):
        return unicode(self.order_num)


class ShiftTable(models.Model):
    """值班表"""
    years = models.CharField(max_length=10)
    month = models.CharField(max_length=10)
    shift_id = models.IntegerField()

    def __unicode__(self):
        return self.month


#网站地区跳出率统计
class City(models.Model):
    """城市表"""
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Tclv(models.Model):
    """地区跳出率"""
    record_time = models.DateTimeField()
    city = models.ForeignKey(City)
    tclv = models.IntegerField()

    def __unicode__(self):
        return self.city.name