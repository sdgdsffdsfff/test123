# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Service', fields ['name']
        db.delete_unique(u'systemcenter_service', ['name'])

        # Adding unique constraint on 'Service', fields ['name', 'host']
        db.create_unique(u'systemcenter_service', ['name', 'host_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Service', fields ['name', 'host']
        db.delete_unique(u'systemcenter_service', ['name', 'host_id'])

        # Adding unique constraint on 'Service', fields ['name']
        db.create_unique(u'systemcenter_service', ['name'])


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
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
        u'networkcenter.devicemodel': {
            'Meta': {'object_name': 'DeviceModel'},
            'brands': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['networkcenter.Brands']"}),
            'device_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['networkcenter.DeviceType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'remark': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
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
        },
        u'systemcenter.host': {
            'Meta': {'object_name': 'Host'},
            'device': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['networkcenter.Device']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_check': ('django.db.models.fields.NullBooleanField', [], {'default': 'True', 'null': 'True', 'blank': 'True'}),
            'is_install': ('django.db.models.fields.NullBooleanField', [], {'default': 'True', 'null': 'True', 'blank': 'True'}),
            'is_run': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'is_virtual': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'owt': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['networkcenter.OwnerTeam']", 'null': 'True', 'blank': 'True'}),
            'pdl': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['systemcenter.ProductLine']", 'null': 'True', 'blank': 'True'}),
            'phy_host': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['systemcenter.Host']", 'null': 'True', 'blank': 'True'}),
            'sys': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['systemcenter.SubSystem']", 'null': 'True', 'blank': 'True'}),
            'sysgroup': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['systemcenter.SysGroup']", 'null': 'True', 'blank': 'True'})
        },
        u'systemcenter.hostinfo': {
            'Meta': {'object_name': 'HostInfo'},
            'host': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['systemcenter.Host']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'os_distribute': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'os_kernel': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'os_type': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'})
        },
        u'systemcenter.productline': {
            'Meta': {'object_name': 'ProductLine'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'remark': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        u'systemcenter.service': {
            'Meta': {'unique_together': "(('name', 'host'),)", 'object_name': 'Service'},
            'host': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['systemcenter.Host']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'port': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'remark': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'status': ('django.db.models.fields.NullBooleanField', [], {'default': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'systemcenter.subsystem': {
            'Meta': {'unique_together': "(('name', 'pdl'),)", 'object_name': 'SubSystem'},
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['networkcenter.Domain']", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'pdl': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['systemcenter.ProductLine']"}),
            'remark': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        u'systemcenter.sysgroup': {
            'Meta': {'unique_together': "(('name', 'subsys'),)", 'object_name': 'SysGroup'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'remark': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'subsys': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['systemcenter.SubSystem']"}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        }
    }

    complete_apps = ['systemcenter']