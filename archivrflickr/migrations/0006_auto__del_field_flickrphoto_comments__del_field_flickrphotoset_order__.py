# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'FlickrPhoto.comments'
        db.delete_column('archivrflickr_flickrphoto', 'comments')

        # Deleting field 'FlickrPhotoset.order'
        db.delete_column('archivrflickr_flickrphotoset', 'order')

        # Adding field 'FlickrPhotoset.created_date'
        db.add_column('archivrflickr_flickrphotoset', 'created_date',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 7, 19, 0, 0)),
                      keep_default=False)

        # Adding field 'FlickrPhotoset.updated_date'
        db.add_column('archivrflickr_flickrphotoset', 'updated_date',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 7, 19, 0, 0)),
                      keep_default=False)

    def backwards(self, orm):
        # Adding field 'FlickrPhoto.comments'
        db.add_column('archivrflickr_flickrphoto', 'comments',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'FlickrPhotoset.order'
        db.add_column('archivrflickr_flickrphotoset', 'order',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'FlickrPhotoset.created_date'
        db.delete_column('archivrflickr_flickrphotoset', 'created_date')

        # Deleting field 'FlickrPhotoset.updated_date'
        db.delete_column('archivrflickr_flickrphotoset', 'updated_date')

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
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'exif_aperture': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'exif_camera': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'exif_color_space': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'exif_date_and_time_digitized': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'exif_date_and_time_modified': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'exif_date_and_time_original': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'exif_exposure': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'exif_exposure_bias': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'exif_exposure_program': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'exif_flash': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'exif_focal_length': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'exif_gps_latitude': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'exif_gps_longitude': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'exif_gps_version_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'exif_host_computer': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'exif_iso_speed': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'exif_make': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'exif_max_aperture_value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'exif_metering_mode': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'exif_model': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'exif_orientation': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'exif_software': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'exif_x_resolution': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'exif_y_resolution': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'exif_ycbcr_positioning': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'farm': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'flickr_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'geo_accuracy': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'geo_country': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'geo_country_place_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'geo_country_woe_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'geo_county': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'geo_county_place_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'geo_county_woe_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'geo_latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '6', 'blank': 'True'}),
            'geo_locality': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'geo_locality_place_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'geo_locality_woe_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'geo_longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '6', 'blank': 'True'}),
            'geo_neighbourhood': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'geo_neighbourhood_place_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'geo_neighbourhood_woe_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'geo_perms_is_contact': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'geo_perms_is_family': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'geo_perms_is_friend': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'geo_perms_is_public': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'geo_place_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'geo_region': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'geo_region_place_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'geo_region_woe_id': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'geo_woe_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'is_video': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'large1600_height': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'large1600_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'large2048_height': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'large2048_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
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
            'Meta': {'ordering': "('-pub_date',)", 'object_name': 'FlickrPhotoComment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archivrflickr.FlickrUser']"}),
            'comment': ('django.db.models.fields.TextField', [], {}),
            'flickr_id': ('django.db.models.fields.CharField', [], {'max_length': '128', 'primary_key': 'True'}),
            'permanent_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archivrflickr.FlickrPhoto']"}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {})
        },
        'archivrflickr.flickrphotoset': {
            'Meta': {'ordering': "('-created_date',)", 'object_name': 'FlickrPhotoset'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'flickr_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archivrflickr.FlickrUser']"}),
            'photos': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['archivrflickr.FlickrPhoto']", 'symmetrical': 'False'}),
            'primary': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'primary_photo_set'", 'null': 'True', 'to': "orm['archivrflickr.FlickrPhoto']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updated_date': ('django.db.models.fields.DateTimeField', [], {})
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
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'icon_farm': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'icon_server': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_pro': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'mobile_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'nsid': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'path_alias': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'photos_count': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'photos_first_date': ('django.db.models.fields.DateTimeField', [], {}),
            'photos_first_date_taken': ('django.db.models.fields.DateTimeField', [], {}),
            'photos_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'photos_views': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'profile_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'realname': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
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