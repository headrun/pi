# -*- coding: utf-8 -*-
import scrapy
from scrapy.conf import settings


class ExampleSpider(scrapy.Spider):
    name = "example"
    start_urls = ['https://example.com/']

    def parse(self, response):
	import pdb;pdb.set_trace()
	for i in range(10):
		yield Request('https://example.com/', callback=self.parse, dont_filter=True)
