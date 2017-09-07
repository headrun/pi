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
		self.get_query_param1 = "select sk, candidate_profile_picture  from linkedin_mapping_meta where candidate_profile_picture != ''  limit 1"
		self.update_imag_path1 = 'update linkedin_mapping_meta set candidate_profile_picture_path = "%s" where sk = "%s"'
		self.get_query_param2 = "select sk, company_logo from linkedin_mapping_meta where company_logo != ''  limit 1"
		self.update_imag_path2 = 'update linkedin_mapping_meta set company_logo_path = "%s" where sk = "%s"'

   	def spider_closed(self, spider):
		close_mysql_connection(self.con, self.cur)

	def parse(self, response):
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
