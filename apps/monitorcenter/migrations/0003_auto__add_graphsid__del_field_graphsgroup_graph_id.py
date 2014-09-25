# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GraphsID'
        db.create_table(u'monitorcenter_graphsid', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('graph_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('graph_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monitorcenter.GraphsGroup'])),
        ))
        db.send_create_signal(u'monitorcenter', ['GraphsID'])

        # Deleting field 'GraphsGroup.graph_id'
        db.delete_column(u'monitorcenter_graphsgroup', 'graph_id')


    def backwards(self, orm):
        # Deleting model 'GraphsID'
        db.delete_table(u'monitorcenter_graphsid')

        # Adding field 'GraphsGroup.graph_id'
        db.add_column(u'monitorcenter_graphsgroup', 'graph_id',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)


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