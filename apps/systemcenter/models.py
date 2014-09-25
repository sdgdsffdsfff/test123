#!/usr/bin/env python
#coding=utf8
# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from apps.networkcenter.models import Device, DomainRecord


class SystemLevel(models.Model):
    level = models.CharField(max_length=10, unique=True, error_messages={'unique': u'名称已经使用'})
    remask = models.CharField(max_length=100, blank=True)
    is_need = models.NullBooleanField(default=True)
    is_relation = models.NullBooleanField(default=True)

    def __unicode__(self):
        return self.level


class SystemTag(models.Model):
    tag = models.CharField(max_length=20)
    remask = models.CharField(max_length=100, blank=True)
    level = models.ForeignKey(SystemLevel)

    class Meta:
        unique_together = (("tag", "level"),)

    def __unicode__(self):
        return self.remask


class ServerPool(models.Model):
    sn = models.CharField(max_length=25, unique=True)
    hostname = models.CharField(max_length=100, blank=True)
    os_type = models.CharField(max_length=100, blank=True)
    os_kernel = models.CharField(max_length=100, blank=True)
    os_release = models.CharField(max_length=100, blank=True)
    ip = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=10, default="00")
    ## 服务器运行状态: 00:待交付 01:维护中, 11:运行中
    install = models.NullBooleanField(default=True)
    ## 装机开关: True:可装机, Flase:不可装机
    detect = models.NullBooleanField(default=True)
    ## 主机体检开关
    collect = models.NullBooleanField(default=True)
    ## 主机性能采集开关
    oper = models.ForeignKey(User, blank=True, null=True, related_name='oper')
    # 运维负责人
    fronter = models.ForeignKey(User,  blank=True, null=True, related_name='fronter')
    # 前端负责人
    dever = models.ForeignKey(User, blank=True, null=True, related_name='dever')
    # 后端负责人
    host = models.ForeignKey('self', null=True, blank=True)
    # 虚拟机宿主机
    is_vrt = models.NullBooleanField(default=False)
    tag = models.ManyToManyField(SystemTag, blank=True)
    description = models.CharField(max_length=50, blank=True)

    def __unicode__(self):
            return self.sn

    def save(self, *args, **kwargs):
        from apps.networkcenter.models import IpAdress
        super(ServerPool, self).save(*args, **kwargs)
        IpAdress.objects.filter(name=self.ip).update(status=True)


class SoftWare(models.Model):
    name = models.CharField(max_length=25, unique=True)
    last_releases = models.CharField(max_length=25, blank=True)
    remask = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return self.name


class ServerSoftVersion(models.Model):
    server = models.ForeignKey(ServerPool)
    software = models.ForeignKey(SoftWare)
    current_use_releases = models.CharField(max_length=25, blank=True)
    install_path = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return self.server


class ServerSLA(models.Model):
    server = models.ForeignKey(ServerPool)
    down_sum = models.IntegerField(default=0)
    down_time = models.IntegerField(default=0)
    creat_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.server


class ServerMonitor(models.Model):
    #主机监控 调用cacti图像
    server = models.ForeignKey(ServerPool)
    graph_id = models.IntegerField()

    def __unicode__(self):
        return u"%s_%s" % (self.server.hostname, self.graph_id)