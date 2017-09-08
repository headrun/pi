from linkedin_voyager_functions import *

class Imagecheck(scrapy.Spider):
	name = 'profiles_voyager_image_check'
	start_urls = ['https://www.youtube.com/']
	handle_httpstatus_list = [404]

        def __init__(self, name=None, **kwargs):
                super(Imagecheck, self).__init__(name, **kwargs)
		self.type_of_crawl = kwargs.get('crawltype', '')
		self.con, self.cur = get_mysql_connection(DB_HOST, 'FACEBOOK', '')
		self.qu1 = "select sk, pi_id, lnkd_original_url, lnkd_profile_url, candidate_profile_picture, company_logo, company_logo_path, candidate_profile_picture_path from linkedin_mapping_meta where company_logo_path != '' or candidate_profile_picture_path != ''"
		self.qu2 = "update linkedin_mapping_meta set company_logo_path = '' where sk = '%s'"
		self.qu3 = "update linkedin_mapping_meta set candidate_profile_picture_path = '' where sk = '%s'"
		self.excel_file_name = 'linkedin_candidate_profiles_notavailable_data_%s.csv'%str(datetime.datetime.now().date())
		if os.path.isfile(self.excel_file_name):
			os.system('rm %s'%self.excel_file_name)
		oupf = open(self.excel_file_name, 'ab+')
		self.todays_excel_file  = csv.writer(oupf)
		self.excel_file_name1 = 'linkedin_company_logosnotavailable_data_%s.csv'%str(datetime.datetime.now().date())
                if os.path.isfile(self.excel_file_name1):
                        os.system('rm %s'%self.excel_file_name1)
                oupf1 = open(self.excel_file_name1, 'ab+')
                self.todays_excel_file1  = csv.writer(oupf1)
                self.excel_file_name2 = 'linkedin_downloaded_image_%s.csv'%str(datetime.datetime.now().date())
                if os.path.isfile(self.excel_file_name2):
                        os.system('rm %s'%self.excel_file_name2)
                oupf2 = open(self.excel_file_name2, 'ab+')
                self.todays_excel_file2  = csv.writer(oupf2)
		self.header_params = ['pi_id', 'lnkd_original_url', 'lnkd_profile_url', 'lnkd_candidate_url[not Available]']
		self.header_params1 = ['pi_id', 'lnkd_original_url', 'lnkd_profile_url', 'lnkd_company_logo_url[not Available]']
		self.header_params2 = ['pi_id', 'lnkd_original_url', 'lnkd_profile_url', 'member_id', 'company_logo', 'candidate_profile_picture', 'company_logo_file_name', 'candidate_profile_picture_file_name', 'modified_url']
		self.todays_excel_file.writerow(self.header_params)
		self.todays_excel_file1.writerow(self.header_params1)
		self.todays_excel_file2.writerow(self.header_params2)
		self.qu2_ = 'select * from linkedin_mapping_meta'
	
	def parse(self, response):
		if self.type_of_crawl == 'fetch':
			recsq = fetchall(self.cur, self.qu1)
			counter = 0
			for qrec in recsq:
				sk, pi_id, lnkd_original_url, lnkd_profile_url, candidate_profile_picture, company_logo, company_logo_path, candidate_profile_picture_path = qrec
				os.chdir('/root/Linkedin/Linkedin/spiders/candidate-profile-pictures/full')
				file_name = commands.getstatusoutput("ls %s" % candidate_profile_picture_path.split('/')[-1])
				counter += 1
				if 'No such file or directory' in file_name[1]:
					print sk, 'image'
					execute_query(self.cur, self.qu3 % (sk))
					valus = [pi_id, lnkd_original_url, lnkd_profile_url, candidate_profile_picture]
					valus =  [normalize(i) for i in valus]
					self.todays_excel_file.writerow(valus)
				os.chdir('/root/Linkedin/Linkedin/spiders/company-logo/full')
				file_name1 = commands.getstatusoutput("ls %s" % company_logo_path.split('/')[-1])
				if 'No such file or directory' in file_name[1]:
					print sk, 'logo'
					execute_query(self.cur, self.qu2 % (sk))
					valus1 = [pi_id, lnkd_original_url, lnkd_profile_url, company_logo]
					valus1 =  [normalize(i) for i in valus1]
					self.todays_excel_file1.writerow(valus1)

		if self.type_of_crawl == 'in_sheet':
			counter = 0
			recsq = fetchall(self.cur, self.qu2_)
			for qrec in recsq:
				qrec = qrec[1:-3]
				pi_id, lnkd_original_url, lnkd_profile_url, member_id, company_logo, candidate_profile_picture, company_logo_path, candidate_profile_picture_path, modified_url = qrec
				if candidate_profile_picture_path:
					candidate_profile_picture_path = candidate_profile_picture_path.split('/')[-1]
				if company_logo_path:
					company_logo_path = company_logo_path.split('/')[-1]
				valus2 = [pi_id, lnkd_original_url, lnkd_profile_url, member_id, company_logo, candidate_profile_picture, company_logo_path, candidate_profile_picture_path, modified_url]
				valus2 =  [normalize(i) for i in valus2]
				self.todays_excel_file2.writerow(valus2)
				counter += 1
				print counter
			
			
			
		
				
					
					
			
			
			
