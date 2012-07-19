from django.contrib import admin
from archivrflickr.models import *


class FlickrPhotoTagInline(admin.TabularInline):
    model = FlickrPhoto.tags.through
    raw_id_fields = ('tag',)

class FlickrPhotoAdmin(admin.ModelAdmin):
    date_hierarchy = 'posted_date'
    list_display = ('posted_date', 'show_thumb', 'title', 'owner', 'featured', 'hidden',)
    list_display_links = ('title', 'show_thumb',)
    list_filter = ('posted_date',)
    search_fields = ['title', 'description', ]
    inlines = [FlickrPhotoTagInline, ]
    exclude = ('tags',)
    fieldsets = [
        ('ArchivrItem', {
            'fields': ('order_date', 'item_genre', 'hidden', 'featured', 'latitude',
                        'longitude',)
        }),
        ('Photo', {
            'fields': ('flickr_id', 'owner', 'title', 'description', 'posted_date',
                        'updated_date', 'taken_date', 'taken_granularity',
                        'license', 'comments', 'safety_level', 'rotation',
                        'visibility_is_public', 'visibility_is_friend',
                        'visibility_is_family', )
        }),
        ('URL etc.', {
            'fields': ('photopage_url', 'farm', 'server', 'secret',
                                            'original_secret', 'original_format',)
        }),
        ('Video', {
            'classes': ('collapse',),
            'fields': ('is_video', 'video_duration', 'video_width', 'video_height',)
        }),
    ]

    # Dynamically generate the fields for photo sizes, geo data and EXIF data.

    size_fields = []
    for (key, desc, l) in FlickrPhoto.FLICKR_PHOTO_SIZES:
        size_fields.append(key+'_width')
        size_fields.append(key+'_height')
    fieldsets.insert(
        3,
        ('Image sizes', {
            'classes': ('collapse',),
            'fields': size_fields,
        })
    )

    geo_fields = ['geo_latitude', 'geo_longitude', 'geo_accuracy', 'geo_place_id',
                                                                    'geo_woe_id', ]
    for (key, desc) in FlickrPhoto.FLICKR_GEO_AREAS:
        geo_fields.append('geo_'+key)
        geo_fields.append('geo_'+key+'_place_id')
        geo_fields.append('geo_'+key+'_woe_id')
    fieldsets.insert(
        5,
        ('Geo data', {
            'classes': ('collapse',),
            'fields': geo_fields,
        })
    )

    exif_fields = []
    for (key, desc) in FlickrPhoto.FLICKR_EXIF_FIELDS:
        exif_fields.append('exif_'+key)
    fieldsets.append(
        ('EXIF data', {
            'classes': ('collapse',),
            'fields': exif_fields,
        })
    )

    def show_thumb(self, instance):
        return '<img src="%s" width="%s" height="%s" alt="Thumbnail" />' % (
            instance.get_url('thumbnail'),
            instance.thumbnail_width,
            instance.thumbnail_height)
    show_thumb.allow_tags = True
    show_thumb.short_description = ''

admin.site.register(FlickrPhoto, FlickrPhotoAdmin)


class FlickrUserAdmin(admin.ModelAdmin):
    date_hierarchy = 'photos_first_date'
    list_display = ('username', 'realname', 'nsid',)
    list_display_links = ('username',)
    search_fields = ('username', 'realname', 'nsid', 'location', 'description',)
    fieldsets = (
        (None, {
            'fields': ('nsid', 'username', 'realname', 'path_alias', 'location',
                        'description', 'photos_url', 'profile_url', 'mobile_url',
                        'icon_server', 'icon_farm', 'is_pro',
                        'photos_first_date_taken', 'photos_first_date',
                        'photos_count', 'photos_views',)
        }),
    )

admin.site.register(FlickrUser, FlickrUserAdmin)
