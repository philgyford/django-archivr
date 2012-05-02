from django.db import models
from django.utils.html import strip_tags
from django.utils.text import truncate_words
from django.utils.translation import ugettext_lazy as _

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

    def numPhotos(self):
        return len(self.photo_list.objects.all())

    def __unicode__(self):
        return u"%s's favorite photos" % self.owner


class FlickrPhoto(ArchivrItem):
    """
    A single photo on Flickr.
    """

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

    # Granularity: http://www.flickr.com/services/api/misc.dates.html
    FLICKR_DATE_GRANULARITIES = (
        (0, 'Y-m-d H:i:s'),
        (4, 'Y-m'),
        (6, 'Y'),
        (8, 'Circa...'),
    )

    # Data from Flickr:
    flickr_id = models.CharField(max_length=50, unique=True,
                                            help_text="ID of this photo on Flickr.")
    owner = models.ForeignKey('FlickrUser')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    posted_date = models.DateTimeField(help_text="UTC")
    updated_date = models.DateTimeField(help_text="UTC")
    taken_date = models.DateTimeField(
                                help_text="In Flickr user's timezone (unknown).")
    taken_granularity = models.PositiveSmallIntegerField(default=0,
                                                choices=FLICKR_DATE_GRANULARITIES)

    comments = models.PositiveIntegerField(default=0)
    license = models.CharField(max_length=50, choices=FLICKR_LICENSES)
    visibility_is_public = models.BooleanField(default=False)
    visibility_is_friend = models.BooleanField(default=False)
    visibility_is_family = models.BooleanField(default=False)

    photopage_url = models.URLField(verify_exists=False)
    farm = models.PositiveSmallIntegerField()
    server = models.PositiveSmallIntegerField()
    secret = models.CharField(max_length=10)
    original_secret = models.CharField(max_length=10, blank=True)
    original_format = models.CharField(max_length=10, blank=True)

    large_height = models.PositiveSmallIntegerField(null=True)
    large_width = models.PositiveSmallIntegerField(null=True)
    largesquare_height = models.PositiveSmallIntegerField(null=True)
    largesquare_width = models.PositiveSmallIntegerField(null=True)
    medium640_height = models.PositiveSmallIntegerField(null=True)
    medium640_width = models.PositiveSmallIntegerField(null=True)
    medium800_height = models.PositiveSmallIntegerField(null=True)
    medium800_width = models.PositiveSmallIntegerField(null=True)
    medium_height = models.PositiveSmallIntegerField(null=True)
    medium_width = models.PositiveSmallIntegerField(null=True)
    original_height = models.PositiveSmallIntegerField(null=True)
    original_width = models.PositiveSmallIntegerField(null=True)
    small320_height = models.PositiveSmallIntegerField(null=True)
    small320_width = models.PositiveSmallIntegerField(null=True)
    small_height = models.PositiveSmallIntegerField(null=True)
    small_width = models.PositiveSmallIntegerField(null=True)
    square_height = models.PositiveSmallIntegerField(null=True)
    square_width = models.PositiveSmallIntegerField(null=True)
    thumbnail_height = models.PositiveSmallIntegerField(null=True)
    thumbnail_width = models.PositiveSmallIntegerField(null=True)

    geo_latitude = models.FloatField(null=True, blank=True)
    geo_longitude = models.FloatField(null=True, blank=True)
    geo_accuracy = models.PositiveSmallIntegerField(null=True, blank=True)
    geo_county = models.CharField(max_length=255, blank=True)
    geo_county_place_id = models.CharField(max_length=50, blank=True)
    geo_county_woe_id = models.PositiveIntegerField(max_length=50, blank=True)
    geo_country = models.CharField(max_length=255, blank=True)
    geo_country_place_id = models.CharField(max_length=50, blank=True)
    geo_country_woe_id = models.PositiveIntegerField(max_length=50, blank=True)
    geo_locality = models.CharField(max_length=255, blank=True)
    geo_locality_place_id = models.CharField(max_length=50, blank=True)
    geo_locality_woe_id = models.PositiveIntegerField(max_length=50, blank=True)
    geo_region = models.CharField(max_length=255, blank=True)
    geo_region_place_id = models.CharField(max_length=50, blank=True)
    geo_region_woe_id = models.PositiveIntegerField(max_length=50, blank=True)

    exif_aperture = models.CharField(max_length=255, blank=True)
    exif_color_space = models.CharField(max_length=255, blank=True)
    exif_exposure = models.CharField(max_length=255, blank=True)
    exif_flash = models.CharField(max_length=255, blank=True)
    exif_focal_length = models.CharField(max_length=255, blank=True)
    exif_iso = models.CharField(max_length=255, blank=True)
    exif_make  = models.CharField(max_length=255, blank=True)
    exif_metering_mode = models.CharField(max_length=255, blank=True)
    exif_model = models.CharField(max_length=255, blank=True)
    exif_orientation = models.CharField(max_length=255, blank=True)
    exif_software = models.CharField(max_length=255, blank=True)
    
    tags = TaggableManager(blank=True, through='FlickrPhotoTag')

    class Meta:
        ordering = ('-taken_date',)
        get_latest_by = 'posted_date'

    def __unicode__(self):
        return u'%s' % self.title

    @models.permalink
    def get_absolute_url(self):
        return ('flickr_photo_detail', (), { 'flickr_id': self.flickr_id, })

    # ALL FlickrPhotos.
    objects = models.Manager()
    # FlickrPhotos that haven't been marked as hidden.
    visible_objects = VisibleManager()

    def _get_photo_url_helper(self, size, secret=None, extension='jpg'):
        size = size and '_%s' % size or ''
        if secret is None:
            secret = self.secret
        return u'http://farm%s.static.flickr.com/%s/%s_%s%s.%s' % (
            self.farm, self.server, self.flickr_id, secret, size, extension)

    def get_square_url(self):
        return self._get_photo_url_helper('s')

    def get_thumbnail_url(self):
        return self._get_photo_url_helper('t')

    def get_small_url(self):
        return self._get_photo_url_helper('m')

    def get_small320_url(self):
        if self.has_small320_photo:
            return self._get_photo_url_helper('n')
        return self.get_original_url()

    def get_medium_url(self):
        if self.has_medium_photo:
            return self._get_photo_url_helper('')
        return self.get_original_url()

    def get_medium640_url(self):
        if self.has_medium640_photo:
            return self._get_photo_url_helper('z')
        return self.get_original_url()

    def get_medium800_url(self):
        if self.has_medium800_photo:
            return self._get_photo_url_helper('c')
        return self.get_original_url()

    def get_large_url(self):
        if self.has_large_photo:
            return self._get_photo_url_helper('b')
        return self.get_original_url()

    def get_largesquare_url(self):
        if self.has_largesquare_photo:
            return self._get_photo_url_helper('q')
        return self.get_original_url()

    def get_original_url(self):
        if self.original_secret:
            return self._get_photo_url_helper('o', secret=self.original_secret,
                                                    extension=self.original_format)
        return self._get_photo_url_helper('o', extension=self.original_format)

    @property
    def has_small320_photo(self):
        if self.small320_width is not None:
            return True
        return False

    @property
    def has_medium_photo(self):
        if self.medium_width is not None:
            return True
        return False

    @property
    def has_medium640_photo(self):
        if self.medium640_width is not None:
            return True
        return False

    @property
    def has_medium800_photo(self):
        if self.medium800_width is not None:
            return True
        return False

    @property
    def has_large_photo(self):
        if self.large_width is not None:
            return True
        return False

    @property
    def has_largesquare_photo(self):
        if self.largesquare_width is not None:
            return True
        return False

    @property
    def has_original_photo(self):
        if self.original_width is not None:
            return True
        return False

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

    def get_absolute_url(self):
        return self.permanent_url

    def get_short_comment(self, num=6):
        return truncate_words(strip_tags(self.comment), num)
    get_short_comment.short_description = _(u'comment')


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
        return ('photoset_detail', (), { 'flickr_id': self.flickr_id })

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
    author_nsid = models.CharField(max_length=50, verbose_name='Author NSID')
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
    realname = models.CharField(max_length=255,
                            help_text="eg, 'Phil Gyford'. Doesn't always exist.")
    path_alias = models.CharField(max_length=50)
    location = models.CharField(max_length=255)
    description = models.TextField()

    photos_url = models.URLField(verify_exists = False)
    profile_url = models.URLField(verify_exists = False)
    mobile_url = models.URLField(verify_exists = False)

    iconserver = models.PositiveSmallIntegerField()
    iconfarm = models.PositiveSmallIntegerField()

    photos_first_date_taken = models.DateTimeField()
    photos_first_date = models.DateTimeField()
    photos_count = models.PositiveIntegerField()
    photos_views = models.PositiveIntegerField()

