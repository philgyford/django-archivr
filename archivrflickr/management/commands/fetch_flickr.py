from optparse import make_option

from django.core.management.base import LabelCommand, CommandError
from django.conf import settings

from archivrflickr.fetch import FlickrFetcher

class Command(LabelCommand):

    # fetch_flickr must be called with one of the valid_labels.
    valid_labels = (
        'photo',
        'photos',
        'photoset',
        'photosets',
        'favorites',
    )

    option_list = LabelCommand.option_list + (
            make_option('--username',
                metavar = 'USERNAME',
                dest = 'username',
                help = 'The Flickr username, as set in settings.py.',),

            # Ignored when fetching photosets.
            make_option('--days',
                metavar = 'DAYS',
                default = 1, # By default we fetch most recent 1 day. Safe.
                dest = 'days',
                help = 'Number of days of recent Photos or Favorites to fetch, or "all". (Default is 1).',),

            make_option('--photo_id',
                metavar = 'PHOTO_ID',
                dest = 'photo_id',
                help = 'The Flickr ID of a Photo to fetch.',),

            make_option('--photoset_id',
                metavar = 'PHOTOSET_ID',
                dest = 'photoset_id',
                help = 'The Flickr ID of a Photoset to fetch.',),

            # We could add options to fetch/not fetch Comments, Sizes, EXIF and Geo
            # data on Photos, but we're going to Keep It Simpleish for now.
    )

    # Will be an instance of FlickrFetcher.
    flickr_fetcher = False

    def handle_label(self, label, **options):
        """
        Initial method called after options are processed.
        Do general checking and setting up the FlickrFetcher before passing off
        to a more specific method.
        """

        if options.get('username') is not None:
            username = options.get('username')
        else:
            raise CommandError('You must pass in a Flickr username.')

        try:
            settings.FLICKR_ACCOUNTS
        except AttributeError:
            raise CommandError('There is no FLICKR_ACCOUNTS in settings.')

        try:
            flickr_settings = settings.FLICKR_ACCOUNTS[username]
        except:
            raise CommandError('There is no "%s" username in settings.FLICKR_ACCOUNTS' % username) 

        # Do we have a valid subcommand after 'fetch_flickr '?
        try:
            self.valid_labels.index(label)
        except ValueError:
            raise CommandError('"%s" is not a valid subcommand. Try one of these: %s' % (
                label,
                ', '.join(self.valid_labels),
            ))

        # Prepare for fetching things...
        self.flickr_fetcher = FlickrFetcher(username=username,
                                api_key=flickr_settings['api_key'],
                                api_secret=flickr_settings['api_secret'],
                                verbosity=options.get('verbosity'))

        # Then, after double-checking we have a method for it, call the subcommand.
        method_name = 'handle_subcommand_'+label
        if hasattr(self, method_name):
            getattr(self, method_name)(**options)
        else:
            raise CommandError('Oops, something went wrong... there\'s no method named "%s"' % method_name) 

    def handle_subcommand_photo(self, **options):
        if options.get('photo_id') is None:
            raise CommandError('A photo_id is required to fetch a Photo.')
        self.flickr_fetcher.fetch_photo(options.get('photo_id'))

    def handle_subcommand_photos(self, **options):
        if options.get('days') == 'all':
            self.flickr_fetcher.fetch_all_photos()
        else:
            self.flickr_fetcher.fetch_recent_photos(options.get('days'))

    def handle_subcommand_photoset(self, **options):
        if options.get('photoset_id') is None:
            raise CommandError('A photoset_id is required to fetch a Photoset.')
        self.flickr_fetcher.fetch_photoset(options.get('photoset_id'))

    def handle_subcommand_photosets(self, **options):
        self.flickr_fetcher.fetch_all_photosets()

    def handle_subcommand_favorites(self, **options):
        print "Yeah, let's get favorites"


    @property
    def help(self):
        lines = ['Archivr Flickr command line interface.', '', ]
        lines.append('Call "fetch_flickr" with one of these subcommands:')
        lines.append('  %s' % ', '.join(self.valid_labels))
        lines.append('')
        lines.append('Examples:')
        lines.append('')
        lines.append('  Fetch ALL of Phil Gyford\'s Photos:')
        lines.append('    ./manage.py fetch_flickr photos --username="Phil Gyford" --days=all')
        lines.append('')
        lines.append('  Fetch a particular one of Phil Gyford\'s Photos:')
        lines.append('    ./manage.py fetch_flickr photo --username="Phil Gyford" --photo_id=7510891034')
        lines.append('')
        lines.append('  Fetch photos Phil Gyford has favorited in the past 3 days:')
        lines.append('    ./manage.py fetch_flickr favorites --username="Phil Gyford" --days=3')
        lines.append('')
        lines.append('  Fetch Phil Gyford\'s Photosets (--days option would have no effect):')
        lines.append('    ./manage.py fetch_flickr photosets --username="Phil Gyford"')
        lines.append('')
        lines.append('The Flickr username should be set in the FLICKR_ACCOUNTS dict in settings.py.')
        lines.append('(See README.)')
        return '\n'.join(lines)

