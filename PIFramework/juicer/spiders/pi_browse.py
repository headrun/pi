from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spider import BaseSpider

class PinBrowse(BaseSpider):
    name ='pin_browse'
    allowed_domains = ['pinterest.com']
    start_urls = ['http://pinterest.com/search/people/?q=Ieva+Mazeikaite']

    def parse(self,response):
        sel=Selector(response)
        import pdb;pdb.set_trace()
        urls = response.xpath('//div[@class="pin user"]//a/@href').extract()
        for url in urls:
                import pdb;pdb.set_trace()

