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
        self.con = MySQLdb.connect(db='FACEBOOK_REVIEWS', host='localhost', charset="utf8", use_unicode=True, user='root', passwd='root')
        self.cur = self.con.cursor()
        self.query = 'insert into facebook_reviews(id, page_id, page_name, reference_url, page_rating, reviews, reviewed_by, review_text, review_rating, reviewed_on, modified_at, created_at) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), now())'
        self.crawl_query = 'insert into facebook_crawl(sk, url, crawl_type, content_type, related_type, crawl_status, meta_data, created_at, modified_at) values(%s, %s, %s, %s, %s, %s, %s, now(), now())'
        #self.ref_url = 'https://www.facebook.com/ajax/pages/review/spotlight_reviews_tab_pager/?cursor={0}&fetch_on_scroll=1&max_fetch_count=10&page_id={1}&sort_order=most_helpful&dpr=1.5&__user=100007435239714&__a=1&__dyn=5V4cjLx2ByK5A9UkKHqAyqomzFE9XG8GAdyedirWqK6EvxGdwIhEpyAueCHxC7oG5VEc8KEjyRUC48G5WAxamjDK7Hze3KFQ5o-44aUS2Sih6UXU98nVV8Gicx2q5o5aayrBy8G5p8hz8fUlg8VEgJ0gazVFE-rxjyoG3m5pVkdxCi78SaCzUfHGVUhxyho-9BmFpEZ7gy5o8k9wRyXyU-8gmyES3m6ogUK8BzXHzEy3C4ogze9AVEgVeaDU8Jai7Vm4S9xCmiaz9oCmUhDzA4Kq1ex62WFUO3C44aKcUWV8zxObwFzGyXwPw&__req=19&__be=1&__pc=PHASED%3ADEFAULT&__rev=4143522&__spin_r=4143522&__spin_b=trunk&__spin_t=1532602443'
        self.ref_url = 'https://www.facebook.com/async/page_recommendation/consideration_signals_tab_pagination/?cursor={0}&page_id={1}&pager_dom_id=u_0_8&should_infinite_scroll=1&is_vertex=0&stories_container_dom_id=recommendations_tab_main_feed&sort_order=most_helpful&dpr=1.5&__user=100007435239714&__a=1&__dyn=5V4cjLx2ByK5A9UkKHqAyqomzFE9XG8GAdyedirWqK6EvxGdwIhEpyEyeCHxC7oG5VEc8W4UJu9x2axuF8iBAVXxWUPwXGt0Bx12KdwJAAhKe-2i5-uiaAz8gCxm1iyECVoyaxG4oO3-5k2eq49842E-qqfCUkUCawRxmul3opAxOdyFE-3WWKu4ooAghzRGm5At28lwxgC3mbKbzUx1qazodopx3yUymfKKey8eohx2cUCjCx3AUGvwyQF8vBojUC6pp8GcByprx6uegiVE4W10GucwVx12HzeeKi8UsyUaoWEKUcUa8&__req=k&__be=1&__pc=PHASED%3ADEFAULT&__rev=4187527&__spin_r=4187527&__spin_b=trunk&__spin_t=1533753183'

	#self.excel_file_name = 'facebook_reviews_data_%s.csv'%str(datetime.datetime.now()).replace(' ', '_')
        #self.header_params = ['page_name', 'page_url', 'page_rating', 'no_of_reviews', 'reviewd_by', 'review_text', 'star_rating', 'reviewed_on']
        #oupf = open(self.excel_file_name, 'ab+')
        #self.todays_excel_file  = csv.writer(oupf)
	#self.todays_excel_file.writerow(self.header_params)
        self.domain = "https://mbasic.facebook.com"
        #self.comments_link = 'https://www.facebook.com/{0}/activity/{1}?comment_tracking=%7B%22tn%22%3A%22O%22%7D'
	
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
        #data_list = sel.xpath('//div[@class="mvm uiP fsm"]/text()').extract()
        #import pdb;pdb.set_trace()
        #rating, reviews = data_list
        rating = ''.join(sel.xpath('//span[@class="_67l1"]/text()').extract())
        reviews = ''.join(sel.xpath('//span[@class="_67l2"]/text()').extract())
        rating = rating.split(' ')[0].encode('utf8')
        #reviews = reviews.split(' ')[0]
        reviews = ''.join(re.findall('(\d+)', reviews)).encode('utf8')
        if 'K' in reviews:
            reviews = str(float(reviews.replace('K', '')) * 1000)
        #next_page_cursor = ''.join(sel.xpath('//div[@id="most_helpful_pager"]/div/a/@href').extract())
        #cursor = ''.join(re.findall('cursor=(.*?)&', next_page_cursor))
        #page_id = ''.join(re.findall('page_id=(.*?)&', next_page_cursor))
        #if not next_page_cursor:
            #next_page_cursor = sel.xpath('//a[contains(text(), "See More")]/@href').extract()[1]
        next_page_cursor = sel.xpath('//a[contains(text(), "See More")]/@ajaxify').extract()[0]
        page_id = ''.join(re.findall('page_id=(.*?)&', next_page_cursor)).encode('utf8')
        cursor = ''.join(re.findall('cursor=(.*?)&', next_page_cursor))
        #import pdb;pdb.set_trace()
        for node in nodes:
            import pdb;pdb.set_trace()
            review_on = ''.join(node.xpath('.//abbr/@title').extract()).encode('utf8')
            review_on = datetime.datetime.strptime(review_on, '%m/%d/%Y %I:%M%p').strftime('%d/%m/%Y %H:%M:%S')
            review = ''.join(node.xpath('.//p/text()').extract()).encode('utf8')
            star_rating = ''.join(node.xpath('.//i/u/text()').extract()).encode('utf8').split(' ')[0]
            name = ''.join(node.xpath('.//span/a[@class="profileLink"]/text()').extract()[0]).encode('utf8')
            #values = (page_name, response.url, rating, reviews, name, review, star_rating, review_on)
            #link = ''.join(node.xpath('.//abbr//parent::a/@href').extract()).split('/')
            link = ''.join(node.xpath('.//abbr//parent::a/@href').extract())
            #review_id = link[-1].split(':')[0].encode('utf8')
            review_id = link.split('/')[-1].split(':')[0].encode('utf8')
            #comment_link = self.comments_link.format(link[1], review_id).encode('utf8')
            comment_link = 'https://www.facebook.com%s'%link
            values = (review_id, page_id, page_name, response.url.encode('utf8'), rating, reviews, name, review, star_rating, review_on)
            crawl_values = (review_id, comment_link, '', 'comment', '', '0', MySQLdb.escape_string(json.dumps({'values':values})))
            #self.todays_excel_file.writerow(values)
            self.cur.execute(self.query, values)
            self.cur.execute(self.crawl_query, crawl_values)
            self.con.commit()
	if cursor:
            link = self.ref_url.format(cursor.encode('utf8'), page_id.encode('utf8'))
            #import pdb;pdb.set_trace()
            yield Request(link, self.parse_next1, meta={'page_rating':rating, 'page_reviews':reviews, 'main_link':response.url, 'page_id':page_id, 'page_name':page_name})

    def parse_next1(self, response):
        data = response.body.replace('for (;', '').replace(';);', '')
        rating = response.meta['page_rating']
        reviews = response.meta['page_reviews']
        main_link = response.meta['main_link']
        rating = response.meta['page_rating']
        reviews = response.meta['page_reviews']
        main_link = response.meta['main_link']
        page_id = response.meta['page_id']
        page_name = response.meta['page_name']
	import pdb;pdb.set_trace()
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
                    '''link = ''.join(node.xpath('.//abbr//parent::a/@href').extract()).split('/')
                    review_id = link[-1].split(':')[0].encode('utf8')
                    comment_link = self.comments_link.format(link[1], review_id).encode('utf8')'''
                    link = ''.join(node.xpath('.//abbr//parent::a/@href').extract())
                    if 'story_fbid' in link:
                        review_id = ''.join(re.findall('story_fbid=(.*?)&', link))
                    else:
                        review_id = link.split('/')[-1].split(':')[0].encode('utf8')
		    comment_link = 'https://www.facebook.com%s'%link
                    values = (review_id, page_id, page_name, main_link, rating, reviews, name, review, star_rating, review_on)
                    crawl_values = (review_id, comment_link, '', 'comment', '', '0', MySQLdb.escape_string(json.dumps({'values':values})))                                                                                                                                                        #self.todays_excel_file.writerow(values)
                    #import pdb;pdb.set_trace()
                    try:
                        self.cur.execute(self.query, values)
                    except:
                        import pdb;pdb.set_trace()
                    self.cur.execute(self.crawl_query, crawl_values)
                    self.con.commit()
		try:
                    data_body1 = data_test[1][3]['__html']
		except:
		    data_body1 = ''
		if data_body1:
                    sel1 = Selector(text=data_body1)
                    #next_page_cursor = ''.join(sel1.xpath('//div[@id="most_helpful_pager"]/div/a/@href').extract())
                    next_page_cursor = ''.join(sel1.xpath('//a[contains(text(), "See More")]/@ajaxify').extract())
                    #import pdb;pdb.set_trace()
                    cursor = ''.join(re.findall('cursor=(.*?)&', next_page_cursor))
                    if cursor:
                        link = self.ref_url.format(cursor.encode('utf8'), page_id.encode('utf8'))
                        yield Request(link, self.parse_next1, meta={'page_rating':rating, 'page_reviews':reviews, 'main_link':main_link, 'page_id':page_id, 'page_name':page_name})

