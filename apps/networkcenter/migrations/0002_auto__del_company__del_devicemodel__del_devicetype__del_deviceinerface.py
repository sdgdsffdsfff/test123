# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'DeviceParameterValue', fields ['device', 'device_para']
        db.delete_unique(u'networkcenter_deviceparametervalue', ['device_id', 'device_para_id'])

        # Removing unique constraint on 'DeviceParameter', fields ['name', 'device_type']
        db.delete_unique(u'networkcenter_deviceparameter', ['name', 'device_type_id'])

        # Removing unique constraint on 'OwnerTeam', fields ['name', 'cop']
        db.delete_unique(u'networkcenter_ownerteam', ['name', 'cop_id'])

        # Removing unique constraint on 'DeviceInerface', fields ['name', 'device']
        db.delete_unique(u'networkcenter_deviceinerface', ['name', 'device_id'])

        # Deleting model 'Company'
        db.delete_table(u'networkcenter_company')

        # Deleting model 'DeviceModel'
        db.delete_table(u'networkcenter_devicemodel')

        # Deleting model 'DeviceType'
        db.delete_table(u'networkcenter_devicetype')

        # Deleting model 'DeviceInerface'
        db.delete_table(u'networkcenter_deviceinerface')

        # Deleting model 'OwnerTeam'
        db.delete_table(u'networkcenter_ownerteam')

        # Deleting model 'DeviceParameter'
        db.delete_table(u'networkcenter_deviceparameter')

        # Deleting model 'Location'
        db.delete_table(u'networkcenter_location')

        # Deleting model 'Supplier'
        db.delete_table(u'networkcenter_supplier')

        # Deleting model 'DeviceParameterValue'
        db.delete_table(u'networkcenter_deviceparametervalue')

        # Deleting model 'Brands'
        db.delete_table(u'networkcenter_brands')

        # Adding model 'DeviceCPU'
        db.create_table(u'networkcenter_devicecpu', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.Device'])),
            ('product', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('vendor', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('slot', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
        ))
        db.send_create_signal(u'networkcenter', ['DeviceCPU'])

        # Adding model 'DeviceTag'
        db.create_table(u'networkcenter_devicetag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('remask', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('level', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.DeviceLevel'])),
        ))
        db.send_create_signal(u'networkcenter', ['DeviceTag'])

        # Adding unique constraint on 'DeviceTag', fields ['tag', 'level']
        db.create_unique(u'networkcenter_devicetag', ['tag', 'level_id'])

        # Adding model 'DeviceNIC'
        db.create_table(u'networkcenter_devicenic', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.Device'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('product', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('vendor', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('mac', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('speed', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('ip', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['networkcenter.IpAdress'], unique=True, null=True, blank=True)),
            ('vlan', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('link', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['networkcenter.DeviceNIC'], unique=True, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
            ('remark', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'networkcenter', ['DeviceNIC'])

        # Adding unique constraint on 'DeviceNIC', fields ['name', 'device']
        db.create_unique(u'networkcenter_devicenic', ['name', 'device_id'])

        # Adding model 'OSInstallQueue'
        db.create_table(u'networkcenter_osinstallqueue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sn', self.gf('django.db.models.fields.CharField')(unique=True, max_length=25)),
            ('status', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
            ('schedule', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('ctime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'networkcenter', ['OSInstallQueue'])

        # Adding model 'DeviceLevel'
        db.create_table(u'networkcenter_devicelevel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('level', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10)),
            ('remask', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('is_need', self.gf('django.db.models.fields.NullBooleanField')(default=True, null=True, blank=True)),
            ('is_relation', self.gf('django.db.models.fields.NullBooleanField')(default=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'networkcenter', ['DeviceLevel'])

        # Adding model 'OSInstallHistory'
        db.create_table(u'networkcenter_osinstallhistory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sn', self.gf('django.db.models.fields.CharField')(unique=True, max_length=25)),
            ('num_time', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('use_time', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'networkcenter', ['OSInstallHistory'])

        # Adding model 'DevicePower'
        db.create_table(u'networkcenter_devicepower', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.Device'])),
            ('power_sn', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('vendor', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('slot', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
        ))
        db.send_create_signal(u'networkcenter', ['DevicePower'])

        # Deleting field 'Device.cop'
        db.delete_column(u'networkcenter_device', 'cop_id')

        # Deleting field 'Device.loc'
        db.delete_column(u'networkcenter_device', 'loc_id')

        # Deleting field 'Device.device_sn'
        db.delete_column(u'networkcenter_device', 'device_sn')

        # Deleting field 'Device.device_type'
        db.delete_column(u'networkcenter_device', 'device_type_id')

        # Deleting field 'Device.brands'
        db.delete_column(u'networkcenter_device', 'brands_id')

        # Deleting field 'Device.owt'
        db.delete_column(u'networkcenter_device', 'owt_id')

        # Deleting field 'Device.model'
        db.delete_column(u'networkcenter_device', 'model_id')

        # Deleting field 'Device.supplier'
        db.delete_column(u'networkcenter_device', 'supplier_id')

        # Adding field 'Device.sn'
        db.add_column(u'networkcenter_device', 'sn',
                      self.gf('django.db.models.fields.CharField')(default=1990, unique=True, max_length=25),
                      keep_default=False)

        # Adding M2M table for field tag on 'Device'
        m2m_table_name = db.shorten_name(u'networkcenter_device_tag')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('device', models.ForeignKey(orm[u'networkcenter.device'], null=False)),
            ('devicetag', models.ForeignKey(orm[u'networkcenter.devicetag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['device_id', 'devicetag_id'])

        # Deleting field 'DeviceMem.mem_sn'
        db.delete_column(u'networkcenter_devicemem', 'mem_sn')

        # Adding field 'DeviceMem.vendor'
        db.add_column(u'networkcenter_devicemem', 'vendor',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True),
                      keep_default=False)

        # Adding field 'DeviceMem.version'
        db.add_column(u'networkcenter_devicemem', 'version',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True),
                      keep_default=False)

        # Adding field 'DeviceDisk.vendor'
        db.add_column(u'networkcenter_devicedisk', 'vendor',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True),
                      keep_default=False)

        # Adding field 'DeviceDisk.version'
        db.add_column(u'networkcenter_devicedisk', 'version',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True),
                      keep_default=False)

        # Deleting field 'Domain.cop'
        db.delete_column(u'networkcenter_domain', 'cop_id')


    def backwards(self, orm):
        # Removing unique constraint on 'DeviceNIC', fields ['name', 'device']
        db.delete_unique(u'networkcenter_devicenic', ['name', 'device_id'])

        # Removing unique constraint on 'DeviceTag', fields ['tag', 'level']
        db.delete_unique(u'networkcenter_devicetag', ['tag', 'level_id'])

        # Adding model 'Company'
        db.create_table(u'networkcenter_company', (
            ('remark', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True)),
        ))
        db.send_create_signal(u'networkcenter', ['Company'])

        # Adding model 'DeviceModel'
        db.create_table(u'networkcenter_devicemodel', (
            ('remark', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('device_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.DeviceType'])),
            ('brands', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.Brands'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'networkcenter', ['DeviceModel'])

        # Adding model 'DeviceType'
        db.create_table(u'networkcenter_devicetype', (
            ('status', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
            ('remark', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'networkcenter', ['DeviceType'])

        # Adding model 'DeviceInerface'
        db.create_table(u'networkcenter_deviceinerface', (
            ('status', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
            ('mac', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('link', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['networkcenter.DeviceInerface'], unique=True, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.Device'])),
            ('ip', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['networkcenter.IpAdress'], unique=True, null=True, blank=True)),
            ('vlan', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('remark', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'networkcenter', ['DeviceInerface'])

        # Adding unique constraint on 'DeviceInerface', fields ['name', 'device']
        db.create_unique(u'networkcenter_deviceinerface', ['name', 'device_id'])

        # Adding model 'OwnerTeam'
        db.create_table(u'networkcenter_ownerteam', (
            ('cop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.Company'])),
            ('remark', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'networkcenter', ['OwnerTeam'])

        # Adding unique constraint on 'OwnerTeam', fields ['name', 'cop']
        db.create_unique(u'networkcenter_ownerteam', ['name', 'cop_id'])

        # Adding model 'DeviceParameter'
        db.create_table(u'networkcenter_deviceparameter', (
            ('status', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
            ('remark', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True)),
            ('device_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.DeviceType'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('desc', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
        ))
        db.send_create_signal(u'networkcenter', ['DeviceParameter'])

        # Adding unique constraint on 'DeviceParameter', fields ['name', 'device_type']
        db.create_unique(u'networkcenter_deviceparameter', ['name', 'device_type_id'])

        # Adding model 'Location'
        db.create_table(u'networkcenter_location', (
            ('remark', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True)),
        ))
        db.send_create_signal(u'networkcenter', ['Location'])

        # Adding model 'Supplier'
        db.create_table(u'networkcenter_supplier', (
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('remark', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True)),
            ('owner', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('mail', self.gf('django.db.models.fields.EmailField')(max_length=50, blank=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'networkcenter', ['Supplier'])

        # Adding model 'DeviceParameterValue'
        db.create_table(u'networkcenter_deviceparametervalue', (
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.Device'])),
            ('device_para', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.DeviceParameter'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'networkcenter', ['DeviceParameterValue'])

        # Adding unique constraint on 'DeviceParameterValue', fields ['device', 'device_para']
        db.create_unique(u'networkcenter_deviceparametervalue', ['device_id', 'device_para_id'])

        # Adding model 'Brands'
        db.create_table(u'networkcenter_brands', (
            ('remark', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True)),
        ))
        db.send_create_signal(u'networkcenter', ['Brands'])

        # Deleting model 'DeviceCPU'
        db.delete_table(u'networkcenter_devicecpu')

        # Deleting model 'DeviceTag'
        db.delete_table(u'networkcenter_devicetag')

        # Deleting model 'DeviceNIC'
        db.delete_table(u'networkcenter_devicenic')

        # Deleting model 'OSInstallQueue'
        db.delete_table(u'networkcenter_osinstallqueue')

        # Deleting model 'DeviceLevel'
        db.delete_table(u'networkcenter_devicelevel')

        # Deleting model 'OSInstallHistory'
        db.delete_table(u'networkcenter_osinstallhistory')

        # Deleting model 'DevicePower'
        db.delete_table(u'networkcenter_devicepower')

        # Adding field 'Device.cop'
        db.add_column(u'networkcenter_device', 'cop',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.Company'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Device.loc'
        db.add_column(u'networkcenter_device', 'loc',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.Location'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Device.device_sn'
        db.add_column(u'networkcenter_device', 'device_sn',
                      self.gf('django.db.models.fields.CharField')(default=1990, max_length=25, unique=True),
                      keep_default=False)

        # Adding field 'Device.device_type'
        db.add_column(u'networkcenter_device', 'device_type',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1990, to=orm['networkcenter.DeviceType']),
                      keep_default=False)

        # Adding field 'Device.brands'
        db.add_column(u'networkcenter_device', 'brands',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.Brands'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Device.owt'
        db.add_column(u'networkcenter_device', 'owt',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.OwnerTeam'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Device.model'
        db.add_column(u'networkcenter_device', 'model',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.DeviceModel'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Device.supplier'
        db.add_column(u'networkcenter_device', 'supplier',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.Supplier'], null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Device.sn'
        db.delete_column(u'networkcenter_device', 'sn')

        # Removing M2M table for field tag on 'Device'
        db.delete_table(db.shorten_name(u'networkcenter_device_tag'))

        # Adding field 'DeviceMem.mem_sn'
        db.add_column(u'networkcenter_devicemem', 'mem_sn',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True),
                      keep_default=False)

        # Deleting field 'DeviceMem.vendor'
        db.delete_column(u'networkcenter_devicemem', 'vendor')

        # Deleting field 'DeviceMem.version'
        db.delete_column(u'networkcenter_devicemem', 'version')

        # Deleting field 'DeviceDisk.vendor'
        db.delete_column(u'networkcenter_devicedisk', 'vendor')

        # Deleting field 'DeviceDisk.version'
        db.delete_column(u'networkcenter_devicedisk', 'version')

        # Adding field 'Domain.cop'
        db.add_column(u'networkcenter_domain', 'cop',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.Company'], null=True, blank=True),
                      keep_default=False)


    models = {
        u'networkcenter.device': {
            'Meta': {'object_name': 'Device'},
            'asset_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'buy_price': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'buy_time': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'create_time': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 5, 19, 0, 0)'}),
            'expired_time': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idc': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['networkcenter.IDC']", 'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['networkcenter.Position']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'purchase_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'rack': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['networkcenter.Rack']", 'null': 'True', 'blank': 'True'}),
            'remark': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'sn': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'}),
            'status': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'tag': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['networkcenter.DeviceTag']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'networkcenter.devicecpu': {
            'Meta': {'object_name': 'DeviceCPU'},
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['networkcenter.Device']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'vendor': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'networkcenter.devicedisk': {
            'Meta': {'object_name': 'DeviceDisk'},
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['networkcenter.Device']"}),
            'disk_sn': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'speed': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'vendor': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'networkcenter.devicelevel': {
            'Meta': {'object_name': 'DeviceLevel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_need': ('django.db.models.fields.NullBooleanField', [], {'default': 'True', 'null': 'True', 'blank': 'True'}),
            'is_relation': ('django.db.models.fields.NullBooleanField', [], {'default': 'True', 'null': 'True', 'blank': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'remask': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'networkcenter.devicemem': {
            'Meta': {'object_name': 'DeviceMem'},
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['networkcenter.Device']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'vendor': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'networkcenter.devicenic': {
            'Meta': {'unique_together': "(('name', 'device'),)", 'object_name': 'DeviceNIC'},
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['networkcenter.Device']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['networkcenter.IpAdress']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'link': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['networkcenter.DeviceNIC']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'mac': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'product': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'remark': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'speed': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'status': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'vendor': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'vlan': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        u'networkcenter.devicepower': {
            'Meta': {'object_name': 'DevicePower'},
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['networkcenter.Device']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'power_sn': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'vendor': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'networkcenter.devicetag': {
            'Meta': {'unique_together': "(('tag', 'level'),)", 'object_name': 'DeviceTag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['networkcenter.DeviceLevel']"}),
            'remask': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'networkcenter.domain': {
            'Meta': {'object_name': 'Domain'},
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
            'create_time': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 5, 19, 0, 0)'}),
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
            'create_time': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 5, 19, 0, 0)'}),
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
        u'networkcenter.osinstallhistory': {
            'Meta': {'object_name': 'OSInstallHistory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_time': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'sn': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'}),
            'use_time': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'networkcenter.osinstallqueue': {
            'Meta': {'object_name': 'OSInstallQueue'},
            'ctime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'schedule': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'sn': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'}),
            'status': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'})
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
            'create_time': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 5, 19, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idc': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['networkcenter.IDC']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'remark': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        }
    }

    complete_apps = ['networkcenter']