import requests
from fb_constants import *
from fb_browse_queries import *
import sys
sys.path.append('/root/alekhys/automation_pi/table_schemas')
from generic_functions import *
import datetime

class FacebookCommentsBrowse(BaseSpider):
    name = "facebook_comment_browse"
    start_urls = ['https://www.facebook.com/login']
    handle_httpstatus_list = [404, 302, 303, 403, 500]

    def __init__(self, *args, **kwargs):
        super(FacebookCommentsBrowse, self).__init__(*args, **kwargs)
        self.login = kwargs.get('login','yagnasree@headrun.com')
        self.con = MySQLdb.connect(db='FACEBOOK_REVIEWS', host='localhost', charset="utf8", use_unicode=True, user='root', passwd='root')
        self.cur = self.con.cursor()
	self.select_query = 'select sk,url,meta_data from facebook_crawl where crawl_status=0 limit 1'
        #self.query = 'insert into facebook_reviews(id, page_id, page_name, reference_url, page_rating, reviews, reviewed_by, review_text, review_rating, reviewed_on, modified_at, created_at) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), now())'
        #self.crawl_query = 'insert into facebook_crawl(sk, url, crawl_type, content_type, related_type, crawl_status, meta_data, created_at, modified_at) values(%s, %s, %s, %s, %s, %s, %s, now(), now())'

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
	self.cur.execute(self.select_query)
        rows = self.cur.fetchall()
        '''for row in rows:
	    id_, review_url, meta_data = row
            yield Request(review_url, callback=self.parse_comment, meta={'row':row})'''
	
	#yield Request('https://www.facebook.com/citizen.manoj/activity/1603461276388166?comment_tracking=%7B%22tn%22%3A%22O%22%7D', callback=self.parse_comment)
	yield Request('https://www.facebook.com/rajareddy.akepati.39/activity/174033273169073?comment_tracking=%7B%22tn%22%3A%22O%22%7D', self.parse_comment)

    def parse_close(self, response):
        sel = Selector(response)
        self.res_afterlogin = sel

    def parse_comment(self, response):
	sel = Selector(response)
	import pdb;pdb.set_trace()
	#comments = ''.join(re.findall('{comments:\[{body:{text:(.*?),ranges', response.body)).replace('"','')
	comment_string = ''.join(re.findall('{comments:(.*),pinnedcomments', response.body))
	#comments = re.findall('body:{text:(.*?)},isfeatured', comment_string)
	comments = re.findall('(body:{text:.*?),surveyGalleryHighlight:false', comment_string)
	'''row = response.meta['row']
	id_, url, meta_data = row'''
	id_ = '174033273169073'
	likes_link = 'https://www.facebook.com/ufi/reaction/profile/browser/?ft_ent_identifier=%s'%id_
	yield Request(likes_link, self.parse_like)
	profile_text = ''.join(re.findall('profiles:(.*),actions', response.body))
	for comment in comments:
	    cmment = ''.join(re.findall('body:{text:(.*?)},isfeatured', comment)).split(',ranges:')[0].replace('"', '')
	    like = ''.join(re.findall('reactioncountmap:.*"1":{default:0,reduced:(.*?)}', comment)).replace('"','')
	    love = ''.join(re.findall('reactioncountmap:.*"2":{default:0,reduced:(.*?)}', comment)).replace('"','')
	    haha = ''.join(re.findall('reactioncountmap:.*"4":{default:0,reduced:(.*?)}', comment)).replace('"','')
	    wow = ''.join(re.findall('reactioncountmap:.*"3":{default:0,reduced:(.*?)}', comment)).replace('"','')
	    sad = ''.join(re.findall('reactioncountmap:.*"7":{default:0,reduced:(.*?)}', comment)).replace('"','')
	    angry = ''.join(re.findall('reactioncountmap:.*"8":{default:0,reduced:(.*?)}', comment)).replace('"','')
	    author_id=''.join(re.findall(',author:(.*),ftentidentifier', comment))
	    commented_by = ''.join(re.findall('id:%s,name:(.*?),firstName'%author_id, profile_text)).replace('"', '')
	    commented_on = ''.join(re.findall('timestamp:{.*,text:(.*),verbose:',comment)).replace('"','')
	    print cmment, like,love,haha,wow,sad,angry , commented_on,commented_by 
	    reply_authors = ''.join(re.findall('replyauthors:(.*),canembed', comment))
	    if reply_authors:
		feed_context = ''.join(re.findall('feedcontext:"(.*)",feedLocationType', response.body))
            	parent_id = ''.join(re.findall(',id:"(.*)",fbid', comment))
		container = ''.join(re.findall('containerorderingmode:"(.*?)"}', comment))

		headers = {
    			'origin': 'https://www.facebook.com',
    			'accept-encoding': 'gzip, deflate, br',
    			'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    			'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    			'content-type': 'application/x-www-form-urlencoded',
    			'accept': '*/*',
    			'referer': response.url,
    			'authority': 'www.facebook.com',
    			'cookie': 'sb=pIKgWzYlnfvKaAfy_OBOHCTp; datr=zYKgWye7t3fZnqekSCfT1qzr; c_user=100007435239714; xs=10%3A16ee7kmmYzw0Yg%3A2%3A1538392131%3A4278%3A9249; pl=n; spin=r.4377939_b.trunk_t.1538562559_s.1_v.2_; fr=0CMeCKv94KPwvQDT6.AWXpejGZL5RJavadyasaqPMJTjc.BbmzXB.8H.AAA.0.0.BbtJoF.AWXmCs9D; presence=EDvF3EtimeF1538562983EuserFA21B07435239714A2EstateFDutF1538562983556CEchFDp_5f1B07435239714F2CC; wd=1301x378; act=1538563000225%2F4; pnl_data2=eyJhIjoib25hZnRlcmxvYWQiLCJjIjoiV2ViUGVybWFsaW5rU3RyZWFtQ29udHJvbGxlciIsImIiOmZhbHNlLCJkIjoiL1lhbmtlZVByaS9wb3N0cy8xMDIxNDY4MzE4ODc4NTg5NSIsImUiOltdfQ%3D%3D',
		}


		data = {
  			'ft_ent_identifier': id_,
  			'parent_comment_ids[0]': parent_id,
  			'source': '',
  			'offsets[0]': '0',
  			'lengths[0]': '1',
  			#'feed_context': '{"is_viewer_page_admin":false,"is_notification_preview":false,"autoplay_with_channelview_or_snowlift":false,"video_player_origin":"permalink","fbfeed_context":true,"location_type":5,"outer_object_element_id":"u_0_v","object_element_id":"u_0_v","is_ad_preview":false,"is_editable":false,"mall_how_many_post_comments":2,"bump_reason":0,"enable_comment":false,"story_width":502,"tn-str":"-R"}',
  			'feed_context': feed_context,
			'numpagerclicks': '1',
  			'containerorderingmode': container,
  			'av': '100007435239714',
  			'__user': '100007435239714',
  			'__a': '1',
  			'__dyn': '7AgNe-4amaxx2u6aJGeFxqewRyaGey8gF4Wo8ovxGdwIhE98nwgUaofUvmbwPG2OUG4XzEeUK3uczoboGq1hVUkz8nxm1Dxa2m4o6e2e2a3GE2KDBw9-6pEsgoxu6U6O11x-2KdwRwGUkBxeEgy85OcGdpEix69wyQE99m4-2emfzaG9wzzUiVE4W10Gucwhp4ax3zHAy85iaxa4oeonzogy898dU-',
  			'__req': 'v',
  			'__be': '1',
  			'__pc': 'PHASED:DEFAULT',
  			'__rev': '4377939',
  			'fb_dtsg': 'AQESrCm9tddd:AQGi68g813w0',
  			'jazoest': '265816983114671095711610010010058658171105545610356495111948',
  			'__spin_r': '4377939',
  			'__spin_b': 'trunk',
  			'__spin_t': '1538562559'
		}

		response = requests.post('https://www.facebook.com/ajax/ufi/reply_fetch.php?dpr=1', headers=headers, params=params)

	    

    def parse_like(self, response):
	sel = Selector(response)
	like = len(sel.xpath('//li[div[contains(text(), "Like")]]/div/ul/li'))
	love = len(sel.xpath('//li[div[contains(text(), "Love")]]/div/ul/li'))
	haha = len(sel.xpath('//li[div[contains(text(), "Haha")]]/div/ul/li'))
	wow = len(sel.xpath('//li[div[contains(text(), "Wow")]]/div/ul/li'))
	sad = len(sel.xpath('//li[div[contains(text(), "Sad")]]/div/ul/li'))
	angry = len(sel.xpath('//li[div[contains(text(), "Angry")]]/div/ul/li'))
	print str(like),str(love),str(haha), str(wow), str(sad), str(angry)
