# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'OSInstallQueue', fields ['sn']
        db.delete_unique(u'networkcenter_osinstallqueue', ['sn'])

        # Deleting model 'OSInstallHistory'
        db.delete_table(u'networkcenter_osinstallhistory')

        # Adding field 'OSInstallQueue.tp_type'
        db.add_column(u'networkcenter_osinstallqueue', 'tp_type',
                      self.gf('django.db.models.fields.CharField')(default='RHEL', max_length=20),
                      keep_default=False)

        # Adding field 'OSInstallQueue.install'
        db.add_column(u'networkcenter_osinstallqueue', 'install',
                      self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True),
                      keep_default=False)

        # Adding field 'OSInstallQueue.deliver'
        db.add_column(u'networkcenter_osinstallqueue', 'deliver',
                      self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True),
                      keep_default=False)

        # Adding field 'OSInstallQueue.ilo_ip'
        db.add_column(u'networkcenter_osinstallqueue', 'ilo_ip',
                      self.gf('django.db.models.fields.CharField')(default=2005, max_length=50),
                      keep_default=False)

        # Adding field 'OSInstallQueue.os_ip'
        db.add_column(u'networkcenter_osinstallqueue', 'os_ip',
                      self.gf('django.db.models.fields.CharField')(default=2005, max_length=50),
                      keep_default=False)

        # Adding field 'OSInstallQueue.create_user'
        db.add_column(u'networkcenter_osinstallqueue', 'create_user',
                      self.gf('django.db.models.fields.CharField')(default=2005, max_length=10),
                      keep_default=False)


        # Changing field 'OSInstallQueue.status'
        db.alter_column(u'networkcenter_osinstallqueue', 'status', self.gf('django.db.models.fields.CharField')(max_length=10))

    def backwards(self, orm):
        # Adding model 'OSInstallHistory'
        db.create_table(u'networkcenter_osinstallhistory', (
            ('use_time', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('num_time', self.gf('django.db.models.fields.IntegerField')(default=0)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sn', self.gf('django.db.models.fields.CharField')(max_length=25, unique=True)),
        ))
        db.send_create_signal(u'networkcenter', ['OSInstallHistory'])

        # Deleting field 'OSInstallQueue.tp_type'
        db.delete_column(u'networkcenter_osinstallqueue', 'tp_type')

        # Deleting field 'OSInstallQueue.install'
        db.delete_column(u'networkcenter_osinstallqueue', 'install')

        # Deleting field 'OSInstallQueue.deliver'
        db.delete_column(u'networkcenter_osinstallqueue', 'deliver')

        # Deleting field 'OSInstallQueue.ilo_ip'
        db.delete_column(u'networkcenter_osinstallqueue', 'ilo_ip')

        # Deleting field 'OSInstallQueue.os_ip'
        db.delete_column(u'networkcenter_osinstallqueue', 'os_ip')

        # Deleting field 'OSInstallQueue.create_user'
        db.delete_column(u'networkcenter_osinstallqueue', 'create_user')


        # Changing field 'OSInstallQueue.status'
        db.alter_column(u'networkcenter_osinstallqueue', 'status', self.gf('django.db.models.fields.NullBooleanField')(null=True))
        # Adding unique constraint on 'OSInstallQueue', fields ['sn']
        db.create_unique(u'networkcenter_osinstallqueue', ['sn'])


    models = {
        u'networkcenter.device': {
            'Meta': {'object_name': 'Device'},
            'asset_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'buy_price': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'buy_time': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'create_time': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 6, 3, 0, 0)'}),
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
            'create_time': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 6, 3, 0, 0)'}),
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
            'create_time': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 6, 3, 0, 0)'}),
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
        u'networkcenter.osinstallqueue': {
            'Meta': {'object_name': 'OSInstallQueue'},
            'create_user': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'ctime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 3, 0, 0)'}),
            'deliver': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ilo_ip': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'install': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'os_ip': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'schedule': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'sn': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'00'", 'max_length': '10'}),
            'tp_type': ('django.db.models.fields.CharField', [], {'default': "'RHEL'", 'max_length': '20'})
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
            'create_time': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 6, 3, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idc': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['networkcenter.IDC']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'remark': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        }
    }

    complete_apps = ['networkcenter']