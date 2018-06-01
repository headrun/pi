import scrapy
from generic_functions import *
from facebook_pages_queries import *
from Facebook.items import *
import urllib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Facebookpagesbrowse(scrapy.Spider):
	name = "facebookpages_browse"
	handle_httpstatus_list = [500]
	
	def __init__(self, name=None, **kwargs):
		super(Facebookpagesbrowse, self).__init__(name, **kwargs)
		self.con, self.cur = get_mysql_connection(DB_HOST, 'FACEBOOK', '')
		recs_pages = fetchmany(self.cur, get_query_param_fbp)
		self.urls = list(recs_pages)
                self.excel_file_name = 'facebook_pages_comments_%s.csv' % str(datetime.datetime.now().date())
                if os.path.isfile(self.excel_file_name):
                        os.system('rm %s'%self.excel_file_name)
                oupf = open(self.excel_file_name, 'ab+')
                self.todays_excel_file  = csv.writer(oupf)
                self.main_dict = {}
                self.inner_comment_dict = {}
                self.post_inner_comments = {}
                self.post_comment_reactions = {}
                dispatcher.connect(self.spider_closed, signals.spider_closed)
		self.excel_file_name = 'facebook_pages_comments_%s.csv' % str(datetime.datetime.now().date())
		if os.path.isfile(self.excel_file_name):
			os.system('rm %s'%self.excel_file_name)
		oupf = open(self.excel_file_name, 'ab+')
		self.todays_excel_file  = csv.writer(oupf)
		self.headers1 = ['page_url', 'page_name', 'page_id', 'post_id', 'post_shares_count', 'post_url', 'post_message', 'post_created_time', 'post_updated_time', 'post_picture', 'post_from_name', 'post_from_id', 'post_to_name', 'post_to_id', 'post_comments_total_count', 'post_reactions_total_count', 'post_like_count', 'post_love_count', 'post_wow_count', 'post_haha_count', 'post_sad_count', 'post_angry_count','comment_id', 'comment_from_id', 'comment_from_name', 'comment_message', 'comment_created_time', 'inner_comments_total_count', 'comment_reactions_total_count', 'comment_like_count', 'comment_love_count', 'comment_wow_count', 'comment_haha_count', 'comment_sad_count', 'comment_angry_count','inner_comment_id', 'inner_comment_from_id', 'inner_comment_from_name', 'inner_comment_message', 'inner_comment_created_time', 'innercomment_like_count', 'inner_comment_love_count', 'inner_comment_wow_count', 'inner_comment_haha_count', 'inner_comment_sad_count', 'inner_comment_angry_count', 'inner_comment_reactions_total_count']
		self.todays_excel_file.writerow(self.headers1)

        def spider_closed(self,spider):
		for page_id,dict_ in self.main_dict.iteritems():
			page_url = dict_.get('page_url','')
			page_name = dict_.get('page_name', '')
			page_id = dict_.get('page_id', '')
			posts = dict_.get('posts', {})
			if posts:
				for p_id, post_dict in posts.iteritems():
					cmnt_dict = post_dict['post_comments']
					if cmnt_dict:
						for c_id, c_dict in cmnt_dict.iteritems():
							inner_dict = c_dict['inner_comments']
							if inner_dict:
								for i_id, i_dict in inner_dict.iteritems():
									values = (page_url, page_name, page_id, post_dict.get('post_id', ''), post_dict.get('post_shares_count', ''), post_dict.get('post_url', ''), post_dict.get('post_message', ''), post_dict.get('post_created_time', ''), post_dict.get('post_updated_time', ''), post_dict.get('post_picture', ''), post_dict.get('post_from_name', ''), post_dict.get('post_from_id', ''), post_dict.get('post_to_name', ''), post_dict.get('post_to_id', ''), post_dict.get('post_comments_total_count', ''), post_dict.get('post_reactions_total_count', ''), post_dict.get('post_like_count', ''), post_dict.get('post_love_count', ''), post_dict.get('post_wow_count', ''), post_dict.get('post_haha_count', ''), post_dict.get('post_sad_count', ''), post_dict.get('post_angry_count', ''), c_dict.get('comment_id', ''), c_dict.get('comment_from_id', ''), c_dict.get('comment_from_name', ''), c_dict.get('comment_message', ''), c_dict.get('comment_created_time', ''), c_dict.get('inner_comments_total_count', ''), c_dict.get('comment_reactions_total_count', ''), c_dict.get('comment_like_count', ''), c_dict.get('comment_love_count', ''), c_dict.get('comment_wow_count', ''), c_dict.get('comment_haha_count', ''), c_dict.get('comment_sad_count', ''), c_dict.get('comment_angry_count', ''), i_dict.get('inner_comment_id', ''), i_dict.get('inner_comment_from_id', ''), i_dict.get('inner_comment_from_name', ''), i_dict.get('inner_comment_message', ''), i_dict.get('inner_comment_created_time', ''), i_dict.get('innercomment_like_count', ''), i_dict.get('inner_comment_love_count', ''), i_dict.get('inner_comment_wow_count', ''), i_dict.get('inner_comment_haha_count', ''), i_dict.get('inner_comment_sad_count', ''), i_dict.get('inner_comment_angry_count', ''), i_dict.get('inner_comment_reactions_total_count', ''))
									self.todays_excel_file.writerow(values)
							else:
								values = (page_url, page_name, page_id, post_dict.get('post_id', ''), post_dict.get('post_shares_count', ''), post_dict.get('post_url', ''), post_dict.get('post_message', ''), post_dict.get('post_created_time', ''), post_dict.get('post_updated_time', ''), post_dict.get('post_picture', ''), post_dict.get('post_from_name', ''), post_dict.get('post_from_id', ''), post_dict.get('post_to_name', ''), post_dict.get('post_to_id', ''), post_dict.get('post_comments_total_count', ''), post_dict.get('post_reactions_total_count', ''), post_dict.get('post_like_count', ''), post_dict.get('post_love_count', ''), post_dict.get('post_wow_count', ''), post_dict.get('post_haha_count', ''), post_dict.get('post_sad_count', ''), post_dict.get('post_angry_count', ''), c_dict.get('comment_id', ''), c_dict.get('comment_from_id', ''), c_dict.get('comment_from_name', ''), c_dict.get('comment_message', ''), c_dict.get('comment_created_time', ''), c_dict.get('inner_comments_total_count', ''), c_dict.get('comment_reactions_total_count', ''), c_dict.get('comment_like_count', ''), c_dict.get('comment_love_count', ''), c_dict.get('comment_wow_count', ''), c_dict.get('comment_haha_count', ''), c_dict.get('comment_sad_count', ''), c_dict.get('comment_angry_count', ''), '', '', '', '', '', '', '', '', '', '', '', '')
								self.todays_excel_file.writerow(values)
					else:
						values = (page_url, page_name, page_id, post_dict.get('post_id', ''), post_dict.get('post_shares_count', ''), post_dict.get('post_url', ''), post_dict.get('post_message', ''), post_dict.get('post_created_time', ''), post_dict.get('post_updated_time', ''), post_dict.get('post_picture', ''), post_dict.get('post_from_name', ''), post_dict.get('post_from_id', ''), post_dict.get('post_to_name', ''), post_dict.get('post_to_id', ''), post_dict.get('post_comments_total_count', ''), post_dict.get('post_reactions_total_count', ''), post_dict.get('post_like_count', ''), post_dict.get('post_love_count', ''), post_dict.get('post_wow_count', ''), post_dict.get('post_haha_count', ''), post_dict.get('post_sad_count', ''), post_dict.get('post_angry_count', ''), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '')
						self.todays_excel_file.writerow(values)				 
				
				
	def start_requests(self):
		for i in self.urls:
			page_id_url = '%s%s?access_token=%s' % (graph_api, i[1], user_access_token)
			execute_query(self.cur, update_query_fbp % ('9', i[0]))
			yield scrapy.Request(page_id_url, self.parse, meta = {'crawl_rec_data':i})

	def parse_pages_meta_item(self, page_sk, page_url, page_id, page_name):
		Fbpagesmeta_ = Fbpagesmeta()
	        Fbpagesmeta_['page_sk']     = normalize(page_sk)
        	Fbpagesmeta_['page_url']    = normalize(page_url)
	        Fbpagesmeta_['page_id']     = normalize(page_id)
        	Fbpagesmeta_['page_name']   = normalize(page_name)
		return Fbpagesmeta_


	def parse(self, response):
		tmp = json.loads(response.body)
		crawl_rec_data = response.meta['crawl_rec_data']
		execute_query(self.cur, update_query_fbp % ('1', crawl_rec_data[0]))
		page_name = tmp.get('name', '')
		page_id = tmp.get('id', '')
		return_pagemeta_item = self.parse_pages_meta_item(crawl_rec_data[0], crawl_rec_data[1], page_id, page_name)
		if return_pagemeta_item:
			yield return_pagemeta_item
			self.main_dict.update({page_id:dict(return_pagemeta_item)})
		if page_id:
			graph_api_url = "%s%s%s" % (graph_api, page_id, graph_api1)
			yield scrapy.Request(graph_api_url, callback= self.parse_next,
		meta = {'crawl_rec_data':response.meta.get('crawl_rec_data',{}), 'page_id' : page_id, 'page_name':page_name, "counter":0, "parsed":''})

	def alert_mail(self, url, message):
		sender_mail = 'facebookdummyfb01@gmail.com'
		receivers_mail_list = ['alekhya@headrun.com']
		sender, receivers  = sender_mail, ','.join(receivers_mail_list)
		msg = MIMEMultipart('alternative')
                msg['Subject'] = 'Alert mail for facebook pages - 500 status for navigation'
                mas = '<h3> Got 500 status for API url : %s </h3>' % url
		mas += '<p>Response body : %s </p>' % normalize(message)
		msg['From'] = sender
		msg['To'] = receivers
		tem = MIMEText(''.join(mas), 'html')
		msg.attach(tem)
		s = smtplib.SMTP('smtp.gmail.com:587')
		s.ehlo()
		s.starttls()
		s.login(sender_mail, '01123123')
		s.sendmail(sender, receivers_mail_list, msg.as_string())
		s.quit()

	def parse_next(self, response):
		if response.status != 200:
			if not response.meta.get('parsed', ''):
				yield scrapy.Request(response.url, callback= self.parse_next,
        	        meta = {'crawl_rec_data':response.meta.get('crawl_rec_data',{}), 'page_id' : response.meta.get('page_id', ''), 'page_name':response.meta.get('page_name',''), "counter":0, "parsed":'yes'}, dont_filter = True)
			else:
				self.alert_mail(response.url, response.body)
		tmp = {}
		try:
			tmp = json.loads(response.body)
		except:
			tmp = {}
		if tmp:
			crawl_rec_data = response.meta['crawl_rec_data']
			total_page_rec = tmp.get('data', [])
			next_page = tmp.get('paging',{}).get('next', '')
			counter = response.meta.get('counter','')
			counter += 1
			if next_page:
				yield scrapy.Request(urllib.unquote(next_page), callback=self.parse_next, meta = {'crawl_rec_data':response.meta.get('crawl_rec_data',{}), 'page_id' : response.meta.get('page_id',''), 'page_name':response.meta.get('page_name', ''), 'counter':counter, "parsed":''}, dont_filter=True, errback=self.parse_next)
                        comment_id_ = 0
			self.post_dict = {}
			for page_rec in total_page_rec:
                                vals = []
				post_shares_count = str(page_rec.get('shares', {}).get('count', ''))
				post_url = page_rec.get('permalink_url', '')
				post_id = page_rec.get('id', '')
				if '/posts/' not in post_url:
					post_url = '%s%s%s' % (response.meta.get('crawl_rec_data')[1], 
					'/posts/', post_id.split('_')[-1])
				post_description = page_rec.get('message', '').replace('\n', '')
				if not post_description:
					post_description = page_rec.get('description', '').replace('\n', '')
				reactions_key = page_rec.get('reactions', {})
				post_link = page_rec.get('link', '')
				post_created_time = page_rec.get('created_time', '').replace('T', ' ')
				post_updated_time = page_rec.get('updated_time', '').replace('T', ' ')
				post_picture = page_rec.get('full_picture', '')
				post_from = page_rec.get('from', {})
				post_from_name = post_from.get('name', '')
				post_from_id = post_from.get('id', '')
				post_to = page_rec.get('to', {})
				post_to_data = post_to.get('data', [])
				if post_to_data:
					post_to_data = post_to_data[0]
				else:
					post_to_data = {}
				post_to_name = post_to_data.get('name', '')
				post_to_id = post_to_data.get('id', '')
				post_comments_key = page_rec.get('comments', {})
				post_comments_total_count = str(post_comments_key.get('summary', '').get('total_count', ''))
				post_reactions_total_count = str(reactions_key.get('summary', {}).get('total_count', ''))
				post_reactions_like_count = self.parse_like(page_rec, 'like')
				post_reactions_love_count = self.parse_like(page_rec, 'love')
				post_reactions_wow_count = self.parse_like(page_rec, 'wow')
				post_reactions_haha_count = self.parse_like(page_rec, 'haha')
				post_reactions_sad_count = self.parse_like(page_rec, 'sad')
				post_reactions_angry_count = self.parse_like(page_rec, 'angry')
				reactions_data = reactions_key.get('data', {})
				post_comments_data = post_comments_key.get('data', [])
				post_sk = md5("%s%s%s" % (crawl_rec_data[0], response.meta['page_id'], post_id))
				post_comment_basic_list = [crawl_rec_data[0], response.meta['page_id'], post_sk, post_id]	
				fbpost_data_item = self.fbppost(crawl_rec_data[0], response.meta['page_id'], post_sk, post_id, post_shares_count, post_url, post_description, post_created_time, post_updated_time, post_picture, post_from_name, post_from_id, post_to_name, post_to_id, post_comments_total_count, post_reactions_total_count, post_reactions_like_count, post_reactions_love_count, post_reactions_wow_count, post_reactions_haha_count, post_reactions_sad_count, post_reactions_angry_count, response.url)
				post_comments_next_page = post_comments_key.get('paging', {}).get('next', '')
				if post_comments_next_page:
					yield Request(post_comments_next_page, callback=self.parse_next_page_comments, meta = {'post_comment_basic_list':post_comment_basic_list})
				comment_dict = {}
				for post_com_data in post_comments_data:
					return_data = self.parse_comments(post_com_data, 'main_comment', post_comment_basic_list, [])
					if return_data:
						if return_data[4]:
							yield Request(return_data[4], callback=self.parse_next_ic, meta = {"post_comment_basic_list":post_comment_basic_list, 'comment_sk':return_data[0].get('comment_sk', ''), 'comment_id':return_data[0].get('comment_id', '')})
						yield return_data[0]
                                                comment_id = dict(return_data[0]).get('comment_id','')
                                                inner_comment = 0
						inner_comment_dict = {}
						for pcom_inner_cmd in return_data[1]:
							return_data1 = self.parse_comments(pcom_inner_cmd, 'inner_comment', post_comment_basic_list, [return_data[0].get('comment_sk', ''), return_data[0].get('comment_id', '')])
							if return_data1:
								yield return_data1[0]
                                                               	inner_comment_dict.update({dict(return_data1[0])['inner_comment_id']:dict(return_data1[0])})
                                                                post_inner_comments = 0
								for pincomm_rea_data in return_data1[1]:
									return_data2i = self.parse_reactions(pincomm_rea_data, 'post_inner_comment_reactions', post_comment_basic_list, [return_data[0].get('comment_sk', ''), return_data[0].get('comment_id', '')], [return_data1[0].get('inner_comment_sk', ''), return_data1[0].get('inner_comment_id', '')])
                                                     
									if return_data2i:
										yield return_data2i
                                                                                post_inner_comments_ = return_data2i.values()
						cmt_dict = dict(return_data[0])                
						cmt_dict.update({'inner_comments':inner_comment_dict})
						comment_dict.update({comment_id:cmt_dict})
                                                post_comment_reactions = 0
						for pcomments_rea_data in return_data[3]:
							return_data2 = self.parse_reactions(pcomments_rea_data, 'post_comment_reactions', post_comment_basic_list, [return_data[0].get('comment_sk', ''), return_data[0].get('comment_id', '')], [])
							if return_data2:
								yield return_data2
                                                                post_com_reactions = return_data2.values()
                                if fbpost_data_item:
                                        yield fbpost_data_item
					post_id = dict(fbpost_data_item)['post_id']
					dump_dict = dict(fbpost_data_item)
					dump_dict.update({'post_comments':comment_dict})
					self.post_dict.update({post_id:dump_dict})
			        post_reac = 0				
				for rea_da in reactions_data:
					rea_return_data = self.parse_reactions(rea_da, 'post_reactions', post_comment_basic_list, [], [])
					if rea_return_data:
						yield rea_return_data
                                                v5 = rea_return_data.values()
			if self.post_dict:
				if 'posts' in self.main_dict[response.meta['page_id']].keys():
					p_dict = self.main_dict[response.meta['page_id']]['posts']
					self.post_dict.update(p_dict)
					self.main_dict[response.meta['page_id']].update({'posts':self.post_dict})
				else:
                        		self.main_dict[response.meta['page_id']].update({'posts':self.post_dict})

	def parse_next_ic(self, response):
		post_comment_basic_list = response.meta.get('post_comment_basic_list', '')
		comment_id = response.meta.get('comment_id', '')
		comment_sk = response.meta.get('comment_sk', '')
                tmp = {}
                try:
                        tmp = json.loads(response.body)
                except:
                        tmp = {}
                if tmp: 
                        net_p = tmp.get('paging',{}).get('next','')
                        if net_p:
                                yield Request(net_p, callback=self.parse_next_ic, meta = {'post_comment_basic_list':post_comment_basic_list, 'comment_sk':comment_sk, 'comment_id':comment_id})
			comments_data = tmp.get('data',[])
			for post_com_data in comments_data:
				return_data1 = self.parse_comments(post_com_data, 'inner_comment', post_comment_basic_list, [comment_sk, comment_id])
				if return_data1:
                                        vals = return_data1.values()
					yield return_data1[0]

		
	def parse_next_page_comments(self, response):
		post_comment_basic_list = response.meta.get('post_comment_basic_list',[])
		tmp = {}
		try:
			tmp = json.loads(response.body)
		except:
			tmp = {}
		if tmp:
			net_p = tmp.get('paging',{}).get('next','')
			if net_p:
				yield Request(net_p, callback=self.parse_next_page_comments, meta = {'post_comment_basic_list':post_comment_basic_list})
			comments_data = tmp.get('data',[])
			for post_com_data in comments_data:
				return_data = self.parse_comments(post_com_data, 'main_comment', post_comment_basic_list, [])
				if return_data:
                                	if return_data[4]:
                                        	yield Request(return_data[4], callback=self.parse_next_ic, meta = {"post_comment_basic_list":post_comment_basic_list, 'comment_sk':return_data[0].get('comment_sk', ''), 'comment_id':return_data[0].get('comment_id', '')})
					yield return_data[0]
					for pcom_inner_cmd in return_data[1]:
						return_data1 = self.parse_comments(pcom_inner_cmd, 'inner_comment', post_comment_basic_list, [return_data[0].get('comment_sk', ''), return_data[0].get('comment_id', '')])
						if return_data1:
							yield return_data1[0]
							for pincomm_rea_data in return_data1[1]:
								return_data2i = self.parse_reactions(pincomm_rea_data, 'post_inner_comment_reactions', post_comment_basic_list, [return_data[0].get('comment_sk', ''), return_data[0].get('comment_id', '')], [return_data1[0].get('inner_comment_sk', ''), return_data1[0].get('inner_comment_id', '')])
								if return_data2i:
									yield return_data2i
					for pcomments_rea_data in return_data[3]:
						return_data2 = self.parse_reactions(pcomments_rea_data, 'post_comment_reactions', post_comment_basic_list, [return_data[0].get('comment_sk', ''), return_data[0].get('comment_id', '')], [])
						if return_data2:
							yield return_data2

				
				

	def parse_fbpostreactions(self, po_tpe, sk1, sk2, sk3, sk4, sk5, sk6, sk7, sk8, rea_da_id, rea_da_name, rea_da_type):
		Fbpagespostreactions_ = Fbpagespostreactions()
		
		if po_tpe == 'post_inner_comment_reactions':
			Fbpagespostreactions_ = Fbpagepostinnercommnetreac()
			Fbpagespostreactions_['comment_sk'] = normalize(sk5)
			Fbpagespostreactions_['comment_id'] = normalize(sk6)
			Fbpagespostreactions_['inner_comment_sk'] = normalize(sk7)
			Fbpagespostreactions_['inner_comment_id'] = normalize(sk8)
		elif po_tpe == 'post_comment_reactions':
			Fbpagespostreactions_ = Fbpagepostcommentreac()
			Fbpagespostreactions_['comment_sk'] = normalize(sk5)
			Fbpagespostreactions_['comment_id'] = normalize(sk6)
			
		Fbpagespostreactions_['reaction_sk']     = normalize(md5("%s%s%s%s%s%s%s%s%s%s" % (sk1, sk2, sk3, sk4,sk5, sk6, sk7, sk8, rea_da_id, rea_da_type)))
		Fbpagespostreactions_['page_sk']         = normalize(sk1)
		Fbpagespostreactions_['page_id']         = normalize(sk2)
		Fbpagespostreactions_['post_sk']         = normalize(sk3)
		Fbpagespostreactions_['post_id']         = normalize(sk4)
		Fbpagespostreactions_['member_id']       = normalize(rea_da_id)
		Fbpagespostreactions_['member_name']     = normalize(rea_da_name)
		Fbpagespostreactions_['reaction_type']   = normalize(rea_da_type)
		return Fbpagespostreactions_



	def parse_reactions(self, rea_da, type_of_reaction, post_comment_basic_list, typ1, typ2):
		rea_da_id = rea_da.get('id', '')
		rea_da_name = rea_da.get('name', '')
		rea_da_type = rea_da.get('type', '')
		sk1, sk2, sk3, sk4 = post_comment_basic_list
		fbpostreactions = ''
		if type_of_reaction == 'post_reactions':
			fbpostreactions = self.parse_fbpostreactions('post_reactions', sk1, sk2, sk3, sk4, '', '','', '', rea_da_id, rea_da_name, rea_da_type)
		elif type_of_reaction == 'post_comment_reactions':
			sk5, sk6 = typ1
			fbpostreactions = self.parse_fbpostreactions('post_comment_reactions',sk1, sk2, sk3, sk4, sk5, sk6,'','', rea_da_id, rea_da_name, rea_da_type)
		else:
			sk5, sk6 = typ1
			sk7, sk8 = typ2
			fbpostreactions = self.parse_fbpostreactions('post_inner_comment_reactions', sk1, sk2, sk3, sk4, sk5, sk6, sk7, sk8, rea_da_id, rea_da_name, rea_da_type)
		return fbpostreactions

	def parse_like(self, page_rec, reaction_type):
		return str(page_rec.get(reaction_type, {}).get('summary', {}).get('total_count', ''))

	def parse_comments(self, p_comments, comment_type_mainorinner, post_comment_basic_list, another_basic):
		sk1, sk2, sk3, sk4 = post_comment_basic_list
		pcomment_total_reactions_key = p_comments.get('reactions', {})
		pcomment_total_reactions_count = str(pcomment_total_reactions_key.get('summary', {}).get('total_count', ''))
		pcomment_reactions_data = pcomment_total_reactions_key.get('data', [])
		pcomment_id = p_comments.get('id', '')
		pcomment_reac_like_count = self.parse_like(p_comments, 'like')
		pcomment_reac_love_count = self.parse_like(p_comments, 'love')
		pcomment_reac_wow_count = self.parse_like(p_comments, 'wow')
		pcomment_reac_haha_count = self.parse_like(p_comments, 'haha')
		pcomment_reac_sad_count = self.parse_like(p_comments, 'sad')
		pcomment_react_angry_count = self.parse_like(p_comments, 'angry')
		pcomment_from = p_comments.get('from', {})
		pcomment_from_name = pcomment_from.get('name', '')
		pcomment_from_id = str(pcomment_from.get('id', ''))
		pcomment_message = p_comments.get('message', '')
		pcomment_created_time = p_comments.get('created_time', '').replace('T', ' ')
		if comment_type_mainorinner == 'main_comment':
			pcommnent_sk = md5("%s%s%s%s%s" % (sk1, sk2, sk3, sk4, pcomment_id))
			p_comment_inner_comment = p_comments.get('comments', {})
			p_comment_inner_comment_next_link = p_comments.get('comments', {}).get('paging', {}).get('next', '')
			pcomment_total_inner_comments_count = str(p_comment_inner_comment.get('summary', {}).get('total_count', ''))
			pcomment_inner_comments_data = p_comment_inner_comment.get('data', [])
			fbpostcomment = self.fbpostcomment(sk1, sk2, sk3, sk4, pcommnent_sk, pcomment_id, pcomment_from_id, pcomment_from_name, pcomment_message, pcomment_created_time, pcomment_total_inner_comments_count, pcomment_total_reactions_count, pcomment_reac_like_count, pcomment_reac_love_count, pcomment_reac_wow_count, pcomment_reac_haha_count, pcomment_reac_sad_count, pcomment_react_angry_count)
			return fbpostcomment, pcomment_inner_comments_data, pcomment_total_inner_comments_count, pcomment_reactions_data, p_comment_inner_comment_next_link
		else:
			sk5, sk6 = another_basic
			pinner_commentsk = md5("%s%s%s%s%s%s%s" % (sk1, sk2, sk3, sk4, sk5, sk6, pcomment_id))
			fbpostinnercomment = self.fbpostinnercomment(sk1, sk2, sk3, sk4, sk5, sk6, pinner_commentsk, pcomment_id, pcomment_from_id, pcomment_from_name, pcomment_message, pcomment_created_time, pcomment_reac_like_count, pcomment_reac_love_count, pcomment_reac_wow_count, pcomment_reac_haha_count, pcomment_reac_sad_count, pcomment_react_angry_count, pcomment_total_reactions_count)	
			return fbpostinnercomment, pcomment_reactions_data

	def fbpostinnercomment(self, sk1, sk2, sk3, sk4, sk5, sk6, pinner_commentsk, pcomment_id, pcomment_from_id, pcomment_from_name, pcomment_message, pcomment_created_time, pcomment_reac_like_count, pcomment_reac_love_count, pcomment_reac_wow_count, pcomment_reac_haha_count, pcomment_reac_sad_count, pcomment_react_angry_count, pcomment_total_reactions_count):
		Fbpagespostinnercomment_ = Fbpagespostinnercomment()
		Fbpagespostinnercomment_['page_sk']                         = normalize(sk1)
		Fbpagespostinnercomment_['page_id']                         = normalize(sk2)
		Fbpagespostinnercomment_['post_sk']                         = normalize(sk3)
		Fbpagespostinnercomment_['post_id']                         = normalize(sk4)
		Fbpagespostinnercomment_['comment_sk']                      = normalize(sk5)
		Fbpagespostinnercomment_['comment_id']                      = normalize(sk6)
		Fbpagespostinnercomment_['inner_comment_sk']                = normalize(pinner_commentsk)
		Fbpagespostinnercomment_['inner_comment_id']                = normalize(pcomment_id)
		Fbpagespostinnercomment_['inner_comment_from_id']           = normalize(pcomment_from_id)
		Fbpagespostinnercomment_['inner_comment_from_name']         = normalize(pcomment_from_name)
		Fbpagespostinnercomment_['inner_comment_message']           = normalize(pcomment_message)
		Fbpagespostinnercomment_['inner_comment_created_time']      = normalize(pcomment_created_time)
		Fbpagespostinnercomment_['innercomment_like_count']         = normalize(pcomment_reac_like_count)
		Fbpagespostinnercomment_['inner_comment_love_count']        = normalize(pcomment_reac_love_count)
		Fbpagespostinnercomment_['inner_comment_wow_count']         = normalize(pcomment_reac_wow_count)
		Fbpagespostinnercomment_['inner_comment_haha_count']        = normalize(pcomment_reac_haha_count)
		Fbpagespostinnercomment_['inner_comment_sad_count']         = normalize(pcomment_reac_sad_count)
		Fbpagespostinnercomment_['inner_comment_angry_count']       = normalize(pcomment_react_angry_count)
		Fbpagespostinnercomment_['inner_comment_reactions_total_count'] = normalize(pcomment_total_reactions_count)
		return Fbpagespostinnercomment_


	def fbpostcomment(self, sk1, sk2, sk3, sk4, pcomment_sk, pcomment_id, pcomment_from_id, pcomment_from_name, pcomment_message, pcomment_created_time, pcomment_total_inner_comments_count, pcomment_total_reactions_count, pcomment_reac_like_count, pcomment_reac_love_count, pcomment_reac_wow_count, pcomment_reac_haha_count, pcomment_reac_sad_count, pcomment_react_angry_count):
		Fbpagespostcomment_ = Fbpagespostcomment()
		Fbpagespostcomment_['page_sk']                         = normalize(sk1)
		Fbpagespostcomment_['page_id']                         = normalize(sk2)
		Fbpagespostcomment_['post_sk']                         = normalize(sk3)
		Fbpagespostcomment_['post_id']                         = normalize(sk4)
		Fbpagespostcomment_['comment_sk']                      = normalize(pcomment_sk)
		Fbpagespostcomment_['comment_id']                      = normalize(pcomment_id)
		Fbpagespostcomment_['comment_from_id']                 = normalize(pcomment_from_id)
		Fbpagespostcomment_['comment_from_name']               = normalize(pcomment_from_name)
		Fbpagespostcomment_['comment_message']                 = normalize(pcomment_message)
		Fbpagespostcomment_['comment_created_time']            = normalize(pcomment_created_time)
		Fbpagespostcomment_['inner_comments_total_count']      = normalize(pcomment_total_inner_comments_count)
		Fbpagespostcomment_['comment_reactions_total_count'] = normalize(pcomment_total_reactions_count)
		Fbpagespostcomment_['comment_like_count']      = normalize(pcomment_reac_like_count)
		Fbpagespostcomment_['comment_love_count']      = normalize(pcomment_reac_love_count)
		Fbpagespostcomment_['comment_wow_count']       = normalize(pcomment_reac_wow_count)
		Fbpagespostcomment_['comment_haha_count']      = normalize(pcomment_reac_haha_count)
		Fbpagespostcomment_['comment_sad_count']       = normalize(pcomment_reac_sad_count)
		Fbpagespostcomment_['comment_angry_count']     = normalize(pcomment_react_angry_count)
		return Fbpagespostcomment_


	def fbppost(self, page_sk, page_id, post_sk, post_id, post_shares_count, post_url, post_description, post_created_time, post_updated_time, post_picture, post_from_name, post_from_id, post_to_name, post_to_id, post_comments_total_count, post_reactions_total_count, post_reactions_like_count, post_reactions_love_count, post_reactions_wow_count, post_reactions_haha_count, post_reactions_sad_count, post_reactions_angry_count, post_json_url):
		Fbpagespost_ = Fbpagespost()
	        Fbpagespost_['page_sk']                 = normalize(page_sk)
		Fbpagespost_['page_id']                 = normalize(page_id)
		Fbpagespost_['post_sk']                 = normalize(post_sk)
		Fbpagespost_['post_id']                 = normalize(post_id)
		Fbpagespost_['post_shares_count']       = normalize(post_shares_count)
		Fbpagespost_['post_url']                = normalize(post_url)
		Fbpagespost_['post_message']            = normalize(post_description)
		Fbpagespost_['post_created_time']       = normalize(post_created_time)
		Fbpagespost_['post_updated_time']       = normalize(post_updated_time)
		Fbpagespost_['post_picture']            = normalize(post_picture)
		Fbpagespost_['post_from_name']          = normalize(post_from_name)
		Fbpagespost_['post_from_id']            = normalize(post_from_id)
		Fbpagespost_['post_to_name']            = normalize(post_to_name)
		Fbpagespost_['post_to_id']              = normalize(post_to_id)
		Fbpagespost_['post_comments_total_count']       = normalize(post_comments_total_count)
		Fbpagespost_['post_reactions_total_count']      = normalize(post_reactions_total_count)
		Fbpagespost_['post_like_count']         = normalize(post_reactions_like_count)
		Fbpagespost_['post_love_count']         = normalize(post_reactions_love_count)
		Fbpagespost_['post_wow_count']          = normalize(post_reactions_wow_count)
		Fbpagespost_['post_haha_count']         = normalize(post_reactions_haha_count)
		Fbpagespost_['post_sad_count']          = normalize(post_reactions_sad_count)
		Fbpagespost_['post_angry_count']        = normalize(post_reactions_angry_count)
		Fbpagespost_['post_json_url']        = normalize(post_json_url)
                values = [normalize(post_description)]
		return Fbpagespost_
