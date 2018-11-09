import requests
from fb_constants import *
from fb_browse_queries import *
import sys
sys.path.append('/root/automation_pi/table_schemas')
from generic_functions import *
import datetime

class FacebookReviewBrowse(BaseSpider):
    name = "facebook_review_browse"
    start_urls = ['https://www.facebook.com/login']
    handle_httpstatus_list = [404, 302, 303, 403, 500]

    def __init__(self, *args, **kwargs):
        super(FacebookReviewBrowse, self).__init__(*args, **kwargs)
        self.login = kwargs.get('login','yagnasree@headrun.com')
	self.main_dict = {}
        self.ref_url = 'https://www.facebook.com/async/page_recommendation/consideration_signals_tab_pagination/?cursor={0}&page_id={1}&pager_dom_id=u_0_8&should_infinite_scroll=1&is_vertex=0&stories_container_dom_id=recommendations_tab_main_feed&sort_order=most_helpful&dpr=1.5&__user=100007435239714&__a=1&__dyn=5V4cjLx2ByK5A9UkKHqAyqomzFE9XG8GAdyedirWqK6EvxGdwIhEpyEyeCHxC7oG5VEc8W4UJu9x2axuF8iBAVXxWUPwXGt0Bx12KdwJAAhKe-2i5-uiaAz8gCxm1iyECVoyaxG4oO3-5k2eq49842E-qqfCUkUCawRxmul3opAxOdyFE-3WWKu4ooAghzRGm5At28lwxgC3mbKbzUx1qazodopx3yUymfKKey8eohx2cUCjCx3AUGvwyQF8vBojUC6pp8GcByprx6uegiVE4W10GucwVx12HzeeKi8UsyUaoWEKUcUa8&__req=k&__be=1&__pc=PHASED%3ADEFAULT&__rev=4187527&__spin_r=4187527&__spin_b=trunk&__spin_t=1533753183'
	self.headers = ['page_url', 'page_name', 'page_rating', 'reviews_count', 'review_from_name', 'review_url', 'review_message', 'review_created_time', 'review_rating', 'review_shares_count', 'review_comments_total_count', 'review_reactions_total_count', 'review_like_count', 'review_love_count', 'review_wow_count', 'review_haha_count', 'review_sad_count', 'review_angry_count','comment_from_name', 'comment_message', 'comment_created_time', 'comment_reactions_total_count', 'comment_like_count', 'comment_love_count', 'comment_wow_count', 'comment_haha_count', 'comment_sad_count', 'comment_angry_count','inner_comments_total_count','inner_comment_from_name', 'inner_comment_message', 'inner_comment_created_time', 'innercomment_like_count', 'inner_comment_love_count', 'inner_comment_wow_count', 'inner_comment_haha_count', 'inner_comment_sad_count', 'inner_comment_angry_count', 'inner_comment_reactions_total_count']
	self.excel_file_name = 'facebook_reviews_data_%s.csv'%str(datetime.datetime.now()).replace(' ', '_')
        oupf = open(self.excel_file_name, 'ab+')
        self.todays_excel_file  = csv.writer(oupf)
	self.todays_excel_file.writerow(self.headers)
        self.domain = "https://mbasic.facebook.com"
	dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self,spider):
        for page_id,dict_ in self.main_dict.iteritems():
            page_url = dict_.get('page_link','')
            page_name = dict_.get('page_name', '')
            page_id = dict_.get('page_id', '')
	    reviews_count = dict_.get('reviews_cnt', '')
	    page_rating = dict_.get('page_rating', '')
            reviews = dict_.get('reviews', {})
            if reviews:
                for r_id, review_dict in reviews.iteritems():
                    cmnt_dict = review_dict.get('review_comments', {})
		    try:
			review_from = review_dict.get('review_from', '').encode('ascii','ignore').decode()
		    except:
			review_from = review_dict.get('review_from', '').decode('utf8').encode('ascii','ignore').decode()
		    try:
			review_message = review_dict.get('review_message', '').encode('ascii','ignore').decode()
		    except:
			review_message = review_dict.get('review_message', '').decode('utf8').encode('ascii','ignore').decode()
                    if cmnt_dict:
                        cmns_count = str(len(cmnt_dict.keys()))
                        for c_id, c_dict in cmnt_dict.iteritems():
			    try:
				comment_from_name = c_dict.get('comment_from_name', '').encode('ascii','ignore').decode()
			    except:
				comment_from_name = c_dict.get('comment_from_name', '').decode('utf8').encode('ascii','ignore').decode()
                            inner_dict = c_dict.get('inner_comments', {})
                            if inner_dict:
                                inner_cmnts_count = str(len(inner_dict.keys()))
                                for i_id, i_dict in inner_dict.iteritems():
				    try:
					inner_comment_from_name = i_dict.get('inner_comment_from_name', '').encode('ascii','ignore').decode()
				    except:
					inner_comment_from_name = i_dict.get('inner_comment_from_name', '').decode('utf8').encode('ascii','ignore').decode()
                                    values = (page_url, page_name, page_rating, reviews_count, review_from, review_dict.get('review_url', ''), review_message, review_dict.get('review_on', ''), review_dict.get('review_rating', ''), review_dict.get('review_shares_count', ''), cmns_count, review_dict.get('review_reactions_total_count', ''), review_dict.get('review_like_count', ''), review_dict.get('review_love_count', ''), review_dict.get('review_wow_count', ''), review_dict.get('review_haha_count', ''), review_dict.get('review_sad_count', ''), review_dict.get('review_angry_count', ''), comment_from_name, c_dict.get('comment_message', ''), c_dict.get('comment_created_time', ''), c_dict.get('comment_reactions_total_count', ''), c_dict.get('comment_like_count', ''), c_dict.get('comment_love_count', ''), c_dict.get('comment_wow_count', ''), c_dict.get('comment_haha_count', ''), c_dict.get('comment_sad_count', ''), c_dict.get('comment_angry_count', ''), inner_cmnts_count, inner_comment_from_name, i_dict.get('inner_comment_message', ''), i_dict.get('inner_comment_created_time', ''), i_dict.get('inner_comment_like_count', ''), i_dict.get('inner_comment_love_count', ''), i_dict.get('inner_comment_wow_count', ''), i_dict.get('inner_comment_haha_count', ''), i_dict.get('inner_comment_sad_count', ''), i_dict.get('inner_comment_angry_count', ''), i_dict.get('inner_comment_reactions_total_count', ''))
                                    self.todays_excel_file.writerow(values)
                            else:
				values = (page_url, page_name, page_rating, reviews_count, review_from, review_dict.get('review_url', ''), review_message, review_dict.get('review_on', ''), review_dict.get('review_rating', ''), review_dict.get('review_shares_count', ''),cmns_count, review_dict.get('review_reactions_total_count', ''), review_dict.get('review_like_count', ''), review_dict.get('review_love_count', ''), review_dict.get('review_wow_count', ''), review_dict.get('review_haha_count', ''), review_dict.get('review_sad_count', ''), review_dict.get('review_angry_count', ''), comment_from_name, c_dict.get('comment_message', ''), c_dict.get('comment_created_time', ''), c_dict.get('comment_reactions_total_count', ''), c_dict.get('comment_like_count', ''), c_dict.get('comment_love_count', ''), c_dict.get('comment_wow_count', ''), c_dict.get('comment_haha_count', ''), c_dict.get('comment_sad_count', ''), c_dict.get('comment_angry_count', ''), '0', '', '', '', '0', '0', '0', '0', '0', '0' ,'0')
                                self.todays_excel_file.writerow(values)
                    else:
                        values = (page_url, page_name, page_rating, reviews_count, review_from, review_dict.get('review_url', ''), review_message, review_dict.get('review_on', ''), review_dict.get('review_rating', ''), review_dict.get('review_shares_count', ''), review_dict.get('review_comments_total_count', ''), review_dict.get('review_reactions_total_count', ''), review_dict.get('review_like_count', ''), review_dict.get('review_love_count', ''), review_dict.get('review_wow_count', ''), review_dict.get('review_haha_count', ''), review_dict.get('review_sad_count', ''), review_dict.get('review_angry_count', ''), '', '', '', '0', '0', '0', '0', '0', '0', '0', '0', '', '', '', '0', '0', '0', '0', '0', '0', '0')
                        self.todays_excel_file.writerow(values)

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
        rating = ''.join(sel.xpath('//span[@class="_67l1"]/text()').extract())
        reviews = ''.join(sel.xpath('//span[@class="_67l2"]/text()').extract())
        rating = rating.split(' ')[0].encode('utf8')
        reviews = ''.join(re.findall('(\d+)', reviews)).encode('utf8')
        if 'K' in reviews:
            reviews = str(float(reviews.replace('K', '')) * 1000)
        next_page_cursor = sel.xpath('//a[contains(text(), "See More")]/@ajaxify').extract()[0]
        page_id = ''.join(re.findall('page_id=(.*?)&', next_page_cursor)).encode('utf8')
        cursor = ''.join(re.findall('cursor=(.*?)&', next_page_cursor))
	self.main_dict.update({page_id:{'page_name':page_name,'page_link':response.url, 'page_rating':rating, 'reviews_cnt':reviews}})
        for node in nodes:
            review_on = ''.join(node.xpath('.//abbr/@title').extract()).encode('utf8')
            review_on = datetime.datetime.strptime(review_on, '%m/%d/%Y %I:%M%p').strftime('%d/%m/%Y %H:%M:%S')
            review = ''.join(node.xpath('.//p/text()').extract()).encode('utf8')
            star_rating = ''.join(node.xpath('.//i/u/text()').extract()).encode('utf8').split(' ')[0]
            name = ''.join(node.xpath('.//span/a[@class="profileLink"]/text()').extract()[0]).encode('utf8')
            link = ''.join(node.xpath('.//abbr//parent::a/@href').extract())
	    review_id = ''.join(node.xpath('.//input[@name="ft_ent_identifier"]/@value').extract())
            comment_link = 'https://www.facebook.com%s'%link
	    r_dict = {review_id:{'review_message':review,'review_on':review_on,'review_from':name, 'review_rating':star_rating, 'review_url':comment_link}}
	    if self.main_dict[page_id].get('reviews', ''):
            	self.main_dict[page_id]['reviews'].update(r_dict)
            else:
                self.main_dict[page_id].update({'reviews':r_dict})
	    yield Request(comment_link, self.parse_comments, meta={'review_id':review_id, 'page_id':page_id}, dont_filter=True)
	if cursor:
            link = self.ref_url.format(cursor.encode('utf8'), page_id.encode('utf8'))
            yield Request(link, self.parse_next1, meta={'page_id':page_id}, dont_filter=True)

    def parse_comments(self, response):
	sel = Selector(response)
        review_id = response.meta['review_id']
        page_id = response.meta['page_id']
        try:
            share_count, pattern = re.findall('sharecount:(\d+),sharecountreduced:\d+,sharefbid:"{0}"(.*?)reactioncountreduced'.format(response.meta['review_id']),response.body)[0]
        except:
            share_count, pattern = re.findall('sharecount:(\d+),sharecountreduced:null,sharefbid:"{0}"(.*?)reactioncountreduced'.format(response.meta['review_id']),response.body)[0]
        like = ''.join(re.findall('reactioncountmap:.*"1":{default:(\d+),reduced:.*?}', pattern)).replace('"','')
        love = ''.join(re.findall('reactioncountmap:.*"2":{default:(\d+),reduced:.*?}', pattern)).replace('"','')
        haha = ''.join(re.findall('reactioncountmap:.*"4":{default:(\d+),reduced:.*?}', pattern)).replace('"','')
        wow = ''.join(re.findall('reactioncountmap:.*"3":{default:(\d+),reduced:.*?}', pattern)).replace('"','')
        sad = ''.join(re.findall('reactioncountmap:.*"7":{default:(\d+),reduced:.*?}', pattern)).replace('"','')
        angry = ''.join(re.findall('reactioncountmap:.*"8":{default:(\d+),reduced:.*?}', pattern)).replace('"','')
	rea_cnt, like, love, haha, wow, sad, angry = count_(like, love, haha, wow, sad, angry)
	self.main_dict[page_id]['reviews'][review_id].update({'review_shares_count':share_count, 'review_reactions_total_count':str(rea_cnt), 'review_like_count':like, 'review_love_count':love,'review_haha_count':haha,'review_sad_count':sad,'review_angry_count':angry, 'review_wow_count':wow})
        comment_string = ''.join(re.findall('{comments:(.*),pinnedcomments', response.body))
        comments = re.findall('(body:{text:.*?),surveyGalleryHighlight:false', comment_string)
        profile_text = ''.join(re.findall('profiles:(.*),actions', response.body))
        for comment in comments:
            cmment = ''.join(re.findall('body:{text:(.*?)},isfeatured', comment)).split(',ranges:')[0].replace('"', '')
            c_like = ''.join(re.findall('reactioncountmap:.*"1":{default:(\d+),reduced:.*?}', comment)).replace('"','')
            c_love = ''.join(re.findall('reactioncountmap:.*"2":{default:(\d+),reduced:.*?}', comment)).replace('"','')
            c_haha = ''.join(re.findall('reactioncountmap:.*"4":{default:(\d+),reduced:.*?}', comment)).replace('"','')
            c_wow = ''.join(re.findall('reactioncountmap:.*"3":{default:(\d+),reduced:.*?}', comment)).replace('"','')
            c_sad = ''.join(re.findall('reactioncountmap:.*"7":{default:(\d+),reduced:.*?}', comment)).replace('"','')
            c_angry = ''.join(re.findall('reactioncountmap:.*"8":{default:(\d+),reduced:.*?}', comment)).replace('"','')
            author_id=''.join(re.findall(',author:(.*),ftentidentifier', comment))
	    comment_id = ''.join(re.findall(',fbid:"(.*)",legacyid', comment))
            commented_by = ''.join(re.findall('id:%s,name:(.*?),firstName'%author_id, profile_text)).replace('"', '')
            commented_on = ''.join(re.findall('timestamp:{.*,text:(.*),verbose:',comment)).replace('"','')
     	    rea_count, c_like, c_love, c_haha, c_wow, c_sad, c_angry = count_(c_like, c_love, c_haha, c_wow, c_sad, c_angry)
	    r_cmnt_dict = {comment_id:{'comment_from_name':commented_by, 'comment_message':cmment, 'comment_created_time':commented_on, 'comment_reactions_total_count':str(rea_count), 'comment_like_count':c_like, 'comment_love_count':c_love, 'comment_haha_count':c_haha, 'comment_wow_count':c_wow, 'comment_sad_count':c_sad, 'comment_angry_count':c_angry}}
	    if self.main_dict[page_id]['reviews'][review_id].get('review_comments', ''):
                self.main_dict[page_id]['reviews'][review_id]['review_comments'].update(r_cmnt_dict)
            else:
            	self.main_dict[page_id]['reviews'][review_id].update({'review_comments':r_cmnt_dict})
	    c_meta = {'comment_id':comment_id, 'page_id':page_id, 'review_id':review_id}
	    comment_link = response.url.replace('www', 'mbasic')
            yield Request(comment_link, self.parse_comment, meta=c_meta, dont_filter=True)

    def parse_comment(self, response):
        sel = Selector(response)
        comment_id = response.meta['comment_id']
        inner_cmnt_link = ''.join(sel.xpath('//div[@id="%s"]//a[text()="Reply"]/@href'%comment_id.split('_')[-1]).extract())
        if inner_cmnt_link:
            comment_link = response.url
            inner_cmnt_link = 'https://mbasic.facebook.com%s'%inner_cmnt_link
            yield Request(inner_cmnt_link, self.parse_inner_comments, meta=response.meta, dont_filter=True)

    def parse_inner_comments(self, response):
        sel = Selector(response)
        comment_id = response.meta['comment_id']
        page_id = response.meta['page_id']
        review_id = response.meta['review_id']
        nodes=sel.xpath('//div[div[h3]]')
        if len(nodes)>1:
            nodes=nodes[1:]
        else:
            nodes = []
        for node in nodes:
            i_c_by = normalize(''.join(node.xpath('./div/h3/a/text()').extract()))
            i_cmnt = normalize(''.join(node.xpath('./div/h3/following-sibling::div[1]//text()').extract()))
            i_c_on = ''.join(node.xpath('.//abbr/text()').extract())
            i_id = ''.join(node.xpath('./@id').extract())
            inner_id = comment_id.split('_')[0]+'_'+i_id
            inner_dtc = {inner_id:{'inner_comment_from_name':i_c_by,'inner_comment_message':i_cmnt,'inner_comment_created_time':i_c_on}}
            if self.main_dict[page_id]['reviews'][review_id]['review_comments'][comment_id].get('inner_comments', ''):
                self.main_dict[page_id]['reviews'][review_id]['review_comments'][comment_id]['inner_comments'].update(inner_dtc)
            else:
                self.main_dict[page_id]['reviews'][review_id]['review_comments'][comment_id].update({'inner_comments':inner_dtc})
            like_link = 'https://mbasic.facebook.com/ufi/reaction/profile/browser/?ft_ent_identifier=%s&__tn__=R'%inner_id.split('_')[-1]
            i_meta = {'comment_id':comment_id, 'page_id':page_id, 'review_id':review_id, 'i_id':inner_id}
            yield Request(like_link, self.parse_like, meta=i_meta, dont_filter=True)

    def parse_like(self, response):
        sel = Selector(response)
        comment_id = response.meta['comment_id']
        page_id = response.meta['page_id']
        review_id = response.meta['review_id']
        i_id = response.meta['i_id']
        like = ''.join(sel.xpath('//a[img[@alt="Like"]]/span/text()').extract())
        love = ''.join(sel.xpath('//a[img[@alt="Love"]]/span/text()').extract())
        haha = ''.join(sel.xpath('//a[img[@alt="Haha"]]/span/text()').extract())
        wow = ''.join(sel.xpath('//a[img[@alt="Wow"]]/span/text()').extract())
        sad = ''.join(sel.xpath('//a[img[@alt="Sad"]]/span/text()').extract())
        angry = ''.join(sel.xpath('//a[img[@alt="Angry"]]/span/text()').extract())
	rea_cnt,like,love,haha,wow,sad,angry = count_(like, love, haha, wow, sad, angry)
        self.main_dict[page_id]['reviews'][review_id]['review_comments'][comment_id]['inner_comments'][i_id].update({'inner_comment_reactions_total_count':str(rea_cnt), 'inner_comment_like_count':like, 'inner_comment_love_count':love,'inner_comment_haha_count':haha,'inner_comment_sad_count':sad,'inner_comment_angry_count':angry, 'inner_comment_wow_count':wow})

    def parse_next1(self, response):
        data = response.body.replace('for (;', '').replace(';);', '')
        page_id = response.meta['page_id']
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
                    link = ''.join(node.xpath('.//abbr//parent::a/@href').extract())
		    review_id = ''.join(node.xpath('.//input[@name="ft_ent_identifier"]/@value').extract())
		    comment_link = 'https://www.facebook.com%s'%link
		    r_dict = {review_id:{'review_message':review,'review_on':review_on,'review_from':name, 'review_rating':star_rating, 'review_url':comment_link}}
		    if self.main_dict[page_id].get('reviews', ''):
                    	self.main_dict[page_id]['reviews'].update(r_dict)
                    else:
                    	self.main_dict[page_id].update({'reviews':r_dict})
		    yield Request(comment_link, self.parse_comments, meta={'review_id':review_id, 'page_id':page_id}, dont_filter=True)
		try:
                    data_body1 = data_test[1][3]['__html']
		except:
		    data_body1 = ''
		if data_body1:
                    sel1 = Selector(text=data_body1)
                    next_page_cursor = ''.join(sel1.xpath('//a[contains(text(), "See More")]/@ajaxify').extract())
                    cursor = ''.join(re.findall('cursor=(.*?)&', next_page_cursor))
                    if cursor:
                        link = self.ref_url.format(cursor.encode('utf8'), page_id.encode('utf8'))
                        yield Request(link, self.parse_next1, meta={'page_id':page_id}, dont_filter=True)

def count_(like, love, haha, wow, sad, angry):
        if not like:
            like = '0'
        if not love:
            love = '0'
        if not haha:
            haha = '0'
        if not wow:
            wow = '0'
        if not sad:
            sad = '0'
        if not angry:
            angry = '0'
        r_cnt = int(like)+int(love)+int(haha)+int(wow)+int(sad)+int(angry)
        return str(r_cnt), like, love, haha, wow, sad, angry

