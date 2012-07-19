from django.db import models

from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase

from archivr.models import ArchivrItem
from archivr.managers import *


class FlickrFavorite(models.Model):
    """
    Linking FlickrPhotos into a FlickrFavoriteList, so that we can capture the 
    date_faved time for each one.
    """
    photo = models.ForeignKey('FlickrPhoto')
    favorite_list = models.ForeignKey('FlickrFavoriteList')
    date_faved = models.DateTimeField()


class FlickrFavoriteList(models.Model):
    owner = models.ForeignKey('FlickrUser')
    date_archived = models.DateTimeField()
    photos = models.ManyToManyField('FlickrPhoto', through='FlickrFavorite')
    primary = models.ForeignKey('FlickrPhoto', related_name='primary_in', null=True)

    def __unicode__(self):
        return u"%s's favorite photos" % self.owner

    @models.permalink
    def get_absolute_url(self):
        return ('flickr_favoritelist_detail', (), {})

    def numPhotos(self):
        return len(self.photo_list.objects.all())


class FlickrPhoto(ArchivrItem):
    """
    A single photo on Flickr.
    """

    # Used in the form to map the stored value with a text string.
    FLICKR_LICENSES = (
        ('0', 'All Rights Reserved'),
        ('1', 'Attribution-NonCommercial-ShareAlike License'),
        ('2', 'Attribution-NonCommercial License'),
        ('3', 'Attribution-NonCommercial-NoDerivs License'),
        ('4', 'Attribution License'),
        ('5', 'Attribution-ShareAlike License'),
        ('6', 'Attribution-NoDerivs License'),
        ('7', 'No known copyright restrictions'),
    )

    # Used in the form to map the stored value with a text string.
    # Granularity: http://www.flickr.com/services/api/misc.dates.html
    FLICKR_DATE_GRANULARITIES = (
        (0, 'Y-m-d H:i:s'),
        (4, 'Y-m'),
        (6, 'Y'),
        (8, 'Circa...'),
    )

    # Used in the FlickrFetcher class.
    # The first value in each row should have corresponding model fields.
    # e.g. 'small' means we should have 'small_width' and 'small_height' model fields.
    # And each row requires a has_x_photo() method/property.
    # The second value must match the "label"s from the Flickr API.
    # The third value corresponds to the letter used to generate the URL for an
    # image of that size. 
    FLICKR_PHOTO_SIZES = (
        ('large', 'Large', 'b'),
        ('large1600', 'Large 1600', 'h'),
        ('large2048', 'Large 2048', 'k'),
        ('largesquare', 'Large Square', 'q'),
        ('medium', 'Medium', ''),
        ('medium640', 'Medium 640', 'z'),
        ('medium800', 'Medium 800', 'c'),
        ('original', 'Original', 'o'),
        ('small', 'Small', 'm'),
        ('small320', 'Small 320', 'n'),
        ('square', 'Square', 's'),
        ('thumbnail', 'Thumbnail', 't'),
    )

    # Used in the FlickrFetcher class.
    # Each of the keys (left) should have corresponding model fields.
    # e.g. for 'county' we have model fields:
    # 'geo_county', 'geo_county_place_id', 'geo_county_woe_id'.
    FLICKR_GEO_AREAS = (
        ('county', 'County'),
        ('country', 'Country'),
        ('locality', 'Locality'),
        ('neighbourhood', 'Neighbourhood'),
        ('region', 'Region'),
    )

    # Used in the FlickrFetcher class.
    # Each key (left), prepended by 'exif_' should have a corresponding model field.
    # Each value (right) is the same as the name of an EXIF property, as returned by
    # the Flickr API.
    FLICKR_EXIF_FIELDS = (
        ('aperture', 'Aperture'),
        ('camera', 'Camera'),
        ('color_space', 'Color Space'),
        ('date_and_time_digitized', 'Date and Time (Digitized)'),
        ('date_and_time_modified', 'Date and Time (Modified)'),
        ('date_and_time_original', 'Date and Time (Original)'),
        ('exposure', 'Exposure'),
        ('exposure_bias', 'Exposure Bias'),
        ('exposure_program', 'Exposure Program'),
        ('flash', 'Flash'),
        ('focal_length', 'Focal Length'),
        ('gps_version_id', 'GPS Version ID'),
        ('gps_latitude', 'GPS Latitude'),
        ('gps_longitude', 'GPS Longitude'),
        ('host_computer', 'Host Computer'),
        ('iso_speed', 'ISO Speed'),
        ('make', 'Make'),
        ('max_aperture_value', 'Max Aperture Value'),
        ('metering_mode', 'Metering Mode'),
        ('model', 'Model'),
        ('orientation', 'Orientation'),
        ('software', 'Software'),
        ('x_resolution', 'X-Resolution'),
        ('y_resolution', 'Y-Resolution'),
        ('ycbcr_positioning', 'YCbCr Positioning'),
    )

    # Data from Flickr:
    flickr_id = models.CharField(max_length=50, unique=True,
                                            help_text="ID of this photo on Flickr.")
    owner = models.ForeignKey('FlickrUser')
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    posted_date = models.DateTimeField(help_text="UTC")
    updated_date = models.DateTimeField(help_text="UTC")
    taken_date = models.DateTimeField(
                                help_text="Stored as UTC, but timezone is unknown.")
    taken_granularity = models.PositiveSmallIntegerField(default=0,
                                                choices=FLICKR_DATE_GRANULARITIES)

    comments = models.PositiveIntegerField(default=0)
    visibility_is_public = models.BooleanField(default=False)
    visibility_is_friend = models.BooleanField(default=False)
    visibility_is_family = models.BooleanField(default=False)

    photopage_url = models.URLField(verify_exists=False)
    farm = models.PositiveSmallIntegerField()
    server = models.PositiveSmallIntegerField()
    secret = models.CharField(max_length=10)
    original_secret = models.CharField(max_length=10, blank=True)
    original_format = models.CharField(max_length=10, blank=True)
    safety_level = models.PositiveSmallIntegerField(null=True)
    rotation = models.PositiveSmallIntegerField(null=True)
    license = models.CharField(max_length=50, choices=FLICKR_LICENSES)

    # If you add another size, add it in FLICKR_PHOTO_SIZES too.
    # And add methods to check the presence of the size for this Photo,
    # and to return the size's URL.
    large_width = models.PositiveSmallIntegerField(null=True)
    large_height = models.PositiveSmallIntegerField(null=True)
    large1600_width = models.PositiveSmallIntegerField(null=True)
    large1600_height = models.PositiveSmallIntegerField(null=True)
    large2048_width = models.PositiveSmallIntegerField(null=True)
    large2048_height = models.PositiveSmallIntegerField(null=True)
    largesquare_width = models.PositiveSmallIntegerField(null=True)
    largesquare_height = models.PositiveSmallIntegerField(null=True)
    medium640_width = models.PositiveSmallIntegerField(null=True)
    medium640_height = models.PositiveSmallIntegerField(null=True)
    medium800_width = models.PositiveSmallIntegerField(null=True)
    medium800_height = models.PositiveSmallIntegerField(null=True)
    medium_width = models.PositiveSmallIntegerField(null=True)
    medium_height = models.PositiveSmallIntegerField(null=True)
    original_width = models.PositiveSmallIntegerField(null=True)
    original_height = models.PositiveSmallIntegerField(null=True)
    small320_width = models.PositiveSmallIntegerField(null=True)
    small320_height = models.PositiveSmallIntegerField(null=True)
    small_width = models.PositiveSmallIntegerField(null=True)
    small_height = models.PositiveSmallIntegerField(null=True)
    square_width = models.PositiveSmallIntegerField(null=True)
    square_height = models.PositiveSmallIntegerField(null=True)
    thumbnail_width = models.PositiveSmallIntegerField(null=True)
    thumbnail_height = models.PositiveSmallIntegerField(null=True)

    is_video = models.BooleanField(default=False)
    video_duration = models.PositiveIntegerField(null=True)
    video_width = models.PositiveSmallIntegerField(null=True)
    video_height = models.PositiveSmallIntegerField(null=True)

    geo_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, 
                                                                        blank=True)
    geo_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, 
                                                                        blank=True)
    geo_accuracy = models.PositiveSmallIntegerField(null=True, blank=True)
    geo_place_id = models.CharField(max_length=50, null=True, blank=True)
    geo_woe_id = models.PositiveIntegerField(null=True, blank=True)

    # Each type of geo field should have an entry in GEO_AREAS, above.
    geo_county = models.CharField(max_length=255, blank=True)
    geo_county_place_id = models.CharField(max_length=50, null=True, blank=True)
    geo_county_woe_id = models.PositiveIntegerField(null=True, blank=True)
    geo_country = models.CharField(max_length=255, blank=True)
    geo_country_place_id = models.CharField(max_length=50, null=True, blank=True)
    geo_country_woe_id = models.PositiveIntegerField(null=True, blank=True)
    geo_locality = models.CharField(max_length=255, blank=True)
    geo_locality_place_id = models.CharField(max_length=50, null=True, blank=True)
    geo_locality_woe_id = models.PositiveIntegerField(null=True, blank=True)
    geo_neighbourhood = models.CharField(max_length=255, blank=True)
    geo_neighbourhood_place_id = models.CharField(max_length=50, null=True,
                                                                        blank=True)
    geo_neighbourhood_woe_id = models.PositiveIntegerField(null=True, blank=True)
    geo_region = models.CharField(max_length=255, blank=True)
    geo_region_place_id = models.CharField(max_length=50, null=True, blank=True)
    geo_region_woe_id = models.PositiveIntegerField(max_length=50, null=True, 
                                                                        blank=True)
    # Not always available.
    geo_perms_is_public = models.NullBooleanField(null=True)
    geo_perms_is_contact = models.NullBooleanField(null=True)
    geo_perms_is_friend = models.NullBooleanField(null=True)
    geo_perms_is_family = models.NullBooleanField(null=True)

    # Each of the EXIF fields should have a corresponding entry in EXIF_FIELDS, above.
    exif_aperture = models.CharField(max_length=255, blank=True)
    exif_camera = models.CharField(max_length=255, blank=True)
    exif_color_space = models.CharField(max_length=255, blank=True)
    exif_date_and_time_digitized = models.CharField(max_length=255, blank=True)
    exif_date_and_time_modified = models.CharField(max_length=255, blank=True)
    exif_date_and_time_original = models.CharField(max_length=255, blank=True)
    exif_exposure = models.CharField(max_length=255, blank=True)
    exif_exposure_bias = models.CharField(max_length=255, blank=True)
    exif_exposure_program = models.CharField(max_length=255, blank=True)
    exif_flash = models.CharField(max_length=255, blank=True)
    exif_focal_length = models.CharField(max_length=255, blank=True)
    exif_gps_version_id = models.CharField(max_length=255, blank=True)
    exif_gps_latitude = models.CharField(max_length=255, blank=True)
    exif_gps_longitude = models.CharField(max_length=255, blank=True)
    exif_host_computer = models.CharField(max_length=255, blank=True)
    exif_iso_speed = models.CharField(max_length=255, blank=True)
    exif_make = models.CharField(max_length=255, blank=True)
    exif_max_aperture_value = models.CharField(max_length=255, blank=True)
    exif_metering_mode = models.CharField(max_length=255, blank=True)
    exif_model = models.CharField(max_length=255, blank=True)
    exif_orientation = models.CharField(max_length=255, blank=True)
    exif_software = models.CharField(max_length=255, blank=True)
    exif_x_resolution = models.CharField(max_length=255, blank=True)
    exif_y_resolution = models.CharField(max_length=255, blank=True)
    exif_ycbcr_positioning = models.CharField(max_length=255, blank=True)

    tags = TaggableManager(blank=True, through='FlickrPhotoTag')

    class Meta:
        ordering = ('-taken_date',)
        get_latest_by = 'posted_date'

    def __unicode__(self):
        if self.title:
            return u'%s' % self.title
        else:
            return u'[%s]' % self.flickr_id

    @models.permalink
    def get_absolute_url(self):
        return ('flickr_photo_detail', (), {'flickr_id': self.flickr_id, })

    # ALL FlickrPhotos.
    objects = models.Manager()
    # FlickrPhotos that haven't been marked as hidden.
    visible_objects = VisibleManager()
    # FlickrPhotos that haven't been marked as hidden and have been marked as 
    # featured.
    featured_objects = FeaturedManager()

    def _get_url_helper(self, size, secret=None, extension='jpg'):
        if secret is None:
            secret = self.secret
        for (key, desc, letter) in self.FLICKR_PHOTO_SIZES:
            if key == size:
                return u'http://farm%s.static.flickr.com/%s/%s_%s_%s.%s' % (
                self.farm, self.server, self.flickr_id, secret, letter, extension)

    def get_url(self, size):
        """
        Call this to get the URL for any photo size. eg:
            get_url('thumbnail')
        might return:
            http://farm9.staticflickr.com/8166/7510891034_ecfe8e3af5_t.jpg
        """
        if self != 'original' and self._has_photo_size_helper(size):
            return self._get_url_helper(size)
        elif self.original_secret:
            return self._get_url_helper('original',
                    secret=self.original_secret, extension=self.original_format)
        else:
            return self._get_url_helper('original', extension=self.original_format)

    def _has_photo_size_helper(self, size):
        """Helper for all the has_x_photo() properties."""
        if vars(self)[size+'_width'] is not None:
            return True
        return False

    @property
    def has_large_photo(self):
        return self._has_photo_size_helper('large')

    @property
    def has_large1600_photo(self):
        return self._has_photo_size_helper('large1600')

    @property
    def has_large2048_photo(self):
        return self._has_photo_size_helper('large2048')

    @property
    def has_largesquare_photo(self):
        return self._has_photo_size_helper('largesquare')

    @property
    def has_medium_photo(self):
        return self._has_photo_size_helper('medium')

    @property
    def has_medium640_photo(self):
        return self._has_photo_size_helper('medium640')

    @property
    def has_medium800_photo(self):
        return self._has_photo_size_helper('medium800')

    @property
    def has_original_photo(self):
        return self._has_photo_size_helper('original')

    @property
    def has_small_photo(self):
        return self._has_photo_size_helper('small')

    @property
    def has_small320_photo(self):
        return self._has_photo_size_helper('small320')

    @property
    def has_square_photo(self):
        return self._has_photo_size_helper('square')

    @property
    def has_thumbnail_photo(self):
        return self._has_photo_size_helper('thumbnail')

    def _next_previous_helper(self, direction, photoset):
        order = direction == 'next' and 'taken_date' or '-taken_date'
        filter = direction == 'next' and 'gt' or 'lt'
        try:
            return self.photoset_set.get(pk=photoset.pk).photos.filter(
                **{'taken_date__%s' % filter: self.taken_date}
                ).order_by(order)[0]
        except IndexError:
            return None

    def get_next_in_set(self, *args, **kwargs):
        """
        Returns the next Entry with "live" status by ``pub_date``, if
        there is one, or ``None`` if there isn't.

        In public-facing templates, use this method instead of
        ``get_next_by_pub_date``, because ``get_next_by_pub_date``
        does not differentiate entry status.

        """
        return self._next_previous_helper('next', *args, **kwargs)

    def get_previous_in_set(self, *args, **kwargs):
        """
        Returns the previous Entry with "live" status by ``pub_date``,
        if there is one, or ``None`` if there isn't.

        In public-facing templates, use this method instead of
        ``get_previous_by_pub_date``, because
        ``get_previous_by_pub_date`` does not differentiate entry
        status..
        """
        return self._next_previous_helper('previous', *args, **kwargs)
    

class FlickrPhotoComment(models.Model):
    """
    Describes a single comment on a ``FlickrPhoto``.
    """
    flickr_id = models.CharField(primary_key=True, max_length=128)
    photo = models.ForeignKey(FlickrPhoto)
    author = models.ForeignKey('FlickrUser')
    pub_date = models.DateTimeField()
    permanent_url = models.URLField(verify_exists=False)
    comment = models.TextField()

    class Meta:
        ordering = ('pub_date',)

    def __unicode__(self):
        return _(u"%(author)s said: %(comment)s") % {
            'author': self.author, 'comment': self.get_short_comment(4)}

    @models.permalink
    def get_absolute_url(self):
        return ('flickr_photo_comment', (), {
                                                'photo_id': self.photo.flickr_id,
                                                'comment_id': self.flickr_id
                                            })

class FlickrPhotoset(models.Model):
    """
    One photoset and its list of ``FlickrPhotos``.
    """
    
    flickr_id = models.CharField(primary_key=True, max_length=50)
    primary = models.ForeignKey(FlickrPhoto, null=True, default=None,
                                                related_name='primary_photo_set')
    owner = models.ForeignKey('FlickrUser')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    photos = models.ManyToManyField(FlickrPhoto)

    class Meta:
        ordering = ('order',)

    def __unicode__(self):
        return u"%s photoset by %s" % (self.title, self.owner)

    @models.permalink
    def get_absolute_url(self):
        return ('flickr_photoset_detail', (), {'flickr_id': self.flickr_id, })

    def highlight(self):
        """
        Return the highlight image of this photo set.

        In case there isn't a ``primary`` image set, the first one is
        selected. (If this causes a ``IndexError``, ``None`` is
        returned.)
        """
        if self.primary is not None:
            return self.primary
        try:
            return self.photos.all()[0]
        except IndexError:
            return None

    def get_time_period(self):
        """
        Return dict with start and end of this photo set.

        Gets ``taken_date`` of first and last ``FlickrPhoto`` and returns
        results as dict::

            { 'start': datetime.datetime, 'end': datetime.datetime }
        """
        start_photo = self.photos.order_by('taken_date')[0]
        end_photo = self.photos.order_by('-taken_date')[0]
        if start_photo.taken_date and end_photo.taken_date:
            return {'start': start_photo.taken_date, 'end': end_photo.taken_date}
        return {'start': start_photo.posted_date, 'end': end_photo.posted_date}


class FlickrPhotoTag(TaggedItemBase):
    """
    Describes the relationship between a django-taggit Tag and a FlickrPhoto.
    Flickr has various fields which are unique to this relationship, rather
    than the Tag itself.
    """
    flickr_id = models.CharField(max_length=255, verbose_name='Flickr ID')
    author = models.ForeignKey('FlickrUser')
    machine_tag = models.BooleanField(default=False)
    content_object = models.ForeignKey(FlickrPhoto,
                                    related_name="%(app_label)s_%(class)s_items")

    class Meta:
        verbose_name = 'FlickrPhoto/Tag Relationship'


class FlickrUser(models.Model):
    """
    A single person on Flickr.
    """
    nsid = models.CharField(max_length=50, help_text='eg, "35034346050@N01"')
    username = models.CharField(max_length=255, help_text="eg, 'philgyford'")
    realname = models.CharField(max_length=255, blank=True,
                            help_text="eg, 'Phil Gyford'. Could be ''.")
    path_alias = models.CharField(max_length=50)
    location = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    photos_url = models.URLField(verify_exists = False)
    profile_url = models.URLField(verify_exists = False)
    mobile_url = models.URLField(verify_exists = False)

    icon_server = models.PositiveSmallIntegerField(default=0)
    icon_farm = models.PositiveSmallIntegerField(default=0)
    is_pro = models.BooleanField(default=False)

    photos_first_date_taken = models.DateTimeField()
    photos_first_date = models.DateTimeField()
    photos_count = models.PositiveIntegerField()
    photos_views = models.PositiveIntegerField(null=True, blank=True,
                                        help_text="Not available for all users.")
    
    def __unicode__(self):
        return u"%s (%s)" % (self.realname, self.username)

    @models.permalink
    def get_absolute_url(self):
        return ('flickr_user_detail', (), {'path_alias': self.path_alias, })
    
    def get_buddy_icon_url(self):
        """See http://www.flickr.com/services/api/misc.buddyicons.html """
        if self.iconserver:
            # Is present, or is not 0...
            return 'http://farm%s.staticflickr.com/%s/buddyicons/%s.jpg' % (
                    self.iconfarm,
                    self.iconserver,
                    self.nsid,
            )
        else:
            return 'http://www.flickr.com/images/buddyicon.gif'


