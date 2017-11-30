import json
import MySQLdb
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from scrapy.http import Request, FormRequest 
import md5
import re
from generic_functions import *
import ast 

con = MySQLdb.connect(host='localhost', user= 'root',passwd='root',db="AGENTS",charset="utf8",use_unicode=True)
cur = con.cursor()

class JUSTDIALTerminal(BaseSpider):
		name = 'justdail_agent_terminal'

                def start_requests(self):
                    select_qry = 'select url,meta_data from urlqueue_dev.justdail_crawl where crawl_status=0 limit 1'
                    cur.execute(select_qry)
                    data = cur.fetchall()
                    for i in data :
                        start_urls = i[0]
                        meta_data = json.loads(i[1])
                        ref_url = meta_data['reference_url']
                        city = meta_data['city']
                        yield Request(start_urls,self.parse,meta=({'ref_url':ref_url,'city':city}))

                
			
		def parse(self,response):
                        sel = Selector(response)
                        main_url = response.meta['ref_url']
                        city = response.meta['city']
			full_data = ''
                        try : full_data = sel.xpath('//script[@type="application/ld+json"]//text()').extract()[1]
                        except : print "no data"
			#data = json.loads(full_data)i
			if full_data:
                        	data = ast.literal_eval(full_data.replace('\r', '').replace('\n','').replace('\t', ''))
                        	sk = response.url.split('/')[4]
				name = data.get('name','')
				photos = "<>".join(data.get('photos',{}).get('url','')).strip('<>')
                        	ref_url_city = response.url.split('/')[3]
				image = data.get('image','')
				address = data.get('address','')
                        	full_address = ",".join(address.values()).replace('PostalAddress,','')
				category = "<>".join(data.get('medicalSpecialty','')).strip('<>')
				payment_mode = "<>".join(data.get('paymentAccepted','')).strip('<>')
				rating = data.get('aggregateRating',{})
                        	rating_val = rating.get('ratingValue','')
                        	rat_count = rating.get('ratingCount','')
				rev = data.get('review','')
                        	services = "<>".join(data.get('availableService','')).strip('<>') 
                        	year = ''
                        	counter = 1
                        	for rev_ in rev :
                            	    review = rev_['reviewBody']
                            	    author_name = rev_['author']['name']
                            	    pub_date = rev_['datePublished']
                            	    rev_query = 'insert into Reviews(sk, program_sk, reviewed_by, reviewed_on, review,created_at, modified_at) values ( %s, %s, %s, %s, %s, now(), now()) on duplicate key update modified_at = now()'
                            	    rev_sk = md5(str(counter)+review+sk)
                            	    vals = (rev_sk,sk,author_name,pub_date,review)
                            	    cur.execute(rev_query,vals)
                            	    counter = counter+1
                        	if not category : category = normalize("<>".join(sel.xpath('//span[@class="comp-text also-list showmore "]//a//text()').extract()))
				tel = "<>".join(sel.xpath('//div//ul[@id="comp-contact"]//div[@class="telCntct cmawht"]/a[@class="tel"]/text()').extract()).strip('<>')
                        	time = "".join(sel.xpath('//div[@id="mhd"]//ul[@id="hroprt"]//span[1]//text()').extract()).replace('\r\n\t','').replace('\t','')
                        	year = "".join(sel.xpath('//p[text()="Year Established"]/parent::div/ul/li/text()').extract())
                        	buisness_info = normalize("".join(sel.xpath('//div[@class="col-sm-12 businfo seoshow "]//text()').extract()))
                        
                        	patt_match = re.findall('\d{4}',year)
                        	if patt_match : year = "".join(year)
				meta_query = 'insert into justdail_meta(sk, name,city,ref_url_city,photos, image, address ,medicalspecialty, payment_mode,rating_val,rating_count,telephone,time, year, available_services, buisness_info, reference_url, main_url, created_at, modified_at) values ( %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s ,%s ,%s, %s, %s, %s, %s,now(), now()) on duplicate key update modified_at = now()'
                        	vals = (normalize(sk),normalize(name),normalize(city),str(ref_url_city),normalize(photos),normalize(image),normalize(full_address),normalize(category),normalize(payment_mode),str(rating_val),str(rat_count),str(tel),str(time),year,normalize(services),normalize(buisness_info),normalize(response.url),normalize(main_url))
                        	cur.execute(meta_query,vals)
                        	con.commit()
                        	up_qry = 'update urlqueue_dev.justdail_crawl set crawl_status=9 where crawl_status=0 and url="%s"' %str(response.url)
                        	cur.execute(up_qry)
                        	con.commit()


