#!/usr/bin/env python
#coding=utf-8

import datetime
from django.db import models
from django.contrib.auth.models import User
#from simple_history import register
from apps.networkcenter.shortcut import device_save, deviceint_save
# Create your models here.
#register(User)


class DeviceLevel(models.Model):
    level = models.CharField(max_length=10, unique=True, error_messages={'unique': u'名称已经使用'})
    remask = models.CharField(max_length=100, blank=True)
    is_need = models.NullBooleanField(default=True)
    is_relation = models.NullBooleanField(default=True)

    def __unicode__(self):
        return self.level


class DeviceTag(models.Model):
    tag = models.CharField(max_length=20)
    remask = models.CharField(max_length=100, blank=True)
    level = models.ForeignKey(DeviceLevel)

    class Meta:
        unique_together = (("tag", "level"),)

    def __unicode__(self):
        return self.remask


class IDC(models.Model):
    name = models.CharField(max_length=50, unique=True, error_messages={'unique': u'名称已经使用'})
    address = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    mail = models.EmailField(max_length=50, blank=True)
    create_time = models.DateField(default=datetime.datetime.now())
    tag = models.CharField(max_length=10, blank=True)
    remark = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return self.name


class Rack(models.Model):
    name = models.CharField(max_length=50, )
    idc = models.ForeignKey(IDC)
    create_time = models.DateField(default=datetime.datetime.now())
    tag = models.CharField(max_length=10, blank=True)
    remark = models.CharField(max_length=100, blank=True)

    class Meta:
        unique_together = (("name", "idc"),)

    def __unicode__(self):
        return self.idc.name+'_'+self.name


class Position(models.Model):
    name = models.CharField(max_length=10)
    rack = models.ForeignKey(Rack)
    tag = models.CharField(max_length=10, blank=True)
    remark = models.CharField(max_length=100, blank=True)
    status = models.NullBooleanField(default=False)

    class Meta:
        unique_together = (("name", "rack"),)

    def __unicode__(self):
        return self.rack.idc.name + "_" + self.rack.name + "_" + self.name


class IpSection(models.Model):
    name = models.CharField(max_length=50)
    idc = models.ForeignKey(IDC)
    remark = models.CharField(max_length=100, blank=True)

    class Meta:
        unique_together = (("name", "idc"),)

    def __unicode__(self):
        return self.name


class IpAdress(models.Model):
    ip_cat = (('ip', 'os ip'), ('iLo', 'ilo ip'),)
    name = models.IPAddressField(max_length=50)
    section = models.ForeignKey(IpSection)
    idc = models.ForeignKey(IDC)
    category = models.CharField(max_length=20, choices=ip_cat, default='Other')
    remark = models.CharField(max_length=100, blank=True)
    create_time = models.DateField(default=datetime.datetime.now())
    status = models.NullBooleanField(default=False)

    class Meta:
        unique_together = (("name", "section"),)

    def __unicode__(self):
        return self.name


class Device(models.Model):
    sn = models.CharField(max_length=25, unique=True, error_messages={'unique': u'设备已存在'})
    idc = models.ForeignKey(IDC, blank=True, null=True)
    rack = models.ForeignKey(Rack, blank=True, null=True)
    position = models.OneToOneField(Position, blank=True, null=True)
    #资产信息
    asset_id = models.CharField(max_length=50, blank=True)
    purchase_id = models.CharField(max_length=50, blank=True)
    buy_price = models.IntegerField(blank=True, null=True)
    buy_time = models.DateField(blank=True, null=True)
    expired_time = models.DateField(blank=True, null=True)
    status = models.NullBooleanField(default=False)
    #status True:已使用 False:未使用
    create_time = models.DateField(default=datetime.datetime.now())
    tag = models.ManyToManyField(DeviceTag, blank=True)
    remark = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return self.sn

    def save(self, *args, **kwargs):
        self.save = device_save(self, *args, **kwargs)


class DeviceCPU(models.Model):
    device = models.ForeignKey(Device)
    product = models.CharField(max_length=50, blank=True)
    vendor = models.CharField(max_length=50, blank=True)
    version = models.CharField(max_length=50, blank=True)
    slot = models.CharField(max_length=50, blank=True)

    def __unicode__(self):
        return self.name


class DeviceMem(models.Model):
    device = models.ForeignKey(Device)
    vendor = models.CharField(max_length=50, blank=True)
    version = models.CharField(max_length=50, blank=True)
    slot = models.CharField(max_length=10, blank=True)
    size = models.CharField(max_length=10, blank=True)

    def __unicode__(self):
        return self.name


class DeviceDisk(models.Model):
    device = models.ForeignKey(Device)
    disk_sn = models.CharField(max_length=50, blank=True)
    vendor = models.CharField(max_length=50, blank=True)
    version = models.CharField(max_length=50, blank=True)
    slot = models.CharField(max_length=10, blank=True)
    speed = models.CharField(max_length=10, blank=True)
    size = models.CharField(max_length=10, blank=True)

    def __unicode__(self):
        return self.name


class DeviceNIC(models.Model):
    device = models.ForeignKey(Device)
    name = models.CharField(max_length=30)
    product = models.CharField(max_length=50, blank=True)
    vendor = models.CharField(max_length=50, blank=True)
    mac = models.CharField(max_length=50, blank=True)
    speed = models.CharField(max_length=50, blank=True)
    ip = models.OneToOneField(IpAdress, null=True, blank=True)
    vlan = models.CharField(max_length=10, blank=True)
    link = models.OneToOneField('self', limit_choices_to={'status': [False]}, blank=True, null=True)
    status = models.NullBooleanField(default=False)
    remark = models.CharField(max_length=100, blank=True)

    class Meta:
        unique_together = (("name", "device"),)

    def __unicode__(self):
        return self.device.sn + "_" + self.name

    def save(self, *args, **kwargs):
        self.save = deviceint_save(self, *args, **kwargs)


class DevicePower(models.Model):
    device = models.ForeignKey(Device)
    power_sn = models.CharField(max_length=50, blank=True)
    vendor = models.CharField(max_length=50, blank=True)
    version = models.CharField(max_length=50, blank=True)
    slot = models.CharField(max_length=10, blank=True)

    def __unicode__(self):
        return u"%s" % self.power_sn


class Domain(models.Model):
    name = models.CharField(max_length=100, unique=True, error_messages={'unique': u'域名已存在'})
    registrar = models.CharField(max_length=50, blank=True, null=True)
    remark = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return self.name


class DomainRecord(models.Model):
    re_type = (('NS', 'NS'), ('A', 'A'), ('CNAME', 'CNAME'), ('MAX', 'MAX'), ('TXT', 'TXT'), ('AAAA', 'AAA'),
               ('SRV', 'SRV'))
    name = models.CharField(max_length=100)
    domain = models.ForeignKey(Domain)
    record_type = models.CharField(max_length=20, choices=re_type)
    record_value = models.CharField(max_length=100)
    record_ttl = models.CharField(max_length=10, blank=True)
    remark = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return self.name+'.'+self.domain.name


class OSInstallTask(models.Model):
    batch_name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return u"{0}".format(self.batch_name)


class OSInstallQueue(models.Model):
    t_type = (("RHEL", "RHEL"), ("ESXI", "ESXI"))
    sn = models.CharField(max_length=25)
    tp_type = models.CharField(max_length=20, choices=t_type, default='RHEL')
    status = models.CharField(max_length=10, default="00")
    # 任务状态： 00:新任务 01:执行中 10：执行失败 11:完成
    install = models.NullBooleanField(default=False)
    # 装机开关: True:可装机, Flase:不可装机
    deliver = models.NullBooleanField(default=False)
    # 交付状态： True： 已交付 Flase：未来交付
    ilo_ip = models.CharField(max_length=50)
    os_ip = models.CharField(max_length=50)
    eth0_mac = models.CharField(max_length=50)
    schedule = models.CharField(max_length=10, blank=True)
    create_user = models.CharField(max_length=10)
    needs_user = models.ForeignKey(User)
    ctime = models.DateTimeField(default=datetime.datetime.now())
    batch = models.ForeignKey(OSInstallTask)

    def __unicode__(self):
        return u"{0}".format(self.sn)