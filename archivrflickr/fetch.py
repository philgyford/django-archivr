import calendar
from datetime import datetime, timedelta
from decimal import Decimal
import math
import pytz
import re

from django.utils.dateparse import parse_datetime

import flickrapi

from archivr.fetch import ArchivrFetcher
from archivr.models import *
from archivrflickr.models import *
from taggit.models import Tag

# This is useful for debugging responses from Flickr.
# Do print ET.tostring(result)
#import xml.etree.ElementTree as ET

class FlickrFetcher(ArchivrFetcher):

    # We could pass in options to only get certain things, but we don't allow that
    # at the moment, keeping it simple. But the switches should be present in the
    # code to respect these settings:
    # Setting any of these to False will result in fewer calls to Flickr's API, and
    # so speed things up a little.
    fetch_content = {
        'photo_comments': True,
        'photo_sizes': True,
        'photo_exif': True,
    }

    # Flickr username of the account we're fetching data for.
    username = ''

    # Flickr NSID of the account we're fetching data for.
    nsid = ''

    # A cache of NSID: FlickrUser object.
    user_cache = dict()

    def __init__(self, username, api_key, api_secret, *args, **kwargs):
        super(FlickrFetcher, self).__init__(*args, **kwargs)

        self.flickr = flickrapi.FlickrAPI(api_key, api_secret, format='etree')

        self.username = username
        self.nsid = self._username_to_nsid(self.username)
        self.log(2, "FlickrFetcher initiated for username '%s' (%s)" %
                                                        (self.username, self.nsid))

    def _username_to_nsid(self, username):
        """
        Convert a flickr username to an NSID
        """
        try:
            return self.flickr.people_findByUsername(
                                        username=username).find('user').attrib['id']
        except flickrapi.FlickrError, err:
            self._handle_api_error('_username_to_nsid', err)

    def _handle_api_error(self, method_name, message):
        self.log(0, 'API ERROR in %s(): %s' % (method_name, message))

    def _fetch_photo_sizes(self, photo_id):
        """Return a dictionary of image sizes for a Flickr Photo.
        Fetches from Flickr, or returns 'None' for every size.

        Required arguments
          photo_id: A Flickr Photo ID as a string
        """
        sizes_data = dict()
        # Set defaults to None.
        for label in [row[1] for row in FlickrPhoto.FLICKR_PHOTO_SIZES]:
            # label will be like 'Small', 'Medium 640', 'Original', etc.
            sizes_data[label] = {'width': None, 'height': None, }

        if self.fetch_content['photo_sizes']:
            self.log(3, "Photo %s: Getting sizes" % photo_id)
            result = self.flickr.photos_getSizes(photo_id=photo_id)
            for el in result.find('sizes').findall('size'):
                sizes_data[el.attrib['label']]['width'] = el.attrib['width']
                sizes_data[el.attrib['label']]['height'] = el.attrib['height']

        if sizes_data['Original']['width'] is None:
            sizes_data['Original']['width'] = 0
        if sizes_data['Original']['height'] is None:
            sizes_data['Original']['height'] = 0

        return sizes_data

    def _fetch_photo_exif(self, photo_id):
        """Fetch the EXIF information for a photo_id

        Required arguments
          photo_id: A Flickr Photo id as a string
        """
        def getRawOrClean(xmlnode):
            try:
                return xmlnode.find('clean').text
            except AttributeError:
                try:
                    return xmlnode.find('raw').text
                except AttributeError:
                    return ''

        def testResultKey(result_elem, label):
            if result_elem.attrib['label'] == label:
                return getRawOrClean(result_elem)
            else:
                return None

        # So we end up with {'Make':'', 'ISO Speed':'',} etc.
        exif_data = {}
        for (key, desc) in FlickrPhoto.FLICKR_EXIF_FIELDS:
            exif_data[desc] = ''

        try:
            assert self.fetch_content['photo_exif']
            self.log(3, "Photo %s: Getting EXIF data" % photo_id)
            result = self.flickr.photos_getExif(photo_id=photo_id)
        except (flickrapi.FlickrError, AssertionError):
            return exif_data

        try:
            for exif_elem in result.find('photo').findall('exif'):
                for label in exif_data.keys():
                    data = testResultKey(exif_elem, label)
                    if data and not exif_data[label]:
                        exif_data[label] = data
            return exif_data
        except:
            return exif_data

    def _prepare_photo_geo(self, photo_xml):
        """Formats the Photo's geo location data so it's easier to use.
        We don't need to fetch the data separately because it's included in the
        data we get back from Flickr's photos.getInfo().

        Required arguments
          photo_xml: A Flickr Photo in Flickrapi's REST XMLNode format
        """
        geo_data = {
            'latitude': None, 'longitude': None, 'accuracy': None,
            'place_id': None, 'woe_id': None,
            'perms_is_public': None, 'perms_is_contact': None,
            'perms_is_friend': None, 'perms_is_family': None,
        }

        # So we add keys like 'county', 'county_place_id' and 'county_woe_id'.
        for (key, desc) in FlickrPhoto.FLICKR_GEO_AREAS:
            geo_data[key] = ''
            geo_data[key+'_place_id'] = ''
            geo_data[key+'_woe_id'] = ''

        location_data = photo_xml.find('photo').find('location')

        if location_data is None:
            return geo_data

        geo_data['latitude'] = Decimal(location_data.attrib['latitude'])
        geo_data['longitude'] = Decimal(location_data.attrib['longitude'])
        geo_data['accuracy'] = int(location_data.attrib['accuracy'])
        geo_data['place_id'] = location_data.attrib['place_id']
        geo_data['woe_id'] = int(location_data.attrib['woeid'])

        for bit in ('county', 'country', 'locality', 'neighbourhood', 'region',):
            if location_data.find(bit) is not None:
                geo_data[bit] = location_data.find(bit).text
                geo_data[bit+'_place_id'] = location_data.find(bit).attrib[
                                                                        'place_id']
                geo_data[bit+'_woe_id'] = int(location_data.find(bit).attrib[
                                                                        'woeid'])

        # The geoperms isn't always available.
        perms_data = photo_xml.find('photo').find('geoperms')
        try: 
            geo_data['perms_is_public'] = bool(perms_data.attrib['ispublic'])
            geo_data['perms_is_contact'] = bool(perms_data.attrib['iscontact'])
            geo_data['perms_is_friend'] = bool(perms_data.attrib['isfriend'])
            geo_data['perms_is_family'] = bool(perms_data.attrib['isfamily'])
        except:
            pass

        return geo_data

    def _get_user(self, nsid):
        """Returns a FlickrUser object.
        This is either:
            a) Fetched from self.user_cache if it's already there, or,
            b) Fetched from Flickr, inserted or updated in the database, added to
               self.user_cache, and returned.
        """
        if nsid not in self.user_cache:
            self.user_cache[nsid] = self._fetch_user(nsid)

        return self.user_cache[nsid]

    def _fetch_user(self, nsid):
        """Fetches data about a Flickr user from Flickr and puts into database.

        If there is already a user in the database with this nsid, then its data is
        updated with the data fetched from Flickr.
        """
        self.log(3, "Fetching data for user %s from Flickr" % nsid)
        try:
            user = self.flickr.people_getInfo(user_id=nsid).find('person')
        except flickrapi.FlickrError, err:
            self._handle_api_error('_fetch_and_save_user', err)
            return None

        # Some tidying up.
        if user.find('photos').find('views') is not None:
            photos_views = int(user.find('photos').find('views').text)
        else:
            photos_views = None

        # In case the date has low granularity ("Circa...")
        first_date_taken = self._fix_vague_date(
                                    user.find('photos').find('firstdatetaken').text)
        # date_taken dates have no timezone associated with them, but with Django
        # 1.4 we have to store a timezone, so we save it as UTC.
        first_date_taken = pytz.UTC.localize(parse_datetime(first_date_taken))

        defaults_dict = {
            'nsid': nsid,
            'username': user.find('username').text,
            'realname': user.find('realname').text or '',
            'path_alias': user.attrib['path_alias'],
            'location': user.find('location').text or '',
            'description': user.find('description').text or '',
            'photos_url': user.find('photosurl').text,
            'profile_url': user.find('profileurl').text,
            'mobile_url': user.find('mobileurl').text,
            'icon_server': user.attrib['iconserver'],
            'icon_farm': user.attrib['iconfarm'],
            'is_pro': bool(user.attrib['ispro']),
            # In case the first date taken has low granularity ("Circa...")
            'photos_first_date_taken': first_date_taken,
            'photos_first_date': pytz.UTC.localize(datetime.utcfromtimestamp(
                                int(user.find('photos').find('firstdate').text))),
            'photos_count': user.find('photos').find('count').text,
            'photos_views': photos_views,
        }
        user_obj, created = FlickrUser.objects.get_or_create(nsid=nsid,
                                                            defaults=defaults_dict)
        if created:
            self.log(3, "Saved new FlickrUser to database with pk %s" % user_obj.pk)
        else:
            self.log(3, "Updating FlickrUser pk %s in database" % user_obj.pk)
            user_obj = FlickrUser(pk=user_obj.pk, **defaults_dict)
            user_obj.save()

        return user_obj

    def _set_photo_tags(self, photo_obj, photo_xml):
        """Adds/deletes tags for a FlickrPhoto to keep them in sync with Flickr.

        Required arguments
          photo_obj: The FlickrPhoto object we're altering tags for.
          photos_xml: Data straight from the Flickr API about a photo.
        """
        # The existing tag-photo relationships.
        tagged_photos = FlickrPhoto.tags.through.objects.filter(
                                                        content_object=photo_obj)

        # The new tags fetched from Flickr.
        remote_tags = self._get_photo_tag_list(photo_xml)

        local_flickr_ids = set([])
        remote_flickr_ids = set([])

        # Get the Flickr IDs of all the current tag-photo relationships.
        for tagged_photo in tagged_photos:
            local_flickr_ids.add(tagged_photo.flickr_id)

        for tag in remote_tags:
            remote_flickr_ids.add(tag['flickr_id'])
            if tag['flickr_id'] not in local_flickr_ids:
                # This tag isn't currently on the photo, so add it.
                tag_obj, tag_created = Tag.objects.get_or_create(
                    slug = tag['slug'], defaults = {'name': tag['name']}
                )
                pt_obj = FlickrPhoto.tags.through(
                        flickr_id = tag['flickr_id'],
                        author = tag['author'],
                        machine_tag = tag['machine_tag'],
                        content_object = photo_obj,
                        tag = tag_obj,
                )
                pt_obj.save()

        flickr_ids_to_delete = local_flickr_ids.difference(remote_flickr_ids)

        # Finally, delete any tag-photo relationships which were identified
        # above as no longer on the photo on Flickr.
        for tagged_photo in tagged_photos:
            if tagged_photo.flickr_id in flickr_ids_to_delete:
                tagged_photo.delete()
        
    def _get_photo_tag_list(self, photo_xml):
        """
        Return a nice list of all tags for a photo on Flickr.

        Each tag is represented as a dictionary in this format:
            tag = {
                'name': 'Cooper Taber',
                'slug': 'coopertaber',
                'flickr_id': '5827-3536073747-40115981',
                'author': [FlickrUser object],
                'machine_tag': False,
            }

        Required arguments
          photos_xml: Data straight from the Flickr API about a photo.
        """
        tags = []
        if photo_xml.find('photo').find('tags') is not None:
            for el in photo_xml.find('photo').find('tags').findall('tag'):
                machine_tag = False
                if el.attrib['machine_tag'].isdigit() and int(
                                                    el.attrib['machine_tag']) == 1:
                    machine_tag = True
                author = self._get_user(el.attrib['author'])
                tags.append(
                    {
                        'name': el.attrib['raw'],
                        'slug': el.text,
                        'flickr_id': el.attrib['id'],
                        'author': author,
                        'machine_tag': machine_tag,
                    }
                )
        return tags

    def _fix_vague_date(self, datetime):
        """Make a vague date from Flickr into a valid Django date.

        Some dates from Flickr are of the form '1956-00-01 00:00:00', ie, 
        their granularity is low so the month is '00'. Django/Python complains at
        this, so we have to change the month to '01'.

        If the date is already OK, it should just return that.

        Required arguments:
          datetime A string of the form 'YYYY-MM-DD hh:mm:ss'
        """
        return re.sub(r'^(?P<year>\d{,4}-)00(?P<remainder>.*?)$',
                                           r'\g<year>01\g<remainder>', datetime)

    def _fetch_photo(self, photo_xml):
        """Synchronize a Flickr Photo with the Django backend.

        Required Arguments
          photo_xml: A Flickr Photo in Flickrapi's ElementTree format
        """

        photo_data = photo_xml.find('photo')
        photo_id = photo_data.attrib['id']
        self.log(3, "Photo %s: Getting extra data from Flickr" % photo_id)

        sizes_data = self._fetch_photo_sizes(photo_id)
        exif_data = self._fetch_photo_exif(photo_id)
        geo_data = self._prepare_photo_geo(photo_xml)

        taken_granularity = int(photo_data.find('dates').attrib['takengranularity'])
        taken = photo_data.find('dates').attrib['taken']
        if taken_granularity == 8:
            # When granularity is 'Circa...' then the month comes back as '00'
            # which makes for an invalid datetime, so we fix it.
            # eg, make '1956-00-01 00:00:00'
            #     into '1956-01-01 00:00:00'
            taken = self._fix_vague_date(taken)
        
        # The date taken has no timezone (because Flickr doesn't know the timezone
        # the photo was taken in). But with Django 1.4 we can't store naive
        # datetimes, so we store it as UTC.
        taken_date = pytz.UTC.localize(parse_datetime(taken))

        # These are both from UTC timestamps:
        upload_date = pytz.UTC.localize(datetime.utcfromtimestamp(
                                    int(photo_data.find('dates').attrib['posted'])))
        updated_date = pytz.UTC.localize(datetime.utcfromtimestamp(
                                int(photo_data.find('dates').attrib['lastupdate'])))

        try:
            original_secret = photo_data.attrib['originalsecret']
        except KeyError:
            original_secret = ''

        owner = self._get_user(photo_data.find('owner').attrib['nsid'])

        defaults_dict = {
            'order_date': upload_date,

            'flickr_id': photo_data.attrib['id'],
            'owner': owner,
            'title': photo_data.find('title').text,
            'description': photo_data.find('description').text,
            
            'posted_date': upload_date,
            'updated_date': updated_date,
            'taken_date': taken_date,
            'taken_granularity': taken_granularity,

            'visibility_is_public': bool(
                                photo_data.find('visibility').attrib['ispublic']),
            'visibility_is_friend': bool(
                                photo_data.find('visibility').attrib['isfriend']),
            'visibility_is_family': bool(
                                photo_data.find('visibility').attrib['isfamily']),

            'photopage_url': photo_data.find('urls').find('url').text,
            'farm': photo_data.attrib['farm'],
            'server': photo_data.attrib['server'],
            'secret': photo_data.attrib['secret'],
            'original_secret': original_secret,
            'original_format': photo_data.attrib['originalformat'],
            'safety_level': int(photo_data.attrib['safety_level']),
            'rotation': int(photo_data.attrib['rotation']),
            'license': int(photo_data.attrib['license']),

            # More geo fields added below...
            'geo_latitude': geo_data['latitude'],
            'geo_longitude': geo_data['longitude'],
            'geo_accuracy': geo_data['accuracy'],
            'geo_place_id': geo_data['place_id'],
            'geo_woe_id': geo_data['woe_id'],
            'geo_perms_is_public': geo_data['perms_is_public'],
            'geo_perms_is_contact': geo_data['perms_is_contact'],
            'geo_perms_is_friend': geo_data['perms_is_friend'],
            'geo_perms_is_family': geo_data['perms_is_family'],

            # Both these on ArchivrItem model.
            'latitude': geo_data['latitude'],
            'longitude': geo_data['longitude'],
        }

        for (key, desc, l) in FlickrPhoto.FLICKR_PHOTO_SIZES:
            defaults_dict[key+'_width'] = sizes_data[desc]['width']
            defaults_dict[key+'_height'] = sizes_data[desc]['height']

        for (key, desc) in FlickrPhoto.FLICKR_GEO_AREAS:
            defaults_dict['geo_'+key] = geo_data[key]

        for (key, desc) in FlickrPhoto.FLICKR_EXIF_FIELDS:
            defaults_dict['exif_'+key] = exif_data[desc]


        if photo_data.find('video') is None:
            defaults_dict['item_genre'] = 'image'
        else:
            defaults_dict['item_genre'] = 'video'
            defaults_dict['is_video'] = True
            defaults_dict['video_duration'] = int(
                                        photo_data.find('video').attrib['duration'])
            defaults_dict['video_width'] = int(
                                        photo_data.find('video').attrib['width'])
            defaults_dict['video_height'] = int(
                                        photo_data.find('video').attrib['height'])

        # For debugging:
        # from django.db import connection
        # print connection.queries
        photo_obj, created = FlickrPhoto.objects.get_or_create(
                                                flickr_id = photo_data.attrib['id'], 
                                                defaults=defaults_dict)

        if created:
            self.log(2, "Created new Flickr Photo %s (Flickr ID: %s)" % 
                                            (photo_obj.pk, photo_obj.flickr_id))

        if created or photo_obj.updated_date < updated_date:
            # This photo is new or updated, so set the tags.
            self._set_photo_tags(photo_obj, photo_xml)

        if photo_obj.updated_date < updated_date:
            # Photo is updated on Flickr, so update local data.
            photo_obj = FlickrPhoto(pk=photo_obj.pk, **defaults_dict)
            photo_obj.save()
            self.log(2, "Updated local data for Flickr Photo %s (Flickr ID: %s)" % 
                                            (photo_obj.pk, photo_obj.flickr_id))

        # TODO: Comments.
        #if self.fetch_content['photo_comments']:
            #comments = self.getPhotoComments(obj.flickr_id)
            #if comments is not None:
                #for c in comments:
                    #c['photo'] = obj
                    #comment, created = PhotoComment.objects.get_or_create(flickr_id=c['flickr_id'], defaults=c)

        return photo_obj

    def _fetch_photo_xml_list(self, photos_xml):
        """Fetch a list of Flickr Photos and put into the Django database.

        Required arguents
          photos_xml: A list of photos in Flickrapi's ElementTree format.
        """
        photo_list = []
        for photo in photos_xml:
            self.log(3, "Photo %s: Getting basic data from Flickr" %
                                                                photo.attrib['id'])
            photo_result = self.flickr.photos_getInfo(photo_id=photo.attrib['id'])
            photo_list.append(self._fetch_photo(photo_result))
        return photo_list


    def fetch_photo(self, photo_id):
        """Fetch a single Flickr photo and put it in the database."""
        self.log(2, "Fetching Photo ID %s" % photo_id)
        photo_result = self.flickr.photos_getInfo(photo_id = photo_id)
        return self._fetch_photo(photo_result)


    def fetch_all_photos(self):
        self.log(2, "Fetching All Photos")


    def fetch_recent_photos(self, days):
        """
        Fetch all a user's Flickr photos for the most recent 'days' days and put
        them in the database.
        """
        self.log(2, "Fetching Photos from past %s day(s)" % days)
        fetch_since = datetime.now() - timedelta(days=int(days))
        timestamp = calendar.timegm(fetch_since.timetuple())

        result = self.flickr.photos_search(user_id=self.nsid, per_page=500,
                                                        min_upload_date=timestamp)
        page_count = result.find('photos').attrib['pages']
        photo_count = 0

        for page in range(1, int(page_count)+1):
            self.log(3, "Fetching page %s of %s" % (page, page_count))
            photo_list = self._fetch_photo_xml_list(
                                            result.find('photos').findall('photo'))
            photo_count += len(photo_list)
            result = self.flickr.photos_search(user_id=self.nsid, page=page+1,
                                        per_page=500, min_upload_date=timestamp)

        self.log(1, "Fetched %s Photo(s)." % photo_count)


    def fetch_photoset(self, photoset_id, order=0):
        """
        Fetches the specified Photoset, and all the Photos in it.
        The ``order`` is for when this is called by fetch_all_photosets(), 
        which is the only way we can give the Photosets their correct order.
        """
        self.log(2, "Fetching Photoset ID %s" % photoset_id)
        result = self.flickr.photosets_getInfo(photoset_id = photoset_id)

        photoset_xml = result.find('photoset')
        primary = self.fetch_photo(photoset_xml.attrib['primary'])
        owner = self._fetch_user(photoset_xml.attrib['owner'])

        photoset, created = FlickrPhotoset.objects.get_or_create(
            flickr_id = photoset_id,
            defaults = {
                'flickr_id': photoset_xml.attrib['id'],
                'primary': primary,
                'owner': owner,
                'title': photoset_xml.find('title').text,
                'description': photoset_xml.find('description').text,
                'created_date': pytz.UTC.localize(datetime.utcfromtimestamp(
                                        int(photoset_xml.attrib['date_create']))),
                'updated_date': pytz.UTC.localize(datetime.utcfromtimestamp(
                                        int(photoset_xml.attrib['date_update']))),
                'order': order,
            }
        )

        if not created:
            # Update the Photoset.
            photoset.primary = primary
            photoset.owner = owner
            photoset.title = photoset_xml.find('title').text
            photoset.description = photoset_xml.find('description').text
            photoset.updated_date = pytz.UTC.localize(datetime.utcfromtimestamp(
                                        int(photoset_xml.attrib['date_update'])))
            photoset.order = order

        num_photos = float(photoset_xml.attrib['photos'])
        page_count = int(math.ceil(num_photos / 500))

        for page in range(1, page_count+1):
            result = self.flickr.photosets_getPhotos(
                                    photoset_id=photoset_id, per_page=500, page=page)
            photo_list = self._fetch_photo_xml_list(
                                        result.find('photoset').findall('photo'))
            for photo in photo_list:
                if photo is not None:
                    photoset.photos.add(photo)

        photoset.save()


    def fetch_all_photosets(self):
        """
        There is no concept of "recent" Photosets, so "all" is the only option.
        """
        self.log(2, "Fetching all Photosets")

        result = self.flickr.photosets_getList(user_id=self.nsid)

        # for i, photoset in enumerate()
        # import xml.etree.ElementTree as ET
        # print ET.tostring(result)
        for i, photoset in enumerate(result.find('photosets').findall('photoset')):
            self.fetch_photoset(photoset.attrib['id'], i + 1)




    def fetch_all_favorites(self):
        pass


    def fetch_recent_favorites(self, days):
        pass
    
