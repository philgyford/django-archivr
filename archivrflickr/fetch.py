import calendar
from datetime import datetime, timedelta

import flickrapi

from archivr.fetch import ArchivrFetcher
from archivr.models import *
from archivrflickr.models import *

class FlickrFetcher(ArchivrFetcher):

    username = ''
    nsid = ''

    # We could pass in options to only get certain things, but we don't allow that
    # at the moment, keeping it simple. But the switches should be present in the
    # code to respect these settings:
    fetch_content = {
        'photo_comments': True,
        'photo_sizes': True,
        'photo_exif': True,
        'photo_geo': True,
    }

    def __init__(self, username, api_key, api_secret, *args, **kwargs):
        super(FlickrFetcher, self).__init__(*args, **kwargs)

        self.flickr = flickrapi.FlickrAPI(api_key, api_secret, format='xmlnode')

        self.username = username
        self.nsid = self._username_to_nsid(self.username)
        self.log(2, "FlickrFetcher initiated for username '%s' (%s)" %
                                                        (self.username, self.nsid))

    def _username_to_nsid(self, username):
        """
        Convert a flickr username to an NSID
        """
        try:
            return self.flickr.people_findByUsername(username=username).user[0]['nsid']        
        except flickrapi.FlickrError, err:
            self._handle_api_error('_username_to_nsid', err)

    def _handle_api_error(self, method_name, message):
        self.log(0, 'API ERROR in %s(): %s' % (method_name, message))


    def fetch_photo(self):
        pass

    def fetch_all_photos(self):
        self.log(2, "Fetching All Photos")

    def fetch_recent_photos(self, days):
        self.log(2, "Fetching Photos from past %s day(s)" % days)
        fetch_since = datetime.now() - timedelta(days=int(days))
        timestamp = calendar.timegm(fetch_since.timetuple())

        result = self.flickr.photos_search(user_id=self.nsid, per_page=500,
                                                        min_upload_date=timestamp)
        print result

        #page_count = result.photos[0]['pages']
        #for page in range(1, int(page_count)+1):
            #photo_list = self._fetch_photo_list(result[u'photos'][u'photo'])
            #photo_count += len(photo_list)
            #result = self.photos_search(min_upload_date=timestamp, page=page+1)

        #print 'Found %s photos.\n' % photo_count

    def fetch_photosets(self):
        pass

    def fetch_favorites(self):
        pass
    
