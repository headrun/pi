import json
import scrapy
import MySQLdb
from scrapy.spiders import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

class McmasterCategorybrowse(BaseSpider):
    name = 'mcmaster_category_browse'
    start_urls = ['https://www.mcmaster.com/mv1540501225/Webparts/Content/RetrieveCatalogPageList.aspx']

    def __init__(self, *args, **kwargs):
        super(McmasterCategorybrowse, self).__init__(*args, **kwargs)
        self.conn = MySQLdb.connect(db='MCMASTER',user='root',passwd='root', host='localhost', use_unicode=True)
        self.cur = self.conn.cursor()
        self.query = 'select sk,main_link from mcmaster where category=""'
	self.update_query = 'update mcmaster set category=%s where sk=%s'
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        self.cur.close()
        self.conn.close()

    def parse(self, response):
        json_data = json.loads(response.body)
	self.cur.execute(self.query)
	rows = self.cur.fetchall()
	for row in rows:
	    sk, main_link = row
	    id_ = main_link.split('=')[-1]
	    category = json_data[id_]
	    try:
	    	self.cur.execute(self.update_query, (category, sk))
	    except:
		self.cur.execute(self.update_query, (category.encode('utf8'), sk))


