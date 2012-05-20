# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'ArchivrItem.coordinate'
        db.delete_column('archivr_archivritem', 'coordinate')

        # Adding field 'ArchivrItem.latitude'
        db.add_column('archivr_archivritem', 'latitude',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=6, blank=True),
                      keep_default=False)

        # Adding field 'ArchivrItem.longitude'
        db.add_column('archivr_archivritem', 'longitude',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=6, blank=True),
                      keep_default=False)

    def backwards(self, orm):
        # Adding field 'ArchivrItem.coordinate'
        db.add_column('archivr_archivritem', 'coordinate',
                      self.gf('django.contrib.gis.db.models.fields.PointField')(null=True),
                      keep_default=False)

        # Deleting field 'ArchivrItem.latitude'
        db.delete_column('archivr_archivritem', 'latitude')

        # Deleting field 'ArchivrItem.longitude'
        db.delete_column('archivr_archivritem', 'longitude')

    models = {
        'archivr.archivritem': {
            'Meta': {'ordering': "('-order_date',)", 'object_name': 'ArchivrItem'},
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_genre': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '6', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '6', 'blank': 'True'}),
            'order_date': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['archivr']