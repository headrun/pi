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
		sk = response.meta.get('sk','')
		profile_data = json.loads(''.join(sel.xpath('//code[contains(text(),"profile.ProfileView")]/text()').extract()))
		keyword = 'com.linkedin.voyager.identity.profile.'
		data_json = profile_data.get('included',[])
		basic_data = filter(None, [i if i['$type'] == "%s%s"%(keyword,'Profile') else ''for i in data_json])
		skills_data = filter(None, [i if i['$type'] == "%s%s"%(keyword,'Skill') else ''for i in data_json])
		certifi_data = filter(None, [i if i['$type'] == "%s%s"%(keyword,'Certification') else ''for i in data_json])
		contributors_data = filter(None, [i if i['$type'] == "%s%s"%(keyword,'Contributor') else ''for i in data_json])
		honors_data = filter(None, [i if i['$type'] == "%s%s"%(keyword,'Honor') else '' for i in data_json])
		picture_data = filter(None, [i if i['$type'] == "%s%s"%(keyword,'Picture') else ''for i in data_json])
		experiences_data = filter(None, [i if i['$type'] == "%s%s"%(keyword,'Position') else ''for i in data_json])
		if basic_data:
			basic_dat = basic_data[0]
			first_name, entity_urn, headline, industry_name,\
			last_name, location, version_tag, summary, address,\
			background_image, maiden_name, interests, phonetic_last_name,\
			phonetic_firt_name, state = self.get_meta_profile(basic_dat)
		if experiences_data:
			experiences_dat = self.get_type_data(experiences_data,'experiences')
		if honors_data:
			honors_dat = self.get_type_data(honors_data,'honors')
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
			
			
			 
		import pdb;pdb.set_trace()
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
		version_tag = basic_dat.get('versionTag','')#birthDate
		summary = basic_dat.get('summary','')
		address = basic_dat.get('address','')
		background_image = basic_dat.get('backgroundImage','')#need to check for one url#urn:li:fs_profile:ACoAAAA3LYwBc6wnTI5z--QGOwRXb9Go6py9TbA,backgroundImage
		maiden_name = basic_dat.get('maidenName','')
		interests = basic_dat.get('interests','')
		phonetic_last_name = basic_dat.get('phoneticLastName','')
		phonetic_firt_name = basic_dat.get('phoneticFirstName','')
		state = basic_dat.get('state','')
		miniprofile = basic_dat.get('miniProfile','')#urn:li:fs_miniProfile:ACoAAAA3LYwBc6wnTI5z--QGOwRXb9Go6py9TbA
		picture_info = basic_dat.get('pictureInfo','')#urn:li:fs_profile:ACoAAAA3LYwBc6wnTI5z--QGOwRXb9Go6py9TbA,pictureInfo
		birthdate = basic_dat.get('birthDate','')#urn:li:fs_profile:ACoAAAA3LYwBc6wnTI5z--QGOwRXb9Go6py9TbA,birthDate
		
		return first_name, entity_urn, headline, industry_name, last_name, location, version_tag, summary, address,\
		background_image, maiden_name, interests, phonetic_last_name, phonetic_firt_name, state

	def get_type_data(self, type_data, type_name):
		list_of_type = []
		for types in type_data:
			keywords, keyvalue = types
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
			if keyvalue == 'skill':
				set_of_type = [type_name, type_entity_urn]
			elif keyvalue == 'contributor':
				set_of_type = [type_name, type_entity_urn, type_member]
			elif keyvalue == 'honor':
				set_of_type = [type_title, type_description, type_occupation, type_issuer, type_issue_date, type_entity_urn ]
			elif keyvalue == 'experiences':
				set_of_type = [type_title, type_time_period, type_location_name, type_company_name, type_description, type_entity_urn]
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
			
		

	def parse_voyage(self, response):
		import pdb;pdb.set_trace()
			
					
		
		
	
	    



	

