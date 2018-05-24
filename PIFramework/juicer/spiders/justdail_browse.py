import json
import MySQLdb
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from scrapy.http import Request, FormRequest
import md5
import json


class Justdialbrowse(BaseSpider):
                name        = 'justdail_agent1'
		start_urls = ['https://www.justdial.com/Gurgaon/Builders-in-Gurgaon/nct-10059255']
		handle_httpstatus_list = [401, 404, 302, 303, 403, 500, 100]
		
		def __init__(self, *args, **kwargs):
			super(Justdialbrowse, self).__init__(*args, **kwargs)
			self.con = MySQLdb.connect(host='localhost', user= 'root',passwd='root',db="urlqueue_dev",charset="utf8",use_unicode=True)
			self.cur = self.con.cursor()
		
                def parse(self,response):
                	sel  = Selector(response)
			listing_urls = sel.xpath('//div[@class="filter-common-wrap category-wrap"]//ul/li/a[@class="lng_commn"]/@href').extract()
			for listing_url in listing_urls:
				url = ''.join(listing_url)
				if url:
					yield Request(url, callback = self.parse_listing)
		def parse_listing(self, response):
			sel  = Selector(response)
			nodes = sel.xpath('//div//ul//li/section[@class=" jgbg"]')
			nodes1 = sel.xpath('//div//ul//li/section[@class=" jbbg"]')
			nodes.extend(nodes1)
                        for node in nodes:
				link = ''.join(node.xpath('.//div[@class="col-md-12 col-xs-12  colsp"]//span[@class="jcn"]//a//@href').extract()) 
				exp = ''.join(node.xpath('.//span[@class="rsrtopn"]/a[@title="Years of Experience"]//span[@class="distnctxt lng_commn"]/text()').extract())
				fee = ''.join(node.xpath('.//span[@class="rsrtopn"]/a[@title="Consultation Fee"]//span[@class="distnctxt lng_commn"]/text()').extract())
				yield Request(link, callback = self.parse_agent, meta = {'city' : response.url.split('/')[3],'url':response.url,'fee':fee,'exp':exp})
			for i in range(1,20) :
				req_link = response.url+'/page-%s'%i
				yield Request(req_link, callback = self.nav_parse, meta = {'city' : req_link.split('/')[3],'url':req_link})

                def parse_agent(self, response):
                        sel = Selector(response)
                        sk = md5.md5(response.url.split('/')[4]+response.meta['city']).hexdigest()
                        meta_data = ({'city': response.meta['city'],'reference_url':response.meta['url'],'fee':response.meta['fee'],'exp':response.meta['exp']})
                        query = 'insert into justdail_crawl(sk, url, crawl_type, content_type,related_type,crawl_status,meta_data,created_at, modified_at) values ( %s, %s, %s, %s, %s, %s, %s, now(), now()) on duplicate key update modified_at = now()'
                        values = (sk, response.url,'','','',0,json.dumps(meta_data))
                        self.cur.execute(query, values)
                        self.con.commit()
		
                def nav_parse(self,response):
                        sel  = Selector(response)
			nodes = sel.xpath('//div//ul//li/section[@class=" jgbg"]')
			nodes1 = sel.xpath('//div//ul//li/section[@class=" jbbg"]')
			nodes.extend(nodes1)
                        for node in nodes:
                                link = ''.join(node.xpath('.//div[@class="col-md-12 col-xs-12  colsp"]//span[@class="jcn"]//a//@href').extract())
                                exp = ''.join(node.xpath('.//span[@class="rsrtopn"]/a[@title="Years of Experience"]//span[@class="distnctxt lng_commn"]/text()').extract())
                                fee = ''.join(node.xpath('.//span[@class="rsrtopn"]/a[@title="Consultation Fee"]//span[@class="distnctxt lng_commn"]/text()').extract())
                                yield Request(link, callback = self.parse_agent, meta = {'city' : response.url.split('/')[3],'url':response.url,'fee':fee,'exp':exp})

			
