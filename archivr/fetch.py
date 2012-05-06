from taggit.models import Tag

class ArchivrFetcher(object):
    """
    The base class for all *Fetcher classes.
    """

    def __init__(self, *args, **kwargs):
        pass

    def setTags(self, item, tag_data):
        """
        Adds/deletes tags on an item (FlickrPhoto, etc).

        Required arguments
            item: The FlickrPhoto (or whatever) object. Should already have been
                        created and saved.
            tag_data: New data about the tags.
        """
        pass


