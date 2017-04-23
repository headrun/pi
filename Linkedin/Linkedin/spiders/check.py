import scrapy
from scrapy.selector import Selector
from scrapy.http import FormRequest, Request

class wWatsmyipaddr(scrapy.Spider):
        name ='whatsmyipaddr_browse'
        start_urls =['https://whatismyipaddress.com/']

        def parse(self,response):
                sel = Selector(response)
                #ip = sel.xpath('//div[@id="main_content"]/div/div/a/text()').extract()[0]
		ip = ''.join(sel.xpath('//a[contains(@href,"whatismyipaddress.com/ip")]/text()').extract())
                print ip

