# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FlickrFavorite'
        db.create_table('archivrflickr_flickrfavorite', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('photo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archivrflickr.FlickrPhoto'])),
            ('favorite_list', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archivrflickr.FlickrFavoriteList'])),
            ('date_faved', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('archivrflickr', ['FlickrFavorite'])

        # Adding model 'FlickrFavoriteList'
        db.create_table('archivrflickr_flickrfavoritelist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archivrflickr.FlickrUser'])),
            ('date_archived', self.gf('django.db.models.fields.DateTimeField')()),
            ('primary', self.gf('django.db.models.fields.related.ForeignKey')(related_name='primary_in', null=True, to=orm['archivrflickr.FlickrPhoto'])),
        ))
        db.send_create_signal('archivrflickr', ['FlickrFavoriteList'])

        # Adding model 'FlickrPhoto'
        db.create_table('archivrflickr_flickrphoto', (
            ('archivritem_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['archivr.ArchivrItem'], unique=True, primary_key=True)),
            ('flickr_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archivrflickr.FlickrUser'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('posted_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('taken_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('taken_granularity', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('comments', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('visibility_is_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('visibility_is_friend', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('visibility_is_family', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('photopage_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('farm', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('server', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('secret', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('original_secret', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('original_format', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('safety_level', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True)),
            ('rotation', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True)),
            ('license', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('large_width', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True)),
            ('large_height', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True)),
            ('largesquare_width', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True)),
            ('largesquare_height', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True)),
            ('medium640_width', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True)),
            ('medium640_height', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True)),
            ('medium800_width', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True)),
            ('medium800_height', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True)),
            ('medium_width', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True)),
            ('medium_height', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True)),
            ('original_width', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True)),
            ('original_height', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True)),
            ('small320_width', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True)),
            ('small320_height', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True)),
            ('small_width', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True)),
            ('small_height', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True)),
            ('square_width', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True)),
            ('square_height', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True)),
            ('thumbnail_width', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True)),
            ('thumbnail_height', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True)),
            ('is_video', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('video_duration', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('video_width', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True)),
            ('video_height', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True)),
            ('geo_latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('geo_longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('geo_accuracy', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('geo_place_id', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('geo_woe_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('geo_county', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('geo_county_place_id', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('geo_county_woe_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('geo_country', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('geo_country_place_id', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('geo_country_woe_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('geo_locality', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('geo_locality_place_id', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('geo_locality_woe_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('geo_neighbourhood', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('geo_neighbourhood_place_id', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('geo_neighbourhood_woe_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('geo_region', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('geo_region_place_id', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('geo_region_woe_id', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=50, null=True, blank=True)),
            ('geo_perms_is_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('geo_perms_is_contact', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('geo_perms_is_friend', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('geo_perms_is_family', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('exif_aperture', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('exif_color_space', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('exif_exposure', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('exif_flash', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('exif_focal_length', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('exif_iso', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('exif_make', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('exif_metering_mode', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('exif_model', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('exif_orientation', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('exif_software', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('archivrflickr', ['FlickrPhoto'])

        # Adding model 'FlickrPhotoComment'
        db.create_table('archivrflickr_flickrphotocomment', (
            ('flickr_id', self.gf('django.db.models.fields.CharField')(max_length=128, primary_key=True)),
            ('photo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archivrflickr.FlickrPhoto'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archivrflickr.FlickrUser'])),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('permanent_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('comment', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('archivrflickr', ['FlickrPhotoComment'])

        # Adding model 'FlickrPhotoset'
        db.create_table('archivrflickr_flickrphotoset', (
            ('flickr_id', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
            ('primary', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='primary_photo_set', null=True, to=orm['archivrflickr.FlickrPhoto'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archivrflickr.FlickrUser'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('order', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
        ))
        db.send_create_signal('archivrflickr', ['FlickrPhotoset'])

        # Adding M2M table for field photos on 'FlickrPhotoset'
        db.create_table('archivrflickr_flickrphotoset_photos', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('flickrphotoset', models.ForeignKey(orm['archivrflickr.flickrphotoset'], null=False)),
            ('flickrphoto', models.ForeignKey(orm['archivrflickr.flickrphoto'], null=False))
        ))
        db.create_unique('archivrflickr_flickrphotoset_photos', ['flickrphotoset_id', 'flickrphoto_id'])

        # Adding model 'FlickrPhotoTag'
        db.create_table('archivrflickr_flickrphototag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(related_name='archivrflickr_flickrphototag_items', to=orm['taggit.Tag'])),
            ('flickr_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archivrflickr.FlickrUser'])),
            ('machine_tag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('content_object', self.gf('django.db.models.fields.related.ForeignKey')(related_name='archivrflickr_flickrphototag_items', to=orm['archivrflickr.FlickrPhoto'])),
        ))
        db.send_create_signal('archivrflickr', ['FlickrPhotoTag'])

        # Adding model 'FlickrUser'
        db.create_table('archivrflickr_flickruser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nsid', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('realname', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('path_alias', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('photos_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('profile_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('mobile_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('icon_server', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('icon_farm', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('is_pro', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('photos_first_date_taken', self.gf('django.db.models.fields.DateTimeField')()),
            ('photos_first_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('photos_count', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('photos_views', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True)),
        ))
        db.send_create_signal('archivrflickr', ['FlickrUser'])

    def backwards(self, orm):
        # Deleting model 'FlickrFavorite'
        db.delete_table('archivrflickr_flickrfavorite')

        # Deleting model 'FlickrFavoriteList'
        db.delete_table('archivrflickr_flickrfavoritelist')

        # Deleting model 'FlickrPhoto'
        db.delete_table('archivrflickr_flickrphoto')

        # Deleting model 'FlickrPhotoComment'
        db.delete_table('archivrflickr_flickrphotocomment')

        # Deleting model 'FlickrPhotoset'
        db.delete_table('archivrflickr_flickrphotoset')

        # Removing M2M table for field photos on 'FlickrPhotoset'
        db.delete_table('archivrflickr_flickrphotoset_photos')

        # Deleting model 'FlickrPhotoTag'
        db.delete_table('archivrflickr_flickrphototag')

        # Deleting model 'FlickrUser'
        db.delete_table('archivrflickr_flickruser')

    models = {
        'archivr.archivritem': {
            'Meta': {'ordering': "('-order_date',)", 'object_name': 'ArchivrItem'},
            'coordinate': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_genre': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            'order_date': ('django.db.models.fields.DateTimeField', [], {})
        },
        'archivrflickr.flickrfavorite': {
            'Meta': {'object_name': 'FlickrFavorite'},
            'date_faved': ('django.db.models.fields.DateTimeField', [], {}),
            'favorite_list': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archivrflickr.FlickrFavoriteList']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archivrflickr.FlickrPhoto']"})
        },
        'archivrflickr.flickrfavoritelist': {
            'Meta': {'object_name': 'FlickrFavoriteList'},
            'date_archived': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archivrflickr.FlickrUser']"}),
            'photos': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['archivrflickr.FlickrPhoto']", 'through': "orm['archivrflickr.FlickrFavorite']", 'symmetrical': 'False'}),
            'primary': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'primary_in'", 'null': 'True', 'to': "orm['archivrflickr.FlickrPhoto']"})
        },
        'archivrflickr.flickrphoto': {
            'Meta': {'ordering': "('-taken_date',)", 'object_name': 'FlickrPhoto', '_ormbases': ['archivr.ArchivrItem']},
            'archivritem_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['archivr.ArchivrItem']", 'unique': 'True', 'primary_key': 'True'}),
            'comments': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'exif_aperture': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'exif_color_space': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'exif_exposure': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'exif_flash': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'exif_focal_length': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'exif_iso': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'exif_make': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'exif_metering_mode': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'exif_model': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'exif_orientation': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'exif_software': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'farm': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'flickr_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'geo_accuracy': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'geo_country': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'geo_country_place_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'geo_country_woe_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'geo_county': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'geo_county_place_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'geo_county_woe_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'geo_latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'geo_locality': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'geo_locality_place_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'geo_locality_woe_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'geo_longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'geo_neighbourhood': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'geo_neighbourhood_place_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'geo_neighbourhood_woe_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'geo_perms_is_contact': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'geo_perms_is_family': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'geo_perms_is_friend': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'geo_perms_is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'geo_place_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'geo_region': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'geo_region_place_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'geo_region_woe_id': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'geo_woe_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'is_video': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'large_height': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'large_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'largesquare_height': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'largesquare_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'license': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'medium640_height': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'medium640_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'medium800_height': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'medium800_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'medium_height': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'medium_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'original_format': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'original_height': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'original_secret': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'original_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archivrflickr.FlickrUser']"}),
            'photopage_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'posted_date': ('django.db.models.fields.DateTimeField', [], {}),
            'rotation': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'safety_level': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'secret': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'server': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'small320_height': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'small320_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'small_height': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'small_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'square_height': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'square_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'taken_date': ('django.db.models.fields.DateTimeField', [], {}),
            'taken_granularity': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'thumbnail_height': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'thumbnail_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_date': ('django.db.models.fields.DateTimeField', [], {}),
            'video_duration': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'video_height': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'video_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'visibility_is_family': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'visibility_is_friend': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'visibility_is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'archivrflickr.flickrphotocomment': {
            'Meta': {'ordering': "('pub_date',)", 'object_name': 'FlickrPhotoComment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archivrflickr.FlickrUser']"}),
            'comment': ('django.db.models.fields.TextField', [], {}),
            'flickr_id': ('django.db.models.fields.CharField', [], {'max_length': '128', 'primary_key': 'True'}),
            'permanent_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archivrflickr.FlickrPhoto']"}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {})
        },
        'archivrflickr.flickrphotoset': {
            'Meta': {'ordering': "('order',)", 'object_name': 'FlickrPhotoset'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'flickr_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archivrflickr.FlickrUser']"}),
            'photos': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['archivrflickr.FlickrPhoto']", 'symmetrical': 'False'}),
            'primary': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'primary_photo_set'", 'null': 'True', 'to': "orm['archivrflickr.FlickrPhoto']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'archivrflickr.flickrphototag': {
            'Meta': {'object_name': 'FlickrPhotoTag'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archivrflickr.FlickrUser']"}),
            'content_object': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'archivrflickr_flickrphototag_items'", 'to': "orm['archivrflickr.FlickrPhoto']"}),
            'flickr_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'machine_tag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'archivrflickr_flickrphototag_items'", 'to': "orm['taggit.Tag']"})
        },
        'archivrflickr.flickruser': {
            'Meta': {'object_name': 'FlickrUser'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'icon_farm': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'icon_server': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_pro': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'mobile_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'nsid': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'path_alias': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'photos_count': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'photos_first_date': ('django.db.models.fields.DateTimeField', [], {}),
            'photos_first_date_taken': ('django.db.models.fields.DateTimeField', [], {}),
            'photos_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'photos_views': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True'}),
            'profile_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'realname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['archivrflickr']