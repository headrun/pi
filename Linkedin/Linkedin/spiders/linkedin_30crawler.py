import sys
import json
import MySQLdb
import urllib
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
import scrapy

class Linkedin30crawl(scrapy.Spider):
	name = 'linkedin_30_crawl'
	
	def __init__(self, *args, **kwargs):
		super(Linkedin30crawl, self).__init__(*args, **kwargs)
		self.login = kwargs.get('login', 'ramanujan')
		self.con = MySQLdb.connect(db   = 'FACEBOOK', \
		host = 'localhost', charset="utf8", use_unicode=True, \
		user = 'root', passwd = 'root')
		self.cur = self.con.cursor()
		get_query_param = "select sk, url, meta_data from linkedin_crawl30 where crawl_status=0 limit 100"
		self.cur.execute(get_query_param)
		self.profiles_list = [i for i in self.cur.fetchall()]

	def start_requests(self):
		for i in self.profiles_list:
			url = i[1]
			url = urllib.quote(url)
			query = "update linkedin_crawl30 set crawl_status=1 where sk ='%s'"%(i[0])
			request = Request(url, self.parse, meta={'sk':i[0], 'meta_data':i[2]})
			requests.extend(request)
		return requests

	def parse(self, response):
		sk = response.meta['sk']
		valid = 'False'
		if response.status== 200 and not 'your request could not be completed' in response.body.lower():
			valid = 'True'
		
		
		
		
		
		





