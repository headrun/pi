from linkedin_voyage_queries import *
from linkedin_voyager_utils import *

class Linkedinimagesvoyager(Voyagerapi):
	name = "linkedinapi_images_browse"
	allowed_domains = ["linkedin.com"]
	start_urls = ('https://www.linkedin.com/uas/login?goback=&trk=hb_signin',)

	def __init__(self, *args, **kwargs):
		super(Linkedinimagesvoyager, self).__init__(*args, **kwargs)
                self.login = kwargs.get('login', 'ramanujan')
                self.con, self.cur = get_mysql_connection(DB_HOST, 'FACEBOOK', '')
                get_query_param = "select sk, profile_sk, image_url from linkedin_connections where image_url != '' and image_path = '' limit 1000"
		self.update_imag_path = "update linkedin_connections set image_path = '%s' where sk = '%s' and profile_sk = '%s'"
                self.cur.execute(get_query_param)
                self.profiles_list = [i
                    for i in self.cur.fetchall()
                ]
                dispatcher.connect(self.spider_closed, signals.spider_closed)
                self.domiain = domain_premium

   	def spider_closed(self, spider):
		close_mysql_connection(self.con, self.cur)

	def parse(self, response):
		for img in self.profiles_list:
			sk, profile_sk, image_url = img
			if image_url:
				yield ImageItem(image_urls=[image_url])
				hashs = hashlib.sha1((image_url).encode('utf-8', 'strict')).hexdigest()
				image_here_path = "%s%s%s"%(profile_images_path, hashs, '.jpg')
				execute_query(self.cur, self.update_imag_path % (image_here_path, sk, profile_sk))
				print sk
			
			
