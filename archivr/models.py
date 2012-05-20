from django.db import models

from archivr.managers import FeaturedManager, VisibleManager

# So we can group different models of the same type together.
# eg, fetch Flickr and Instagram photos together.
ARCHIVR_ITEM_GENRES = (
    ('image', 'Image: Photos, etc.'),
    ('status', 'Status: Tweet, etc.'),
    ('link', 'Link: Pinboard, Delicious, etc.'),
    ('video', 'Video: YouTube, Flickr video, etc.'),
)

class ArchivrItem(models.Model):
    """
    The class that all Archivr classes representing "things" (eg, Tweet, Photo,
    Link, etc) will be descended from.
    Stores data that is common across all these items, and lets us fetch items of
    different types together, ordered by date (for example).
    """

    order_date = models.DateTimeField(
                                help_text="The date used for ordering the item")

    item_genre = models.CharField(max_length=20, default='',
                                                    choices=ARCHIVR_ITEM_GENRES)

    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True,
                                                                        blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True,
                                                                        blank=True)

    # Irrespective of the item's settings on the origin service.
    hidden = models.BooleanField(default=False,
                                help_text="Is this item hidden from public view?")
    # Might be useful to pick out certain items.
    featured = models.BooleanField(default=False,
                                                help_text="Is this highlighted?")

    # It would be nice to have something like this, using GeoDjango, but that seems
    # like quite an overhead for this project at the moment.
    #coordinate = models.PointField(srid=4326, null=True, blank=True,
                                            #help_text="Where this item is located")

    class Meta:
        ordering = ('-order_date',)
        get_latest_by = 'order_date'

    # ALL items.
    objects = models.Manager()
    # Items that haven't been marked as hidden.
    visible_objects = VisibleManager()
    # Items that haven't been marked as hidden and have been marked as featured.
    featured_objects = FeaturedManager()


    def is_a(self, item_kind):
        """
        Test what kind of item this is.
        eg `item.is_a('tweet')`
        Note, this doesn't refer to the item_genre, which is a more general grouping.
        """
        if hasattr(self, str(item_kind)):
            return True
        else:
            return False

