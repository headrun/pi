from tornado.auth import _oauth10a_signature
from urllib import urlencode
import binascii
import uuid
import time

from juicer.utils import *
from juicer.items import Twitter

class TwitterProfilesTerminal(JuicerSpider):
    name = 'twitter_profiles_terminal'

    def parse(self, response):
        dat = json.loads(response.body)
        name = str(dat.get('name', ''))
        desc  = str(dat.get('description', ''))
        location = str(dat.get('location', ''))
        tweets = str(dat.get('statuses_count', ''))
        following = str(dat.get('friends_count', ''))
        followers = str(dat.get('followers_count', ''))
        likes = str(dat.get('favourites_count', ''))
        image = str(dat.get('profile_image_url'))
        listed_count = str(dat.get('listed_count', ''))
        timezone = str(dat.get('time_zone', ''))
        lang = str(dat.get('lang', '').title())
        verified = str(dat.get('verified', ''))
        sk = response.meta['sk']
        sk_ = md5(sk+name)
        twitter = Twitter()
        twitter.update({"sk":normalize(sk_),"screen_name":normalize(sk), "name":normalize(name),"description":normalize(desc),"location":normalize(location),"tweets":normalize(tweets),"following":normalize(following),"followers":normalize(followers),"likes":normalize(likes),"image":normalize(image),"lists":normalize(listed_count),"timezone":normalize(timezone),"language":normalize(lang),"is_verified":normalize(verified),"twitter_url":normalize(response.meta.get('data','').get('twitter_url',''))})
        yield twitter
        self.got_page(sk,1)


