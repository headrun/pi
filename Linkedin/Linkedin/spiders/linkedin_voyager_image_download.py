from linkedin_voyage_queries import *
from linkedin_voyager_utils import *

class Linkedinimagesvoyager(Voyagerapi):
	name = "linkedinapi_images_browse"
	allowed_domains = ["linkedin.com"]
	start_urls = ('https://www.linkedin.com/uas/login?goback=&trk=hb_signin',)

	def __init__(self, *args, **kwargs):
		super(Linkedinimagesvoyager, self).__init__(*args, **kwargs)
		self.type_of_crawl = kwargs.get('crawl_type', '')
                self.con, self.cur = get_mysql_connection(DB_HOST, 'FACEBOOK', '')
                get_query_param = "select sk, profile_sk, image_url from linkedin_connections where image_url != '' and image_path = '' limit 1000"
		self.update_imag_path = "update linkedin_connections set image_path = '%s' where sk = '%s' and profile_sk = '%s'"
                self.cur.execute(get_query_param)
                self.profiles_list = [i
                    for i in self.cur.fetchall()
                ]
                dispatcher.connect(self.spider_closed, signals.spider_closed)
                self.domiain = domain_premium
		self.get_query_param1 = "select sk, candidate_profile_picture  from linkedin_mapping_meta where candidate_profile_picture != ''  and candidate_profile_picture_path = '' limit 1000"
		self.update_imag_path1 = 'update linkedin_mapping_meta set candidate_profile_picture_path = "%s" where sk = "%s"'
		self.get_query_param2 = "select sk, company_logo from linkedin_mapping_meta where company_logo != ''  and company_logo_path = '' limit 1000"
		self.update_imag_path2 = 'update linkedin_mapping_meta set company_logo_path = "%s" where sk = "%s"'
		self.get_query_param5 = "select sk, lnkd_original_url, modified_url from linkedin_mapping_meta where member_id = ''"
		self.pulse_url = 'https://www.linkedin.com/pulse-fe/api/v1/followableEntity?vanityName=%s'
		self.qu4 = 'select sk, member_id, profile_image, profile_url from linkedin_meta where member_id  = "%s" order by modified_at desc limit 1'
		self.qu3 = 'select exp_company_logo from linkedin_experiences where profile_sk = "%s" limit 1'
		self.qu6 = 'update linkedin_mapping_meta set member_id="%s", candidate_profile_picture = "%s", company_logo="%s", modified_at=now() where sk = "%s"'

   	def spider_closed(self, spider):
		close_mysql_connection(self.con, self.cur)

	def linkedin_pub_url(self, linkedin_profilef):
		if 'http:' in linkedin_profilef:
			linkedin_profilef = linkedin_profilef.replace('http:', 'https:')
	        if 'id.www' in linkedin_profilef:
        		linkedin_profilef = linkedin_profilef.replace('id.www', 'https://www')
	        if 'www.linkedin.com' and 'https:' not in linkedin_profilef:
        		linkedin_profilef = linkedin_profilef.replace('www.', 'https://www')
        	if linkedin_profilef.startswith('linkedin.com'):
            		linkedin_profilef = linkedin_profilef.replace('linkedin.com', 'https://www.linkedin.com')
	        if 'https:' not in linkedin_profilef:
        		linkedin_profilef = re.sub('(\D+)\.linkedin.com', 'https://www.linkedin.com', linkedin_profilef) 
	        linkedin_profilef = re.sub('https://(.*?).linkedin.com/', 'https://www.linkedin.com/', linkedin_profilef)
        	if linkedin_profilef.endswith('/en') or linkedin_profilef.endswith('/fr'):
            		linkedin_profilef = linkedin_profilef[:-3]
        	linkedin_profilef = linkedin_profilef.strip('"').strip().strip("'").strip().strip('/').strip()
        	if not linkedin_profilef.startswith('https://www.linkedin.com'):
            		linkedin_profilef = ''.join(re.findall('.*(https://.*)', linkedin_profilef))
        	if '/pub/' in linkedin_profilef:
            		cv = ''.join(filter(None, re.split('https://www.linkedin.com/pub/.*?/(.*)', linkedin_profilef))).split('/')[::-1]
            		cv[0] = cv[0].zfill(3)
            		cv[1] = cv[1].zfill(3)
            		if cv[-1] == '0': del cv[-1]
            		linkedin_profilef = ('%s%s%s%s' % ('https://www.linkedin.com/in/', ''.join(re.findall('https://www.linkedin.com/pub/(.*?)/.*', linkedin_profilef)), '-', ''.join(cv)))
        	return linkedin_profilef


	def parse(self, response):
		if self.type_of_crawl == 'without_member_id':
			profiles_list5 = fetchall(self.cur, self.get_query_param5)
			for pf5 in profiles_list5:
				sk, link_or_url, mf_url = pf5
				link_ori_url = self.linkedin_pub_url(link_or_url)
				member_id, exp_company_logo, candidate_profile_picture = ['']*3
				if 'view?id='  in link_ori_url:
					recs = fetchmany(self.cur, 'select member_id from linkedin_meta where profileview_url = "%s" '% link_ori_url)
					if recs:
						member_id = recs[0][0]
				else:
					link_ori_url_van = link_ori_url.strip('/').split('/')[-1]
					developer_pf_url = self.pulse_url % link_ori_url_van
					try:
						reql = json.loads(requests.get(developer_pf_url).text)
						reql_member_id = reql.get('urn', '')
						if reql_member_id:
							member_id = reql_member_id.split('urn:li:member:')[1]
					except:
						pass
				if member_id:
					rowp = fetchmany(self.cur, self.qu4 % member_id)
					if rowp:
						sk_, member_id, candidate_profile_picture, modified_url = rowp[0]
						rowcm = fetchmany(self.cur, self.qu3 % sk_)
						if rowcm:
							exp_company_logo = rowcm[0][0]
						execute_query(self.cur, self.qu6 %(member_id, candidate_profile_picture, exp_company_logo, sk))
						
				else:
					file("mapping_meta_new2","ab+").write("%s\n" % link_or_url)
					
		if self.type_of_crawl == 'connections':
			for img in self.profiles_list:
				sk, profile_sk, image_url = img
				if image_url:
					yield ImageItem(image_urls=[image_url])
					hashs, image_here_path = self.parse_basic(image_url, profile_images_path)
					execute_query(self.cur, self.update_imag_path % (image_here_path, sk, profile_sk))
		if self.type_of_crawl == 'profilepicture_download':
			profiles_list1 = fetchall(self.cur, self.get_query_param1)
			counter = 0
			for img1 in profiles_list1:
				sk, candidate_profile_picture = img1
				if candidate_profile_picture:
					yield ImageItem(image_urls=[candidate_profile_picture])
					hashs, image_here_path = self.parse_basic(candidate_profile_picture, '/root/Linkedin/Linkedin/spiders/candidate-profile-pictures/full/')
					execute_query(self.cur, self.update_imag_path1 % (image_here_path, sk))
					counter += 1
					print counter, sk, 'pf'
		if self.type_of_crawl == 'companylogo_download':
			profiles_list2 = fetchall(self.cur, self.get_query_param2)
			counter = 0
			for img2 in profiles_list2:
				sk, company_logo = img2
				if company_logo:
					yield ImageItem(image_urls=[company_logo])
					hashs, image_here_path = self.parse_basic(company_logo, '/root/Linkedin/Linkedin/spiders/company-logo/full/')
					execute_query(self.cur, self.update_imag_path2 % (image_here_path, sk))
					counter += 1
					print counter, sk, 'logo'

	def parse_basic(self, candidate_profile_picture, path):
		hashs = hashlib.sha1((candidate_profile_picture).encode('utf-8', 'strict')).hexdigest()
		image_here_path = "%s%s%s"%(path, hashs, '.jpg')
		return hashs, image_here_path
