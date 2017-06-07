from linkedin_logins import *
from linkedin_voyage_queries import *
from linkedin_voyager_utils import *

class Linkedinpremiumapivoyager(Voyagerapi):
	name = "linkedinapivoyager_browse"
	allowed_domains = ["linkedin.com"]
	start_urls = ('https://www.linkedin.com/uas/login?goback=&trk=hb_signin',)

	def __init__(self, *args, **kwargs):
		super(Linkedinpremiumapivoyager, self).__init__(*args, **kwargs)
                self.login = kwargs.get('login', 'ramanujan')
                self.con, self.cur = get_mysql_connection(DB_HOST, DB_NAME_REQ, '')
                #get_query_param = "select sk, url, meta_data from linkedin_crawl where crawl_status=0 limit 15"
		get_query_param = "select sk, url, meta_data from linkedin_crawl where crawl_status=0 and url like '%linkedin.com%' order by rand() limit 1"
		import pdb;pdb.set_trace()
                self.cur.execute(get_query_param)
                self.profiles_list = [i
                    for i in self.cur.fetchall()
                ]
                dispatcher.connect(self.spider_closed, signals.spider_closed)
                self.domain = domain_premium

	def parse(self, response):
                sel = Selector(response)
                logincsrf = ''.join(sel.xpath('//input[@name="loginCsrfParam"]/@value').extract())
                csrf_token = ''.join(sel.xpath('//input[@name="csrfToken"]/@value').extract())
                source_alias = ''.join(sel.xpath('//input[@name="sourceAlias"]/@value').extract())
                login_account = mails_dict[self.login]
                account_mail, account_password = login_account
                if account_mail and self.profiles_list:
                        return [FormRequest.from_response(response, formname = 'login_form',\
                        formdata={'session_key':account_mail,'session_password':account_password,'isJsEnabled':'','source_app':'','tryCount':'','clickedSuggestion':'','signin':'Sign In','session_redirect':'','trk':'hb_signin','loginCsrfParam':logincsrf,'fromEmail':'','csrfToken':csrf_token,'sourceAlias':source_alias},callback=self.parse_next, meta={'csrf_token':csrf_token, 'login_mail':account_mail})]

    	def spider_closed(self, spider):
		cv = requests.get('https://www.linkedin.com/logout/').text
		close_mysql_connection(self.con, self.cur)

	def parse_next(self, response):
                sel = Selector(response)
                for li in self.profiles_list:
                	meta_data = json.loads(li[2])
	                email_address = meta_data.get('email_address', '')
        	        sk, profile_url, m_data = li
                	meta_data = json.loads(m_data)
	                vals = (sk, profile_url, sk, profile_url)
        	        self.update_status(sk, 9, 0)
                	yield Request(profile_url, callback = self.parse_correct, meta = {
	                    "sk": sk,
        	            'email_address': email_address,
                	    'csrf_token': response.meta['csrf_token'],
			    'login_mail': response.meta.get('login_mail','')
	                })

	def parse_correct(self, response):
                sel = Selector(response)
                sk = response.meta['sk']
		login_mail = response.meta.get('login_mail','')
                cooki_list = response.request.headers.get('Cookie', [])
                li_at_cookie = ''.join(re.findall('li_at=(.*?); ', cooki_list))
                headers = {
                    'cookie': 'li_at=%s;JSESSIONID="%s"' % (li_at_cookie, response.meta['csrf_token']),
                    'x-requested-with': 'XMLHttpRequest',
                    'csrf-token': response.meta['csrf_token'],
                    'authority': 'www.linkedin.com',
                    'referer': 'https://www.linkedin.com/',
                }
                sk = response.meta.get('sk', '')
                profile_data = {}
                try:
                	profile_data = json.loads(''.join(sel.xpath('//code[contains(text(),"profile.ProfileView")]/text()').extract()))
                except:
			try:
                		profile_data = json.loads(sel.xpath('//code[contains(text(),"profile.ProfileView")]/text()').extract()[0])
			except:
				profile_data = {}

                meb = sel.xpath('//code[contains(text(),"PatentView")][contains(text(),"objectUrn")][contains(text(),"urn:li:member:")]').extract()
                keyword = 'com.linkedin.voyager.identity.profile.'
                data_json = profile_data.get('included', [])
                basic_data = filter(None, [i
                    if i['$type'] == "%s%s" % (keyword, 'Profile')
                    else ''
                    for i in data_json
                ])
                languages_data = filter(None, [i['name']
                    if i['$type'] == "%s%s" % (keyword, 'Language')
                    else ''
                    for i in data_json
                ])
                if languages_data:
                    languages_data = ', '.join(languages_data)
                else :
                    languages_data = ''
                connections_count = textify(re.findall('connectionsCount&quot;:(\d+),', response.body))
                followers_count = textify(re.findall('followersCount&quot;:(\d+),', response.body))

		linke_a, linkd_javatex, view_url_construction = {}, '' , ''
		try: linke_a = json.loads(sel.xpath('//code[contains(text(),"authToken")]/text()').extract()[0].replace('\\','').replace('\n','').strip()).get('included','')
		except: 
			try:
				cv = (sel.xpath('//code[contains(text(),"authToken")]/text()').extract()[0].replace('\\','').replace('\n','').replace(' "','').strip())
				linke_a = re.findall('included":(\[.*\])',cv)
				linke_a = json.loads(re.sub('pdfFileName=.*(").*&authType=name','',linke_a[0]))
			except: 
				linke_a = {}
		if linke_a:
			enum_l = [i for i,j in enumerate(linke_a) if 'authToken' in j.get('requestUrl','')]
			if enum_l:
				enumd = enum_l[0]
				linkd_javatex = linke_a[enumd].get('requestUrl','')
				linkedin_auth = ''.join(re.findall('authToken=(.*?)&',linke_a[enumd].get('requestUrl','')))
				cvv = textify(re.findall('\?id=(.*?)&',linkd_javatex))
				if cvv:
					view_url_construction = profile_view_url%(cvv,linkedin_auth)
				

                if basic_data:
                	basic_dat = basic_data[0]
	                entity_urn = basic_dat.get('entityUrn', '')
        	        for_entity = entity_urn.replace('urn:li:fs_profile:', '')
                	if entity_urn:
                		url_to = main_profile_api % for_entity
		                yield Request(url_to, headers = headers, callback = self.parse_voyage, meta = {
        	            'url_type': 'basic',
                	    'headers': headers,
	                    'main_url': url_to,
        	            'sk': sk,
                	    'languages_data': languages_data,
	                    'connections_count': connections_count,
        	            'followers_count': followers_count,
			    'login_mail': login_mail,
			    'view_url_construction': view_url_construction
        		        })
				self.update_status(sk, 10, '')
		else:
			self.update_status(sk, 6, '')
			track_item = self.get_track_item(sk, '', login_mail, '176.9.181.34', '6')
			yield track_item
			

	def get_meta_profile(self, basic_dat):
                first_name = basic_dat.get('firstName', '')
                entity_urn = basic_dat.get('entityUrn', '')
                headline = basic_dat.get('headline', '')
                industry_name = basic_dat.get('industryName', '')
                last_name = basic_dat.get('lastName', '')
                location = basic_dat.get('locationName', '')
                location_postal_code = basic_dat.get('location', {}).get('basicLocation', {}).get('postalCode', '')
                location_country_code = basic_dat.get('location', {}).get('basicLocation', {}).get('countryCode', '')
                version_tag = basic_dat.get('versionTag', '')
                summary = basic_dat.get('summary', '')
                address = basic_dat.get('address', '')
                background_image = basic_dat.get('backgroundImage', {}).get('image', {}).get('com.linkedin.voyager.common.MediaProcessorImage', {}).get('id', '')
                if background_image:
                        background_image = "%s%s" % ("https://media.licdn.com/media", background_image)
                maiden_name = basic_dat.get('maidenName', '')
                interests = basic_dat.get('interests', '')
                phonetic_last_name = basic_dat.get('phoneticLastName', '')
                phonetic_firt_name = basic_dat.get('phoneticFirstName', '')
                state = basic_dat.get('state', '')
                miniprofile = basic_dat.get('miniProfile', '')
                picture_info = basic_dat.get('pictureInfo', {}).get('masterImage', '')
                if picture_info:
                        picture_info = "%s%s" % ("https://media.licdn.com/media", picture_info)
                birthdate = basic_dat.get('birthDate', {})
                miniprofile = basic_dat.get('miniProfile', {})
                object_urn = miniprofile.get('objectUrn', '')
                object_urn = self.get_digit(object_urn)
                tracking_id = miniprofile.get('trackingId', '')
                public_identifier = miniprofile.get('publicIdentifier', '')
                return first_name, entity_urn, headline, industry_name, last_name, location, location_postal_code, location_country_code, version_tag, summary, address, background_image, maiden_name, interests, phonetic_last_name, phonetic_firt_name, state, miniprofile, picture_info, birthdate, object_urn, tracking_id, public_identifier

	def get_basic_item(self, sk, first_name, entity_urn, headline, industry_name, last_name, location, location_postal_code, location_country_code, version_tag, summary, address, background_image, maiden_name, interests, phonetic_last_name, phonetic_firt_name, state, miniprofile, picture_info, birthdate, object_urn, tracking_id, public_identifier, ref_url, languages_data, connections_count, followers_count, view_url_construction):
		linkedin_meta = Linkedinmeta()
		linkedin_meta['sk'] = normalize(str(object_urn))
		linkedin_meta['profile_url'] = normalize(ref_url)
		linkedin_meta['profileview_url'] = normalize(view_url_construction)
		linkedin_meta['name'] = normalize("%s%s%s"%(first_name,' ', last_name))
		linkedin_meta['first_name'] = normalize(first_name)
		linkedin_meta['last_name'] = normalize(last_name)
		linkedin_meta['member_id'] = normalize(str(object_urn))
		linkedin_meta['headline'] = normalize(headline)
		linkedin_meta['no_of_followers'] = normalize(followers_count)
		if public_identifier:
			linkedin_meta['profile_post_url'] = normalize("https://www.linkedin.com/today/author/%s?trk=prof-sm"%public_identifier)
		linkedin_meta['summary'] = normalize(summary.replace('<br>','').replace('</br>',''))
		linkedin_meta['number_of_connections'] = normalize(connections_count)
		linkedin_meta['industry'] = normalize(industry_name)
		linkedin_meta['location'] = normalize(location)
		linkedin_meta['languages'] = normalize(languages_data)
		linkedin_meta['emails'] = ''
		linkedin_meta['websites'] = ''
		linkedin_meta['addresses'] = normalize(address)
		linkedin_meta['message_handles'] = ''
		linkedin_meta['phone_numbers'] = ''
		linkedin_meta['birthday'] = normalize(str(birthdate.get('day','')))
		linkedin_meta['birth_year'] = normalize(str(birthdate.get('year','')))
		linkedin_meta['birth_month'] = normalize(str(birthdate.get('month','')))
		linkedin_meta['twitter_accounts'] = ''
		linkedin_meta['profile_image'] = normalize(picture_info)
		linkedin_meta['interests'] = ''
		linkedin_meta['location_postal_code'] = normalize(location_postal_code)
		linkedin_meta['location_country_code'] = normalize(location_country_code)
		linkedin_meta['background_image'] = normalize(background_image)
		return linkedin_meta


	def parse_voyage(self, response):
		data = json.loads(response.body)
		sk = response.meta['sk']
		headers = response.meta['headers']
		data_elements = data.get('elements', [])
		url_type = response.meta['url_type']
		main_url = response.meta['main_url']
		url_paging  = data.get('paging',[])
		login_mail = response.meta.get('login_mail','')
		languages_data = response.meta.get('languages_data','')
		main_member_id = response.meta.get('main_member_id','')
		connections_count = response.meta.get('connections_count','')
		followers_count = response.meta.get('followers_count','')
		view_url_construction = response.meta.get('view_url_construction','')
		if url_type == 'basic':
			first_name, entity_urn, headline, industry_name, last_name, location,\
			 location_postal_code, location_country_code, version_tag, summary,\
			 address, background_image, maiden_name, interests, phonetic_last_name,\
			 phonetic_firt_name, state, miniprofile, picture_info, birthdate, object_urn,\
			 tracking_id, public_identifier = self.get_meta_profile(data)
                        if '/in/' not in main_url:
                                main_url = "https://www.linkedin.com/in/%s/"%public_identifier
			if public_identifier or first_name:
				basic_main_data = self.get_basic_item(sk, first_name, entity_urn,
				 headline, industry_name, last_name, location, location_postal_code,
				 location_country_code, version_tag, summary, address, background_image,
				 maiden_name, interests, phonetic_last_name, phonetic_firt_name, state,
				 miniprofile, picture_info, birthdate, object_urn, tracking_id,
				 public_identifier, main_url, languages_data, connections_count, followers_count, view_url_construction)
				if basic_main_data:
					yield basic_main_data
					self.update_status(sk, 1, '')
					track_item = self.get_track_item(sk, str(object_urn), login_mail, '176.9.181.34', '1')
					yield track_item

			if public_identifier:
				for api in api_whole_list:
					api_url_public = api[0]%public_identifier
					yield Request(api_url_public, headers=headers, callback=self.parse_voyage, meta={'url_type':api[1], 'main_url':api_url_public, 'headers':headers, 'main_member_id':self.get_digit(object_urn),'sk':str(object_urn)})
		else:
			for dataloop in data_elements:
				data_retruned = self.type_of_item(dataloop, url_type, main_member_id, sk)
				if data_retruned:
					yield data_retruned

		if url_type != 'basic':
			if url_paging:
				count_data = url_paging.get('count','')
				start_data = url_paging.get('start','')
				total_data = url_paging.get('total','')
				if total_data > count_data+start_data:
					cons_part = ''
					if '?' not in main_url:
						cons_part = "?count=%s&start=%s"%(count_data, start_data+count_data)
					else:
						cons_part = "&count=%s&start=%s"%(count_data, start_data+count_data)
					retrun_url = "%s%s"%(main_url,cons_part)
					yield Request(retrun_url, headers=headers, callback=self.parse_voyage, meta={'url_type':url_type, 'main_url':main_url, 'headers':headers, 'sk':sk, 'main_member_id':main_member_id})
			
					
