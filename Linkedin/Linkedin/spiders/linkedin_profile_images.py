from linkedin_voyager_functions import *
from Linkedin.items import *
from linkedin_profile_images_queries import *

class Profileimage(scrapy.Spider):
	name = 'profiles_image_browse'
	start_urls = ['https://www.youtube.com/']
	handle_httpstatus_list = [404]

        def __init__(self, name=None, **kwargs):
                super(Profileimage, self).__init__(name, **kwargs)
		self.type_of_crawl = kwargs.get('crawltype', '')
		self.limit = kwargs.get('limit','1000')
		self.con, self.cur = get_mysql_connection(DB_HOST, DB_NAME_REQ, '')
		cv1 = "limit %s"%(self.limit)
		qu13 = qu13+cv1
	
	def parse(self, response):
		if self.type_of_crawl == 'denormalization':
			recs = fetchall(self.cur, qu18)
			for rc in recs:
				pf_imag, img_path = fetchmany(self.cur, qu19 % rc) [0]
				execute_query(self.cur, qu20 % (pf_imag, img_path, rc[0]))
			
		if self.type_of_crawl == 'yield':
			with open('image_ids_list1', 'r') as f:
				counter = 0
				rows = f.readlines()
				for row in rows:
					counter +=1
					recs = fetchmany(self.cur, qu1%row)
					for index, rec in enumerate(recs):
						sk, image = rec
						if not image: continue
						hashs = hashlib.sha1(image.encode('utf-8', 'strict')).hexdigest()
						yield ImageItem(image_urls=[image])
						image_path = "%s%s%s"%(image_full_path, hashs,'.jpg')
						execute_query(self.cur, qu2%(image_path, sk, row))
		if self.type_of_crawl == 'updatingprofileurl':
			recs = fetchall(self.cur, qu13)
			counter = 0
			for rcs in recs:
				counter += 1
				get_pr_url = fetchone(self.cur, qu14%rcs)
				execute_query(self.cur, qu15%(get_pr_url, rcs[0]))
		if self.type_of_crawl == 'connection':
			recsc = fetchall(self.cur, qu5)
			for rcs in recsc:
				countc, me_id, pr_imurl, pr_impath = rcs
				execute_query(self.cur, qu7%(pr_imurl, pr_impath, me_id))
		if self.type_of_crawl == 'missed':
			with open('missedimageids','r') as f:
				rows = f.readlines()
				for row in rows:
					recs = fetchmany(self.cur, qu8%normalize(row))
					me_id, pr_imurl, pr_impath = recs[0]
					counter += 1
					execute_query(self.cur, qu7%(pr_imurl, pr_impath, me_id))
		if self.type_of_crawl == 'emptypath':
			recsq = fetchmany(self.cur, qu9)
			for qrec in recsq:
				sk, member_id, profile_image, image_path, profile_url = qrec
				hashs = hashlib.sha1(profile_image.encode('utf-8', 'strict')).hexdigest()
				yield ImageItem(image_urls=[profile_image])
				image_path = "%s%s%s"%(image_full_path, hashs, '.jpg')
				execute_query(self.cur, qu2%(image_path, sk, member_id))
		if self.type_of_crawl == 'emptyimage':
			recsq = fetchmany(self.cur, qu10)
			for qrec in recsq:
				sk, member_id, profile_image, image_path, profile_url = qrec
				get_img = fetchone(self.cur, qu11%member_id)
				execute_query(self.cur, qu12%(get_img, sk, member_id))
		if self.type_of_crawl == 'fetch':
			if os.path.isfile('image_ids_list1'):
				os.system('rm image_ids_list1')
			recsq = fetchall(self.cur, qu4)
			for qrec in recsq:
				sk, member_id, profile_image, image_path, profile_url = qrec
				image_hash_name = image_path.split('/')[-1]
				real_path = os.path.dirname(os.path.realpath(__file__))
				os.chdir(image_full_path)
				file_name = commands.getstatusoutput("ls %s"%image_hash_name)
				if 'No such file or directory' in file_name[1]:
					file("image_ids_list1","ab+").write("%s\n" %member_id)
		if self.type_of_crawl == 'ldeveloperall':
			recs = fetchall(self.cur, qu17)
			for rec in recs:
				sk, image, profile_url,row = rec
				profile_vanityname  =  profile_url.split('/')
				if profile_url.endswith('/') or profile_url.endswith('/en'):
					profile_vanityname = profile_vanityname[-2]
				else:
					profile_vanityname = profile_vanityname[-1]
				developer_pf_url = pulse_url % profile_vanityname
				yield Request(developer_pf_url, callback=self.parse_developer, meta={'sk':sk, 'image':image, 'profile_url':profile_url, 'member_id':str(row)}, dont_filter=True)

	def parse_developer(self, response):
		sel = Selector(response)
		sk = response.meta.get('sk','')
		image = ''
		member_id = response.meta.get('member_id','').strip('\n')
		if 'cws/member/public_profile' in response.url:
			image = extract_data(sel, '//div[@class="member-photo"]/img/@src')
		else:
			try:
				sel = json.loads(response.body)
				image = sel.get('image','').get('url','')
			except:
				pass
			
		if 'icon_no_photo' in image or 'ghost_person' in image:
			image = ''
		if image:
			hashs = hashlib.sha1(image.encode('utf-8', 'strict')).hexdigest()
			yield ImageItem(image_urls=[image])
			image_path = "%s%s%s"%(images_full_path, hashs,'.jpg')
			execute_query(self.cur, qu7%(image, image_path, member_id))
			execute_query(self.cur, qu21 % (image, image_path, member_id))
		else:
			execute_query(self.cur, qu2%('', sk, member_id ))
			execute_query(self.cur, qu22%('', member_id ))
			
			
		
				
					
					
			
			
			
