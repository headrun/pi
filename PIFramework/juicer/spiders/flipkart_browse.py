from juicer.utils import *
from juicer.items import *
from selenium import webdriver
import MySQLdb
import time
import scrapy
import json

class FlipkartBestsellersbrowse(JuicerSpider):
    name = "flipkart_bestsellers_browse"
    start_urls = ['https://www.flipkart.com/search?q=bestsellers&otracker=start&as-show=off&as=off']
    handle_httpstatus_list = [404, 302, 303, 403, 500, 999, 503]

    def __init__(self, *args, **kwargs):
        super(FlipkartBestsellersbrowse, self).__init__(*args, **kwargs)
        self.URL = "https://www.flipkart.com/"
        self.driver = webdriver.PhantomJS("/root/pi_crawling/test/phantomjs-2.1.1-linux-x86_64/bin/phantomjs")

    def parse(self, response):
        sel = Selector(response)
        url = 'https://www.flipkart.com/api/1/product/smart-browse/facets?store=search.flipkart.com&filters=facet-show=all&q=bestsellers'
        yield Request(url, self.parse_next)

    def parse_next(self,response):
        sel = Selector(response)
        body = json.loads(response.body)
        data = body['RESPONSE']['storeMetaInfoList']
        for uri in data :
            url = "https://www.flipkart.com"+uri[u'uri'] 
            url = str(url)
            title = uri[u'title']
            headers = {'Referer':'https://www.flipkart.com/cameras-accessories/pr?sid=jek&q=bestsellers&otracker=categorytree'}
            payload = {'count' :60,'disableProductData':'true','q':'bestsellers','start':0,'store':'jek'}
            link = 'https://www.flipkart.com/api/1/product/smart-browse'
            yield Request(url, self.parse_meta_links, method="POST", body=json.dumps(payload),headers=headers)

    def parse_meta_links(self,response):
        sel = Selector(response)
        import pdb;pdb.set_trace()


