from tornado.auth import _oauth10a_signature
from urllib import urlencode
import binascii
import uuid
import time

from juicer.utils import *

API_URL = 'https://api.twitter.com/1.1/users/show.json'
access_token = dict(key='16950741-8LHKI317UCMiNvEW2iLc564CKl15AnRNnAuHYroco', secret='U6CjXnoii013YMkOQRZfpLwZ12IkZdQCkTHV2lK0JgqXx')
consumer_token = dict(key='Ub2YlYi5i9VLiU6qVGcw', secret='qjx2esDiY70OxAVqVrA80AK9QLYXU2gYSmmcEPKJSg')


class TwitterBrowse(JuicerSpider):
    name = 'twitter_browse'
    start_urls = ['https://twitter.com/robots.txt']


    def _oauth_request_parameters(self, url, consumer_token, access_token, parameters={}, method="GET"):
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

    def parse(self, response):
        with open('twitter1.txt', 'r') as f:
            rows = f.readlines()
            for row in rows:
                screen_url = row.strip()
                if not screen_url: continue
                screen_name = screen_url.split('/')[-1].strip()
                arguments = {}
                arguments['screen_name'] = screen_name
                TW_URL = 'https://api.twitter.com/1.1/users/show.json'
                extra_arguments = self._oauth_request_parameters(TW_URL, consumer_token, access_token, arguments)
                arguments.update(extra_arguments)
                arguments = urlencode(arguments)
                url = '%s?%s' %(TW_URL, arguments)
                meta_aux = {"twitter_url":screen_url}
                self.get_page('twitter_profiles_terminal', url, screen_name, meta_aux)

