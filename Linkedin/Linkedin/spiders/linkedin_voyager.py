from linkedin_queries import *
from Linkedin.items import *
from linkedin_logins import *
from linkedin_functions import *

class Linkedinpremiumvoyager(scrapy.Spider):
	name = "linkedinvoyager_browse"
	allowed_domains = ["linkedin.com"]
	start_urls = ('https://www.linkedin.com/uas/login?goback=&trk=hb_signin',)

	def __init__(self, *args, **kwargs):
		super(Linkedinpremiumvoyager, self).__init__(*args, **kwargs)
		self.login = kwargs.get('login', 'ramanujan')
		self.con, self.cur = get_mysql_connection(DB_HOST, REQ_DB_NAME, '')
		get_query_param = "select sk, url, meta_data from linkedin_crawl where crawl_status=0 limit 15"
		self.cur.execute(get_query_param)
		self.profiles_list = [i for i in self.cur.fetchall()]
		#self.profiles_list = [('chandna53', 'https://www.linkedin.com/in/aravindrajanm/', '{}')]
		#self.profiles_list = [('chihara','https://www.linkedin.com/in/masaki-ken-chihara-32b488','{}')]
		self.profiles_list = [('Tathagat_Varma','https://www.linkedin.com/in/tathagat/','{}')]
		#self.profiles_list = [('chandna53', 'https://www.linkedin.com/profile/view?id=AAEAAAHnjg4BtEvirnqz9c8yFBK3_k8065JDH1g&authType=name&authToken=Iym5','{}')]
		#https://www.linkedin.com/in/mukhsonrofi/
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
                    	formdata={'session_key':account_mail,'session_password':account_password,'isJsEnabled':'','source_app':'','tryCount':'','clickedSuggestion':'','signin':'Sign In','session_redirect':'','trk':'hb_signin','loginCsrfParam':logincsrf,'fromEmail':'','csrfToken':csrf_token,'sourceAlias':source_alias},callback=self.parse_next, meta={'csrf_token':csrf_token})]

    	def spider_closed(self, spider):
		cv = requests.get('https://www.linkedin.com/logout/').text

	def parse_next(self, response):
		sel = Selector(response)
		for li in self.profiles_list:
			meta_data = json.loads(li[2])
			email_address = meta_data.get('email_address','')
			sk, profile_url, m_data = li
			meta_data = json.loads(m_data)
			vals = (sk, profile_url, sk, profile_url)
			self.cur.execute(update_get_params%(9,sk))
			yield Request(profile_url, callback=self.parse_correct, meta={"sk":sk, 'email_address':email_address, 'csrf_token':response.meta['csrf_token']})

	def parse_correct(self, response):
		sel = Selector(response)
                cooki_list = response.request.headers.get('Cookie',[])
                li_at_cookie = ''.join(re.findall('li_at=(.*?); ',cooki_list))
                headers = {
                    'cookie': 'li_at=%s;JSESSIONID="%s"'%(li_at_cookie, response.meta['csrf_token']) ,
                    'x-requested-with': 'XMLHttpRequest',
                    'csrf-token': response.meta['csrf_token'],
                    'authority': 'www.linkedin.com',
                    'referer': 'https://www.linkedin.com/',
                }
		sk = response.meta.get('sk','')
		profile_data = json.loads(''.join(sel.xpath('//code[contains(text(),"profile.ProfileView")]/text()').extract()))
		meb = sel.xpath('//code[contains(text(),"PatentView")][contains(text(),"objectUrn")][contains(text(),"urn:li:member:")]').extract()
		keyword = 'com.linkedin.voyager.identity.profile.'
		data_json = profile_data.get('included',[])
		basic_data = filter(None, [i if i['$type'] == "%s%s"%(keyword,'Profile') else ''for i in data_json])
		skills_data = filter(None, [i if i['$type'] == "%s%s"%(keyword,'Skill') else ''for i in data_json])
		certifi_data = filter(None, [i if i['$type'] == "%s%s"%(keyword,'Certification') else ''for i in data_json])
		contributors_data = filter(None, [i if i['$type'] == "%s%s"%(keyword,'Contributor') else ''for i in data_json])
		honors_data = filter(None, [i if i['$type'] == "%s%s"%(keyword,'Honor') else '' for i in data_json])
		picture_data = filter(None, [i if i['$type'] == "%s%s"%(keyword,'Picture') else ''for i in data_json])
		experiences_data = filter(None, [i if i['$type'] == "%s%s"%(keyword,'Position') else ''for i in data_json])
		volunteercause_data = filter(None, [i if i['$type'] == "%s%s"%(keyword,'VolunteerCause') else ''for i in data_json])
		educations_data = filter(None, [i if i['$type'] == "%s%s"%(keyword,'Education') else ''for i in data_json])

		if basic_data:
			basic_dat = basic_data[0]
			entity_urn = basic_dat.get('entityUrn','')
			for_entity = entity_urn.replace('urn:li:fs_profile:','')
			if entity_urn:
				url_to = 'https://www.linkedin.com/voyager/api/identity/profiles/%s'%for_entity
        	        	yield Request(url_to, headers=headers, callback=self.parse_voyage, meta={'url_type':'basic', 'headers':headers, 'main_url':url_to})
		if volunteercause_data:
			volunteercause_dat = self.get_type_data(volunteercause_data, 'vcause')
		if experiences_data:
			experiences_dat = self.get_type_data(experiences_data,'experiences')
		if honors_data:
			honors_dat = self.get_type_data(honors_data,'honors')
		if educations_data:
			educations_dat = self.get_type_data(educations_data, 'educations')
		if picture_data:
			picture_dat = picture_data[0].get('masterImage','')#u'/AAEAAQAAAAAAAAubAAAAJDhiZWYxZjhlLWEzMGQtNDA1Yi05YjQ4LTZlN2M3NDM1MzI1Yg.jpg'
			if picture_dat:
				picture_dat = 'https://media.licdn.com/mpr/mpr/shrinknp_400_400/%s'%(picture_dat)

		if skills_data:
			skill_dat = self.get_type_data(skills_data,'skill')
			for skil in skill_dat:
				skil_name, skill_entityurn = skil

		if certifi_data:
			certifications_dat = self.get_cer_data(certifi_data)
			for cert in certifications_dat:
				cerrtification_name, certifaction_entity_urn, cer_full_name, cer_time_period_fs, certifcaio_url = cert
		if contributors_data:
			values = self.get_type_data(contributors_data,'contributors')
			
		"""params = {
		    'includeHiddenEndorsers':'true',
		    'count':'50',
		}
		cooki_list = response.request.headers.get('Cookie',[])
		li_at_cookie = ''.join(re.findall('li_at=(.*?); ',cooki_list))
		headers = {
		    'cookie': 'li_at=%s;JSESSIONID="%s"'%(li_at_cookie, response.meta['csrf_token']) ,
		    'x-requested-with': 'XMLHttpRequest',
		    'csrf-token': response.meta['csrf_token'],
		    'authority': 'www.linkedin.com',
		    'referer': 'https://www.linkedin.com/',
		}
		params_new =  (
		   ('includeHiddenEndorsers', 'true'),
		    ('count', '50'),
		)
		url_to = 'https://www.linkedin.com/voyager/api/identity/profiles/aravindrajanm/profileContactInfo'
		yield Request(url_to, headers=headers, callback=self.parse_voyage)"""


	def get_meta_profile(self, basic_dat):
		first_name = basic_dat.get('firstName','')
		entity_urn = basic_dat.get('entityUrn','')#urn:li:fs_profile:ACoAAAA3LYwBc6wnTI5z--QGOwRXb9Go6py9TbA
		headline = basic_dat.get('headline','')
		industry_name = basic_dat.get('industryName','')
		last_name = basic_dat.get('lastName','')
		location = basic_dat.get('locationName','')
		location_postal_code = basic_dat.get('location',{}).get('basicLocation',{}).get('postalCode','')
		location_country_code = basic_dat.get('location',{}).get('basicLocation',{}).get('countryCode','')
		version_tag = basic_dat.get('versionTag','')#birthDate
		summary = basic_dat.get('summary','')
		address = basic_dat.get('address','')
		background_image = basic_dat.get('backgroundImage',{}).get('image',{}).get('com.linkedin.voyager.common.MediaProcessorImage',{}).get('id','')#need to check for one url#urn:li:fs_profile:ACoAAAA3LYwBc6wnTI5z--QGOwRXb9Go6py9TbA,backgroundImage#fromapi #/AAEAAQAAAAAAAAyPAAAAJGIyYjI0ZmYzLWJhMWMtNGI3Ni1iMmUwLTQyYjMwNTg4YjE0Yw.jpg
		maiden_name = basic_dat.get('maidenName','')
		interests = basic_dat.get('interests','')
		phonetic_last_name = basic_dat.get('phoneticLastName','')
		phonetic_firt_name = basic_dat.get('phoneticFirstName','')
		state = basic_dat.get('state','')
		miniprofile = basic_dat.get('miniProfile','')#urn:li:fs_miniProfile:ACoAAAA3LYwBc6wnTI5z--QGOwRXb9Go6py9TbA
		picture_info = basic_dat.get('pictureInfo',{}).get('masterImage','')#urn:li:fs_profile:ACoAAAA3LYwBc6wnTI5z--QGOwRXb9Go6py9TbA,pictureInfo
		birthdate = basic_dat.get('birthDate','')#urn:li:fs_profile:ACoAAAA3LYwBc6wnTI5z--QGOwRXb9Go6py9TbA,birthDate#fromapi {u'day': 30, u'month': 8}
		miniprofile = basic_dat.get('miniProfile',{})
		object_urn = miniprofile.get('objectUrn','')#urn:li:member:3616140
		tracking_id = miniprofile.get('trackingId','')#u'VY1FJS/EQs6N2oDsGKF3dQ=='
		public_identifier = miniprofile.get('publicIdentifier','')
		return first_name, entity_urn, headline, industry_name, last_name, location, location_postal_code, location_country_code, version_tag, summary, address, background_image, maiden_name, interests, phonetic_last_name, phonetic_firt_name, state, miniprofile, picture_info, birthdate, object_urn, tracking_id, public_identifier

	def get_type_data(self, type_data, type_name):
		list_of_type = []
		keyvalue = type_name
		for keywords in type_data:
			type_name = keywords.get('name','')
			type_entity_urn = keywords.get('entityUrn','')
			type_member = keywords.get('member','')#urn:li:fs_miniProfile:ACoAAAA3LYwBc6wnTI5z--QGOwRXb9Go6py9TbA
			type_profile_urn = keywords.get('profileUrn','')#urn:li:fs_miniProfile:ACoAAAA3LYwBc6wnTI5z--QGOwRXb9Go6py9TbA
			type_description = keywords.get('description','')
			type_title = keywords.get('title','')
			type_occupation = keywords.get('occupation','')#urn:li:fs_position:(ACoAAAA3LYwBc6wnTI5z--QGOwRXb9Go6py9TbA,27571481)
			type_issuer = keywords.get('issuer','')
			type_issue_date = keywords.get('issueDate','')#urn:li:fs_honor:(ACoAAAA3LYwBc6wnTI5z--QGOwRXb9Go6py9TbA,97),issueDate
			type_time_period = keywords.get('timePeriod','')#urn:li:fs_position:(ACoAAAA3LYwBc6wnTI5z--QGOwRXb9Go6py9TbA,598862789),timePeriod
			type_location_name = keywords.get('locationName','')
			type_company_name = keywords.get('companyName','')
			type_cause_name = keywords.get('causeName','')
			type_cause_type = keywords.get('causeType','')
			type_degree_name = keywords.get('degreeName','')
			type_field_ofstudy = keywords.get('fieldOfStudy','')
			type_school_name = keywords.get('schoolName','')
			type_activities = keywords.get('activities','')
			set_of_type = []
			if keyvalue == 'skill':
				set_of_type = [type_name, type_entity_urn]
			elif keyvalue == 'contributor':
				set_of_type = [type_name, type_entity_urn, type_member]
			elif keyvalue == 'honor':
				set_of_type = [type_title, type_description, type_occupation, type_issuer, type_issue_date, type_entity_urn ]
			elif keyvalue == 'experiences':
				set_of_type = [type_title, type_time_period, type_location_name, type_company_name, type_description, type_entity_urn, type_description]
			elif keyvalue == 'vcause':
				set_of_type = [type_cause_name, type_cause_type]
			elif keyvalue == 'educations':
				set_of_type = [type_degree_name, type_field_ofstudy, type_school_name, type_activities, type_entity_urn, type_time_period]
			list_of_type.append(set_of_type)
		return list_of_type

	def get_cer_data(self, certifications_data):
		list_of_cert = []
		for certification in certifications_data:
			cerrtification_name = certification.get('displaySource','')
			certifaction_entity_urn = certification.get('entityUrn','')
			full_name = certification.get('name','')
			time_period_fs = certification.get('timePeriod','')
			certifcaio_url = certification.get('url','')
			set_of_cer = [cerrtification_name, certifaction_entity_urn, full_name, time_period_fs, certifcaio_url]
			list_of_cert.append(set_of_cer)
		return list_of_cert

	def get_start_end_date(self, data):
		start_date = data.get('startDate', {})
		end_date = data.get('endDate', {})
		start_year = start_date.get('year','')
		start_month = start_date.get('month','')
		end_year = end_date.get('year','')
		end_month = end_date.get('month','')
		return str(end_year), str(end_month), str(start_year), str(start_month)

	def get_skills_data(self, data_elements, url_type):
		skill_part = data_elements.get('skill',{})
		skill_name = skill_part.get('name','')
		skill_entity_urn = skill_part.get('entityUrn','')
		skill_endorsement_count = data_elements.get('endorsementCount','')
		public_topic_skill_url, member_topic_skill_url = ['']*2
		if '..' not in skill_name and skill_name:
			skill_url_part = skill_name.lower().replace(' ','-')
			public_topic_skill_url = "https://www.linkedin.com/topic/%s?trk=pprofile_topic"%skill_url_part
			member_topic_skill_url = "https://www.linkedin.com/topic/%s?trk=mprofile_topic"%skill_url_part
		return skill_name, skill_entity_urn, skill_endorsement_count, public_topic_skill_url, member_topic_skill_url

	def get_volunteers_data(self,  data_elements, url_type):
		volunteer_role = data_elements.get('role','')
		volunteer_cause = data_elements.get('cause','')
		organization_name = data_elements.get('companyName','')
		organization_logo = data_elements.get('company',{}).get('miniCompany',{}).get('logo',{}).get('com.linkedin.voyager.common.MediaProcessorImage',{}).get('id','')
		if organization_logo:
			organization_logo = "%s%s"%("https://media.licdn.com/media", organization_logo)
		description = data_elements.get('description','')
                time_period = data_elements.get('timePeriod')
		start_year, start_month = ['']*2
                if time_period:
                        end_year, end_month, start_year, start_month = self.get_start_end_date(time_period)
		return volunteer_role

	def get_given_data(self, data_elements, url_type):
		summary = data_elements.get('recommendationText','')
		recommendation_id = data_elements.get('entityUrn','')
		if recommendation_id:
			recommendation_id = textify(re.findall('\d+', recommendation_id))
		recommendee = data_elements.get('recommendee', '')
		recommender = data_elements.get('recommender', '')
		recommender_name =  recommender.get('firstName', '')
		recommendee_name =  recommendee.get('firstName', '')
		recommendee_lastname = recommendee.get('lastName', '')
		recommendee_name_full = "%s%s%s"%(recommendee_name,' ',recommendee_lastname)
		profile_url = recommendee.get('publicIdentifier', '')
		profile_image = recommendee.get('picture',{}).get('com.linkedin.voyager.common.MediaProcessorImage',{}).get('id','')
		if profile_url:
			profile_url = "https://www.linkedin.com/in/%s/"%(profile_url)
		profile_member_id = recommendee.get('objectUrn','')
		if profile_member_id:
			profile_member_id =  textify(re.findall('\d+', profile_member_id))
		created =  data_elements.get('created','')
		if created:
			created = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(created)/1000)))
		relation_ship = data_elements.get('relationship','').lower().replace('_',' ').replace('recommender',recommender_name).replace('recommendee',recommendee_name)
		date_and_relationship = ', '.join([created, relation_ship]).strip(', ').strip()
		return recommendee_name_full

	def get_projects_data(self, data_elements, url_type):
		project_description = data_elements.get('description','')
		time_period = data_elements.get('timePeriod',{})
		end_year, end_month, start_year, start_month = ['']*4
		if time_period:
			end_year, end_month, start_year, start_month = self.get_start_end_date(time_period)
                start_date = '-'.join([start_year, start_month])
                end_date = '-'.join([end_year, end_month])
		project_url = data_elements.get('url','')
		project_title = data_elements.get('title','')
		project_members_count = data_elements.get('memebers',[])
		if project_members_count:
			project_members_count = str(len(project_members_count)-1)
			if project_members_count !=0:
				project_members_names = '<>'.join(["%s%s%s"%(member.get('member',{}).get('firstName',''),' ', member.get('member',{}).get('lastName','')) for member in data_elements.get('members',[])]).strip('<>').strip()
		return project_title
	def get_digit(self, value):
		value = textify(re.findall('\d+'), value)
		return value
	def get_posts_data(self, data_elements, url_type, main_member_id):
		post_url = data_elements.get('permaLink','')
		post_image = data_elements.get('image',{}).get('com.linkedin.voyager.common.MediaProcessorImage',{}).get('id','')
		post_title = data_elements.get('title','')
		post_author_id = main_member_id
		posted_date = data_elements.get('postedDate',{})
		posted_year = posted_date.get('year','')
		posted_month = posted_date.get('month','')
		posted_day = posted_date.get('day','')
		posted_date = ("%s%s%s%s%s"%(posted_year, '-', posted_month, '-', posted_day)).strip().strip('-')
		post_article_id = data_elements.get('entityUrn','')
		post_article_id = self.get_digit(post_article_id)
		return post_title
			 

	def get_received_data(self, data_elements, url_type):
		summary = data_elements.get('recommendationText','')
		recommender = data_elements.get('recommender',{})
		recommendee_name = data_elements.get('recommendee',{}).get('firstName',{})
		profile_identifier = recommender.get('publicIdentifier','')
		if profile_identifier:
			profile_identifier = "https://www.linkedin.com/in/%s/"%(profile_identifier)
		headline = recommender.get('occupation','')
		recommender_name = recommender.get('firstName','')
		relation_ship = data_elements.get('relationship','').lower().replace('_',' ').replace('recommender',recommender_name).replace('recommendee',recommendee_name)
		created =  data_elements.get('created','')
		if created:
			created = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(created)/1000)))
		date_and_relationship = ', '.join([created, relation_ship]).strip(', ').strip()
		first_name = recommender.get('firstName','')
		last_name = recommender.get('lastName','')
		name =("%s%s%s"%(first_name, ' ', last_name)).strip()
		object_urn_member_id = recommender.get('objectUrn','')
		ent_id = data_elements.get('entityUrn','')
		if object_urn_member_id:
			object_urn_member_id = textify(re.findall('\d+',object_urn_member_id))
		if ent_id:
			ent_id = textify(re.findall('\d+',ent_id))
		profile_image = recommender.get('picture',{}).get('com.linkedin.voyager.common.MediaProcessorImage',{}).get('id','')
		if profile_image:
			profile_image = "%s%s"%("https://media.licdn.com/media", profile_image)
		return name
		
	def get_experiences_data(self, data_elements, url_type):
		exp_location = data_elements.get('locationName','')
		exp_company_name = data_elements.get('companyName','')
		exp_company_beta = data_elements.get('companyUrn','')
		exp_entity_urn = data_elements.get('entityUrn','')
		if exp_company_beta:
			exp_company_beta = textify(re.findall('\d+',exp_company_beta))
			exp_company_url = "https://www.linkedin.com/company-beta/%s/"%exp_company_beta
		if exp_entity_urn:
			exp_entity_urn = textify(re.findall('\d+', exp_entity_urn))
		exp_title = data_elements.get('title','')
		time_period = data_elements.get('timePeriod')
		if time_period:
			end_year, end_month, start_year, start_month = self.get_start_end_date(time_period)
		start_date = '-'.join([start_year, start_month])
		end_date = '-'.join([end_year, end_month])
		exp_company_logo = data_elements.get('company',{}).get('miniCompany',{}).get('logo',{}).get('com.linkedin.voyager.common.MediaProcessorImage',{}).get('id','')#/p/4/000/154/201/07a04df.png'
		exp_company_id = str(exp_company_beta)
		exp_position_id = exp_entity_urn
		exp_summary = data_elements.get('description','')
		return exp_title
	def get_orgs_data(self, data_elements, url_type):
		description = data_elements.get('description','')
		occupation_name = data_elements.get('occupation','')#urn:li:fs_position:(ACoAAAECOWgBe45sd0lkrTBFpVgxRsvMe3DEeRQ,24971278)
                time_period = data_elements.get('timePeriod')
                start_year, start_month = ['']*2
                if time_period:
                        end_year, end_month, start_year, start_month = self.get_start_end_date(time_period)
		postion = data_elements.get('position', '')
		name = data_elements.get('name','')
		return name
		

	def parse_voyage(self, response):
		data = json.loads(response.body)
		headers = response.meta['headers']
		data_elements = data.get('elements', [])
		url_type = response.meta['url_type']
		main_url = response.meta['main_url']
		url_paging  = data.get('paging',[])
		main_member_id = response.meta.get('main_member_id','')
		if url_type == 'basic':
			first_name, entity_urn, headline, industry_name, last_name, location, location_postal_code, location_country_code, version_tag, summary, address, background_image, maiden_name, interests, phonetic_last_name, phonetic_firt_name, state, miniprofile, picture_info, birthdate, object_urn, tracking_id, public_identifier = self.get_meta_profile(data)
			if public_identifier:
				api_url = [('https://www.linkedin.com/voyager/api/identity/profiles/%s/positions'%public_identifier,'experiences'),('https://www.linkedin.com/voyager/api/identity/profiles/%s/featuredSkills?includeHiddenEndorsers=true&count=50'%public_identifier,'skills'),('https://www.linkedin.com/voyager/api/identity/profiles/%s/volunteerExperiences'%public_identifier,'volunteer'),('https://www.linkedin.com/voyager/api/identity/profiles/%s/recommendations?q=received'%(public_identifier),'received'),('https://www.linkedin.com/voyager/api/identity/profiles/%s/recommendations?q=given'%(public_identifier),'given'), ('https://www.linkedin.com/voyager/api/identity/profiles/%s/projects'%(public_identifier),'projects'),('https://www.linkedin.com/voyager/api/identity/profiles/%s/posts'%(public_identifier),'posts'),('https://www.linkedin.com/voyager/api/identity/profiles/%s/organizations'%(public_identifier),'organizations')]
				for api in api_url:
					yield Request(api[0], headers=headers, callback=self.parse_voyage, meta={'url_type':api[1], 'main_url':api[0], 'headers':headers, 'main_member_id':textify(re.findall('\d+',object_urn))})
		import pdb;pdb.set_trace()
		if url_type == 'organizations':
			for datao in data_elements:
				data_org = self.get_orgs_data(datao, url_type)
		if url_type == 'posts':
			for datap in data_elements:
				data_posts = self.get_posts_data(datap, url_type, main_member_id)
		if url_type == 'volunteer':
			for datav in data_elements:
				data_volunteer = self.get_volunteers_data(datav, url_type)

		if url_type == 'experiences':
			for datae in data_elements:
				data_return = self.get_experiences_data(datae, url_type)
		
                if url_type == 'skills':
                        for datas in data_elements:
                                data_skills = self.get_skills_data(datas, url_type)
		if url_type == 'received':
			for datar in data_elements:
				data_received = self.get_received_data(datar, url_type)

		if url_type == 'given':
			for datag in data_elements:
				data_given = self.get_given_data(datag, url_type)
				print data_given
		if url_type == 'projects':
			for datap in data_elements:
				 data_projects = self.get_projects_data(datap, url_type)

		if url_type != 'basic' and url_type != 'projects':
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
					yield Request(retrun_url, headers=headers, callback=self.parse_voyage, meta={'url_type':url_type, 'main_url':main_url, 'headers':headers})
			
					
