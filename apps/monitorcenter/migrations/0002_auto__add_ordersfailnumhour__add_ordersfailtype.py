# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'OrdersFailNumHour'
        db.create_table(u'monitorcenter_ordersfailnumhour', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('record_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('fail_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monitorcenter.OrdersFailType'])),
            ('order_num', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'monitorcenter', ['OrdersFailNumHour'])

        # Adding model 'OrdersFailType'
        db.create_table(u'monitorcenter_ordersfailtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type_id', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('remask', self.gf('django.db.models.fields.CharField')(max_length=511, null=True, blank=True)),
        ))
        db.send_create_signal(u'monitorcenter', ['OrdersFailType'])


    def backwards(self, orm):
        # Deleting model 'OrdersFailNumHour'
        db.delete_table(u'monitorcenter_ordersfailnumhour')

        # Deleting model 'OrdersFailType'
        db.delete_table(u'monitorcenter_ordersfailtype')


    models = {
        u'monitorcenter.cactihost': {
            'Meta': {'object_name': 'CactiHost'},
            'host': ('django.db.models.fields.CharField', [], {'max_length': '511', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'monitorcenter.graphsgroup': {
            'Meta': {'object_name': 'GraphsGroup'},
            'cacti_host': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monitorcenter.CactiHost']"}),
            'graph_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'monitorcenter.ordersfailnumhour': {
            'Meta': {'object_name': 'OrdersFailNumHour'},
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
        }
    }

    complete_apps = ['monitorcenter']