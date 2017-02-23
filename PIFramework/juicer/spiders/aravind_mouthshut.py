# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector


class MouthshutSpider(scrapy.Spider):
    name = "mouthshut"

    def __init__(self, *args, **kwargs):
        super(MouthshutSpider, self).__init__(*args, **kwargs)
        self.search = kwargs.get('search', 'Apollo Hospitals')
        self.start_urls = ['https://www.mouthshut.com/search/prodsrch.aspx?data=%s&type=&p=0' % self.search]

    def parse(self, response):
        sel = Selector(response)
        nodes = sel.xpath('//div[@class="box product"]//div[@class="reviews small"]//a[contains(text(), "Reviews")]/@href').extract()
        import pdb;pdb.set_trace()
        pagination = "..."
