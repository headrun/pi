from tripadvisor_input import Company_names
import re
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request
import csv
class TripadvisorBrowse(BaseSpider):

    name = 'tripadvisor_browse' 
    start_urls = []

    def __init__(self, *args, **kwargs):
        self.domain = 'https://www.tripadvisor.in'
	self.excel_file_name = 'Tripadvisor_pages_list.csv'
	self.oupf = open(self.excel_file_name, 'ab+')
        self.todays_excel_file  = csv.writer(self.oupf)
	self.header = ['Keyword', 'Url']
	self.todays_excel_file.writerow(self.header)

    def start_requests(self):
	for company in Company_names:
        	url = 'https://www.tripadvisor.in/Search?q='+str(company)
		yield Request(url, self.parse, meta={'keyword':company})

    def parse(self, response):
        sel = Selector(response)
	links = response.xpath('//div[contains(@class, "result ")]/div[@class="result_wrap "]/@onclick').extract()
	keyword = response.meta['keyword']
        for link in links:
	    link = self.domain + ''.join(re.findall('(/.*.html)', link)).replace('?t=1','')
	    self.todays_excel_file.writerow([keyword, link])
	offset = "".join(sel.xpath('//a[@class="ui_button nav next primary "]//@data-offset').extract())
        if  offset :
            nav_link =  response.url.split('&')[0] + '&o=' + str(offset)         
            yield Request(nav_link, callback=self.parse, meta={'keyword':keyword}, dont_filter=True)
        



