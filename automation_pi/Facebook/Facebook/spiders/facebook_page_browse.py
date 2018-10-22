from fb_constants import *
from fb_browse_queries import *
import sys
sys.path.append('/root/alekhys/automation_pi/table_schemas')
from generic_functions import *
import json

class FacebookPagebrowse(BaseSpider):
    name = "facebook_page_crawler"
    start_urls = ['https://www.facebook.com/login']
    handle_httpstatus_list = [404, 302, 303, 403, 500, 400]

    def __init__(self, *args, **kwargs):
        super(FacebookPagebrowse, self).__init__(*args, **kwargs)
        self.login = kwargs.get('login','yagnasree@headrun.com')
        self.domain = "https://mbasic.facebook.com"
        self.main_dict = {}
	dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self,spider):
	try:
		f1 = open('facebook_data.txt', 'w')
		f1.write(str(self.main_dict))
	except:
		pass
    	for page_id,dict_ in self.main_dict.iteritems():
            page_url = dict_.get('page_link','')
            page_name = dict_.get('page_name', '')
            page_id = dict_.get('page_id', '')
            posts = dict_.get('posts', {})
            if posts:
            	for p_id, post_dict in posts.iteritems():
                    cmnt_dict = post_dict.get('post_comments', {})
                    if cmnt_dict:
			cmns_count = str(len(cmnt_dict.keys()))
                    	for c_id, c_dict in cmnt_dict.iteritems():
                            inner_dict = c_dict.get('inner_comments', {})
                            if inner_dict:
				inner_cmnts_count = str(len(inner_dict.keys()))
                            	for i_id, i_dict in inner_dict.iteritems():
                                    values = (page_url, page_name,  post_dict.get('post_from', '').encode('ascii','ignore').decode(), post_dict.get('post_url', ''), post_dict.get('post_message', '').encode('ascii','ignore').decode(), post_dict.get('post_on', ''), post_dict.get('post_picture', ''), post_dict.get('post_shares_count', ''),cmns_count, post_dict.get('post_reactions_total_count', ''), post_dict.get('post_like_count', ''), post_dict.get('post_love_count', ''), post_dict.get('post_wow_count', ''), post_dict.get('post_haha_count', ''), post_dict.get('post_sad_count', ''), post_dict.get('post_angry_count', ''), c_dict.get('comment_from_name', '').encode('ascii','ignore').decode(), c_dict.get('comment_message', ''), c_dict.get('comment_created_time', ''), c_dict.get('comment_reactions_total_count', ''), c_dict.get('comment_like_count', ''), c_dict.get('comment_love_count', ''), c_dict.get('comment_wow_count', ''), c_dict.get('comment_haha_count', ''), c_dict.get('comment_sad_count', ''), c_dict.get('comment_angry_count', ''), inner_cmnts_count,i_dict.get('inner_comment_from_name', '').encode('ascii','ignore').decode(), i_dict.get('inner_comment_message', ''), i_dict.get('inner_comment_created_time', ''), i_dict.get('inner_comment_like_count', ''), i_dict.get('inner_comment_love_count', ''), i_dict.get('inner_comment_wow_count', ''), i_dict.get('inner_comment_haha_count', ''), i_dict.get('inner_comment_sad_count', ''), i_dict.get('inner_comment_angry_count', ''), i_dict.get('inner_comment_reactions_total_count', ''))
                                    self.todays_excel_file.writerow(values)
                            else:
					values = (page_url, page_name,  post_dict.get('post_from', '').encode('ascii','ignore').decode(), post_dict.get('post_url', ''), post_dict.get('post_message', '').encode('ascii','ignore').decode(), post_dict.get('post_on', ''), post_dict.get('post_picture', ''), post_dict.get('post_shares_count', ''),cmns_count, post_dict.get('post_reactions_total_count', ''), post_dict.get('post_like_count', ''), post_dict.get('post_love_count', ''), post_dict.get('post_wow_count', ''), post_dict.get('post_haha_count', ''), post_dict.get('post_sad_count', ''), post_dict.get('post_angry_count', ''), c_dict.get('comment_from_name', '').encode('ascii','ignore').decode(), c_dict.get('comment_message', ''), c_dict.get('comment_created_time', ''), c_dict.get('comment_reactions_total_count', ''), c_dict.get('comment_like_count', ''), c_dict.get('comment_love_count', ''), c_dict.get('comment_wow_count', ''), c_dict.get('comment_haha_count', ''), c_dict.get('comment_sad_count', ''), c_dict.get('comment_angry_count', ''), '', '', '', '', '', '', '', '', '', '' ,'')	
					self.todays_excel_file.writerow(values)
		    else:   
                    	values = (page_url, page_name,  post_dict.get('post_from', '').encode('ascii','ignore').decode(), post_dict.get('post_url', ''), post_dict.get('post_message', '').encode('ascii','ignore').decode(), post_dict.get('post_on', ''), post_dict.get('post_picture', ''), post_dict.get('post_shares_count', ''),post_dict.get('post_comments_total_count', ''), post_dict.get('post_reactions_total_count', ''), post_dict.get('post_like_count', ''), post_dict.get('post_love_count', ''), post_dict.get('post_wow_count', ''), post_dict.get('post_haha_count', ''), post_dict.get('post_sad_count', ''), post_dict.get('post_angry_count', ''), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '')
                    	self.todays_excel_file.writerow(values)

    def parse(self, response):
        sel = Selector(response)
        login  = constants_dict[self.login]
        lsd = ''.join(sel.xpath('//input[@name="lsd"]/@value').extract())
        lgnrnd = ''.join(sel.xpath('//input[@name="lgnrnd"]/@value').extract())
        return [FormRequest.from_response(response, formname = 'login_form',\
                                formdata={'email': login[0],'pass':login[1],'lsd':lsd, 'lgnrnd':lgnrnd},callback=self.parse_redirect)]

    def parse_close(self, response):
        sel = Selector(response)
        self.res_afterlogin = sel

    def parse_redirect(self,response):
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
	links = ['https://www.facebook.com/Blur.at.Sathyam/','https://www.facebook.com/escapecinemas/','https://www.facebook.com/IDbySPICinemas/','https://www.facebook.com/KripaCinemas/','https://www.facebook.com/LeReveCinemas/','https://www.facebook.com/PalazzobySpiCinemas/','https://www.facebook.com/S2CINEMAS/','https://www.facebook.com/sathyamcinemas/','https://www.facebook.com/spicinemasindia/','https://www.facebook.com/thecinemapondy/','https://www.facebook.com/TheCinemaKSPPrime/','https://www.facebook.com/TheCinemabySPI/']
	for link in links:
		yield Request(link, self.parse_page)

    def parse_page(self, response):
	sel = Selector(response)
	page_name = normalize(''.join(sel.xpath('//link/@title').extract()))
	text = normalize(''.join(re.findall('"www_pages_reaction_see_more_unitwww_pages_home"><div><a ajaxify=(.*?) href', response.body)).replace('"',''))
	page_id, cursor, surface,unit_count= re.findall('page_id=(.*)&cursor=(.*)&surface=(.*)&unit_count=(.*)&referrer', text)[0]
	self.main_dict.update({page_id:{'page_name':page_name,'page_link':response.url}})
	yield Request('https://www.facebook.com{0}&dpr=1&fb_dtsg_ag=AdweMpnHaFZ8sUldzFZJ8YyADqLJjwxgfefvkv9G6JSAbQ%3AAdy304sxIFoqAazjyWaKaIEwd-sfaV4vP3RArV63s9YQCQ&__user=100007435239714&__a=1&__dyn=7AgNe-4amaUmgDxiWJGi9FxqeCwDKEyGgS8WGuS-CGgqx-6ES2N6xvyAubGqK6qxeqax2qqE88ObGubyRyUgyElWAxamjDK7GgPwXGtxifGdgHAy8K26ih4-e-mdx26pV8Gicx2q1yByECVoyaDzp8hz8faxle7Ve4bhoeGzVFE-rx2-9wCAgjxmuqdxC26dyFFEy2m6bGmmUS695UCUZqBCykgxieEjU8l8im2FebKqifyoPKi9zo4-4e5aGfKKeAK3iiEWbDyu9AVFoOjyF-23XxmaJ5gjUC6olz5G9BK9DDzEjVEtyEpy-fwCAzoO1agGV9-uqV8y7EK5oWiaKEKUcEjgKrGmu48y8x6mUgBx2q69U&__req=l&__be=1&__pc=PHASED%3ADEFAULT&__rev=4377939&__spin_r=4377939&__spin_b=trunk&__spin_t=1538562559'.format(text), self.parse_pages, meta={'page_link':response.url, 'page_id':page_id}, dont_filter=True)


    def parse_pages(self, response):
	sel = Selector(response)
	page_url = response.meta['page_link']
	page_id = response.meta['page_id']
	try:
		body = json.loads('{'+response.body.split(');{')[1])
	except:
		body = ''
	if body:
	    body_text = body['domops'][0][3]['__html']
	    sel = Selector(text=body_text)
	    post_nodes = sel.xpath('//div[@class="_5va1 _427x"]')
	    if not post_nodes:
	    	post_nodes = sel.xpath('//div[@class="_4-u2 _4-u8"][not(@id)]')
	    for node in post_nodes:
		p_dict = {}
		post_text = ''.join(node.xpath('.//div[@data-ad-preview="message"]//text()').extract()).replace('See More', '')
		post_date = node.xpath('.//span[@class="timestampContent"]/text()').extract()
		if post_date:
		    post_date = post_date[0]
		post_from = normalize(''.join(node.xpath('.//h6//a/text()').extract()))
		if not post_from:
		    post_from = normalize(node.xpath('.//h5//a/text()').extract()[0])
		post_id = ''.join(node.xpath('.//input[@name="ft_ent_identifier"]/@value').extract())
		post_images = '<>'.join(node.xpath('.//img[contains(@class, "scaledImageFit")]/@src').extract())
		p_link = ''.join(node.xpath('.//a[abbr]/@href').extract()[0])
		post_url = 'https://www.facebook.com/%s/posts/%s'%(p_link.split('/')[1], post_id)
		comment_url = '{0}?comment_tracking=%7B%22tn%22%3A%22O%22%7D'.format(post_url)
		c_meta = {'page_id':page_id, 'post_id':post_id}
		yield Request(comment_url, self.parse_comments, meta=c_meta,dont_filter=True)
		p_dict = {post_id:{'post_url':post_url,'post_message':post_text,'post_on':post_date,'post_picture':post_images,'post_from':post_from}}
		if self.main_dict[page_id].get('posts', ''):
		    self.main_dict[page_id]['posts'].update(p_dict)
		else:
		    self.main_dict[page_id].update({'posts':p_dict})
		post_like_link = 'https://www.facebook.com/ufi/reaction/profile/browser/?ft_ent_identifier=%s'%post_id
	text = ''.join(sel.xpath('//div[@id="www_pages_reaction_see_more_unitwww_pages_home"]/div/a/@ajaxify').extract())
	if text:
	    yield Request('https://www.facebook.com{0}&dpr=1&fb_dtsg_ag=AdweMpnHaFZ8sUldzFZJ8YyADqLJjwxgfefvkv9G6JSAbQ%3AAdy304sxIFoqAazjyWaKaIEwd-sfaV4vP3RArV63s9YQCQ&__user=100007435239714&__a=1&__dyn=7AgNe-4amaUmgDxiWJGi9FxqeCwDKEyGgS8WGuS-CGgqx-6ES2N6xvyAubGqK6qxeqax2qqE88ObGubyRyUgyElWAxamjDK7GgPwXGtxifGdgHAy8K26ih4-e-mdx26pV8Gicx2q1yByECVoyaDzp8hz8faxle7Ve4bhoeGzVFE-rx2-9wCAgjxmuqdxC26dyFFEy2m6bGmmUS695UCUZqBCykgxieEjU8l8im2FebKqifyoPKi9zo4-4e5aGfKKeAK3iiEWbDyu9AVFoOjyF-23XxmaJ5gjUC6olz5G9BK9DDzEjVEtyEpy-fwCAzoO1agGV9-uqV8y7EK5oWiaKEKUcEjgKrGmu48y8x6mUgBx2q69U&__req=l&__be=1&__pc=PHASED%3ADEFAULT&__rev=4377939&__spin_r=4377939&__spin_b=trunk&__spin_t=1538562559'.format(text), self.parse_pages, meta=response.meta, dont_filter=True)

    def parse_comments(self, response):
	sel = Selector(response)
	post_id = response.meta['post_id']
	page_id = response.meta['page_id']
	try:
	    share_count, pattern = re.findall('"sharecount":(\d+),"sharecountreduced":"\d+","sharefbid":"{0}"(.*?)reactioncountreduced"'.format(response.meta['post_id']),response.body)[0]
	except:
	    share_count, pattern = re.findall('"sharecount":(\d+),"sharecountreduced":null,"sharefbid":"{0}"(.*?)reactioncountreduced"'.format(response.meta['post_id']),response.body)[0]
	like = ''.join(re.findall('reactioncountmap":.*"1":{"default":(\d+),"reduced":.*?}', pattern)).replace('"','')
        love = ''.join(re.findall('reactioncountmap":.*"2":{"default":(\d+),"reduced":.*?}', pattern)).replace('"','')
        haha = ''.join(re.findall('reactioncountmap":.*"4":{"default":(\d+),"reduced":.*?}', pattern)).replace('"','')
        wow = ''.join(re.findall('reactioncountmap":.*"3":{"default":(\d+),"reduced":.*?}', pattern)).replace('"','')
        sad = ''.join(re.findall('reactioncountmap":.*"7":{"default":(\d+),"reduced":.*?}', pattern)).replace('"','')
        angry = ''.join(re.findall('reactioncountmap":.*"8":{"default":(\d+),"reduced":.*?}', pattern)).replace('"','')
	rea_cnt = int(like)+int(love)+int(haha)+int(wow)+int(sad)+int(angry)
	self.main_dict[page_id]['posts'][post_id].update({'post_shares_count':share_count, 'post_reactions_total_count':str(rea_cnt), 'post_like_count':like, 'post_love_count':love,'post_haha_count':haha,'post_sad_count':sad,'post_angry_count':angry, 'post_wow_count':wow})
	comments = json.loads(re.findall('"ftentidentifier":"{0}".*?"comments":(.*?),"pinnedcomments"'.format(response.meta['post_id']),response.body)[0])
	profiles = re.findall('"profiles":({.*?}),"actions"', response.body)
	p_dict = {}
	for profile in profiles:
	    p_dict.update(json.loads(profile))
	comments = re.findall('"comments":(\[.*?\]),"pinnedcomments"', response.body)
	comment_list = []
	for comment in comments:
	    comment = json.loads(comment)
	    if comment:
		comment_list.extend(comment)
	comment_count = 0
	for cmnt in comment_list:
	    if cmnt['ftentidentifier'] == post_id and cmnt['parentcommentid'] == "":
	        comment_text = normalize(cmnt['body']['text'])
		comment_id = cmnt['id']
            	c_like = cmnt['reactioncountmap']['1']['default']
                c_love = cmnt['reactioncountmap']['2']['default']
            	c_haha = cmnt['reactioncountmap']['4']['default']
            	c_wow = cmnt['reactioncountmap']['3']['default']
            	c_sad = cmnt['reactioncountmap']['7']['default']
            	c_angry = cmnt['reactioncountmap']['8']['default']
		rea_count = int(c_like)+int(c_love)+int(c_haha)+int(c_wow)+int(c_sad)+int(c_angry)
		comment_count = comment_count + 1
		comment_on = cmnt['timestamp']['verbose']
		c_id = cmnt['author']
		c_by = normalize(p_dict[c_id]['name'])
		p_cmnt_dict = {comment_id:{'comment_from_name':c_by, 'comment_message':comment_text, 'comment_created_time':comment_on, 'comment_reactions_total_count':str(rea_count), 'comment_like_count':c_like, 'comment_love_count':c_love, 'comment_haha_count':c_haha, 'comment_wow_count':c_wow, 'comment_sad_count':c_sad, 'comment_angry_count':c_angry}}
		if self.main_dict[page_id]['posts'][post_id].get('post_comments', ''):
		    self.main_dict[page_id]['posts'][post_id]['post_comments'].update(p_cmnt_dict)
		else:
		    self.main_dict[page_id]['posts'][post_id].update({'post_comments':p_cmnt_dict})
		c_meta = {'comment_id':comment_id, 'page_id':page_id, 'post_id':post_id}
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
	post_id = response.meta['post_id']
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
	    if self.main_dict[page_id]['posts'][post_id]['post_comments'][comment_id].get('inner_comments', ''):
		self.main_dict[page_id]['posts'][post_id]['post_comments'][comment_id]['inner_comments'].update(inner_dtc)
	    else:
		self.main_dict[page_id]['posts'][post_id]['post_comments'][comment_id].update({'inner_comments':inner_dtc})
	    like_link = 'https://mbasic.facebook.com/ufi/reaction/profile/browser/?ft_ent_identifier=%s&__tn__=R'%inner_id
	    i_meta = {'comment_id':comment_id, 'page_id':page_id, 'post_id':post_id, 'i_id':inner_id}
	    yield Request(like_link, self.parse_like, meta=i_meta)	

    def parse_like(self, response):
        sel = Selector(response)
	comment_id = response.meta['comment_id']
        page_id = response.meta['page_id']
        post_id = response.meta['post_id']
	i_id = response.meta['i_id']
	like = ''.join(sel.xpath('//a[img[@alt="Like"]]/span/text()').extract())
	love = ''.join(sel.xpath('//a[img[@alt="Love"]]/span/text()').extract())
	haha = ''.join(sel.xpath('//a[img[@alt="Haha"]]/span/text()').extract())
	wow = ''.join(sel.xpath('//a[img[@alt="Wow"]]/span/text()').extract())
	sad = ''.join(sel.xpath('//a[img[@alt="Sad"]]/span/text()').extract())
	angry = ''.join(sel.xpath('//a[img[@alt="Angry"]]/span/text()').extract())
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
	rea_cnt = int(like)+int(love)+int(haha)+int(wow)+int(sad)+int(angry)
        self.main_dict[page_id]['posts'][post_id]['post_comments'][comment_id]['inner_comments'][i_id].update({'inner_comment_reactions_total_count':str(rea_cnt), 'inner_comment_like_count':like, 'inner_comment_love_count':love,'inner_comment_haha_count':haha,'inner_comment_sad_count':sad,'inner_comment_angry_count':angry, 'inner_comment_wow_count':wow})

