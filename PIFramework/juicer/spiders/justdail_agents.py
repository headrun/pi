import json
import MySQLdb
from juicer.utils import *

#con = MySQLdb.connect(host='localhost', user= 'root', db="AGENTS",charset="utf8",use_unicode=True)
#cur = con.cursor()

links = ['http://www.justdial.com/%s/Estate-Agents']

class JUSTDIAL(JuicerSpider):
		name        = 'justdail_agent_browse'
		start_urls  =  ['https://www.justdial.com/Trichy/Ophthalmologists/nct-10343851']
                handle_httpstatus_list = [404, 302, 303, 403, 500]

			
		def parse(self,response):
                        import pdb;pdb.set_trace()

		def parse_cities(self,response):
			sel			 = HTML(response)
			city		 = response.meta['city']

			print city
			agents_nodes = sel.select('//section[@class="jbbg"]//section[@class="jrcl "]//aside[@class="compdt"]//span[@class="jcn "]//a/@href')
			if not agents_nodes:
				agents_nodes = sel.select('//section[@class="jgbg"]//section[@class="jrcl "]//aside[@class="compdt"]//span[contains(@class,"jcn")]//a/@href')

			for agent in agents_nodes:
				link = textify(agent)
				yield Request(link, callback = self.parse_agent, meta = {'city' : response.meta['city']}, priority=1)

			"""if self.crawl_type == "keepup":	
				for i in range(1,50):
					link = "%s/page-%s" %(response.meta['org_link'], i)
					yield Request(link, callback = self.parse_cities, meta = {'org_link' : response.meta['org_link'],
																			  'page' : i,
																			  'city' : response.meta['city'] },
																			   priority = 1)"""
			
		def parse_agent(self, response):
				sel = HTML(response)
				title 	=  textify(sel.select('//section[@class="jbbg jddtl"]//section[@class="jcar_wrp"]//h1//span[@title]/@title'))
				ph_nume = textify(sel.select('//section[@class="jbbg jddtl"]//a[@class="tel"]//text()'))
				sk = response.url.split("/")[4]
				print "%s <> %s <> %s <> %s" %(title, ph_nume, sk, response.meta['city'])
				query = 'insert into justdial_agents_full(sk, agency_name, city, phone_number, address, reference_url, created_at, modified_at) values ( %s, %s, %s, %s, %s, %s, now(), now()) on duplicate key update modified_at = now()'
				values = (sk, title, response.meta['city'], ph_nume, '', response.url)
				cur.execute(query, values)
