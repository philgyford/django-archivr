# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'FlickrPhoto.safety_level'
        db.add_column('archivrflickr_flickrphoto', 'safety_level',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True),
                      keep_default=False)

        # Adding field 'FlickrPhoto.rotation'
        db.add_column('archivrflickr_flickrphoto', 'rotation',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True),
                      keep_default=False)

        # Adding field 'FlickrPhoto.is_video'
        db.add_column('archivrflickr_flickrphoto', 'is_video',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'FlickrPhoto.video_duration'
        db.add_column('archivrflickr_flickrphoto', 'video_duration',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True),
                      keep_default=False)

        # Adding field 'FlickrPhoto.video_width'
        db.add_column('archivrflickr_flickrphoto', 'video_width',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True),
                      keep_default=False)

        # Adding field 'FlickrPhoto.video_height'
        db.add_column('archivrflickr_flickrphoto', 'video_height',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting field 'FlickrPhoto.safety_level'
        db.delete_column('archivrflickr_flickrphoto', 'safety_level')

        # Deleting field 'FlickrPhoto.rotation'
        db.delete_column('archivrflickr_flickrphoto', 'rotation')

        # Deleting field 'FlickrPhoto.is_video'
        db.delete_column('archivrflickr_flickrphoto', 'is_video')

        # Deleting field 'FlickrPhoto.video_duration'
        db.delete_column('archivrflickr_flickrphoto', 'video_duration')

        # Deleting field 'FlickrPhoto.video_width'
        db.delete_column('archivrflickr_flickrphoto', 'video_width')

        # Deleting field 'FlickrPhoto.video_height'
        db.delete_column('archivrflickr_flickrphoto', 'video_height')

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
            'geo_country_place_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'geo_country_woe_id': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '50', 'blank': 'True'}),
            'geo_county': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'geo_county_place_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'geo_county_woe_id': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '50', 'blank': 'True'}),
            'geo_latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'geo_locality': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'geo_locality_place_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'geo_locality_woe_id': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '50', 'blank': 'True'}),
            'geo_longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'geo_region': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'geo_region_place_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'geo_region_woe_id': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '50', 'blank': 'True'}),
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
            'author_nsid': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'content_object': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'archivrflickr_flickrphototag_items'", 'to': "orm['archivrflickr.FlickrPhoto']"}),
            'flickr_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'machine_tag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'archivrflickr_flickrphototag_items'", 'to': "orm['taggit.Tag']"})
        },
        'archivrflickr.flickruser': {
            'Meta': {'object_name': 'FlickrUser'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'iconfarm': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'iconserver': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'mobile_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'nsid': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'path_alias': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'photos_count': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'photos_first_date': ('django.db.models.fields.DateTimeField', [], {}),
            'photos_first_date_taken': ('django.db.models.fields.DateTimeField', [], {}),
            'photos_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'photos_views': ('django.db.models.fields.PositiveIntegerField', [], {}),
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