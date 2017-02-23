import xlwt
import time
import binascii
import uuid
import json
import requests
from tornado.auth import _oauth10a_signature
from urllib import urlencode

header = ['ScreenName', 'Name', 'Description', 'Location', 'Tweets', 'Following', 'Followers',\
	  'Likes', 'Image', 'Lists', 'TimeZone', 'Language', 'IsVerified', 'Twitter URL']

class TwitterAPICrawler:

	def __init__(self, *args, **kwargs):
		access_token = dict(key='16950741-8LHKI317UCMiNvEW2iLc564CKl15AnRNnAuHYroco', secret='U6CjXnoii013YMkOQRZfpLwZ12IkZdQCkTHV2lK0JgqXx')
		consumer_token = dict(key='Ub2YlYi5i9VLiU6qVGcw', secret='qjx2esDiY70OxAVqVrA80AK9QLYXU2gYSmmcEPKJSg')

		excel_file_name = 'twitter_profiles.xls'
		todays_excel_file = xlwt.Workbook(encoding="utf-8")
		todays_excel_sheet1 = todays_excel_file.add_sheet("sheet1")
		row_count = 1

		for i, row in enumerate(header):
			todays_excel_sheet1.write(0, i, row) 


	def _oauth_request_parameters(url, consumer_token, access_token, parameters={},
				      method="GET"):
	    """Returns the OAuth parameters as a dict for the given request.

	    parameters should include all POST arguments and query string arguments
	    that will be sent with the request.
	    """
	    base_args = dict(
		oauth_consumer_key=consumer_token["key"],
		oauth_token=access_token["key"],
		oauth_signature_method="HMAC-SHA1",
		oauth_timestamp=str(int(time.time())),
		oauth_nonce=binascii.b2a_hex(uuid.uuid4().bytes),
		oauth_version="1.0a",
	    )
	    args = {}
	    args.update(base_args)
	    args.update(parameters)
	    signature = _oauth10a_signature(consumer_token, method, url, args,
					     access_token)
	    base_args["oauth_signature"] = signature
	    return base_args


"""for screen_url in open('t.txt'):
    screen_name = screen_url.split('/')[-1].strip()
    arguments = {}
    arguments['screen_name'] = screen_name
    print screen_name
    TW_URL = 'https://api.twitter.com/1.1/users/show.json'
    extra_arguments = oauth_request_parameters(TW_URL, consumer_token, access_token, arguments)
    arguments.update(extra_arguments)
    arguments = urlencode(arguments)
    url = '%s?%s' %(TW_URL, arguments)

    data = requests.get(url).content
    dat = json.loads(data)
    name = dat.get('name', '')
    desc  = dat.get('description', '')
    location = dat.get('location', '')
    tweets = dat.get('statuses_count', '')
    following = dat.get('friends_count', '')
    followers = dat.get('followers_count', '')
    likes = dat.get('favourites_count', '')
    image = dat.get('profile_image_url')
    listed_count = dat.get('listed_count', '')
    timezone = dat.get('time_zone', '')
    lang = dat.get('lang', '').title()
    verified = dat.get('verified', '')

    values = [screen_name, name, desc, location, tweets, following, followers,\
		likes, image, listed_count, timezone, lang, verified, screen_url]

    for col_count, value in enumerate(values):
	todays_excel_sheet1.write(row_count, col_count, value)

    row_count = row_count+1

todays_excel_file.save(excel_file_name)"""
