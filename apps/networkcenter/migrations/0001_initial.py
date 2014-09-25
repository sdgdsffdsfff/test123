# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Company'
        db.create_table(u'networkcenter_company', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('remark', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'networkcenter', ['Company'])

        # Adding model 'OwnerTeam'
        db.create_table(u'networkcenter_ownerteam', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('cop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.Company'])),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('remark', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'networkcenter', ['OwnerTeam'])

        # Adding unique constraint on 'OwnerTeam', fields ['name', 'cop']
        db.create_unique(u'networkcenter_ownerteam', ['name', 'cop_id'])

        # Adding model 'Location'
        db.create_table(u'networkcenter_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('remark', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'networkcenter', ['Location'])

        # Adding model 'IDC'
        db.create_table(u'networkcenter_idc', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('mail', self.gf('django.db.models.fields.EmailField')(max_length=50, blank=True)),
            ('create_time', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 3, 10, 0, 0))),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('remark', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'networkcenter', ['IDC'])

        # Adding model 'Rack'
        db.create_table(u'networkcenter_rack', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('idc', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.IDC'])),
            ('create_time', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 3, 10, 0, 0))),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('remark', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'networkcenter', ['Rack'])

        # Adding unique constraint on 'Rack', fields ['name', 'idc']
        db.create_unique(u'networkcenter_rack', ['name', 'idc_id'])

        # Adding model 'Position'
        db.create_table(u'networkcenter_position', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('rack', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.Rack'])),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('remark', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('status', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
        ))
        db.send_create_signal(u'networkcenter', ['Position'])

        # Adding unique constraint on 'Position', fields ['name', 'rack']
        db.create_unique(u'networkcenter_position', ['name', 'rack_id'])

        # Adding model 'Brands'
        db.create_table(u'networkcenter_brands', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('remark', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'networkcenter', ['Brands'])

        # Adding model 'Supplier'
        db.create_table(u'networkcenter_supplier', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('owner', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('mail', self.gf('django.db.models.fields.EmailField')(max_length=50, blank=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('remark', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'networkcenter', ['Supplier'])

        # Adding model 'DeviceType'
        db.create_table(u'networkcenter_devicetype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('remark', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('status', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
        ))
        db.send_create_signal(u'networkcenter', ['DeviceType'])

        # Adding model 'DeviceModel'
        db.create_table(u'networkcenter_devicemodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('device_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.DeviceType'])),
            ('brands', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.Brands'])),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('remark', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'networkcenter', ['DeviceModel'])

        # Adding model 'IpSection'
        db.create_table(u'networkcenter_ipsection', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('idc', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.IDC'])),
            ('remark', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'networkcenter', ['IpSection'])

        # Adding unique constraint on 'IpSection', fields ['name', 'idc']
        db.create_unique(u'networkcenter_ipsection', ['name', 'idc_id'])

        # Adding model 'IpAdress'
        db.create_table(u'networkcenter_ipadress', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.IpSection'])),
            ('idc', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.IDC'])),
            ('category', self.gf('django.db.models.fields.CharField')(default='Other', max_length=20)),
            ('remark', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('create_time', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 3, 10, 0, 0))),
            ('status', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
        ))
        db.send_create_signal(u'networkcenter', ['IpAdress'])

        # Adding unique constraint on 'IpAdress', fields ['name', 'section']
        db.create_unique(u'networkcenter_ipadress', ['name', 'section_id'])

        # Adding model 'Device'
        db.create_table(u'networkcenter_device', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('device_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.DeviceType'])),
            ('device_sn', self.gf('django.db.models.fields.CharField')(unique=True, max_length=25)),
            ('brands', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.Brands'], null=True, blank=True)),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.DeviceModel'], null=True, blank=True)),
            ('cop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.Company'], null=True, blank=True)),
            ('owt', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.OwnerTeam'], null=True, blank=True)),
            ('loc', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.Location'], null=True, blank=True)),
            ('idc', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.IDC'], null=True, blank=True)),
            ('rack', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.Rack'], null=True, blank=True)),
            ('position', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['networkcenter.Position'], unique=True, null=True, blank=True)),
            ('asset_id', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('purchase_id', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('buy_price', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('buy_time', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('expired_time', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('supplier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.Supplier'], null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
            ('create_time', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 3, 10, 0, 0))),
            ('remark', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'networkcenter', ['Device'])

        # Adding model 'DeviceInerface'
        db.create_table(u'networkcenter_deviceinerface', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.Device'])),
            ('mac', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('ip', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['networkcenter.IpAdress'], unique=True, null=True, blank=True)),
            ('vlan', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('link', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['networkcenter.DeviceInerface'], unique=True, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
            ('remark', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'networkcenter', ['DeviceInerface'])

        # Adding unique constraint on 'DeviceInerface', fields ['name', 'device']
        db.create_unique(u'networkcenter_deviceinerface', ['name', 'device_id'])

        # Adding model 'DeviceMem'
        db.create_table(u'networkcenter_devicemem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.Device'])),
            ('mem_sn', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('slot', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('size', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
        ))
        db.send_create_signal(u'networkcenter', ['DeviceMem'])

        # Adding model 'DeviceDisk'
        db.create_table(u'networkcenter_devicedisk', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.Device'])),
            ('disk_sn', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('slot', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('speed', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('size', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
        ))
        db.send_create_signal(u'networkcenter', ['DeviceDisk'])

        # Adding model 'DeviceParameter'
        db.create_table(u'networkcenter_deviceparameter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('device_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.DeviceType'])),
            ('desc', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('remark', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('status', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
        ))
        db.send_create_signal(u'networkcenter', ['DeviceParameter'])

        # Adding unique constraint on 'DeviceParameter', fields ['name', 'device_type']
        db.create_unique(u'networkcenter_deviceparameter', ['name', 'device_type_id'])

        # Adding model 'DeviceParameterValue'
        db.create_table(u'networkcenter_deviceparametervalue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.Device'])),
            ('device_para', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.DeviceParameter'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'networkcenter', ['DeviceParameterValue'])

        # Adding unique constraint on 'DeviceParameterValue', fields ['device', 'device_para']
        db.create_unique(u'networkcenter_deviceparametervalue', ['device_id', 'device_para_id'])

        # Adding model 'Domain'
        db.create_table(u'networkcenter_domain', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('cop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.Company'], null=True, blank=True)),
            ('registrar', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('remark', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'networkcenter', ['Domain'])

        # Adding model 'DomainRecord'
        db.create_table(u'networkcenter_domainrecord', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('domain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.Domain'])),
            ('record_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('record_value', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('record_ttl', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('remark', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'networkcenter', ['DomainRecord'])


    def backwards(self, orm):
        # Removing unique constraint on 'DeviceParameterValue', fields ['device', 'device_para']
        db.delete_unique(u'networkcenter_deviceparametervalue', ['device_id', 'device_para_id'])

        # Removing unique constraint on 'DeviceParameter', fields ['name', 'device_type']
        db.delete_unique(u'networkcenter_deviceparameter', ['name', 'device_type_id'])

        # Removing unique constraint on 'DeviceInerface', fields ['name', 'device']
        db.delete_unique(u'networkcenter_deviceinerface', ['name', 'device_id'])

        # Removing unique constraint on 'IpAdress', fields ['name', 'section']
        db.delete_unique(u'networkcenter_ipadress', ['name', 'section_id'])

        # Removing unique constraint on 'IpSection', fields ['name', 'idc']
        db.delete_unique(u'networkcenter_ipsection', ['name', 'idc_id'])

        # Removing unique constraint on 'Position', fields ['name', 'rack']
        db.delete_unique(u'networkcenter_position', ['name', 'rack_id'])

        # Removing unique constraint on 'Rack', fields ['name', 'idc']
        db.delete_unique(u'networkcenter_rack', ['name', 'idc_id'])

        # Removing unique constraint on 'OwnerTeam', fields ['name', 'cop']
        db.delete_unique(u'networkcenter_ownerteam', ['name', 'cop_id'])

        # Deleting model 'Company'
        db.delete_table(u'networkcenter_company')

        # Deleting model 'OwnerTeam'
        db.delete_table(u'networkcenter_ownerteam')

        # Deleting model 'Location'
        db.delete_table(u'networkcenter_location')

        # Deleting model 'IDC'
        db.delete_table(u'networkcenter_idc')

        # Deleting model 'Rack'
        db.delete_table(u'networkcenter_rack')

        # Deleting model 'Position'
        db.delete_table(u'networkcenter_position')

        # Deleting model 'Brands'
        db.delete_table(u'networkcenter_brands')

        # Deleting model 'Supplier'
        db.delete_table(u'networkcenter_supplier')

        # Deleting model 'DeviceType'
        db.delete_table(u'networkcenter_devicetype')

        # Deleting model 'DeviceModel'
        db.delete_table(u'networkcenter_devicemodel')

        # Deleting model 'IpSection'
        db.delete_table(u'networkcenter_ipsection')

        # Deleting model 'IpAdress'
        db.delete_table(u'networkcenter_ipadress')

        # Deleting model 'Device'
        db.delete_table(u'networkcenter_device')

        # Deleting model 'DeviceInerface'
        db.delete_table(u'networkcenter_deviceinerface')

        # Deleting model 'DeviceMem'
        db.delete_table(u'networkcenter_devicemem')

        # Deleting model 'DeviceDisk'
        db.delete_table(u'networkcenter_devicedisk')

        # Deleting model 'DeviceParameter'
        db.delete_table(u'networkcenter_deviceparameter')

        # Deleting model 'DeviceParameterValue'
        db.delete_table(u'networkcenter_deviceparametervalue')

        # Deleting model 'Domain'
        db.delete_table(u'networkcenter_domain')

        # Deleting model 'DomainRecord'
        db.delete_table(u'networkcenter_domainrecord')


    models = {
        u'networkcenter.brands': {
            'Meta': {'object_name': 'Brands'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'remark': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        u'networkcenter.company': {
            'Meta': {'object_name': 'Company'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'remark': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        u'networkcenter.device': {
            'Meta': {'object_name': 'Device'},
            'asset_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'brands': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['networkcenter.Brands']", 'null': 'True', 'blank': 'True'}),
            'buy_price': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'buy_time': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'cop': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['networkcenter.Company']", 'null': 'True', 'blank': 'True'}),
            'create_time': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 3, 10, 0, 0)'}),
            'device_sn': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'}),
            'device_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['networkcenter.DeviceType']"}),
            'expired_time': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idc': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['networkcenter.IDC']", 'null': 'True', 'blank': 'True'}),
            'loc': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['networkcenter.Location']", 'null': 'True', 'blank': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['networkcenter.DeviceModel']", 'null': 'True', 'blank': 'True'}),
            'owt': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['networkcenter.OwnerTeam']", 'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['networkcenter.Position']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'purchase_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'rack': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['networkcenter.Rack']", 'null': 'True', 'blank': 'True'}),
            'remark': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'status': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['networkcenter.Supplier']", 'null': 'True', 'blank': 'True'})
        },
        u'networkcenter.devicedisk': {
            'Meta': {'object_name': 'DeviceDisk'},
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['networkcenter.Device']"}),
            'disk_sn': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'speed': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        u'networkcenter.deviceinerface': {
            'Meta': {'unique_together': "(('name', 'device'),)", 'object_name': 'DeviceInerface'},
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['networkcenter.Device']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['networkcenter.IpAdress']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'link': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['networkcenter.DeviceInerface']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'mac': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'remark': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'status': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'vlan': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        u'networkcenter.devicemem': {
            'Meta': {'object_name': 'DeviceMem'},
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['networkcenter.Device']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mem_sn': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        u'networkcenter.devicemodel': {
            'Meta': {'object_name': 'DeviceModel'},
            'brands': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['networkcenter.Brands']"}),
            'device_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['networkcenter.DeviceType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'remark': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        u'networkcenter.deviceparameter': {
            'Meta': {'unique_together': "(('name', 'device_type'),)", 'object_name': 'DeviceParameter'},
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'device_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['networkcenter.DeviceType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'remark': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'status': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'})
        },
        u'networkcenter.deviceparametervalue': {
            'Meta': {'unique_together': "(('device', 'device_para'),)", 'object_name': 'DeviceParameterValue'},
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['networkcenter.Device']"}),
            'device_para': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['networkcenter.DeviceParameter']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'networkcenter.devicetype': {
            'Meta': {'object_name': 'DeviceType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'remark': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'status': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        u'networkcenter.domain': {
            'Meta': {'object_name': 'Domain'},
            'cop': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['networkcenter.Company']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'registrar': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'remark': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'networkcenter.domainrecord': {
            'Meta': {'object_name': 'DomainRecord'},
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['networkcenter.Domain']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'record_ttl': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'record_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'record_value': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'remark': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'networkcenter.idc': {
            'Meta': {'object_name': 'IDC'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'create_time': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 3, 10, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail': ('django.db.models.fields.EmailField', [], {'max_length': '50', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'remark': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        u'networkcenter.ipadress': {
            'Meta': {'unique_together': "(('name', 'section'),)", 'object_name': 'IpAdress'},
            'category': ('django.db.models.fields.CharField', [], {'default': "'Other'", 'max_length': '20'}),
            'create_time': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 3, 10, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idc': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['networkcenter.IDC']"}),
            'name': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'remark': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['networkcenter.IpSection']"}),
            'status': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'})
        },
        u'networkcenter.ipsection': {
            'Meta': {'unique_together': "(('name', 'idc'),)", 'object_name': 'IpSection'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idc': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['networkcenter.IDC']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'remark': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'networkcenter.location': {
            'Meta': {'object_name': 'Location'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'remark': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        u'networkcenter.ownerteam': {
            'Meta': {'unique_together': "(('name', 'cop'),)", 'object_name': 'OwnerTeam'},
            'cop': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['networkcenter.Company']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'remark': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        u'networkcenter.position': {
            'Meta': {'unique_together': "(('name', 'rack'),)", 'object_name': 'Position'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'rack': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['networkcenter.Rack']"}),
            'remark': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'status': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        u'networkcenter.rack': {
            'Meta': {'unique_together': "(('name', 'idc'),)", 'object_name': 'Rack'},
            'create_time': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 3, 10, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idc': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['networkcenter.IDC']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'remark': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        u'networkcenter.supplier': {
            'Meta': {'object_name': 'Supplier'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail': ('django.db.models.fields.EmailField', [], {'max_length': '50', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'owner': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'remark': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        }
    }

    complete_apps = ['networkcenter']