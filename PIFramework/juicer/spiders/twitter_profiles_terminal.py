from tornado.auth import _oauth10a_signature
from urllib import urlencode
import binascii
import uuid
import time

from juicer.utils import *

class TwitterProfilesTerminal(JuicerSpider):
    name = 'twitter_profiles_terminal'

    def parse(self, response):
        import pdb;pdb.set_trace()
        dat = json.loads(response.body)
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

