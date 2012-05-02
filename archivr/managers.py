from django.db import models


class VisibleManager(models.Manager):
    """
    All ArchivrItems that are not 'hidden'.
    """
    def get_query_set(self):
        return super(VisibleManager, self).get_query_set().filter(hidden=False)

