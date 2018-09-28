import os
import hashlib
import leveldb
from time import time

from scrapy import conf
from scrapy.http import Headers
from scrapy.utils.misc import load_object
from scrapy.utils.project import data_path
from scrapy.responsetypes import responsetypes
from scrapy.utils.httpobj import urlparse_cached
from scrapy.utils.http import headers_dict_to_raw, headers_raw_to_dict

from utils import make_dir

class LevelDBCacheStorage(object):

    def __init__(self, settings=conf.settings):
        self.expiration_secs = settings.getint('HTTPCACHE_EXPIRATION_SECS')
        self._dbs = {}

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def retrieve_response(self, spider, request):
        """Return response if present in cache, or None otherwise."""
        metadata = self._read_meta(spider, request)
        if metadata is None:
            return # not cached

        db = self._get_request_path(spider, request)
        data = db.Get(hashlib.md5(request.url).hexdigest())
        data = eval(data)
        body = data['response_body']
        rawheaders = data['response_headers']
        url = metadata.get('response_url') or metadata['url']
        status = metadata['status']
        headers = Headers(headers_raw_to_dict(rawheaders))
        respcls = responsetypes.from_args(headers=headers, url=url)
        response = respcls(url=url, headers=headers, status=status, body=body)
        return response

    def store_response(self, spider, request, response):
        """Store the given response in the cache."""
        db = self._get_request_path(spider, request)

        metadata = {
            'url': request.url,
            'method': request.method,
            'status': response.status,
            'response_url': response.url,
            'timestamp': time(),
        }

        data = {}
        data['meta'] = metadata
        data['response_headers'] = headers_dict_to_raw(response.headers)
        data['response_body'] = response.body
        data['request_headers'] = headers_dict_to_raw(request.headers)
        data['request_body'] = request.body

        db.Put(hashlib.md5(request.url).hexdigest(), repr(data))


    def _get_request_path(self, spider, request):
        key = hashlib.md5(request.url).hexdigest()
        path = os.path.join(conf.settings.get('HTTPCACHE_DIR'), spider.name)

        make_dir(path)          # Create cache directory if not exists

        db = self._dbs.get(path)
        if not db:
            db = leveldb.LevelDB(path)
            self._dbs[path] = db

        return db

    def _read_meta(self, spider, request):
        db = self._get_request_path(spider, request)
        try:
            data = db.Get(hashlib.md5(request.url).hexdigest())
            data = eval(data)
        except KeyError:
            return

        mtime = data['meta']['timestamp']

        if 0 < self.expiration_secs < time() - mtime:
            return # expired

        return data['meta']
