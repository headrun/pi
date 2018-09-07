from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request
import re
import MySQLdb
import hashlib

class IndeedBrowse(BaseSpider):

    name = 'indeed_browse'
    start_urls = []
    handle_httpstatus_list = [301,302]

    def __init__(self):
	self.conn = MySQLdb.connect(db='INDEED',user='root',passwd='root', charset="utf8",host='localhost',use_unicode=True)
        self.cur = self.conn.cursor()
	self.query1 = 'insert into job_meta(sk, keyword, location, job_count, reference_url, created_at, modified_at) values(%s, %s, %s, %s, %s, now(), now()) on duplicate key update modified_at=now()'
    	self.query2 = 'insert into jobs(sk, job_sk, title, company_name, location, salary , posted_on, description, reference_url, reviews, rating, modified_at, created_at) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), now()) on duplicate key update modified_at=now()'

    def __del__(self):
        self.conn.close()
        self.cur.close()

    def start_requests(self):
	with open('indeed_input.txt', 'r') as f:
            rows = f.readlines()
        for row in rows:
            row = row.replace('\n', '')
	    link = row.split('/')[-1]
	    row = '%s&sort=date'%row
	    keyword, location = link.split('-jobs-in-')
	    link = 'https://www.indeed.co.in/jobs?q=%s&l=%s&sort=date'%(keyword.replace('-', '+'), location.replace('-', '+'))
            yield Request(link, callback=self.parse, meta={'url':row})

    def parse(self, response):
	sel = Selector(response)
	keyword = ''.join(sel.xpath('//input[@id="what"]/@value').extract())
	location = ''.join(sel.xpath('//input[@id="where"]/@value').extract())
	job_cnt = ''.join(sel.xpath('//div[@id="searchCount"]/text()').extract())
	job_cnt = job_cnt.split(' ')[-1].replace('\n', '')
	sk = hashlib.md5(keyword+location).hexdigest()
	job_links1 = sel.xpath('//h2[@class="jobtitle"]/@id').extract()
	values = (sk, keyword, location, job_cnt, response.url)
	self.cur.execute(self.query1, values)
	self.conn.commit()
	for link in job_links1:
	    job_sk = link.split('_')[-1]
	    link = 'https://www.indeed.co.in/viewjob?jk=%s'%job_sk
	    yield Request(link, self.parse_next, meta={'main_sk':sk, 'job_sk':job_sk})
    
    def parse_next(self, response):
	sel = Selector(response)
	main_sk = response.meta['main_sk']
	sk = response.meta['job_sk']
	title = ''.join(sel.xpath('//b[@class="jobtitle"]/font/text()').extract())
	c_name = ''.join(sel.xpath('//b[@class="jobtitle"]/following-sibling::span[@class="company"]/text()').extract())
	reviews = ''.join(sel.xpath('//span[@class="slNoUnderline"]/text()').extract())
	reviews = ''.join(re.findall('(\d+)', reviews))
	location = ''.join(sel.xpath('//b[@class="jobtitle"]/following-sibling::span[@class="location"]/text()').extract())
	salary = ''.join(sel.xpath('//p[contains(text(), "Salary:")]/text()').extract()).replace('Salary:', '')
	posted_on = ''.join(sel.xpath('//div[@class="result-link-bar"]/span[@class="date"]/text()').extract())
	desc = ' '.join(sel.xpath('//span[@id="job_summary"]//text()').extract())
	cmp_url = ''.join(sel.xpath('//a[@data-tn-element="reviewStars"]/@href').extract())
	if cmp_url:
	    cmp_url = 'https://www.indeed.co.in%s'%cmp_url
	    values = (sk, main_sk, title, c_name, location, salary , posted_on, desc, response.url, reviews) 
	    yield Request(cmp_url, self.parse_next1, meta={'values':values},dont_filter=True)
	else:
	    values = (sk, main_sk, title, c_name, location, salary , posted_on, desc, response.url, reviews, '')
	    self.cur.execute(self.query2, values)
            self.conn.commit()

    def parse_next1(self, response):
	sel = Selector(response)
	values = list(response.meta['values'])
	rating = ''.join(sel.xpath('//span[@class="cmp-average-rating"]/text()').extract())
	values.append(rating)
	self.cur.execute(self.query2, values)
	self.conn.commit()
