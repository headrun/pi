from linkedin_voyager_functions import *
from Linkedin.items import *

class Profileimage(scrapy.Spider):
	name = 'profiles_image_browse'
	start_urls = ['https://www.youtube.com/']
	handle_httpstatus_list = [404]

        def __init__(self, name=None, **kwargs):
                super(Profileimage, self).__init__(name, **kwargs)
		self.type_of_crawl = kwargs.get('crawltype', '')
		self.con, self.cur = get_mysql_connection(DB_HOST, DB_NAME_REQ, '')
		self.qu1 = "select sk, profile_image from FACEBOOK.linkedin_meta where member_id = '%s'"
		self.qu2 = "update FACEBOOK.linkedin_meta set image_path = '%s' where sk = '%s'"
		self.qu3 = "update FACEBOOK.linkedin_meta set image_path = '%s' where member_id = '%s'"
		self.qu4  = "select sk, member_id, profile_image, image_path, profile_url  from FACEBOOK.linkedin_meta where image_path != '';"
			
	
	def parse(self, response):
		if self.type_of_crawl == 'yield':
			#with open('/root/kiranmayi/Linkedin/Linkedin/spiders/image_ids_list', 'r') as f:
			with open('/root/kiranmayi/Linkedin/Linkedin/spiders/image_ids_list1', 'r') as f:
				counter = 0
				rows = f.readlines()
				for row in rows:
					counter +=1
					recs = fetchmany(self.cur, self.qu1%row)
					for index, rec in enumerate(recs):
						sk, image = rec
						hashs = hashlib.sha1(image.encode('utf-8', 'strict')).hexdigest()
						yield ImageItem(image_urls=[image])
						image_path = "%s%s%s"%("/root/Linkedin/Linkedin/spiders/images/full/",hashs,'.jpg')
						execute_query(self.cur, self.qu2%(image_path, sk))
						execute_query(self.cur, self.qu3%(image_path, row))
						print counter

		if self.type_of_crawl == 'fetch':
			recsq = fetchall(self.cur, self.qu4)
			counter = 0
			for qrec in recsq:
				sk, member_id, profile_image, image_path, profile_url = qrec
				image_hash_name = image_path.split('/')[-1]
				real_path = os.path.dirname(os.path.realpath(__file__))
				os.chdir('/root/Linkedin/Linkedin/spiders/images/full')
				file_name = commands.getstatusoutput("ls %s"%image_hash_name)
				if 'No such file or directory' in file_name[1]:
					counter += 1
					print sk, member_id, profile_url
					file("image_ids_list1","ab+").write("%s\n" %member_id)
					print counter
			
			
		
				
					
					
			
			
			
