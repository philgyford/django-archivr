# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ArchivrItem'
        db.create_table('archivr_archivritem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('coordinate', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('item_genre', self.gf('django.db.models.fields.CharField')(default='', max_length=20)),
        ))
        db.send_create_signal('archivr', ['ArchivrItem'])

    def backwards(self, orm):
        # Deleting model 'ArchivrItem'
        db.delete_table('archivr_archivritem')

    models = {
        'archivr.archivritem': {
            'Meta': {'ordering': "('-order_date',)", 'object_name': 'ArchivrItem'},
            'coordinate': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_genre': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            'order_date': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['archivr']