from scrapy.http import  Request,FormRequest
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
import json
import re
from ast import *
import MySQLdb
from generic_functions import *

con = MySQLdb.connect(host='localhost', user= 'root',passwd='root',db="AGENTS1",charset="utf8",use_unicode=True)
cur = con.cursor()

class Justdial1(BaseSpider):
    name = 'justdail_agent_newterminal1'
    handle_httpstatus_list = [401, 404, 302, 303, 403, 500, 100]


    def get_cookies(self, headers):
        res_headers = json.dumps(str(headers))
        res_headers = json.loads(res_headers)
        my_dict = literal_eval(res_headers)
        cookies = {}
        for i in my_dict.get('Set-Cookie', []):
            key_ = i
            data = i.split(';')[0]
            if data:
                try : key, val = data.split('=', 1)
                except : continue
                cookies.update({key.strip():val.strip()})
	return cookies

    def start_requests(self):
	select_qry = 'select url,meta_data,sk from urlqueue_dev.justdail_crawl where crawl_status=0 limit 50'
	cur.execute(select_qry)
	data = cur.fetchall()
	for i in data :
	    start_urls = i[0]
	    meta_data = json.loads(i[1])
	    ref_url = meta_data['reference_url']
            city = meta_data['city']
	    distance = meta_data['distance']
	    program_sk = i[2]
	    yield Request(start_urls,self.parse,meta=({'ref_url':ref_url,'city':city,'distance':distance,'program_sk':program_sk}))

    def parse(self, response):
        sel = Selector(response)
	url = response.url
        main_url = response.meta['ref_url']
        city = response.meta['city']
	sk = md5(normalize(url)+normalize(main_url))
	program_sk = response.meta.get('program_sk','')
	distance = response.meta.get('distance','')
        ref_url_city = response.url.split('/')[3]
        name = ''.join(sel.xpath('//div[@class="tleorlp"]/h1/span[@class="item"]/span/text()').extract())
	place = ''.join(response.xpath('//span[@class="lng_add"]//text()').extract()[0]).replace('\t','').replace('\n','')
        rat_value = ''.join(sel.xpath('//span[@class="rating"]/span[@class="total-rate"]/span/text()').extract())
        rat_votes=''.join(sel.xpath('//span[@class="rtngsval"]/span[@class="votes"]//text()').extract()).strip(' ')
        address = ''.join(sel.xpath('//span[@class="comp-text"]/span[@id="fulladdress"]/span/span//text()').extract())
        services = '<>'.join(sel.xpath('//ul[@class="alstdul"]/li/span[@class="sritxt"]/span/text()').extract())
        payment_mode = '<>'.join(sel.xpath('//ul[@class="alstdul"]/li/span[@class="lng_mdpay"]/text()').extract())
        images = '<>'.join(sel.xpath('//div[@id="gal_img"]/ul[@class="catyimgul"]/li/a[@class="e_prop "]/@data-original').extract())
        photo = ''.join(sel.xpath('//div[@class="col-sm-12 padding0 col-xs-12"]/div[@class="detail-banner"]/img/@data-src').extract())
        category = normalize("<>".join(sel.xpath('//span[@class="comp-text also-list showmore "]//a//text()').extract()))
        tel = "<>".join(sel.xpath('//div//ul[@id="comp-contact"]//div[@class="telCntct cmawht"]/a[@class="tel"]/text()').extract()).strip('<>')
	days = sel.xpath('//div[@class="mreinfwpr"]//ul[@class="alstdul dn"]/li/span[@class="mreinflispn1 lng_commn"]/text()').extract()
	timings = sel.xpath('//div[@class="mreinfwpr"]//ul[@class="alstdul dn"]/li/span[contains(@class, "mreinflispn2")]//text()').extract()
        open_hours = '<>'.join(map(lambda a,b: normalize(a)+':-'+normalize(b), days,timings))
	website_link = ''.join(sel.xpath('//span[@class="mreinfp comp-text"]/a/@href').extract())
        year = ''
        year = "".join(sel.xpath('//p[text()="Year Established"]/parent::div/ul/li/text()').extract())
        buisness_info = normalize("".join(sel.xpath('//div[@class="col-sm-12 businfo seoshow "]//text()').extract()))
	book_appointment = '<>'.join(response.xpath('//section[@id="alldtlbtn"]/a//text()').extract()).replace('\n','').replace('\t','')
	number_of_ratings=''.join(response.xpath('//ul[@class="tabsCustom"]/li[contains(text(),"All Ratings")]/text()').extract()).replace('All Ratings','').replace('\n','').replace('\t','').replace('(','').replace(')','')
        patt_match = re.findall('\d{4}',year)
        if patt_match : year = "".join(year)
	aux_info=''
	meta_query = 'insert into justdail_meta(sk, name, city, ref_url_city, photos, image, address ,medicalspecialty, payment_mode, rating_val, rating_count, telephone, time, year, available_services, buisness_info, aux_info,reference_url, main_url, place, website_link, book_appointment, distance,number_of_ratings,program_sk,created_at, modified_at) values ( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),now()) on duplicate key update modified_at = now(),place=%s,website_link=%s,book_appointment=%s,distance=%s,time=%s,image=%s,number_of_ratings=%s,program_sk=%s'
	vals = (normalize(sk),normalize(name),normalize(city),str(ref_url_city),normalize(photo),normalize(images),normalize(address),normalize(category),normalize(payment_mode),str(rat_value),str(rat_votes),str(tel),str(open_hours),str(year),normalize(services),normalize(buisness_info),aux_info,normalize(response.url),normalize(main_url),normalize(place),normalize(website_link),normalize(book_appointment),normalize(distance),normalize(number_of_ratings),normalize(program_sk),normalize(place),normalize(website_link),normalize(book_appointment),normalize(distance),normalize(open_hours),normalize(images),normalize(number_of_ratings),normalize(program_sk))
        cur.execute(meta_query,vals)
        con.commit()
        up_qry = 'update urlqueue_dev.justdail_crawl set crawl_status=9 where crawl_status=0 and url="%s"' %str(response.url)
        cur.execute(up_qry)
        con.commit()
        review_nodes = response.xpath('//div[@class="col-sm-12 allratingM"]/div[@class="allratR"]')
        for node in review_nodes:
            rev_name = ''.join(node.xpath('./span[@class="fr"]/span[@class="rName lng_commn"]//text()').extract())
            rev_rat = ''.join(node.xpath('./span[@class="fr"]/span[@class="star_m"]/@aria-label').extract()).replace('Rated','').strip()
            rev_on = ''.join(node.xpath('./span[@class="dtyr ratx pull-right"]/text()').extract())
            rev_text = ''.join(node.xpath('.//div/p[@class="thr lng_commn"]/text()').extract())
            rev_query = 'insert into Reviews(sk, program_sk, reviewed_by, reviewed_on, review,rating_value,created_at, modified_at) values ( %s,%s, %s, %s, %s, %s, now(), now()) on duplicate key update modified_at = now(),rating_value=%s'
            rev_sk = md5(rev_name+sk+rev_on+rev_text+normalize(sk))
            vals1 = (rev_sk,sk,rev_name,rev_on,rev_text,rev_rat,rev_rat)
            cur.execute(rev_query,vals1)
        cookies = self.get_cookies(response.headers)
        headers = {
	'accept-encoding': 'gzip, deflate, br',
    	'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    	'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
    	'accept': '*/*',
    	'referer': response.url,
    	'authority': 'www.justdial.com',
    	'x-requested-with': 'XMLHttpRequest',
        }
        cid = ''.join(set(sel.xpath('//input[@name="docid"][@id="mpdocid"]/@value').extract()))
        main_page = "https://www.justdial.com/functions/reviews_initial.php?ct=%s&cid=%s&tab=&city=Chennai&abgraph=0&pg_no=1" % (city,cid)
        yield Request(main_page, callback=self.parse_login, headers=headers, method="GET", cookies=cookies, \
				meta={"main_url" :response.url, "headers":headers,"city":city,"rat_votes":str(rat_votes),"sk":sk})

    def parse_login(self, response):
	data = json.loads(response.body)
	js_revis = data.get('jsreviewdocids', '')
	headers = response.meta.get('headers', '')
        city = response.meta.get('city','')
	rat_votes = response.meta.get('rat_votes','')
	sk = response.meta.get('sk','')
	cookies = self.get_cookies(response.headers)
	if js_revis:
		second_page = 'https://www.justdial.com/functions/ratingsbypage.php?city=%s&cases=allreviews&jsonArr=[]&pgno=2&total=%s&cid=%s&cn=&type=&seo_url=0' % (city,rat_votes,js_revis)
		yield Request(second_page, callback=self.parse_next, headers=headers, method="GET", cookies=cookies, meta={"headers":headers,'sk':sk})

		
    def parse_next(self, response):
	sel = Selector(response)
	headers = response.meta.get('headers', '') 
	sk = response.meta['sk']
	review_nodes = response.xpath('//div[@class="col-sm-12 allratingM"]/div[@class="allratR"]')
	for node in review_nodes:
	    rev_rat =[]
	    re_ra=','.join(node.xpath('./span[@class="fr"]//span[contains(@class,"ms")]/@class').extract()).replace('10','1.0').replace('5','0.5').replace('ms','')
	    xa = re_ra.split(',') 
	    for ra in xa:
		rev_rat.append(float(ra))
	    rev_rat1 = sum(rev_rat)
	    rev_name = ''.join(node.xpath('./span[@class="fr"]/span[@class="rName"]/text()').extract())
	    rev_date = ''.join(node.xpath('./span[@itemprop="datePublished"]//text()').extract())
	    rev_text = ''.join(node.xpath('.//div[@itemprop="reviewBody"]/p/text()').extract())
	    rev_sk = md5(normalize(rev_name)+normalize(rev_date)+normalize(rev_text)+normalize(sk))
	    rev_query = 'insert into Reviews(sk, program_sk, reviewed_by, reviewed_on, review,rating_value,created_at, modified_at) values ( %s,%s, %s, %s, %s, %s, now(), now()) on duplicate key update modified_at = now(),rating_value=%s'
	    vals = (rev_sk,sk,rev_name,rev_date,rev_text,rev_rat1,rev_rat1)
	    cur.execute(rev_query,vals)
	    con.commit()
        cookies = self.get_cookies(response.headers)
	next_check = sel.xpath('//a[@href="#rvw"][contains(text(), "Next")]/@onclick').extract()
	current_val = int(''.join(re.findall('pgno=(\d+)', response.url)))+1
	if next_check:
		new_url = re.sub('pgno=\d+&', "%s%s%s" % ('pgno=', str(int(''.join(re.findall('pgno=(\d+)', response.url)))+1), '&'), response.url )
		yield Request(new_url, callback=self.parse_next, headers=headers, method="GET", cookies=cookies, meta={"headers" : headers,"sk":sk})

