import logging

class ArchivrFetcher(object):
    """
    The base class for all *Fetcher classes.
    """

    # Verbosity level; 0=minimal output, 1=normal output,
    # 2=verbose output, 3=very verbose output
    verbosity = 1


    def __init__(self, *args, **kwargs):
        if kwargs.get('verbosity') is not None:
            self.verbosity = int(kwargs.get('verbosity'))


    def log(self, level, message):
        """
        Logging method.
        Call with a numerical level, from 0-3, like self.verbosity.
        `0` messages will always be output.
        """
        if int(level) <= self.verbosity:
            print message


    def setTags(self, item, tag_data):
        """
        Adds/deletes tags on an item (FlickrPhoto, etc).

        Required arguments
            item: The FlickrPhoto (or whatever) object. Should already have been
                        created and saved.
            tag_data: New data about the tags.
        """
        pass


