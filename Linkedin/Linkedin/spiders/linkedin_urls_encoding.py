from linkedin_voyager_functions import *
import csv

class Companyliurls(object):
	def __init__(self, *args, **kwargs):
		self.con, self.cur = get_mysql_connection(DB_HOST, 'FACEBOOK', '')
		self.qu1 = 'select sk, meta_data, url, crawl_status from linkedin_crawltable where meta_data like  "%s"'
		self.qu2 = 'select sk, meta_data, url, crawl_status from LINKEDIN_NEW.linkedin_crawl where meta_data like  "%s"'
		#self.qu3 = 'select name, first_name, last_name, headline, member_id, profile_url  from linkedin_meta where sk like "%s"'
		self.qu3 = 'select * from linkedin_meta where sk like "%s"'
		self.qu4 = 'select sk, meta_data, url, crawl_status from LINKEDIN_VOYAGER_CRAWL.linkedin_crawl where meta_data like  "%s"'	
		self.headers = ['profile_url','profileview_url','name','first_name','last_name','member_id','headline','no_of_followers','profile_post_url','summary','number_of_connections','industry','location','languages','emails','websites','addresses','message_handles','phone_numbers','birthday','birth_year','birth_month','twitter_accounts','profile_image','interests','location_postal_code','location_country_code', 'given_data', 'given_url_in_file', 'status', 'encode_values_in_db_but_not_in_sheet']
		self.excel_file_name = 'linkedin_urls_result.csv'
		if os.path.isfile(self.excel_file_name):
			os.system('rm %s'%self.excel_file_name)
		oupf = open(self.excel_file_name, 'ab+')
		self.todays_excel_file  = csv.writer(oupf)

	def main(self):
		with open('linkedin_urls.txt', 'r') as f:
			rows = f.readlines()
			for inde, row in enumerate(rows):
				row = row.strip('\n')
				pattern = "%s%s%s" % ('%', row, '%')
				data = fetchmany(self.cur, self.qu1% pattern)
				if not data:
					data = fetchmany(self.cur, self.qu2 % pattern)
				if data:
					tup_data = data[0]
					sk, meta_data, url, crawl_status = tup_data
					new_sk = sk[0:25]
					pa_new_sk  = "%s%s%s" % ('%', new_sk, '%')
					data1 = fetchmany(self.cur, self.qu3 % pa_new_sk)
					if not data1:
						tup_data1 = fetchmany(self.cur, self.qu4 % pattern)
						if tup_data1:
							tup_data1 = tup_data1[0]
							sk, meta_data, url, crawl_status = tup_data1
							new_sk = sk[0:25]
							pa_new_sk  = "%s%s%s" % ('%', new_sk, '%')
							data1 = fetchmany(self.cur, self.qu3 % pa_new_sk)
					final_list = []
					if  data1:
						
						"""name, first_name, last_name, headline, member_id, profile_url = data1[0]
						row_valus = [meta_data, name, first_name, last_name, headline, member_id, profile_url, row]
						row_valus[0] = row_valus[0].replace('{','').replace('}','').replace('"','')
						print row_valus"""
						meta_data = meta_data.replace('{','').replace('}','').replace('"','')
						fileds_list = list(data1)[0]
						final_list = list(fileds_list)[1:-5]
						#fil_list = list(chain.from_iterable(fileds_list))[1:-5]
						final_list.extend([meta_data, row,'Available'])
						
					else:
						print 'no_data in db', row, '>>>', crawl_status, pa_new_sk
						final_list = ['' for i in self.headers]
						final_list = final_list[:-1]
						final_list[-1] = 'Not Available'
						final_list[-2] = row
					if inde == 0:
						self.todays_excel_file.writerow(self.headers)
					final_list = [str(row1) if isinstance(row1, long) else row1 for row1 in final_list]
					is_acii = 'no'
					try:
						print final_list[2]
					except:
						is_acii = 'yes'
					final_list = [i.encode('utf8') for i in final_list]
					final_list.extend([is_acii])
					self.todays_excel_file.writerow(final_list)
				else:
					print 'no data' , row
	
if __name__ == '__main__':
	Companyliurls().main()
