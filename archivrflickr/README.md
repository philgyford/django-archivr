# Archivr Flickr

The project's `settings.py` should have something like this:

	FLICKR_ACCOUNTS = {
		'Phil Gyford': {
			'api_key': '7f9324567fyd87ghjk487dhs01d21bc5',
			'api_secret': 'd987dfkg96sk34fg',
		},
	}

But using your own Flickr username, and [API key and secret](http://www.flickr.com/services/apps/create/apply/). You can find your [Flickr username here](http://www.adamwlewis.com/articles/what-is-my-flickr-id), because it's never what I think it is.

You can have multiple sets of usernames and API keys/secrets if you have more
than one account.

Use the management command to fetch photos, eg:

	$ ./manage.py fetch_flickr photos --username="Phil Gyford"

Do this for more help:

	$ ./manage.py fetch_flickr --help

