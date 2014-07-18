# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Report'
        db.create_table(u'core_report', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['locations.Location'])),
            ('reporter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workers.Worker'])),
            ('data', self.gf(u'django_hstore.fields.DictionaryField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Report'])


    def backwards(self, orm):
        # Deleting model 'Report'
        db.delete_table(u'core_report')


    models = {
        u'core.report': {
            'Meta': {'object_name': 'Report'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data': (u'django_hstore.fields.DictionaryField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['locations.Location']"}),
            'reporter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['workers.Worker']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'locations.location': {
            'Meta': {'object_name': 'Location'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'location_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'locations'", 'to': u"orm['locations.LocationType']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'to': u"orm['locations.Location']", 'null': 'True', 'blank': 'True'}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'locations.locationtype': {
            'Meta': {'object_name': 'LocationType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'rapidsms.contact': {
            'Meta': {'object_name': 'Contact'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'workers.role': {
            'Meta': {'object_name': 'Role'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'workers.worker': {
            'Meta': {'object_name': 'Worker'},
            'contact': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'worker'", 'unique': 'True', 'null': 'True', 'to': u"orm['rapidsms.Contact']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['locations.Location']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['workers.Role']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['core']