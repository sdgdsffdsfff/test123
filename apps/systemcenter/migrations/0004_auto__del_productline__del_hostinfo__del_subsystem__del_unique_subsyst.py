# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Service', fields ['name', 'host']
        db.delete_unique(u'systemcenter_service', ['name', 'host_id'])

        # Removing unique constraint on 'SysGroup', fields ['name', 'subsys']
        db.delete_unique(u'systemcenter_sysgroup', ['name', 'subsys_id'])

        # Removing unique constraint on 'SubSystem', fields ['name', 'pdl']
        db.delete_unique(u'systemcenter_subsystem', ['name', 'pdl_id'])

        # Deleting model 'ProductLine'
        db.delete_table(u'systemcenter_productline')

        # Deleting model 'HostInfo'
        db.delete_table(u'systemcenter_hostinfo')

        # Deleting model 'SubSystem'
        db.delete_table(u'systemcenter_subsystem')

        # Deleting model 'SysGroup'
        db.delete_table(u'systemcenter_sysgroup')

        # Deleting model 'Host'
        db.delete_table(u'systemcenter_host')

        # Removing M2M table for field sys on 'Host'
        db.delete_table(db.shorten_name(u'systemcenter_host_sys'))

        # Removing M2M table for field pdl on 'Host'
        db.delete_table(db.shorten_name(u'systemcenter_host_pdl'))

        # Removing M2M table for field sysgroup on 'Host'
        db.delete_table(db.shorten_name(u'systemcenter_host_sysgroup'))

        # Deleting model 'Service'
        db.delete_table(u'systemcenter_service')

        # Adding model 'SoftWare'
        db.create_table(u'systemcenter_software', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=25)),
            ('last_releases', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('remask', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'systemcenter', ['SoftWare'])

        # Adding model 'SystemLevel'
        db.create_table(u'systemcenter_systemlevel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('level', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10)),
            ('remask', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('is_need', self.gf('django.db.models.fields.NullBooleanField')(default=True, null=True, blank=True)),
            ('is_relation', self.gf('django.db.models.fields.NullBooleanField')(default=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'systemcenter', ['SystemLevel'])

        # Adding model 'SystemTag'
        db.create_table(u'systemcenter_systemtag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('remask', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('level', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['systemcenter.SystemLevel'])),
        ))
        db.send_create_signal(u'systemcenter', ['SystemTag'])

        # Adding unique constraint on 'SystemTag', fields ['tag', 'level']
        db.create_unique(u'systemcenter_systemtag', ['tag', 'level_id'])

        # Adding model 'ServerPool'
        db.create_table(u'systemcenter_serverpool', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sn', self.gf('django.db.models.fields.CharField')(unique=True, max_length=25)),
            ('hostname', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('os_type', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('os_kernel', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('os_release', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('status', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
            ('install', self.gf('django.db.models.fields.NullBooleanField')(default=True, null=True, blank=True)),
            ('detect', self.gf('django.db.models.fields.NullBooleanField')(default=True, null=True, blank=True)),
            ('collect', self.gf('django.db.models.fields.NullBooleanField')(default=True, null=True, blank=True)),
            ('oper', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='oper', null=True, to=orm['auth.User'])),
            ('fronter', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='fronter', null=True, to=orm['auth.User'])),
            ('dever', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='dever', null=True, to=orm['auth.User'])),
            ('host', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['systemcenter.ServerPool'], null=True, blank=True)),
        ))
        db.send_create_signal(u'systemcenter', ['ServerPool'])

        # Adding M2M table for field tag on 'ServerPool'
        m2m_table_name = db.shorten_name(u'systemcenter_serverpool_tag')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('serverpool', models.ForeignKey(orm[u'systemcenter.serverpool'], null=False)),
            ('systemtag', models.ForeignKey(orm[u'systemcenter.systemtag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['serverpool_id', 'systemtag_id'])

        # Adding model 'ServerSLA'
        db.create_table(u'systemcenter_serversla', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('server', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['systemcenter.ServerPool'])),
            ('down_sum', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('down_time', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('creat_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'systemcenter', ['ServerSLA'])

        # Adding model 'ServerSoftVersion'
        db.create_table(u'systemcenter_serversoftversion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('server', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['systemcenter.ServerPool'])),
            ('software', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['systemcenter.SoftWare'])),
            ('current_use_releases', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('install_path', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'systemcenter', ['ServerSoftVersion'])


    def backwards(self, orm):
        # Removing unique constraint on 'SystemTag', fields ['tag', 'level']
        db.delete_unique(u'systemcenter_systemtag', ['tag', 'level_id'])

        # Adding model 'ProductLine'
        db.create_table(u'systemcenter_productline', (
            ('remark', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True)),
        ))
        db.send_create_signal(u'systemcenter', ['ProductLine'])

        # Adding model 'HostInfo'
        db.create_table(u'systemcenter_hostinfo', (
            ('os_kernel', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('os_distribute', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('host', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['systemcenter.Host'], unique=True)),
            ('os_type', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'systemcenter', ['HostInfo'])

        # Adding model 'SubSystem'
        db.create_table(u'systemcenter_subsystem', (
            ('domain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.DomainRecord'], blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('remark', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('pdl', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['systemcenter.ProductLine'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'systemcenter', ['SubSystem'])

        # Adding unique constraint on 'SubSystem', fields ['name', 'pdl']
        db.create_unique(u'systemcenter_subsystem', ['name', 'pdl_id'])

        # Adding model 'SysGroup'
        db.create_table(u'systemcenter_sysgroup', (
            ('remark', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('subsys', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['systemcenter.SubSystem'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'systemcenter', ['SysGroup'])

        # Adding unique constraint on 'SysGroup', fields ['name', 'subsys']
        db.create_unique(u'systemcenter_sysgroup', ['name', 'subsys_id'])

        # Adding model 'Host'
        db.create_table(u'systemcenter_host', (
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('is_check', self.gf('django.db.models.fields.NullBooleanField')(default=True, null=True, blank=True)),
            ('device', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['networkcenter.Device'], unique=True)),
            ('owt', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['networkcenter.OwnerTeam'], null=True, blank=True)),
            ('is_install', self.gf('django.db.models.fields.NullBooleanField')(default=True, null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('is_run', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
            ('phy_host', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['systemcenter.Host'], null=True, blank=True)),
            ('is_virtual', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
        ))
        db.send_create_signal(u'systemcenter', ['Host'])

        # Adding M2M table for field sys on 'Host'
        m2m_table_name = db.shorten_name(u'systemcenter_host_sys')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('host', models.ForeignKey(orm[u'systemcenter.host'], null=False)),
            ('subsystem', models.ForeignKey(orm[u'systemcenter.subsystem'], null=False))
        ))
        db.create_unique(m2m_table_name, ['host_id', 'subsystem_id'])

        # Adding M2M table for field pdl on 'Host'
        m2m_table_name = db.shorten_name(u'systemcenter_host_pdl')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('host', models.ForeignKey(orm[u'systemcenter.host'], null=False)),
            ('productline', models.ForeignKey(orm[u'systemcenter.productline'], null=False))
        ))
        db.create_unique(m2m_table_name, ['host_id', 'productline_id'])

        # Adding M2M table for field sysgroup on 'Host'
        m2m_table_name = db.shorten_name(u'systemcenter_host_sysgroup')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('host', models.ForeignKey(orm[u'systemcenter.host'], null=False)),
            ('sysgroup', models.ForeignKey(orm[u'systemcenter.sysgroup'], null=False))
        ))
        db.create_unique(m2m_table_name, ['host_id', 'sysgroup_id'])

        # Adding model 'Service'
        db.create_table(u'systemcenter_service', (
            ('status', self.gf('django.db.models.fields.NullBooleanField')(default=True, null=True, blank=True)),
            ('remark', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('host', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['systemcenter.Host'])),
            ('port', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
        ))
        db.send_create_signal(u'systemcenter', ['Service'])

        # Adding unique constraint on 'Service', fields ['name', 'host']
        db.create_unique(u'systemcenter_service', ['name', 'host_id'])

        # Deleting model 'SoftWare'
        db.delete_table(u'systemcenter_software')

        # Deleting model 'SystemLevel'
        db.delete_table(u'systemcenter_systemlevel')

        # Deleting model 'SystemTag'
        db.delete_table(u'systemcenter_systemtag')

        # Deleting model 'ServerPool'
        db.delete_table(u'systemcenter_serverpool')

        # Removing M2M table for field tag on 'ServerPool'
        db.delete_table(db.shorten_name(u'systemcenter_serverpool_tag'))

        # Deleting model 'ServerSLA'
        db.delete_table(u'systemcenter_serversla')

        # Deleting model 'ServerSoftVersion'
        db.delete_table(u'systemcenter_serversoftversion')


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
        u'systemcenter.serverpool': {
            'Meta': {'object_name': 'ServerPool'},
            'collect': ('django.db.models.fields.NullBooleanField', [], {'default': 'True', 'null': 'True', 'blank': 'True'}),
            'detect': ('django.db.models.fields.NullBooleanField', [], {'default': 'True', 'null': 'True', 'blank': 'True'}),
            'dever': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'dever'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'fronter': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'fronter'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'host': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['systemcenter.ServerPool']", 'null': 'True', 'blank': 'True'}),
            'hostname': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'install': ('django.db.models.fields.NullBooleanField', [], {'default': 'True', 'null': 'True', 'blank': 'True'}),
            'oper': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'oper'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'os_kernel': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'os_release': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'os_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'sn': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'}),
            'status': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
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