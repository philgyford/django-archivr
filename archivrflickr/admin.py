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
    search_fields = ['title', 'description',]
    inlines = [FlickrPhotoTagInline,]
    exclude = ('tags',)
    fieldsets = (
        ('ArchivrItem', {
            'fields': ('order_date', 'item_genre', 'hidden', 'featured', 'latitude', 'longitude',)
        }),
        ('Photo', {
            'fields': ('flickr_id', 'owner', 'title', 'description', 'posted_date', 'updated_date', 'taken_date', 'taken_granularity', 'license', 'comments','safety_level', 'rotation', 'visibility_is_public', 'visibility_is_friend', 'visibility_is_family', )
        }),
        ('URL etc.', {
            'fields': ('photopage_url', 'farm', 'server', 'secret', 'original_secret', 'original_format',)
        }),
        ('Image sizes', {
            'classes': ('collapse',),
            'fields': ('large_width', 'large_height', 'largesquare_width','largesquare_height', 'medium640_width', 'medium640_height', 'medium800_width', 'medium800_height', 'medium_width', 'medium_height', 'original_width', 'original_height', 'small320_width', 'small320_height', 'small_width', 'small_height', 'square_width', 'square_height', 'thumbnail_width', 'thumbnail_height',)
        }),
        ('Video', {
            'classes': ('collapse',),
            'fields': ('is_video', 'video_duration', 'video_width', 'video_height',)
        }),
        ('Geo data', {
            'classes': ('collapse',),
            'fields': ('geo_latitude', 'geo_longitude', 'geo_accuracy', 'geo_county', 'geo_county_place_id', 'geo_county_woe_id', 'geo_country', 'geo_country_place_id', 'geo_country_woe_id', 'geo_locality', 'geo_locality_place_id', 'geo_locality_woe_id', 'geo_region', 'geo_region_place_id', 'geo_region_woe_id',)
        }),
        ('EXIF data', {
            'classes': ('collapse',),
            'fields': ('exif_aperture', 'exif_color_space', 'exif_exposure', 'exif_flash', 'exif_focal_length', 'exif_iso', 'exif_make', 'exif_metering_mode', 'exif_model', 'exif_orientation', 'exif_software',)
        }),
    )

    def show_thumb(self, instance):
        return '<img src="%s" width="%s" height="%s" alt="Thumbnail" />' % (instance.get_thumbnail_url(), instance.thumbnail_width, instance.thumbnail_height)
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
            'fields': ('nsid', 'username', 'realname', 'path_alias', 'location', 'description', 'photos_url', 'profile_url', 'mobile_url', 'icon_server', 'icon_farm', 'is_pro', 'photos_first_date_taken', 'photos_first_date', 'photos_count', 'photos_views',)
        }),
    )

admin.site.register(FlickrUser, FlickrUserAdmin)
