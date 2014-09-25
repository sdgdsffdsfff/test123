# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CactiHost'
        db.create_table(u'monitorcenter_cactihost', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=511, null=True, blank=True)),
        ))
        db.send_create_signal(u'monitorcenter', ['CactiHost'])

        # Adding model 'GraphsGroup'
        db.create_table(u'monitorcenter_graphsgroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('graph_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('cacti_host', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monitorcenter.CactiHost'])),
        ))
        db.send_create_signal(u'monitorcenter', ['GraphsGroup'])


    def backwards(self, orm):
        # Deleting model 'CactiHost'
        db.delete_table(u'monitorcenter_cactihost')

        # Deleting model 'GraphsGroup'
        db.delete_table(u'monitorcenter_graphsgroup')


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
        }
    }

    complete_apps = ['monitorcenter']