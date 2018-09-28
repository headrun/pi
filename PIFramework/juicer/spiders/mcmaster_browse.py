import json
import md5
import scrapy
import MySQLdb
import csv
from mcmaster_config import *
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
import time
from juicer.utils import *
from juicer.items import *

class Mcmasterbrowse(JuicerSpider):
    name = 'mcmaster_browse'
    start_urls = [start_url]

    def __init__(self, *args, **kwargs):
        super(Mcmasterbrowse, self).__init__(*args, **kwargs)
        self.conn = MySQLdb.connect(db='urlqueue_dev',user='root',passwd='', host='localhost', use_unicode=True)
        self.cur = self.conn.cursor()
        #self.insert_query = "INSERT INTO mcmaster_crawl(sk, url, crawl_status, meta_data, created_at, modified_at) values(%s, %s, %s, %s, now(), now()) on duplicate key update modified_at = now()"
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        self.cur.close()
        self.conn.close()

    def parse(self, response):
        json_data = json.loads(response.body)
        counter = 0
        data = json_data.items()
        for data_ in data :
        	id_ , category = data_
                counter=counter+1
                print counter,category
                if id_ : 
 		        cate_link = cat_link % (mvcode,str(id_))
                        if cate_link : yield Request(cate_link,self.parse_next,meta={'category':category})

    def parse_next(self, response) :
        sel = Selector(response)
        nodes = sel.xpath('//table[@class="ItmTbl"]')
        main_cat = response.meta.get('category','')
        meta_data = {}
        for node in nodes :
                headers = node.xpath('.//td[contains(@class,"Price")]//span//text()').extract()
        	product_link  = node.xpath('.//td[contains(@class,"ItmTblCellPartNbr")]')
                for inner_node in product_link :
		    product_id = "".join(inner_node.xpath(".//text()").extract())
                    id_ = "".join(inner_node.xpath("./@data-mcm-prodgrps").extract())
                    price = inner_node.xpath('./following-sibling::td[contains(@class,"ItmTblCellPrce") and contains(@data-mcm-prodgrps, "%s")]/text()'%id_).extract()
                    if len(price)>1 :
		    	price1 = headers[0] + ':' + price[0]
                    	price2 = headers[1] + ':' + price[1]
                        price = price1+"<>"+price2
                    else : price = "".join(price)
                    ref_url = "https://www.mcmaster.com/#"+ product_id
                    meta_data.update({"constructed_url":response.url,'price':price,'product_id':product_id,'main_cat':main_cat,'ref_url':ref_url})
                    url = meta_link % (mvcode,product_id) 
                    self.get_page("mcmaster_data_terminal",url,sk,meta_data)
                    #values = (product_id, url, 0, json.dumps(meta_data))
                    #self.cur.execute(self.insert_query , values)
