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
		self.profiles_list = [('aravindrajanm', 'https://www.linkedin.com/in/aravindrajanm/', '{}'),('scoping','https://www.linkedin.com/in/scopingbrands/','{}'),('rachel','https://www.linkedin.com/in/rachelcanda/','{}'),('dennis','https://www.linkedin.com/in/dennis-t-22179ab4/','{}')]
		#self.profiles_list = [('chihara','https://www.linkedin.com/in/masaki-ken-chihara-32b488','{}')]
		#self.profiles_list = [('Tathagat_Varma','https://www.linkedin.com/in/tathagat/','{}')]
		#self.profiles_list = [('bharat','https://www.linkedin.com/in/bharat-punia-2a329b38/','{}')]
		#self.profiles_list = [('new', 'https://www.linkedin.com/profile/view?id=AAEAAARJxN0Btz6ZOefhR94II32G--rYJYcvwbU&authType=name&authToken=Vq9T','{}')]
		#self.profiles_list = [('for_orgs','https://www.linkedin.com/profile/view?id=AAEAAAECOWgBCJloFOc9oO5uYRBn7pjRe3c3_iI&authType=name&authToken=hTN9','{}')]
		#self.profiles_list = [('for_honors','https://www.linkedin.com/in/tapansinghel','{}')]
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
		sk = response.meta['sk']
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
		profile_data = {}
		try:
			profile_data = json.loads(''.join(sel.xpath('//code[contains(text(),"profile.ProfileView")]/text()').extract()))
		except:
			profile_data = json.loads(sel.xpath('//code[contains(text(),"profile.ProfileView")]/text()').extract()[0])
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
		languages_data = filter(None, [i['name'] if i['$type'] == "%s%s"%(keyword,'Language') else ''for i in data_json])
		if languages_data:
			languages_data = '<>'.join(languages_data)
		connections_count = textify(re.findall('connectionsCount&quot;:(\d+),', response.body))
		followers_count = textify(re.findall('followersCount&quot;:(\d+),', response.body))
		course_data = filter(None, [i if i['$type'] == "%s%s"%(keyword,'Course') else ''for i in data_json])
		if basic_data:
			basic_dat = basic_data[0]
			entity_urn = basic_dat.get('entityUrn','')
			for_entity = entity_urn.replace('urn:li:fs_profile:','')
			if entity_urn:
				url_to = 'https://www.linkedin.com/voyager/api/identity/profiles/%s'%for_entity
        	        	yield Request(url_to, headers=headers, callback=self.parse_voyage, meta={'url_type':'basic', 'headers':headers, 'main_url':url_to, 'sk':sk, 'languages_data':languages_data, 'connections_count':connections_count, 'followers_count':followers_count})

		"""if volunteercause_data:
			volunteercause_dat = self.get_type_data(volunteercause_data, 'vcause')
		if experiences_data:
			experiences_dat = self.get_type_data(experiences_data,'experiences')
		if honors_data:
			honors_dat = self.get_type_data(honors_data,'honors')
		if educations_data:
			educations_dat = self.get_type_data(educations_data, 'educations')"""
		if picture_data:
			picture_dat = picture_data[0].get('masterImage','')#u'/AAEAAQAAAAAAAAubAAAAJDhiZWYxZjhlLWEzMGQtNDA1Yi05YjQ4LTZlN2M3NDM1MzI1Yg.jpg'
			if picture_dat:
				picture_dat = 'https://media.licdn.com/mpr/mpr/shrinknp_400_400/%s'%(picture_dat)

		"""if skills_data:
			skill_dat = self.get_type_data(skills_data,'skill')
			for skil in skill_dat:
				skil_name, skill_entityurn = skil

		if certifi_data:
			certifications_dat = self.get_cer_data(certifi_data)
			for cert in certifications_dat:
				cerrtification_name, certifaction_entity_urn, cer_full_name, cer_time_period_fs, certifcaio_url = cert
		if contributors_data:
			values = self.get_type_data(contributors_data,'contributors')"""
			


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

                if background_image:
                        background_image = "%s%s"%("https://media.licdn.com/media", background_image)

		maiden_name = basic_dat.get('maidenName','')
		interests = basic_dat.get('interests','')
		phonetic_last_name = basic_dat.get('phoneticLastName','')
		phonetic_firt_name = basic_dat.get('phoneticFirstName','')
		state = basic_dat.get('state','')
		miniprofile = basic_dat.get('miniProfile','')#urn:li:fs_miniProfile:ACoAAAA3LYwBc6wnTI5z--QGOwRXb9Go6py9TbA
		picture_info = basic_dat.get('pictureInfo',{}).get('masterImage','')#urn:li:fs_profile:ACoAAAA3LYwBc6wnTI5z--QGOwRXb9Go6py9TbA,pictureInfo
		if picture_info:
			picture_info = "%s%s"%("https://media.licdn.com/media", picture_info)
		birthdate = basic_dat.get('birthDate','')#urn:li:fs_profile:ACoAAAA3LYwBc6wnTI5z--QGOwRXb9Go6py9TbA,birthDate#fromapi {u'day': 30, u'month': 8}
		miniprofile = basic_dat.get('miniProfile',{})
		object_urn = miniprofile.get('objectUrn','')#urn:li:member:3616140
		object_urn = self.get_digit(object_urn)
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

	def get_certifications_data(self, data_elements, url_type, sk):
		certification_id =data_elements.get('entityUrn','')
		certification_id = self.get_digit(certification_id)
                time_period = data_elements.get('timePeriod','')
                start_year, start_month = ['']*2
                if time_period:
                        end_year, end_month, start_year, start_month = self.get_start_end_date(time_period)
		date_cer = ('%s%s%s'%(start_year, '-', start_month)).strip('-').strip()
		certification_title = data_elements.get('name','')
		certification_company_logo = data_elements.get('company',{}).get('logo',{}).get('com.linkedin.voyager.common.MediaProcessorImage',{}).get('id','')
                if certification_company_logo:
                        certification_company_logo = "%s%s"%("https://media.licdn.com/media", certification_company_logo)

		certification_company_name = data_elements.get('authority','')
		certifications_licence = data_elements.get('licenseNumber','')#need to add this in certifications table
		item = self.get_certifications_item(sk, certification_id, certification_title, date_cer, certification_company_name, certification_company_logo, certifications_licence)
		return item
	def get_certifications_item(self, sk,  cer_id, cer_name, cer_iso_stdate,au_com_name, au_media_logo, certifications_licence):
		linkedin_cer_ = Linkedincertifications()
		linkedin_cer_['sk'] = md5("%s%s%s%s%s"%(sk, cer_id, cer_name, cer_iso_stdate,au_com_name))
		linkedin_cer_['profile_sk'] = normalize(sk)
		linkedin_cer_['certification_id']= normalize(cer_id)
		linkedin_cer_['certification_date'] = normalize(cer_iso_stdate)
		linkedin_cer_['certification_title'] = normalize(cer_name)
		linkedin_cer_['certification_company_logo'] = normalize(au_media_logo)
		linkedin_cer_['certification_company_name'] = normalize(au_com_name)
		linkedin_cer_['certification_licence'] = normalize(certifications_licence)
		if cer_id or cer_name or au_media_logo:
			return linkedin_cer_
		else:
			return ''

		

	def get_educations_data(self, data_elements, url_type, sk):
                time_period = data_elements.get('timePeriod','')
                start_year, start_month, end_year, end_month = ['']*4
                if time_period:
                        end_year, end_month, start_year, start_month = self.get_start_end_date(time_period)
		edu_degree = data_elements.get('degreeName','')
		edu_field_of_study = data_elements.get('fieldOfStudy','')
		edu_school_name = data_elements.get('schoolName','')
		school_logo = data_elements.get('school',{}).get('logo',{}).get('com.linkedin.voyager.common.MediaProcessorImage',{}).get('id','')
                if school_logo:
                        school_logo = "%s%s"%("https://media.licdn.com/media", school_logo)
		edu_activities = data_elements.get('activities','')#need to add this in educations table
		edu_grade = data_elements.get('grade','') # need to add this in educations table
		edu_school_id = data_elements.get('schoolUrn','')
		edu_school_id = self.get_digit(edu_school_id)
		education_id = data_elements.get('entityUrn','')
		education_id = self.get_digit(education_id)
		item = self.get_educations_item(sk, start_year, start_month, '', end_year, '', end_month, edu_degree, edu_field_of_study, edu_school_name, school_logo, edu_grade, edu_activities, education_id, edu_school_id)
		return item

	def get_educations_item(self, sk, edu_start_year, edu_start_month, formatedustart, edu_end_year, formatedusend, edu_end_month, edu_degree, edu_field_ofstdy, edu_name, edu_schoologo, edu_grade, edu_activities, edu_id, edu_scho_id):
		linkedin_educations_ = Linkedineducations()
		linkedin_educations_['sk'] = md5("%s%s%s%s%s%s"%(sk, edu_degree, edu_field_ofstdy, edu_name, edu_id, edu_scho_id))
		linkedin_educations_['profile_sk'] = normalize(sk)
		linkedin_educations_['edu_start_year'] = normalize(edu_start_year)
		linkedin_educations_['edu_start_month'] = normalize(edu_start_month)
		linkedin_educations_['edu_start_date'] = normalize(formatedustart)
		linkedin_educations_['edu_end_year'] = normalize(edu_end_year)
		linkedin_educations_['edu_end_date'] = normalize(formatedusend)
		linkedin_educations_['edu_end_month'] = normalize(edu_end_month)
		linkedin_educations_['edu_degree'] = normalize(edu_degree)
		linkedin_educations_['edu_field_of_study'] = normalize(edu_field_ofstdy)
		linkedin_educations_['edu_school_name'] = normalize(edu_name.replace('&#39;',''))
		linkedin_educations_['school_logo'] = normalize(edu_schoologo)
		linkedin_educations_['edu_grade'] = normalize(edu_grade)
		linkedin_educations_['edu_activities'] = normalize(edu_activities)
		linkedin_educations_['post_article_id'] = ''
		linkedin_educations_['education_id'] = normalize(edu_id)
		linkedin_educations_['school_id'] = normalize(edu_scho_id)
		if edu_degree or edu_field_ofstdy or edu_name:
			return linkedin_educations_
		else:
			return ''


	def get_start_end_date(self, data):
		start_date = data.get('startDate', {})
		end_date = data.get('endDate', {})
		start_year = start_date.get('year','')
		start_month = start_date.get('month','')
		end_year = end_date.get('year','')
		end_month = end_date.get('month','')
		return str(end_year), str(end_month), str(start_year), str(start_month)

	def get_skills_data(self, data_elements, url_type, sk):
		skill_part = data_elements.get('skill',{})
		skill_name = skill_part.get('name','')
		skill_entity_urn = skill_part.get('entityUrn','')
		skill_endorsement_count = str(data_elements.get('endorsementCount',''))
		public_topic_skill_url, member_topic_skill_url = ['']*2
		if '..' not in skill_name and skill_name:
			skill_url_part = skill_name.lower().replace(' ','-')
			public_topic_skill_url = "https://www.linkedin.com/topic/%s?trk=pprofile_topic"%skill_url_part
			member_topic_skill_url = "https://www.linkedin.com/topic/%s?trk=mprofile_topic"%skill_url_part
		item = self.get_skills_item(sk, skill_name, skill_endorsement_count, public_topic_skill_url, member_topic_skill_url)
		return item

	def get_skills_item(self, sk, ski_name, ski_endo_count, public_topic_url, member_topic_url):
		linkedin_ski_ = Linkedinskills()
		linkedin_ski_['sk'] = md5("%s%s%s%s"%(sk, ski_name, ski_endo_count, public_topic_url))
		linkedin_ski_['profile_sk']= normalize(sk)
		linkedin_ski_['skill_name'] = normalize(ski_name)
		linkedin_ski_['endoresement_count'] = normalize(ski_endo_count)
		linkedin_ski_['member_topic_skill_url'] = normalize(member_topic_url)
		linkedin_ski_['public_topic_skill_url'] = normalize(public_topic_url)
		if ski_name:
			return linkedin_ski_
		else:
			return ''


	def get_volunteers_data(self,  data_elements, url_type, sk):
		volunteer_role = data_elements.get('role','')
		volunteer_cause = data_elements.get('cause','')
		organization_name = data_elements.get('companyName','')
		organization_logo = data_elements.get('company',{}).get('miniCompany',{}).get('logo',{}).get('com.linkedin.voyager.common.MediaProcessorImage',{}).get('id','')
		if organization_logo:
			organization_logo = "%s%s"%("https://media.licdn.com/media", organization_logo)
		description = data_elements.get('description','')
                time_period = data_elements.get('timePeriod')
		organization_id = data_elements.get('companyUrn','')
		organization_id = self.get_digit(organization_id)
		start_year, start_month, end_year, end_month = ['']*4
                if time_period:
                        end_year, end_month, start_year, start_month = self.get_start_end_date(time_period)

		item = self.get_volunteers_item(sk, '', description, volunteer_cause, organization_name, volunteer_role, organization_logo, str(start_year), str(start_month), '', str(end_month), str(end_year), organization_id)
		return item
	
	def get_volunteers_item(self, sk, volun_interests, vol_desc, vol_cause, vol_org_name, vol_role, vol_media_logo, vol_start_date_year, vol_start_date_month, vol_single_date_iso, end_month, end_year, organization_id):
		linkedin_volun_ = Linkedinvolunteerexp()
		linkedin_volun_['sk'] = md5("%s%s%s%s%s"%(sk,volun_interests, vol_desc, vol_cause, vol_org_name))
		linkedin_volun_['profile_sk'] = normalize(sk)
		linkedin_volun_['volunteer_interests'] = normalize(volun_interests)
		linkedin_volun_['volunteer_role'] = normalize(vol_role)
		linkedin_volun_['volunteer_cause'] = normalize(vol_cause)
		linkedin_volun_['organization_name'] = normalize(vol_org_name)
		linkedin_volun_['organization_logo'] = normalize(vol_media_logo)
		linkedin_volun_['description'] = normalize(vol_desc)
		linkedin_volun_['start_date_year'] = normalize(vol_start_date_year)
		linkedin_volun_['start_date_month'] = normalize(vol_start_date_month)
		linkedin_volun_['volunteer_date'] = normalize(vol_single_date_iso)
		linkedin_volun_['end_date_year'] = normalize(end_year)
		linkedin_volun_['end_date_month'] = normalize(end_month)
		linkedin_volun_['organization_id'] = normalize(organization_id)
		if linkedin_volun_['volunteer_role'] or linkedin_volun_['volunteer_cause'] or linkedin_volun_['organization_name']: 
			return linkedin_volun_
		else:
			return ''


	def get_given_data(self, data_elements, url_type, sk):
		summary = data_elements.get('recommendationText','')
		recommendation_id = data_elements.get('entityUrn','')
		if recommendation_id:
			recommendation_id = self.get_digit(recommendation_id)
		recommendee = data_elements.get('recommendee', '')
		recommender = data_elements.get('recommender', '')
		recommender_name =  recommender.get('firstName', '')
		recommendee_name =  recommendee.get('firstName', '')
		recommendee_lastname = recommendee.get('lastName', '')
		recommendee_name_full = "%s%s%s"%(recommendee_name,' ',recommendee_lastname)
		profile_url = recommendee.get('publicIdentifier', '')
		profile_image = recommendee.get('picture',{}).get('com.linkedin.voyager.common.MediaProcessorImage',{}).get('id','')
                if profile_image:
                        profile_image = "%s%s"%("https://media.licdn.com/media", profile_image)

		if profile_url:
			profile_url = "https://www.linkedin.com/in/%s/"%(profile_url)
		profile_member_id = recommendee.get('objectUrn','')
		if profile_member_id:
			profile_member_id = self.get_digit(profile_member_id)

		created =  data_elements.get('created','')
		if created:
			created = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(created)/1000)))
		relation_ship = data_elements.get('relationship','').lower().replace('_',' ').replace('recommender',recommender_name).replace('recommendee',recommendee_name)
		date_and_relationship =  ''
		try: date_and_relationship = ', '.join([str(created), str(relation_ship)]).strip(', ').strip()
		except:  date_and_relationship = ', '.join([str(created), str(relation_ship.encode('utf8'))])
		item = self.get_given_item(sk, recommendee_lastname, recommendee_name_full, summary, '', recommendation_id, date_and_relationship, profile_image, profile_member_id, profile_url, created)
		return item

	def get_given_item(self, sk, giv_lastname, giv_fullname, giv_text, giv_title, giv_recom_id, giv_date_relationship, giv_mem_pic, giv_mem_id, giv_profile_link, giv_created_date):

		linkedin_give_rec_ = Linkedingivenrecommendations()
		linkedin_give_rec_['sk'] = md5("%s%s%s%s%s%s%s"%(sk, giv_lastname, giv_fullname, giv_text, giv_title, giv_recom_id, giv_mem_id))
		linkedin_give_rec_['profile_sk'] = normalize(sk)
		linkedin_give_rec_['last_name'] = normalize(giv_lastname)
		linkedin_give_rec_['name'] = normalize(giv_fullname)
		linkedin_give_rec_['date_and_relationship'] = normalize(giv_date_relationship)
		linkedin_give_rec_['title'] = normalize(giv_title)
		linkedin_give_rec_['created_date'] = normalize(giv_created_date)
		linkedin_give_rec_['summary'] = normalize(giv_text)
		linkedin_give_rec_['profile_image'] =  normalize(giv_mem_pic)
		linkedin_give_rec_['profile_member_id'] = normalize(giv_mem_id)
		linkedin_give_rec_['profile_url'] = normalize(giv_profile_link)
		linkedin_give_rec_['recommendation_id'] = normalize(giv_recom_id)
		if giv_lastname or giv_fullname or giv_title or giv_mem_id or giv_recom_id:
			return linkedin_give_rec_
		else:
			return ''



	def get_projects_data(self, data_elements, url_type, sk):
		project_description = data_elements.get('description','')
		time_period = data_elements.get('timePeriod',{})
		end_year, end_month, start_year, start_month = ['']*4
		if time_period:
			end_year, end_month, start_year, start_month = self.get_start_end_date(time_period)
                start_date = '-'.join([start_year, start_month]).strip().strip('-')
                end_date = '-'.join([end_year, end_month]).strip().strip('-')
		project_url = data_elements.get('url','')
		project_title = data_elements.get('title','')
		project_members_count = data_elements.get('memebers',[])
		project_members_names = ''
		if project_members_count:
			project_members_count = str(len(project_members_count)-1)
			if project_members_count !=0:
				project_members_names = '<>'.join(["%s%s%s"%(member.get('member',{}).get('firstName',''),' ', member.get('member',{}).get('lastName','')) for member in data_elements.get('members',[])]).strip('<>').strip()
		else:
			project_members_count = ''
		item = self.get_projects_item(sk, project_title, project_url, project_description, str(project_members_count), start_date, end_date, project_members_names)
		return item
	
	def get_projects_item(self, sk, pro_title, pro_url, pro_desc, pro_team_mates, pro_startdate_iso, pro_enddate_iso, team_mates_list):
		linkedin_proj_ = Linkedinprojects()
		linkedin_proj_['sk'] = md5("%s%s%s%s%s"%(sk,pro_title, pro_url, pro_desc, pro_team_mates))
		linkedin_proj_['profile_sk'] = normalize(sk)
		linkedin_proj_['project_date'] = ''
		linkedin_proj_['number_of_project_members'] = normalize(pro_team_mates)
		linkedin_proj_['project_member_names'] = normalize(team_mates_list)
		linkedin_proj_['project_occupation_name'] = ''
		linkedin_proj_['project_title'] = normalize(pro_title)
		linkedin_proj_['project_url']  = normalize(pro_url)
		linkedin_proj_['project_start_date'] = normalize(pro_startdate_iso)
		linkedin_proj_['project_end_date'] = normalize(pro_enddate_iso)
		linkedin_proj_['project_description'] = normalize(pro_desc)
		if linkedin_proj_['project_title'] or linkedin_proj_['project_description']:
			return linkedin_proj_
		else:
			return ''

		
	def get_digit(self, value):
		values = textify(re.findall(',(\d+)', value))
		if not values:
			values = textify(re.findall('\d+', value))
		return values

	def get_posts_data(self, data_elements, url_type, main_member_id, sk):
		post_url = data_elements.get('permaLink','')
		post_image = data_elements.get('image',{}).get('com.linkedin.voyager.common.MediaProcessorImage',{}).get('id','')
                if post_image:
                        post_image = "%s%s"%("https://media.licdn.com/media", post_image)
		post_title = data_elements.get('title','')
		post_author_id = main_member_id
		posted_date = data_elements.get('postedDate',{})
		posted_year = posted_date.get('year','')
		posted_month = posted_date.get('month','')
		posted_day = posted_date.get('day','')
		posted_date = ("%s%s%s%s%s"%(posted_year, '-', posted_month, '-', posted_day)).strip().strip('-')
		post_article_id = data_elements.get('entityUrn','')
		post_article_id = self.get_digit(post_article_id)
		item = self.get_posts_item(sk,post_url, post_image, post_title, post_author_id, '', posted_date, post_article_id)
		return item

	def get_posts_item(self, sk, post_url, post_image, post_title, post_author_id, post_state, post_date, sk_post):
		linkedin_posts_ = Linkedinposts()
		linkedin_posts_['sk'] = normalize(md5("%s%s%s%s%s"%(sk_post, post_title, sk, post_date, post_state)))
		linkedin_posts_['profile_sk'] = normalize(sk)
		linkedin_posts_['post_url'] = normalize(post_url)
		linkedin_posts_['post_image'] = normalize(post_image)
		linkedin_posts_['post_title'] = normalize(post_title)
		linkedin_posts_['post_author_id'] = normalize(post_author_id)
		linkedin_posts_['post_state'] = normalize(post_state)
		linkedin_posts_['post_date'] = normalize(post_date)
		linkedin_posts_['post_article_id'] = normalize(sk_post)
		if post_title or post_url or post_date:
			return linkedin_posts_
		else:
			return ''

	def get_received_data(self, data_elements, url_type, sk):
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
			object_urn_member_id = self.get_digit(object_urn_member_id)
		if ent_id:
			ent_id = self.get_digit(ent_id)
		profile_image = recommender.get('picture',{}).get('com.linkedin.voyager.common.MediaProcessorImage',{}).get('id','')
		if profile_image:
			profile_image = "%s%s"%("https://media.licdn.com/media", profile_image)
		item = self.get_received_item(sk, '', ent_id, object_urn_member_id, name,  summary, profile_image, profile_identifier , headline, date_and_relationship, created, '')
		return item
	def get_received_item(self, sk, rec_role, rec_id, rec_memid,  rec_name_full, rec_text, rec_mem_pic, rec_profile_link, rec_headline, rec_date_rela, rec_fmt_Datec, rec_organization):
	
		linkedin_rec_ = Linkedinrecrecommendations()
		linkedin_rec_['sk'] = md5("%s%s%s%s%s%s%s"%(sk, rec_role, rec_id, rec_fmt_Datec, rec_date_rela, rec_profile_link, rec_mem_pic))  
		linkedin_rec_['profile_sk'] = normalize(sk)
		linkedin_rec_['role'] = normalize(rec_role)
		linkedin_rec_['profile_member_id'] = normalize(rec_memid)
		linkedin_rec_['id'] = normalize(rec_id)
		linkedin_rec_['edu_start_date'] = ''
		linkedin_rec_['name'] = normalize(rec_name_full)
		linkedin_rec_['organization'] = normalize(rec_organization)
		linkedin_rec_['created_date'] = normalize(rec_fmt_Datec)
		linkedin_rec_['date_and_relationship'] = normalize(rec_date_rela)
		linkedin_rec_['headline'] = normalize(rec_headline)
		linkedin_rec_['profile_url'] = normalize(rec_profile_link)
		linkedin_rec_['profile_image'] = normalize(rec_mem_pic)
		linkedin_rec_['summary'] = normalize(rec_text)
		if rec_id or rec_name_full or rec_headline or rec_mem_pic or rec_role:
			return linkedin_rec_
		else:
			return ''

		
	def get_experiences_data(self, data_elements, url_type, sk):
		exp_location = data_elements.get('locationName','')
		exp_company_name = data_elements.get('companyName','')
		exp_company_beta = data_elements.get('companyUrn','')
		exp_entity_urn = data_elements.get('entityUrn','')
		exp_company_url = ''
		if exp_company_beta:
			exp_company_beta = textify(re.findall('\d+',exp_company_beta))
			exp_company_url = "https://www.linkedin.com/company-beta/%s/"%exp_company_beta
		if exp_entity_urn:
			exp_entity_urn = self.get_digit(exp_entity_urn)
		exp_title = data_elements.get('title','')
		time_period = data_elements.get('timePeriod')
		if time_period:
			end_year, end_month, start_year, start_month = self.get_start_end_date(time_period)
		start_date = '-'.join([start_year, start_month]).strip('-').strip()
		end_date = '-'.join([end_year, end_month]).strip('-').strip()
		exp_company_logo = data_elements.get('company',{}).get('miniCompany',{}).get('logo',{}).get('com.linkedin.voyager.common.MediaProcessorImage',{}).get('id','')#/p/4/000/154/201/07a04df.png'
                if exp_company_logo:
                        exp_company_logo = "%s%s"%("https://media.licdn.com/media", exp_company_logo)

		exp_company_id = str(exp_company_beta)
		exp_position_id = exp_entity_urn
		exp_summary = data_elements.get('description','')
		item = self.get_experiences_item(sk, exp_location, exp_position_id, exp_company_id, start_date , exp_summary, exp_company_name, exp_company_url, exp_title, end_date, exp_company_logo ,'')
		return item

	def get_experiences_item(self, sk, pos_fmt_location, pos_position_id, pos_company_id, pos_startdate_iso, pos_summary, pos_company_name, pos_cpny_url, pos_title, pos_enddate_iso, pos_media_image, pos_fmt_duration):
		linkedin_epx_ = Linkedinexperiences()
		linkedin_epx_['sk']= md5("%s%s%s%s%s%s"%(sk, pos_fmt_location, pos_position_id, pos_company_id, pos_startdate_iso, pos_summary)) 
		linkedin_epx_['profile_sk'] = normalize(sk)
		linkedin_epx_['exp_location'] = normalize(pos_fmt_location)
		linkedin_epx_['exp_company_name'] = normalize(pos_company_name)
		linkedin_epx_['exp_company_url'] = normalize(pos_cpny_url)
		linkedin_epx_['exp_title']  =normalize(pos_title)
		linkedin_epx_['start_date'] = normalize(pos_startdate_iso)
		linkedin_epx_['end_date'] = normalize(pos_enddate_iso)
		linkedin_epx_['exp_company_logo'] = normalize(pos_media_image)
		linkedin_epx_['exp_duration'] = normalize(pos_fmt_duration)
		linkedin_epx_['exp_company_id'] = normalize(pos_company_id)
		linkedin_epx_['exp_position_id'] = normalize(pos_position_id)
		linkedin_epx_['exp_summary'] = normalize(pos_summary)
		if pos_title or pos_cpny_url or pos_fmt_location:
			return linkedin_epx_
		else:
			return ''


	def get_orgs_data(self, data_elements, url_type, sk):
		description = data_elements.get('description','')
		occupation_name = data_elements.get('occupation','')#urn:li:fs_position:(ACoAAAECOWgBe45sd0lkrTBFpVgxRsvMe3DEeRQ,24971278)
                time_period = data_elements.get('timePeriod')
                start_year, start_month, end_year, end_month = ['']*4
                if time_period:
                        end_year, end_month, start_year, start_month = self.get_start_end_date(time_period)
		start_date = ("%s%s%s"%(start_year, '-', start_month)).strip().strip('-')
		end_date  = ("%s%s%s"%(end_year, '-', end_month)).strip().strip('-')
		postion = data_elements.get('position', '')
		name = data_elements.get('name','')
		item = self.get_orgs_item(sk, name, postion,  start_date, description, end_date, '')
		return item

	def get_orgs_item(self, sk, org_name, org_position, org_st_dateiso, org_desc, org_ended_dateiso, org_occupation_name ):
		linkedin_org_ = Linkedinorganizations()
		linkedin_org_['sk'] = md5("%s%s%s%s%s"%(sk, org_name, org_position, org_st_dateiso, org_desc))
		linkedin_org_['profile_sk'] = normalize(sk)
		linkedin_org_['name'] = normalize(org_name)
		linkedin_org_['position'] = normalize(org_position)
		linkedin_org_['start_date'] = normalize(org_st_dateiso)
		linkedin_org_['end_date'] = normalize(org_ended_dateiso)
		linkedin_org_['description']  = normalize(org_desc)
		linkedin_org_['occupation_name'] = normalize(org_occupation_name)
		if linkedin_org_['name'] or linkedin_org_['position']:
			return linkedin_org_
		else:
			return ''


		

	def get_public_data(self, data_elements, url_type, sk):
		publication_title = data_elements.get('name','')
		publication_url = data_elements.get('url','')
		publisher_name = data_elements.get('publisher','')
		pulication_description = data_elements.get('description','')
		publication_date = data_elements.get('date',{})
		publication_day = str(publication_date.get('day',''))
		publication_month = str(publication_date.get('month',''))
		publication_year = str(publication_date.get('year',''))
		if  publication_date:
			publication_date  = '-'.join([publication_year, publication_month, publication_day])
		else:
			publication_date = ''
		item = self.get_public_item(sk, publication_title, publisher_name, pulication_description, publication_url, publication_date)
		return item

	def get_public_item(self, sk, publication_title, publisher_name, pulication_description, publication_url, publication_date):
		linkedin_public_ = Linkedinpublications()
		linkedin_public_['sk'] = '%s%s%s%s'%(sk, publication_title, publisher_name, pulication_description)
		linkedin_public_['profile_sk'] = normalize(sk)
		linkedin_public_['publication_title'] = normalize(publication_title)
		linkedin_public_['publication_url'] = normalize(publication_url)
		linkedin_public_['publisher'] = normalize(publisher_name)
		linkedin_public_['publication_description'] = normalize(pulication_description)
		linkedin_public_['publication_date'] = normalize(publication_date)
		if publication_title or pulication_description or publisher_name:
			return linkedin_public_
		else:
			return ''

	def get_honors_data(self, data_elements, url_type, sk):
		honor_summary = data_elements.get('description','')
		honor_title = data_elements.get('title','')#need to replace occupation field with title for honors table
		honor_issuer = data_elements.get('issuer','')
		iss_date = data_elements.get('issueDate','')
		iss_month = iss_date.get('month','')
		iss_year = iss_date.get('year','')
		iss_day = iss_date.get('day','')
		hon_id = data_elements.get('entityUrn','')
		hon_id = self.get_digit(hon_id)
		if iss_month:
			iss_month = calendar.month_name[iss_month]
		honor_on = ("%s%s%s%s%s"%(iss_day, ' ', iss_month,' ', iss_year)).strip()
		item = self.get_honors_item(sk, honor_title, honor_issuer, honor_on, honor_summary, hon_id)
		return item

	def get_honors_item(self, sk, hon_title, hon_issuer, hon_on, hon_desc, hon_id):

		linkedin_hon_ = Linkedinhonors()
		linkedin_hon_['sk']  = md5("%s%s%s%s%s%s"%(sk, hon_title, hon_issuer, hon_on, hon_desc, hon_id))
		linkedin_hon_['profile_sk'] = normalize(sk)
		linkedin_hon_['honor_on'] = normalize(hon_on)
		linkedin_hon_['honor_issuer'] = normalize(hon_issuer)
		linkedin_hon_['honor_summary'] = normalize(hon_desc)
		linkedin_hon_['honor_title'] = normalize(hon_title)
		if hon_title or hon_issuer or hon_desc:
			return linkedin_hon_
		else:
			return ''

	def get_courses_data(self, data_elements, url_type, sk):
		course_name = data_elements.get('name','')
		course_number = data_elements.get('number','')
		link_course_ = Linkedincourse()
		link_course_['sk'] = md5("%s%s%s"%(sk, course_name, str(course_number)))
		link_course_['profile_sk'] = normalize(sk)
		link_course_['course_name'] = normalize(course_name)
		link_course_['course_number'] = normalize(course_number)
		if course_name or course_number:
			return link_course_
		else:
			return ''
		

	def get_channel_data(self, data_elements, url_type, sk):
		entity = data_elements.get('entity', {}).get('com.linkedin.voyager.growth.interests.Channel',{})
		channel_followers =  data_elements.get('followingInfo',{}).get('followerCount','')
		channel_title = entity.get('name','')
		channel_link = entity.get('id','')
		if channel_link:
			channel_link = "https://www.linkedin.com/channels/%s?trk=prof-following-chan-icon"%(channel_link)
		channel_image = entity.get('logo',{}).get('com.linkedin.voyager.common.MediaProcessorImage',{}).get('id','')
                if channel_image:
                        channel_image = "%s%s"%("https://media.licdn.com/media", channel_image)
		item = self.get_channel_item(sk, str(channel_followers), channel_title, channel_link, channel_image)
		return item

	def get_channel_item(self, sk, foc_followerscount, foc_name, foc_link_channel, foc_image):
		linkedin_foc_ = Linkedinfollowchannels()
		linkedin_foc_['sk'] = md5("%s%s%s%s%s"%(sk, foc_followerscount, foc_name, foc_link_channel, foc_image))
		linkedin_foc_['profile_sk'] = normalize(sk)
		linkedin_foc_['channel_followers'] = normalize(foc_followerscount)
		linkedin_foc_['channel_title'] = normalize(foc_name)
		linkedin_foc_['channel_link'] =normalize(foc_link_channel)
		linkedin_foc_['channel_image'] = normalize(foc_image)
		if linkedin_foc_['channel_title']:
			return linkedin_foc_
		else:
			return ''


	def get_influencers_data(self, data_elements, url_type, sk):
		entity = data_elements.get('entity', {}).get('com.linkedin.voyager.identity.shared.MiniProfile',{})
		inflencer_first_name = entity.get('firstName','')
		influencer_last_name = entity.get('lastName','')
		influencer_name = "%s%s%s"%(inflencer_first_name, ' ', influencer_last_name)
		influencer_image = entity.get('picture',{}).get('com.linkedin.voyager.common.MediaProcessorImage',{}).get('id','')
                if influencer_image:
                        influencer_image = "%s%s"%("https://media.licdn.com/media", influencer_image)

		influencer_profile_url = entity.get('publicIdentifier','')
		if influencer_profile_url:
			influencer_profile_url = "https://www.linkedin.com/in/%s/"%(influencer_profile_url)
		influencer_headline = entity.get('occupation', '')
		influencer_no_of_members = data_elements.get('followingInfo',{}).get('followerCount','')#need to add this in table get_influencers data
		item = self.get_influencers_item(sk, influencer_name, influencer_profile_url, influencer_headline, inflencer_first_name, influencer_last_name, influencer_image, str(influencer_no_of_members))
		return item

	def get_influencers_item(self, sk, inf_titf, inf_profile_url, inf_headline, inf_first_name, inf_last_name, inf_member_logo, inf_fol):
		linkedin_inf_ = Linkedinfollowinfluencers()
		linkedin_inf_['sk'] = md5("%s%s%s%s"%(inf_titf, sk, inf_profile_url, inf_headline))
		linkedin_inf_['profile_sk'] = normalize(sk)
		linkedin_inf_['inflencer_name'] = normalize(inf_titf)
		linkedin_inf_['influencer_firstname'] = normalize(inf_first_name)
		linkedin_inf_['influencer_lastname'] = normalize(inf_last_name)
		linkedin_inf_['influencer_image'] = normalize(inf_member_logo)
		linkedin_inf_['influencer_profile_url'] = normalize(inf_profile_url)
		linkedin_inf_['influencer_headline'] = normalize(inf_headline)
		linkedin_inf_['influencer_followers_count'] = normalize(inf_fol)
		if linkedin_inf_['inflencer_name']:
			return linkedin_inf_
		else:
			return ''

	def get_groups_data(self, data_elements, url_type, sk):
		entity = data_elements.get('entity',{}).get('com.linkedin.voyager.entities.shared.MiniGroup',{})
		if url_type == 'schools':
			entity = data_elements.get('entity',{}).get('com.linkedin.voyager.entities.shared.MiniSchool',{})
		if url_type == 'companies':
			entity = data_elements.get('entity',{}).get('com.linkedin.voyager.entities.shared.MiniCompany',{})
		group_description = entity.get('groupDescription','')#neeed to add group_desc in groups table
		group_link = entity.get('objectUrn','')
		group_link = self.get_digit(group_link)
		group_id = group_link
		if group_link:
			if url_type == 'schools':
				group_link = "https://www.linkedin.com/edu/school?id=%s"%(group_link)
			elif url_type == 'companies':
				group_link = "https://www.linkedin.com/company-beta/%s/"%(group_link)
			else:
				group_link = "https://www.linkedin.com/groups?gid=%s&goback="%(group_link)
		group_name = entity.get('groupName','')
		if url_type == 'schools':
			group_name = entity.get('schoolName','')
		if url_type == 'companies':
			group_name = entity.get('name','')

		group_logo = entity.get('logo',{}).get('com.linkedin.voyager.common.MediaProcessorImage',{}).get('id','')
                if group_logo:
                        group_logo = "%s%s"%("https://media.licdn.com/media", group_logo)

		grp_no_members = data_elements.get('followingInfo',{}).get('followerCount','')
		if url_type == 'groups':
			item = self.get_groups_item(sk, group_description, group_link, group_name, str(grp_no_members), group_id, group_logo )
			return item
		if url_type == 'schools':
			item = self.get_schools_item(sk, str(grp_no_members), group_name, group_link, group_logo )
			return item
		if url_type == 'companies':
			item = self.get_companies_item(sk, group_name, group_logo, group_link, str(grp_no_members))
			return item

	def get_companies_item(self, sk, comp_canonicalname, comp_logo, comp_link, companies_count):
		linkedin_comp_ = Linkedinfollowcompanies()
		linkedin_comp_['sk'] = md5("%s%s%s%s%s"%(sk, comp_canonicalname, comp_logo, comp_link, companies_count))
		linkedin_comp_['profile_sk'] = normalize(sk)
		linkedin_comp_['company_canonical_name'] =  normalize(comp_canonicalname)
		linkedin_comp_['total_followee_count'] = normalize(str(companies_count))
		linkedin_comp_['company_logo'] = normalize(comp_logo)
		linkedin_comp_['company_universal_name'] = ''
		linkedin_comp_['company_url'] = normalize(comp_link)
		if linkedin_comp_['company_canonical_name'] or linkedin_comp_['company_universal_name']:
			return linkedin_comp_
		else:
			return ''


	def get_schools_item(self, sk, foll_schools_counts, sch_name, sch_link, sch_image):
		linkedin_scho_ = Linkedinfollowschools()
		linkedin_scho_['sk'] = md5("%s%s%s%s"%(sk, sch_image, sch_name, str(foll_schools_counts)))
		linkedin_scho_['profile_sk'] = normalize(sk)
		linkedin_scho_['school_name'] = normalize(sch_name)
		linkedin_scho_['school_image'] = normalize(sch_image)
		linkedin_scho_['school_region'] = ''
		linkedin_scho_['school_link'] = normalize(sch_link)
		linkedin_scho_['total_followee_count'] = normalize(str(foll_schools_counts))
		if sch_name or sch_region :
			return linkedin_scho_
		else:
			return ''



		


	def get_groups_item(self, sk, grp_desc , grp_link, grp_name, grp_members, grp_id, grp_logo):
		linkedin_groups_ = Linkedingroups()
		linkedin_groups_['sk'] = md5("%s%s%s%s%s"%(sk, grp_link, grp_name, grp_members, grp_id))
		linkedin_groups_['profile_sk'] = normalize(sk)
		linkedin_groups_['group_link'] = normalize(grp_link)
		linkedin_groups_['group_name'] = normalize(grp_name)
		linkedin_groups_['no_of_members'] = normalize(grp_members)
		linkedin_groups_['group_logo'] = normalize(grp_logo)
		linkedin_groups_['group_id'] = normalize(str(grp_id))
		linkedin_groups_['group_description'] = normalize(grp_desc)
		if grp_link or grp_name or grp_members or grp_id:
			return linkedin_groups_
		else:
			return ''

		
	def get_basic_item(self, sk, first_name, entity_urn, headline, industry_name, last_name, location, location_postal_code, location_country_code, version_tag, summary, address, background_image, maiden_name, interests, phonetic_last_name, phonetic_firt_name, state, miniprofile, picture_info, birthdate, object_urn, tracking_id, public_identifier, ref_url, languages_data, connections_count, followers_count):
		linkedin_meta = Linkedinmeta()
		linkedin_meta['sk'] = normalize(sk)
		linkedin_meta['profile_url'] = normalize(ref_url)
		linkedin_meta['profileview_url'] = ''
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
		linkedin_meta['birthday'] = normalize(str(birthdate))
		linkedin_meta['birth_year'] = ''
		linkedin_meta['birth_month'] = ''
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
		languages_data = response.meta.get('languages_data','')
		main_member_id = response.meta.get('main_member_id','')
		connections_count = response.meta.get('connections_count','')
		followers_count = response.meta.get('followers_count','')
		if url_type == 'basic':
			first_name, entity_urn, headline, industry_name, last_name, location, location_postal_code, location_country_code, version_tag, summary, address, background_image, maiden_name, interests, phonetic_last_name, phonetic_firt_name, state, miniprofile, picture_info, birthdate, object_urn, tracking_id, public_identifier = self.get_meta_profile(data)
                        if '/in/' not in main_url:
                                main_url = "https://www.linkedin.com/in/%s/"%public_identifier
			if public_identifier or first_name:
				basic_main_data = self.get_basic_item(sk, first_name, entity_urn, headline, industry_name, last_name, location, location_postal_code, location_country_code, version_tag, summary, address, background_image, maiden_name, interests, phonetic_last_name, phonetic_firt_name, state, miniprofile, picture_info, birthdate, object_urn, tracking_id, public_identifier, main_url, languages_data, connections_count, followers_count)
				if basic_main_data:
					yield basic_main_data
			if public_identifier:
				api_url = [('https://www.linkedin.com/voyager/api/identity/profiles/%s/positions'%public_identifier,'experiences'),('https://www.linkedin.com/voyager/api/identity/profiles/%s/featuredSkills?includeHiddenEndorsers=true&count=50'%public_identifier,'skills'),('https://www.linkedin.com/voyager/api/identity/profiles/%s/volunteerExperiences'%public_identifier,'volunteer'),('https://www.linkedin.com/voyager/api/identity/profiles/%s/recommendations?q=received'%(public_identifier),'received'),('https://www.linkedin.com/voyager/api/identity/profiles/%s/recommendations?q=given'%(public_identifier),'given'), ('https://www.linkedin.com/voyager/api/identity/profiles/%s/projects'%(public_identifier),'projects'),('https://www.linkedin.com/voyager/api/identity/profiles/%s/posts'%(public_identifier),'posts'),('https://www.linkedin.com/voyager/api/identity/profiles/%s/organizations'%(public_identifier),'organizations'),('https://www.linkedin.com/voyager/api/identity/profiles/%s/honors'%(public_identifier),'honors'),('https://www.linkedin.com/voyager/api/identity/profiles/%s/publications'%(public_identifier),'publications'),('https://www.linkedin.com/voyager/api/identity/profiles/%s/courses'%(public_identifier),'courses'),('https://www.linkedin.com/voyager/api/identity/profiles/%s/certifications'%(public_identifier),'certifications'), ('https://www.linkedin.com/voyager/api/identity/profiles/%s/educations'%(public_identifier),'educations'),('https://www.linkedin.com/voyager/api/identity/profiles/%s/following?entityType=GROUP&q=followedEntities'%(public_identifier),'groups'),('https://www.linkedin.com/voyager/api/identity/profiles/%s/following?entityType=SCHOOL&q=followedEntities'%(public_identifier),'schools'),('https://www.linkedin.com/voyager/api/identity/profiles/%s/following?entityType=COMPANY&q=followedEntities'%(public_identifier),'companies'),('https://www.linkedin.com/voyager/api/identity/profiles/%s/following?entityType=INFLUENCER&q=followedEntities'%(public_identifier), 'influencers'),('https://www.linkedin.com/voyager/api/identity/profiles/%s/following?entityType=CHANNEL&q=followedEntities'%(public_identifier),'channel')]
				for api in api_url:
					yield Request(api[0], headers=headers, callback=self.parse_voyage, meta={'url_type':api[1], 'main_url':api[0], 'headers':headers, 'main_member_id':self.get_digit(object_urn),'sk':sk})
		if url_type == 'groups' or url_type == "schools" or url_type == 'companies':#for groups members remaining followers
			for datag in data_elements: #need to change datatype for group logo
				data_groups = self.get_groups_data(datag, url_type, sk)
				if data_groups:
					yield data_groups

		if url_type == 'channel':
			for datac in data_elements:
				data_channel = self.get_channel_data(datac, url_type, sk)
				if data_channel:
					yield data_channel

		if url_type == 'influencers':
			for datain in data_elements:
				data_influencers = self.get_influencers_data(datain, url_type, sk)
				if data_influencers:
					yield data_influencers

		if url_type == 'educations':
			for dataedu  in data_elements:
				data_educations = self.get_educations_data(dataedu, url_type, sk)
				if data_educations:
					yield data_educations

		if url_type == 'certifications':
			for datace in data_elements:
				data_certifications = self.get_certifications_data(datace, url_type, sk)
				if data_certifications:
					yield data_certifications
		if url_type == 'courses':#need to create table for courses and delete course recommendations
			for dataco in data_elements:
				data_courses = self.get_courses_data(dataco, url_type, sk)
				if data_courses:
					yield data_courses

		if url_type == 'publications': #need to create this table
			for datapu in data_elements:
				data_publications = self.get_public_data(datapu, url_type, sk)
				if data_publications:
					yield data_publications

		if url_type == 'honors':
			for datah in data_elements:
				data_honors = self.get_honors_data(datah, url_type, sk)
				if data_honors:
					yield data_honors

		if url_type == 'organizations':
			for datao in data_elements:
				data_org = self.get_orgs_data(datao, url_type, sk)
				if data_org:
					yield data_org
		if url_type == 'posts':
			for datap in data_elements:
				data_posts = self.get_posts_data(datap, url_type, main_member_id, sk)
				if data_posts:
					yield data_posts

		if url_type == 'volunteer':
			for datav in data_elements:
				data_volunteer = self.get_volunteers_data(datav, url_type, sk)
				if data_volunteer:
					yield data_volunteer

		if url_type == 'experiences':
			for datae in data_elements:
				data_return = self.get_experiences_data(datae, url_type, sk)
				if data_return:
					yield data_return
		
                if url_type == 'skills':
                        for datas in data_elements:
                                data_skills = self.get_skills_data(datas, url_type, sk)
				if data_skills:
					yield data_skills
		if url_type == 'received':
			for datar in data_elements:
				data_received = self.get_received_data(datar, url_type, sk)
				if data_received:
					yield data_received

		if url_type == 'given':
			for datag in data_elements:
				data_given = self.get_given_data(datag, url_type, sk)
				if data_given:
					yield data_given

		if url_type == 'projects':
			for datap in data_elements:
				data_projects = self.get_projects_data(datap, url_type, sk)
				if data_projects:
					yield data_projects
				
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
			
					
