# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UfsObj'
        db.create_table('objsys_ufsobj', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('full_path', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('ufs_url', self.gf('django.db.models.fields.TextField')()),
            ('uuid', self.gf('django.db.models.fields.CharField')(default='147f6b63-82d6-4fad-87ca-0b17e02b4f07', max_length=60)),
            ('head_md5', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('total_md5', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('size', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('valid', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('objsys', ['UfsObj'])

        # Adding M2M table for field relations on 'UfsObj'
        m2m_table_name = db.shorten_name('objsys_ufsobj_relations')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_ufsobj', models.ForeignKey(orm['objsys.ufsobj'], null=False)),
            ('to_ufsobj', models.ForeignKey(orm['objsys.ufsobj'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_ufsobj_id', 'to_ufsobj_id'])

        # Adding model 'CollectionItem'
        db.create_table('objsys_collectionitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('obj', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['objsys.UfsObj'])),
            ('uuid', self.gf('django.db.models.fields.CharField')(default='a56beab3-fafa-4d7c-ac4d-08fed65d9d54', max_length=60)),
            ('id_in_col', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('objsys', ['CollectionItem'])


    def backwards(self, orm):
        # Deleting model 'UfsObj'
        db.delete_table('objsys_ufsobj')

        # Removing M2M table for field relations on 'UfsObj'
        db.delete_table(db.shorten_name('objsys_ufsobj_relations'))

        # Deleting model 'CollectionItem'
        db.delete_table('objsys_collectionitem')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'objsys.collectionitem': {
            'Meta': {'object_name': 'CollectionItem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_in_col': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'obj': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['objsys.UfsObj']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'d35b9541-389c-4a89-b672-bd6519a215e4'", 'max_length': '60'})
        },
        'objsys.ufsobj': {
            'Meta': {'object_name': 'UfsObj'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'full_path': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'head_md5': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'relations': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'relations_rel_+'", 'null': 'True', 'to': "orm['objsys.UfsObj']"}),
            'size': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'total_md5': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'ufs_url': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'0510c6ee-4483-4a9a-9e92-a548813cec44'", 'max_length': '60'}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['objsys']