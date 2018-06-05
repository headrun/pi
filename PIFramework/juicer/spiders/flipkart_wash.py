from juicer.utils import *
from juicer.items import *
from selenium import webdriver
import MySQLdb
import time
import scrapy
import json

class FlipkartBestsellersbrowse(JuicerSpider):
    name = "flipkart_washingmachine_browse"
    start_urls = ['https://www.flipkart.com/washing-machines/pr?sid=j9e,abm,8qx&otracker=categorytree&page=1']
    handle_httpstatus_list = [404, 302, 303, 403, 500, 999, 503]

    def __init__(self, *args, **kwargs):
        super(FlipkartBestsellersbrowse, self).__init__(*args, **kwargs)
        self.URL = "https://www.flipkart.com"

    def parse(self, response):
        sel = Selector(response)
        links = sel.xpath('//div[@class="_1UoZlX"]//a//@href').extract()
        for i in links :
            product_link = 'https://www.flipkart.com' + str(i)
            print product_link
            sk = product_link.split('&')[0].split('pid=')[-1]
            if product_link : self.get_page('flipkart_bestsellers_terminal', product_link, sk)

        for i in range(2,40) :
            link = "https://www.flipkart.com/washing-machines/pr?sid=j9e,abm,8qx&otracker=categorytree&page=%s"%str(i)
            yield Request(link,callback=self.parse_next,dont_filter=True)

    def parse_next(self,response):
        sel = Selector(response)
        links = sel.xpath('//div[@class="_1UoZlX"]//a//@href').extract()
        for i in links :
            product_link = 'https://www.flipkart.com' + str(i)
            print product_link
            sk = product_link.split('&')[0].split('pid=')[-1]
            if product_link : self.get_page('flipkart_bestsellers_terminal', product_link, sk)
        
  








