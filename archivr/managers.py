from django.db import models

class FeaturedManager(models.Manager):
    """
    All ArchivrItems that are not 'hidden' and are 'featured'.
    """
    def get_query_set(self):
        return super(FeaturedManager, self).get_query_set().filter(hidden=False).filter(featured=True)

class VisibleManager(models.Manager):
    """
    All ArchivrItems that are not 'hidden'.
    """
    def get_query_set(self):
        return super(VisibleManager, self).get_query_set().filter(hidden=False)

