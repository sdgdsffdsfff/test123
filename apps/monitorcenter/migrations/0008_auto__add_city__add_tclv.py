# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'City'
        db.create_table(u'monitorcenter_city', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'monitorcenter', ['City'])

        # Adding model 'Tclv'
        db.create_table(u'monitorcenter_tclv', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('record_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monitorcenter.City'])),
            ('tclv', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'monitorcenter', ['Tclv'])


    def backwards(self, orm):
        # Deleting model 'City'
        db.delete_table(u'monitorcenter_city')

        # Deleting model 'Tclv'
        db.delete_table(u'monitorcenter_tclv')


    models = {
        u'monitorcenter.cactihost': {
            'Meta': {'object_name': 'CactiHost'},
            'host': ('django.db.models.fields.CharField', [], {'max_length': '511', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'monitorcenter.city': {
            'Meta': {'object_name': 'City'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'monitorcenter.graphsgroup': {
            'Meta': {'object_name': 'GraphsGroup'},
            'cacti_host': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monitorcenter.CactiHost']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'monitorcenter.graphsid': {
            'Meta': {'object_name': 'GraphsID'},
            'graph_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monitorcenter.GraphsGroup']"}),
            'graph_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'monitorcenter.ordersfailnumhour': {
            'Meta': {'unique_together': "(('record_time', 'fail_type'),)", 'object_name': 'OrdersFailNumHour'},
            'fail_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monitorcenter.OrdersFailType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order_num': ('django.db.models.fields.IntegerField', [], {}),
            'record_time': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'monitorcenter.ordersfailtype': {
            'Meta': {'object_name': 'OrdersFailType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'remask': ('django.db.models.fields.CharField', [], {'max_length': '511', 'null': 'True', 'blank': 'True'}),
            'type_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'})
        },
        u'monitorcenter.shifttable': {
            'Meta': {'object_name': 'ShiftTable'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'month': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'shift_id': ('django.db.models.fields.IntegerField', [], {}),
            'years': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'monitorcenter.tclv': {
            'Meta': {'object_name': 'Tclv'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monitorcenter.City']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'record_time': ('django.db.models.fields.DateTimeField', [], {}),
            'tclv': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['monitorcenter']