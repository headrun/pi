from juicer.utils import *
from juicer.items import *
import scrapy
import hashlib
import csv
import datetime
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest
import datetime
city = 'chennai'


class MagicBrowse(JuicerSpider):
    name = "magic_data_browse"
    start_urls = ['https://www.magicbricks.com/property-for-rent/residential-real-estate?bedroom=2&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Service-Apartment&cityName=%s'%city]

    def __init__(self, *args, **kwargs):
        super(MagicBrowse, self).__init__(*args, **kwargs)
	self.domain_url = 'https://www.magicbricks.com/property-for-rent/residential-real-estate?bedroom=2&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Service-Apartment&cityName=%s'%city

    def parse(self, response):
        sel = Selector(response)
        pages = []
        total_count = "".join(sel.xpath('//div[@class="SRmTab"]//span[@itemprop="name"]//text()').extract()).strip('(').strip(')')
        page_count = int(total_count)/30+1
        links = sel.xpath("//h3//a//@href").extract()
        for link in links : 
            sk = link.split('=')[-1]
	    self.get_page('magic_data_terminal', link, sk)
        for page in range(1,page_count) :
            nav_url = self.domain_url+'&page=%s'%str(page)
            if nav_url : yield Request(nav_url,self.parse_next)

    def parse_next(self,response):
        sel = Selector(response)
        links = sel.xpath("//h3//a//@href").extract()
        for link in links :
            sk = link.split('=')[-1]
            self.get_page('magic_data_terminal', link, sk)
	


