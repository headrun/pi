from tornado.auth import _oauth10a_signature
from urllib import urlencode
import binascii
import uuid
import time
from scrapy.exceptions import NotConfigured, IgnoreRequest
from juicer.utils import *
from juicer.items import Twitter


class TwitterProfilesTerminal(JuicerSpider):
    name = 'twitter_profiles_terminal'
    handle_http_status_list = ['429', '404', '403', '401']
    """def __init__(self, *args, **kwargs):
        super(TwitterProfilesTerminal, self).__init__(*args, **kwargs)
    def __init__(self, name=None, **kwargs):
        #self.crawl_type = kwargs.get('crawl_type', 'twitter')
        super(TwitterProfilesTerminal, self).__init__(name, **kwargs)
        if self.crawl_type == 'twitter':
            import pdb;pdb.set_trace()
            self.start_urls = ['https://api.twitter.com/1.1/users/show.json?screen_name=__ravi__&oauth_nonce=7b087494a9fe4ebb80517d157ff1c788&oauth_timestamp=1491541679&oauth_consumer_key=Ub2YlYi5i9VLiU6qVGcw&oauth_signature_method=HMAC-SHA1&oauth_version=1.0a&oauth_token=16950741-8LHKI317UCMiNvEW2iLc564CKl15AnRNnAuHYroco&oauth_signature=%2Fz6onlcuJdWYhXgEt5ZawMEOfHo%3D']"""


    def parse(self, response):
        dat = json.loads(response.body)
        name = str(dat.get('name', '').encode('utf8'))
        desc  = str(dat.get('description', '').encode('utf8'))
        location = str(dat.get('location', '').encode('utf8'))
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
        try:
            sk_ = md5(sk+name.encode('utf8'))
        except:
            sk_ = md5(sk+name.decode('utf8'))
        data_meta = response.meta.get('data',{})
        twitter = Twitter()
        twitter.update({"sk":normalize(sk_),"screen_name":normalize(sk), "name":normalize(name),"description":normalize(desc),"location":normalize(location),"tweets":normalize(tweets),"following":normalize(following),"followers":normalize(followers),"likes":normalize(likes),"image":normalize(image),"lists":normalize(listed_count),"timezone":normalize(timezone),"language":normalize(lang),"is_verified":normalize(verified),"twitter_url":normalize(response.meta.get('data','').get('twitter_url','')), 'email_id':normalize(data_meta.get('email_id',''))})
        yield twitter
        self.got_page(sk,1)


