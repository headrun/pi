from linkedin_voyager_functions import *

class Imagecheck(scrapy.Spider):
	name = 'profiles_voyager_image_check'
	start_urls = ['https://www.youtube.com/']
	handle_httpstatus_list = [404]

        def __init__(self, name=None, **kwargs):
                super(Imagecheck, self).__init__(name, **kwargs)
		self.type_of_crawl = kwargs.get('crawltype', '')
		self.con, self.cur = get_mysql_connection(DB_HOST, 'FACEBOOK', '')
		self.qu1 = "select sk, pi_id, lnkd_original_url, lnkd_profile_url, candidate_profile_picture, company_logo, company_logo_path, candidate_profile_picture_path from linkedin_mapping_meta where candidate_profile_picture_path != ''"
		self.qu11 = "select sk, pi_id, lnkd_original_url, lnkd_profile_url, candidate_profile_picture, company_logo, company_logo_path, candidate_profile_picture_path from linkedin_mapping_meta where company_logo_path != ''"
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
                self.excel_file_name3 = 'linkedin_unavailable_%s.csv'%str(datetime.datetime.now().date())
                if os.path.isfile(self.excel_file_name3):
                        os.system('rm %s'%self.excel_file_name3)
                oupf3 = open(self.excel_file_name3, 'ab+')
                self.todays_excel_file3  = csv.writer(oupf3)

		self.header_params = ['pi_id', 'lnkd_original_url', 'lnkd_profile_url', 'lnkd_candidate_url[not Available]']
		self.header_params1 = ['pi_id', 'lnkd_original_url', 'lnkd_profile_url', 'lnkd_company_logo_url[not Available]']
		self.header_params2 = ['pi_id', 'lnkd_original_url', 'lnkd_profile_url', 'member_id', 'company_logo', 'candidate_profile_picture', 'company_logo_file_name', 'candidate_profile_picture_file_name', 'company_logo_path', 'candidate_profile_picture_path', 'modified_url']
		self.header_params3 = ['pi_id', 'lnkd_original_url', 'lnkd_profile_url']
		self.todays_excel_file.writerow(self.header_params)
		self.todays_excel_file1.writerow(self.header_params1)
		self.todays_excel_file2.writerow(self.header_params2)
		self.todays_excel_file3.writerow(self.header_params3)
		self.qu2_ = 'select * from linkedin_mapping_meta'
		self.qu3_ = 'select * from linkedin_mapping_meta where member_id = ""'
	
	def parse(self, response):
		if self.type_of_crawl == 'fetch':
			recsq = fetchall(self.cur, self.qu1)
			recsq11 = fetchall(self.cur, self.qu11)
			counter = 0
			os.chdir('/root/Linkedin/Linkedin/spiders/candidate-profile-pictures/full')
			for qrec in recsq:
				sk, pi_id, lnkd_original_url, lnkd_profile_url, candidate_profile_picture, company_logo, company_logo_path, candidate_profile_picture_path = qrec
				if candidate_profile_picture_path:
					file_name = commands.getstatusoutput("ls %s" % candidate_profile_picture_path.split('/')[-1])
					counter += 1
					if 'No such file or directory' in file_name[1]:
						print sk, 'image'
						execute_query(self.cur, self.qu3 % (sk))
						valus = [pi_id, lnkd_original_url, lnkd_profile_url, candidate_profile_picture]
						valus =  [normalize(i) for i in valus]
						self.todays_excel_file.writerow(valus)
					else:
						os.system("cp %s %s" % (candidate_profile_picture_path.split('/')[-1], '/root/Linkedin/Linkedin/spiders/candidate-profile-pictures/'))
				print counter
			print 'candidate profiles checking is completed'
			os.chdir('/root/Linkedin/Linkedin/spiders/company-logo/full')
			counter = 0
			for qrec1 in recsq11:
				sk, pi_id, lnkd_original_url, lnkd_profile_url, candidate_profile_picture, company_logo, company_logo_path, candidate_profile_picture_path = qrec1
				if company_logo_path:
					file_name1 = commands.getstatusoutput("ls %s" % company_logo_path.split('/')[-1])
					if 'No such file or directory' in file_name1[1]:
						print sk, 'logo'
						execute_query(self.cur, self.qu2 % (sk))
						valus1 = [pi_id, lnkd_original_url, lnkd_profile_url, company_logo]
						valus1 =  [normalize(i) for i in valus1]
						self.todays_excel_file1.writerow(valus1)
					else:
						os.system("cp %s %s" % (company_logo_path.split('/')[-1], '/root/Linkedin/Linkedin/spiders/company-logo/'))
				print counter
			print 'company logos checking is completed'

		if self.type_of_crawl == 'in_sheet':
			counter = 0
			recsq = fetchall(self.cur, self.qu2_)
			for qrec in recsq:
				qrec = qrec[1:-3]
				pi_id, lnkd_original_url, lnkd_profile_url, member_id, company_logo, candidate_profile_picture, company_logo_path, candidate_profile_picture_path, modified_url = qrec
				candidate_profile_picture_path1, company_logo_path1 = ['']*2
				if candidate_profile_picture_path:
					candidate_profile_picture_path = candidate_profile_picture_path.split('/')[-1]
					candidate_profile_picture_path1 = '%s%s' % ('/candidate-profile-pictures/', candidate_profile_picture_path)
				if company_logo_path:
					company_logo_path = company_logo_path.split('/')[-1]
					company_logo_path1 = '%s%s' % ('/company-logo/', company_logo_path)
				valus2 = [pi_id, lnkd_original_url, lnkd_profile_url, member_id, company_logo, candidate_profile_picture, company_logo_path, candidate_profile_picture_path, company_logo_path1, candidate_profile_picture_path1, modified_url]
				valus2 =  [normalize(i) for i in valus2]
				self.todays_excel_file2.writerow(valus2)
				counter += 1
				print counter
		if self.type_of_crawl == 'insheet_notmapped':
			counter = 0
			recqr = fetchall(self.cur, self.qu3_)
			for qrec in recqr:
				qrec = qrec[1:-9]
				pi_d, orig_url, pro_ul = qrec
				valus2_ = [pi_d, orig_url, pro_ul]
				valus2_ =  [normalize(i) for i in valus2_]
				self.todays_excel_file3.writerow(valus2_)
				counter += 1
				print counter
			
				
