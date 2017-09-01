from linkedin_voyager_functions import *

class Companylidsurls(object):
	def __init__(self, *args, **kwargs):
		self.con, self.cur = get_mysql_connection(DB_HOST, 'FACEBOOK', '')
		#self.qu1 = 'select profile_sk , connections_profile_url from linkedin_connections where date(modified_at)>"2017-04-17" and date(modified_at)<"2017-08-21" and member_id = "%s"'
		self.qu1 = "select distinct member_id  from  linkedin_meta where date(modified_at) < '2017-08-20'"
		self.qu2 = "select distinct member_id  from  linkedin_connections where date(modified_at) > '2017-08-20'"
		self.query2 = "select connections_profile_url, member_id, sk from FACEBOOK.linkedin_connections where date(modified_at) >= '2017-08-20'"
                self.excel_file_name = 'linkedin_connections_profiles_%s.csv'%str(datetime.datetime.now().date())
                if os.path.isfile(self.excel_file_name):
                        os.system('rm %s'%self.excel_file_name)
                oupf = open(self.excel_file_name, 'ab+')
                self.todays_excel_file  = csv.writer(oupf)
                self.headers = ['Linkedin_Profile_url', 'member_id']
		self.todays_excel_file.writerow(self.headers)

		

	def main(self):
		"""with open('duplicate_members', 'r') as f:
			rows = f.readlines()
			for inde, row in enumerate(rows):
				row = row.strip('\n')
				one_ = fetchmany(self.cur, self.qu1 % row)
				pf_sk = '<>'.join([i[0] for i in one_])
				pf_url = '<>'.join([i[0] for i in one_])
				file("duplicate_member_info","ab+").write("%s, %s, %s\n" % (row, pf_sk, pf_url))"""
		re1 = fetchall(self.cur, self.qu1)
		re2 = fetchall(self.cur, self.qu2)
		re2 = [str(i[0]) for i in re2]
		re1 = [str(i[0]) for i in re1]
		new_list = []
		for i  in re1:
			 if i in re2:
				new_list.append(i)
		print len(new_list)
		total_distinct_list = []
		total_connection_records = fetchall(self.cur, self.query2)
		for tocr in total_connection_records:
			linkedin_profilef, member_id, connection_sk = tocr
			if member_id in new_list:
				continue
			total_distinct_list.append((linkedin_profilef, member_id))
		print len(total_distinct_list), 'total_length'
		print len(set(total_distinct_list)), 'total_distinct_lenth'
		total_distinct_list = set(total_distinct_list)
		for  tdl in total_distinct_list:
			lk_url, mem_id = tdl
			values = [lk_url, mem_id]
			values = [normalize(i) for i in values]
			self.todays_excel_file.writerow(values)
			
			
		
		
		
	
if __name__ == '__main__':
	Companylidsurls().main()
