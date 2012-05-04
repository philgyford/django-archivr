from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

from archivr.managers import FeaturedManager, VisibleManager

# So we can group different models of the same type together.
# eg, fetch Flickr and Instagram photos together.
ARCHIVR_ITEM_GENRES = (
    ('image', 'Image: Photos, etc.'),
    ('status', 'Status: Tweet, etc.'),
    ('link', 'Link: Pinboard, Delicious, etc.'),
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
    # Irrespective of the item's settings on the origin service.
    hidden = models.BooleanField(default=False,
                                help_text="Is this item hidden from public view?")
    # Might be useful to pick out certain items.
    featured = models.BooleanField(default=False,
                                                help_text="Is this highlighted?")
    coordinate = models.PointField(null=True,
                                            help_text="Where this item is located")
    item_genre = models.CharField(max_length=20, default='',
                                                    choices=ARCHIVR_ITEM_GENRES)


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

