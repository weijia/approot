# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'CollectionItem'
        db.delete_table('objsys_collectionitem')

        # Adding model 'ObjRelation'
        db.create_table('objsys_objrelation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_obj', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='from', null=True, to=orm['objsys.UfsObj'])),
            ('to_obj', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='to', null=True, to=orm['objsys.UfsObj'])),
            ('relation', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('valid', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('objsys', ['ObjRelation'])

        # Adding field 'UfsObj.obj_created'
        db.add_column('objsys_ufsobj', 'obj_created',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'UfsObj.obj_last_modified'
        db.add_column('objsys_ufsobj', 'obj_last_modified',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'CollectionItem'
        db.create_table('objsys_collectionitem', (
            ('id_in_col', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('obj', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['objsys.UfsObj'])),
            ('uuid', self.gf('django.db.models.fields.CharField')(default='288051d6-2101-4536-a1bb-ca673a45824d', max_length=60)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('objsys', ['CollectionItem'])

        # Deleting model 'ObjRelation'
        db.delete_table('objsys_objrelation')

        # Deleting field 'UfsObj.obj_created'
        db.delete_column('objsys_ufsobj', 'obj_created')

        # Deleting field 'UfsObj.obj_last_modified'
        db.delete_column('objsys_ufsobj', 'obj_last_modified')


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
        'objsys.description': {
            'Meta': {'object_name': 'Description'},
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'objsys.objrelation': {
            'Meta': {'object_name': 'ObjRelation'},
            'from_obj': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'from'", 'null': 'True', 'to': "orm['objsys.UfsObj']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'relation': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'to_obj': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'to'", 'null': 'True', 'to': "orm['objsys.UfsObj']"}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'objsys.ufsobj': {
            'Meta': {'object_name': 'UfsObj'},
            'description_json': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'descriptions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'descriptions'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['objsys.Description']"}),
            'full_path': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'head_md5': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'obj_created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'obj_last_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'relations': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'relations_rel_+'", 'null': 'True', 'to': "orm['objsys.UfsObj']"}),
            'size': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'total_md5': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'ufs_url': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'c3ff7db4-34c2-4a5a-a334-a2fec1f63460'", 'max_length': '60'}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['objsys']