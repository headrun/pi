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
	yield Request('https://www.facebook.com/escapecinemas/', self.parse_page)

    def parse_page(self, response):
	sel = Selector(response)
	page_name = ''.join(sel.xpath('//link/@title').extract())
	text = normalize(''.join(re.findall('"www_pages_reaction_see_more_unitwww_pages_home"><div><a ajaxify=(.*?) href', response.body)).replace('"',''))
	page_id, cursor, surface,unit_count= re.findall('page_id=(.*)&cursor=(.*)&surface=(.*)&unit_count=(.*)&referrer', text)[0]
	headers = {
    		'accept-encoding': 'gzip, deflate, br',
    		'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    		'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    		'accept': '*/*',
    		'referer': 'https://www.facebook.com/Blur.at.Sathyam/',
    		'authority': 'www.facebook.com',
    		'cookie': 'sb=pIKgWzYlnfvKaAfy_OBOHCTp; datr=zYKgWye7t3fZnqekSCfT1qzr; c_user=100007435239714; xs=10%3A16ee7kmmYzw0Yg%3A2%3A1538392131%3A4278%3A9249; pl=n; spin=r.4377939_b.trunk_t.1538562559_s.1_v.2_; act=1538567695597%2F29; fr=0CMeCKv94KPwvQDT6.AWXxZPOXNPWIwlIgMQiRp9257IE.BbmzXB.8H.Fu0.0.0.BbtLa_.AWXKsz57; wd=1301x378; presence=EDvF3EtimeF1538571732EuserFA21B07435239714A2EstateFDutF1538571732657CEchFDp_5f1B07435239714F2CC',
	}

	params = {
	    'page_id':page_id,
	    'cursor': cursor,
	    'surface': surface,
	    'unit_count': unit_count,
	    'referrer': '',
	    'dpr': '1',
	    'fb_dtsg_ag': 'AdweMpnHaFZ8sUldzFZJ8YyADqLJjwxgfefvkv9G6JSAbQ:Ady304sxIFoqAazjyWaKaIEwd-sfaV4vP3RArV63s9YQCQ',
	    #'fb_dtsg_ag': 'AdzKmvdjLJHI4lVPFCPOyecMZLrI5yTUHB_ageYFwSwM1g:AdwqwIKJHvo_sLmo4EsRRyifl8BGnH2-v4SrXD_6J1-2-Q',
	    '__user': '100007435239714',
	    '__a': '1',
	    '__dyn': '7AgNe-4amaUmgDxiWJGi9FxqeCwDKEyGgS8WGuS-CGgqx-6ES2N6xvyAubGqK6qxeqax2qqE88ObGubyRyUgyElWAxamjDK7GgPwXGtxifGdgHAy8K26ih4-e-mdx26pV8Gicx2q1yByECVoyaDzp8hz8faxle7Ve4bhoeGzVFE-rx2-9wCAgjxmuqdxC26dyFFEy2m6bGmmUS695UCUZqBCykgxieEjU8l8im2FebKqifyoPKi9zo4-4e5aGfKKeAK3iiEWbDyu9AVFoOjyF-23XxmaJ5gjUC6olz5G9BK9DDzEjVEtyEpy-fwCAzoO1agGV9-uqV8y7EK5oWiaKEKUcEjgKrGmu48y8x6mUgBx2q69U',
	    #'__dyn': '7AgNe-4amaUmgDxiWJGi9FxqeCwKyaF3ozGFXheCGgqx-6ES2N6xvyAubGqK6qxeqax2qqE88ObGubyRyUgyElWAxamjDK7GgPwXGtxifGdgHAy8K26ih4-e-mdx26pV8Gicx2q1yByECVoyaDzp8hz8faxle7Ve4bhoeGzVFE-rx2-9wCAgjxmuqdxC26dyFFEy2m6bGmmUS695UCUZqBCykgxieEjU8l8im2FebKqifyoPKi9zo4-4e5aGfCUWiUd9azEKu9UXCBz9eaDU8fK5oGQ6K9xC5oNoOmUCuuexfCxSaxCbU-2qidz84F2HAypVHAy8uyUlzF8GWyXwOxd2VKFpUgy8y4prx2m49E88',
	    '__req': 'l',
	    '__be': '1',
	    '__pc': 'PHASED:DEFAULT',
	    '__rev': '4377939',
	    '__spin_r': '4377939',
	    '__spin_b': 'trunk',
	    '__spin_t': '1538562559',
	}
	yield Request('https://www.facebook.com{0}&dpr=1&fb_dtsg_ag=AdweMpnHaFZ8sUldzFZJ8YyADqLJjwxgfefvkv9G6JSAbQ%3AAdy304sxIFoqAazjyWaKaIEwd-sfaV4vP3RArV63s9YQCQ&__user=100007435239714&__a=1&__dyn=7AgNe-4amaUmgDxiWJGi9FxqeCwDKEyGgS8WGuS-CGgqx-6ES2N6xvyAubGqK6qxeqax2qqE88ObGubyRyUgyElWAxamjDK7GgPwXGtxifGdgHAy8K26ih4-e-mdx26pV8Gicx2q1yByECVoyaDzp8hz8faxle7Ve4bhoeGzVFE-rx2-9wCAgjxmuqdxC26dyFFEy2m6bGmmUS695UCUZqBCykgxieEjU8l8im2FebKqifyoPKi9zo4-4e5aGfKKeAK3iiEWbDyu9AVFoOjyF-23XxmaJ5gjUC6olz5G9BK9DDzEjVEtyEpy-fwCAzoO1agGV9-uqV8y7EK5oWiaKEKUcEjgKrGmu48y8x6mUgBx2q69U&__req=l&__be=1&__pc=PHASED%3ADEFAULT&__rev=4377939&__spin_r=4377939&__spin_b=trunk&__spin_t=1538562559'.format(text), self.parse_pages, meta={'page_name':page_name, 'page_link':response.url, 'page_id':page_id})

    def parse_pages(self, response):
	sel = Selector(response)
	meta = response.meta
	page_url = meta['page_link']
	page_name = meta['page_name']
	page_id = meta['page_id']
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
		post_text = ''.join(node.xpath('.//div[@data-ad-preview="message"]//text()').extract()).replace('See More', '')
		post_date = node.xpath('.//span[@class="timestampContent"]/text()').extract()
		if post_date:
		    post_date = post_date[0]
		post_from = ''.join(node.xpath('.//h6//a/text()').extract())
		if not post_from:
		    post_from = node.xpath('.//h5//a/text()').extract()[0]
		post_to =  ''
		post_id = ''.join(node.xpath('.//input[@name="ft_ent_identifier"]/@value').extract())
		post_images = '<>'.join(node.xpath('.//img[contains(@class, "scaledImageFit")]/@src').extract())
		post_url = '%sposts/%s'%(page_url,post_id)
		comment_url = '{0}posts/{1}?comment_tracking=%7B%22tn%22%3A%22O%22%7D'.format(page_url, post_id)
		c_meta = {'page_name':page_name, 'page_link':page_url, 'page_id':page_id, 'post_id':post_id}
		yield Request(comment_url, self.parse_comments, meta=c_meta)
		print '*******************************************************************'
		print post_text.encode('ascii','ignore').decode()
		print post_date
		print post_from
		print post_id
		print post_images
		print post_url
		post_like_link = 'https://www.facebook.com/ufi/reaction/profile/browser/?ft_ent_identifier=%s'%post_id
        	#yield Request(post_like_link, self.parse_like, meta=meta)

	text = ''.join(sel.xpath('//div[@id="www_pages_reaction_see_more_unitwww_pages_home"]/div/a/@ajaxify').extract())
	#import pdb;pdb.set_trace()
	if text:
	    yield Request('https://www.facebook.com{0}&dpr=1&fb_dtsg_ag=AdweMpnHaFZ8sUldzFZJ8YyADqLJjwxgfefvkv9G6JSAbQ%3AAdy304sxIFoqAazjyWaKaIEwd-sfaV4vP3RArV63s9YQCQ&__user=100007435239714&__a=1&__dyn=7AgNe-4amaUmgDxiWJGi9FxqeCwDKEyGgS8WGuS-CGgqx-6ES2N6xvyAubGqK6qxeqax2qqE88ObGubyRyUgyElWAxamjDK7GgPwXGtxifGdgHAy8K26ih4-e-mdx26pV8Gicx2q1yByECVoyaDzp8hz8faxle7Ve4bhoeGzVFE-rx2-9wCAgjxmuqdxC26dyFFEy2m6bGmmUS695UCUZqBCykgxieEjU8l8im2FebKqifyoPKi9zo4-4e5aGfKKeAK3iiEWbDyu9AVFoOjyF-23XxmaJ5gjUC6olz5G9BK9DDzEjVEtyEpy-fwCAzoO1agGV9-uqV8y7EK5oWiaKEKUcEjgKrGmu48y8x6mUgBx2q69U&__req=l&__be=1&__pc=PHASED%3ADEFAULT&__rev=4377939&__spin_r=4377939&__spin_b=trunk&__spin_t=1538562559'.format(text), self.parse_pages, meta=meta)

    def parse_comments(self, response):
	sel = Selector(response)
	meta = response.meta
	post_id = response.meta['post_id']
	try:
	    share_count, pattern = re.findall('"sharecount":(\d+),"sharecountreduced":"\d+","sharefbid":"{0}"(.*?)reactioncountreduced"'.format(response.meta['post_id']),response.body)[0]
	except:
	    share_count, pattern = re.findall('"sharecount":(\d+),"sharecountreduced":null,"sharefbid":"{0}"(.*?)reactioncountreduced"'.format(response.meta['post_id']),response.body)[0]
	#share_count, patter, comments = re.findall('"sharecount":(\d+),"sharecountreduced":"\d+","sharefbid":"{0}"(.*?)reactioncountreduced".*"comments":(.*?),"pinnedcomments"'.format(response.meta['post_id']),response.body)[0]
	like = ''.join(re.findall('reactioncountmap":.*"1":{"default":(\d+),"reduced":.*?}', pattern)).replace('"','')
        love = ''.join(re.findall('reactioncountmap":.*"2":{"default":(\d+),"reduced":.*?}', pattern)).replace('"','')
        haha = ''.join(re.findall('reactioncountmap":.*"4":{"default":(\d+),"reduced":.*?}', pattern)).replace('"','')
        wow = ''.join(re.findall('reactioncountmap":.*"3":{"default":(\d+),"reduced":.*?}', pattern)).replace('"','')
        sad = ''.join(re.findall('reactioncountmap":.*"7":{"default":(\d+),"reduced":.*?}', pattern)).replace('"','')
        angry = ''.join(re.findall('reactioncountmap":.*"8":{"default":(\d+),"reduced":.*?}', pattern)).replace('"','')
	comments = json.loads(re.findall('"ftentidentifier":"{0}".*?"comments":(.*?),"pinnedcomments"'.format(response.meta['post_id']),response.body)[0])
	print str(like),str(love),str(haha), str(wow), str(sad), str(angry)
	'''comment_count = len(comments)
	for comment in comments:
	    comment_text = comment['body']['text']
	    c_like = comment['reactioncountmap']['1']['default']
	    c_love = comment['reactioncountmap']['2']['default']
	    c_haha = comment['reactioncountmap']['4']['default']
	    c_wow = comment['reactioncountmap']['3']['default']
	    c_sad = comment['reactioncountmap']['7']['default']
	    c_angry = comment['reactioncountmap']['8']['default']'''
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
	        comment_text = cmnt['body']['text']
		print comment_text
		comment_id = cmnt['id']
            	c_like = cmnt['reactioncountmap']['1']['default']
                c_love = cmnt['reactioncountmap']['2']['default']
            	c_haha = cmnt['reactioncountmap']['4']['default']
            	c_wow = cmnt['reactioncountmap']['3']['default']
            	c_sad = cmnt['reactioncountmap']['7']['default']
            	c_angry = cmnt['reactioncountmap']['8']['default']
		comment_count = comment_count + 1
		print str(c_like),str(c_love),str(c_haha), str(c_wow), str(c_sad), str(c_angry)
		comment_on = cmnt['timestamp']['verbose']
		c_id = cmnt['author']
		c_by = p_dict[c_id]['name']
		has_inner_comments = cmnt['recentreplytimestamp']
		if has_inner_comments:
		    comment_link = ''
		print str(comment_on)
		print str(c_by)
	print str(comment_count)

    def parse_like(self, response):
        sel = Selector(response)
        like = len(sel.xpath('//li[div[contains(text(), "Like")]]/div/ul/li'))
        love = len(sel.xpath('//li[div[contains(text(), "Love")]]/div/ul/li'))
        haha = len(sel.xpath('//li[div[contains(text(), "Haha")]]/div/ul/li'))
        wow = len(sel.xpath('//li[div[contains(text(), "Wow")]]/div/ul/li'))
        sad = len(sel.xpath('//li[div[contains(text(), "Sad")]]/div/ul/li'))
        angry = len(sel.xpath('//li[div[contains(text(), "Angry")]]/div/ul/li'))
        print str(like),str(love),str(haha), str(wow), str(sad), str(angry)
	
