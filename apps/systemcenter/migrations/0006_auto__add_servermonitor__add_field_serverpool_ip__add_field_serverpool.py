# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'ServerPool', fields ['hostname']
        db.delete_unique(u'systemcenter_serverpool', ['hostname'])

        # Adding model 'ServerMonitor'
        db.create_table(u'systemcenter_servermonitor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('server', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['systemcenter.ServerPool'])),
            ('graph_id', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'systemcenter', ['ServerMonitor'])

        # Adding field 'ServerPool.ip'
        db.add_column(u'systemcenter_serverpool', 'ip',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True),
                      keep_default=False)

        # Adding field 'ServerPool.description'
        db.add_column(u'systemcenter_serverpool', 'description',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True),
                      keep_default=False)


        # Changing field 'ServerPool.status'
        db.alter_column(u'systemcenter_serverpool', 'status', self.gf('django.db.models.fields.CharField')(max_length=10))

    def backwards(self, orm):
        # Deleting model 'ServerMonitor'
        db.delete_table(u'systemcenter_servermonitor')

        # Deleting field 'ServerPool.ip'
        db.delete_column(u'systemcenter_serverpool', 'ip')

        # Deleting field 'ServerPool.description'
        db.delete_column(u'systemcenter_serverpool', 'description')


        # Changing field 'ServerPool.status'
        db.alter_column(u'systemcenter_serverpool', 'status', self.gf('django.db.models.fields.NullBooleanField')(null=True))
        # Adding unique constraint on 'ServerPool', fields ['hostname']
        db.create_unique(u'systemcenter_serverpool', ['hostname'])


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
        u'systemcenter.servermonitor': {
            'Meta': {'object_name': 'ServerMonitor'},
            'graph_id': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['systemcenter.ServerPool']"})
        },
        u'systemcenter.serverpool': {
            'Meta': {'object_name': 'ServerPool'},
            'collect': ('django.db.models.fields.NullBooleanField', [], {'default': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'detect': ('django.db.models.fields.NullBooleanField', [], {'default': 'True', 'null': 'True', 'blank': 'True'}),
            'dever': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'dever'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'fronter': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'fronter'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'host': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['systemcenter.ServerPool']", 'null': 'True', 'blank': 'True'}),
            'hostname': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'install': ('django.db.models.fields.NullBooleanField', [], {'default': 'True', 'null': 'True', 'blank': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'is_vrt': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'oper': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'oper'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'os_kernel': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'os_release': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'os_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'sn': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'00'", 'max_length': '10'}),
            'tag': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['systemcenter.SystemTag']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'systemcenter.serversla': {
            'Meta': {'object_name': 'ServerSLA'},
            'creat_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'down_sum': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'down_time': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['systemcenter.ServerPool']"})
        },
        u'systemcenter.serversoftversion': {
            'Meta': {'object_name': 'ServerSoftVersion'},
            'current_use_releases': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'install_path': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['systemcenter.ServerPool']"}),
            'software': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['systemcenter.SoftWare']"})
        },
        u'systemcenter.software': {
            'Meta': {'object_name': 'SoftWare'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_releases': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'}),
            'remask': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'systemcenter.systemlevel': {
            'Meta': {'object_name': 'SystemLevel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_need': ('django.db.models.fields.NullBooleanField', [], {'default': 'True', 'null': 'True', 'blank': 'True'}),
            'is_relation': ('django.db.models.fields.NullBooleanField', [], {'default': 'True', 'null': 'True', 'blank': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'remask': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'systemcenter.systemtag': {
            'Meta': {'unique_together': "(('tag', 'level'),)", 'object_name': 'SystemTag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['systemcenter.SystemLevel']"}),
            'remask': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['systemcenter']