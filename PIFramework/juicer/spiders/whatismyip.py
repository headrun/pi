from juicer.utils import *
from juicer.items import *


class WhatsmyipBrowse(JuicerSpider):
    name = 'whatsmyip_browse'
    start_urls = ['http://whatismyipaddress.com/']
    count = 0
    print settings['PROXIES_LIST']


    def parse(self, response):
        sel = Selector(response)
        self.count += 1
	try:
	        print ''.join(sel.xpath('//div[@id="section_left"]//a/text()').extract()[0])
	except:
		print response.url
		import pdb;pdb.set_trace()
        '''if self.count < 10:
           yield Request(response.url, self.parse, dont_filter=True)'''
