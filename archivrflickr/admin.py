from django.contrib import admin
from django.contrib import gis 
from archivrflickr.models import FlickrPhoto


class FlickrPhotoTagInline(admin.TabularInline):
    model = FlickrPhoto.tags.through
    raw_id_fields = ('tag',)


class FlickrPhotoAdmin(gis.admin.OSMGeoAdmin):
    date_hierarchy = 'posted_date'
    list_display = ('posted_date', 'show_thumb', 'title', 'owner', 'hidden',)
    list_display_links = ('title', 'show_thumb',)
    list_filter = ('posted_date',)
    search_fields = ['title', 'description',]
    inlines = [FlickrPhotoTagInline,]
    exclude = ('tags',)
    fieldsets = (
        ('ArchivrItem', {
            'fields': ('order_date', 'hidden', 'coordinate', 'item_genre',)
        }),
        ('Photo', {
            'fields': ('flickr_id', 'owner', 'title', 'description', 'posted_date', 'updated_date', 'taken_date', 'taken_granularity', 'license', 'comments', 'visibility_is_public', 'visibility_is_friend', 'visibility_is_family',)
        }),
        ('URL etc.', {
            'fields': ('photopage_url', 'farm', 'server', 'secret', 'original_secret', 'original_format',)
        }),
        ('Image sizes', {
            'classes': ('collapse',),
            'fields': ('large_width', 'large_height', 'largesquare_width','largesquare_height', 'medium640_width', 'medium640_height', 'medium800_width', 'medium800_height', 'medium_width', 'medium_height', 'original_width', 'original_height', 'small320_width', 'small320_height', 'small_width', 'small_height', 'square_width', 'square_height', 'thumbnail_width', 'thumbnail_height',)
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

#gis.admin.site.register(FlickrPhoto, gis.admin.OSMGeoAdmin)
