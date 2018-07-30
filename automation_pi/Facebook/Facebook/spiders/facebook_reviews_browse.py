import requests
from fb_constants import *
from fb_browse_queries import *
import sys
sys.path.append('/root/alekhys/automation_pi/table_schemas')
from generic_functions import *
import datetime

class FacebookReviewBrowse(BaseSpider):
    name = "facebook_review_browse"
    start_urls = ['https://www.facebook.com/login']
    handle_httpstatus_list = [404, 302, 303, 403, 500]
    
    def __init__(self, *args, **kwargs):
        super(FacebookReviewBrowse, self).__init__(*args, **kwargs)
        self.login = kwargs.get('login','yagnasree@headrun.com')
	self.con = MySQLdb.connect(db='FACEBOOK', host='localhost', charset="utf8", use_unicode=True, user='root', passwd='root')
        self.cur = self.con.cursor()
	self.query = 'insert into facebook_reviews(page_name, reference_url, page_rating, reviews, reviewed_by, review_text, review_rating, reviewed_on, modified_at, created_at) values(%s, %s, %s, %s, %s, %s, %s, %s, now(), now())'
	self.ref_url = 'https://www.facebook.com/ajax/pages/review/spotlight_reviews_tab_pager/?cursor={0}&fetch_on_scroll=1&max_fetch_count=10&page_id={1}&sort_order=most_helpful&dpr=1.5&__user=100007435239714&__a=1&__dyn=5V4cjLx2ByK5A9UkKHqAyqomzFE9XG8GAdyedirWqK6EvxGdwIhEpyAueCHxC7oG5VEc8KEjyRUC48G5WAxamjDK7Hze3KFQ5o-44aUS2Sih6UXU98nVV8Gicx2q5o5aayrBy8G5p8hz8fUlg8VEgJ0gazVFE-rxjyoG3m5pVkdxCi78SaCzUfHGVUhxyho-9BmFpEZ7gy5o8k9wRyXyU-8gmyES3m6ogUK8BzXHzEy3C4ogze9AVEgVeaDU8Jai7Vm4S9xCmiaz9oCmUhDzA4Kq1ex62WFUO3C44aKcUWV8zxObwFzGyXwPw&__req=19&__be=1&__pc=PHASED%3ADEFAULT&__rev=4143522&__spin_r=4143522&__spin_b=trunk&__spin_t=1532602443'
	self.excel_file_name = 'facebook_reviews_data_%s.csv'%str(datetime.datetime.now()).replace(' ', '_')
    	self.header_params = ['page_name', 'page_url', 'page_rating', 'no_of_reviews', 'reviewd_by', 'review_text', 'star_rating', 'reviewed_on']
	oupf = open(self.excel_file_name, 'ab+')
        self.todays_excel_file  = csv.writer(oupf)
        self.todays_excel_file.writerow(self.header_params)
	self.domain = "https://mbasic.facebook.com"

    def parse(self, response):
        sel = Selector(response)
        login  = constants_dict[self.login]
        lsd = ''.join(sel.xpath('//input[@name="lsd"]/@value').extract())
        lgnrnd = ''.join(sel.xpath('//input[@name="lgnrnd"]/@value').extract())
        return [FormRequest.from_response(response, formname = 'login_form',\
                                formdata={'email': login[0],'pass':login[1],'lsd':lsd, 'lgnrnd':lgnrnd},callback=self.parse_redirect)]

    def parse_redirect(self, response):
        sel = Selector(response)
        if 'Your account has been disabled' in response.body :
            noti_xpath = 'Your account has been disabled'
            user = constants_dict[self.login][0]
            pwd = constants_dict[self.login][1]
        yield Request('https://mbasic.facebook.com/support/?notif_t=feature_limits',callback=self.parse_next)

    def parse_next(self, response):
        yield Request(self.domain, callback=self.parse_close)
        sel = Selector(response)
        noti_xpath = "".join(sel.xpath('//div//span[contains(text(),"temporarily")]//text()').extract())
        if noti_xpath :
            user = constants_dict[self.login][0]
            pwd = constants_dict[self.login][1]
	with open('input.txt', 'r') as f:
            rows = f.readlines()
	for row in rows:
            yield Request(row.replace('\n', ''), callback=self.parse_review)

    def parse_close(self, response):
        sel = Selector(response)
        self.res_afterlogin = sel

    def parse_review(self, response):
	sel = Selector(response)
	nodes = sel.xpath('//div[@class="_4-u2 mbm _4mrt _5jmm _5pat _5v3q _4-u8"]')
	page_name = ''.join(sel.xpath('//link/@title').extract()).encode('utf8')
        data_list = sel.xpath('//div[@class="mvm uiP fsm"]/text()').extract()
        rating, reviews = data_list
        rating = rating.split(' ')[0]
        reviews = reviews.split(' ')[0]
        if 'K' in reviews:
            reviews = str(float(reviews.replace('K', '')) * 1000)
        for node in nodes:
            review_on = ''.join(node.xpath('.//abbr/@title').extract()).encode('utf8')
	    review_on = datetime.datetime.strptime(review_on, '%m/%d/%Y %I:%M%p').strftime('%d/%m/%Y %H:%M:%S')
            review = ''.join(node.xpath('.//p/text()').extract()).encode('utf8')
            star_rating = ''.join(node.xpath('.//i/u/text()').extract()).encode('utf8').split(' ')[0]
            name = ''.join(node.xpath('.//span/a[@class="profileLink"]/text()').extract()[0]).encode('utf8')
	    values = (page_name, response.url, rating, reviews, name, review, star_rating, review_on)
	    self.todays_excel_file.writerow(values)
	    self.cur.execute(self.query, values)
            self.con.commit()
	next_page_cursor = ''.join(sel.xpath('//div[@id="most_helpful_pager"]/div/a/@href').extract())
	cursor = ''.join(re.findall('cursor=(.*?)&', next_page_cursor))
	page_id = ''.join(re.findall('page_id=(.*?)&', next_page_cursor))
	if cursor:
	    link = self.ref_url.format(cursor.encode('utf8'), page_id.encode('utf8'))
	    yield Request(link, self.parse_next1, meta={'page_rating':rating, 'page_reviews':reviews, 'main_link':response.url, 'page_id':page_id, 'page_name':page_name})

    def parse_next1(self, response):
	data = response.body.replace('for (;', '').replace(';);', '')
	rating = response.meta['page_rating']
	reviews = response.meta['page_reviews']
	main_link = response.meta['main_link']
	page_id = response.meta['page_id']
	page_name = response.meta['page_name']
	if data:
	    data_test = json.loads(data).get('domops', [])
	    if data_test:
		data_body = data_test[0][3]['__html']
		sel = Selector(text=data_body)
		nodes = sel.xpath('//div[@class="_4-u2 mbm _4mrt _5jmm _5pat _5v3q _4-u8"]')
		for node in nodes:
		    review_on = ''.join(node.xpath('.//abbr/@title').extract()).encode('utf8')
		    review_on = datetime.datetime.strptime(review_on, '%m/%d/%Y %I:%M%p').strftime('%d/%m/%Y %H:%M:%S')
		    review = ''.join(node.xpath('.//p/text()').extract()).encode('utf8')
		    star_rating = ''.join(node.xpath('.//i/u/text()').extract()).encode('utf8').split(' ')[0]
		    name = ''.join(node.xpath('.//span/a[@class="profileLink"]/text()').extract()[0]).encode('utf8')
		    values = (page_name, main_link, rating, reviews, name, review, star_rating, review_on)
		    self.todays_excel_file.writerow(values)
		    self.cur.execute(self.query, values)
                    self.con.commit()
	 	data_body1 = data_test[1][3]['__html']	
		sel1 = Selector(text=data_body1)
		next_page_cursor = ''.join(sel1.xpath('//div[@id="most_helpful_pager"]/div/a/@href').extract())
	        cursor = ''.join(re.findall('cursor=(.*?)&', next_page_cursor))
        	if cursor:
                	link = self.ref_url.format(cursor.encode('utf8'), page_id.encode('utf8'))
                	yield Request(link, self.parse_next1, meta={'page_rating':rating, 'page_reviews':reviews, 'main_link':main_link, 'page_id':page_id, 'page_name':page_name})

