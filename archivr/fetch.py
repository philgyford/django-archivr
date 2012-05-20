import logging

class ArchivrFetcher(object):
    """The base class for all *Fetcher classes.
    """

    # Verbosity level; 0=minimal output, 1=normal output,
    # 2=verbose output, 3=very verbose output
    verbosity = 1


    def __init__(self, *args, **kwargs):
        if kwargs.get('verbosity') is not None:
            self.verbosity = int(kwargs.get('verbosity'))


    def log(self, level, message):
        """Logging method.
        Call with a numerical level, from 0-3, like self.verbosity.
        `0` messages will always be output.
        """
        if int(level) <= self.verbosity:
            print message




