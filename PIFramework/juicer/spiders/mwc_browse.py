from juicer.utils import *
from juicer.items import *
import scrapy
import hashlib
import csv
import datetime
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest
import datetime


class MWC(JuicerSpider):
    name = "mwc_exhibitors_browse"
    start_urls = ['https://www.mwcbarcelona.com/exhibition/2019-exhibitors/']

    def __init__(self, *args, **kwargs):
        super(MWC, self).__init__(*args, **kwargs)
	self.domain_url = 'https://www.mwcbarcelona.com/'

    def parse(self, response):
        sel = Selector(response)
        total_count = int(sel.xpath("//a[@class='page-numbers']//text()").extract()[-1])+1 
        for i in range(1,total_count) : 
        	link = 'https://www.mwcbarcelona.com/exhibition/2019-exhibitors/page/'+str(i)
        	yield Request(link,self.parse_next)

    def parse_next(self,response):
        sel = Selector(response)
        links = sel.xpath('//div[@class="listing"]//a//@href').extract()
        for link in links :
            sk = link.split('/')[-2]
            self.get_page('mwc_exhibitors_terminal', link, sk)
	


