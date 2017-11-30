import json
import MySQLdb
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from scrapy.http import Request, FormRequest 
con = MySQLdb.connect(host='localhost', user= 'root',passwd='root',db="urlqueue_dev",charset="utf8",use_unicode=True)
cur = con.cursor()
import md5


class JUSTDIAL(BaseSpider):
		name        = 'justdail_agent'
		start_urls  =  ['https://www.justdial.com/Chennai/doctors']

	        def parse(self,response):
			sel  = Selector(response)
			agents_nodes = sel.xpath('//div//ul//li//span[@class="jcn"]//a//@href').extract()
			for agent in agents_nodes:
			    link = "".join(agent)
			    yield Request(link, callback = self.parse_agent, meta = {'city' : response.url.split('/')[3],'url':response.url})
                        for i in range(1,55) : 
                            req_link = response.url+'/page-%s'%i
                            yield Request(req_link, callback = self.nav_parse, meta = {'city' : req_link.split('/')[3],'url':req_link})
				
		def parse_agent(self, response):
			sel = Selector(response)
			sk = md5.md5(response.url.split('/')[4]+response.meta['city']).hexdigest()
                        meta_data = ({'city': response.meta['city'],'reference_url':response.meta['url']})
			query = 'insert into justdail_crawl(sk, url, crawl_type, content_type,related_type,crawl_status,meta_data,created_at, modified_at) values ( %s, %s, %s, %s, %s, %s, %s, now(), now()) on duplicate key update modified_at = now()'
			values = (sk, response.url,'','','',0,json.dumps(meta_data))
			cur.execute(query, values)
			con.commit()

                def nav_parse(self,response):
                        sel  = Selector(response)
                        agents_nodes = sel.xpath('//div//ul//li//span[@class="jcn"]//a//@href').extract()
                        for agent in agents_nodes:
                            link = "".join(agent)
                            yield Request(link, callback = self.parse_agent, meta = {'city' : response.url.split('/')[3],'url':response.url})
