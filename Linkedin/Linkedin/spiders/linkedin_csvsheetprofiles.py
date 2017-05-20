from linkedin_functions import *
import cProfile

class Licsvfilepremium(object):

    def __init__(self, *args, **kwargs):
	self.con, self.cur = get_mysql_connection(DB_HOST, REQ_DB_NAME, '')
	self.modified_at     = options.modified_at
        self.excel_file_name = 'linkedin_profiles58501_2500_%s.csv'%str(datetime.datetime.now().date())
	if os.path.isfile(self.excel_file_name):
		os.system('rm %s'%self.excel_file_name)
	oupf = open(self.excel_file_name, 'ab+')
	self.todays_excel_file  = csv.writer(oupf)
	self.header_params =  []
	self.size = 1000
	patternk = '%keys%'
	self.query2 = "select sk, url, meta_data, crawl_status from LINKEDIN_NEW.linkedin_crawl where date(created_at) >= '%s' limit 58501, 2500"%(self.modified_at)
	#self.query2 = "select sk, url, meta_data, crawl_status from FACEBOOK.linkedin_crawl where date(modified_at) >= '%s'"%(self.modified_at)
	self.list_tables = ['linkedin_certifications','linkedin_courserecommendations','linkedin_following_channels','linkedin_following_companies','linkedin_following_influencers','linkedin_following_schools','linkedin_given_recommendations','linkedin_groups','linkedin_organizations','linkedin_posts','linkedin_projects','linkedin_received_recommendations','linkedin_skills','linkedin_volunteer_experiences']
	self.list_tables1 = ['linkedin_educations','linkedin_experiences','linkedin_honors']

        q0 = 'SELECT COLUMN_NAME FROM information_schema.columns where table_schema= "%s" and table_name = "%s"'%('FACEBOOK', 'linkedin_meta')
        self.cur.execute(q0)
        fields = self.cur.fetchall()
        fileds_list = list(fields)
        self.fil_list = list(chain.from_iterable(fileds_list))[1:-3]

	self.main()

    def __del__(self):
        self.con.close()
        self.cur.close()

    def querydesign(self,tble, sk):
	q2 = 'SELECT COLUMN_NAME FROM information_schema.columns where table_schema= "%s" and table_name = "%s"'%('FACEBOOK', tble)
	self.cur.execute(q2)
	fields = self.cur.fetchall()
	fileds_list = list(fields)
	fil_list = list(chain.from_iterable(fileds_list))[2:-3]
	self.header_params.extend([tble])
	q1 = 'select * from %s where profile_sk="%s" and date(modified_at)>= "%s"'%(tble, sk, self.modified_at)
	self.cur.execute(q1)
	values = self.cur.fetchall()
	final_to_update = []
	for val in values:
		vals_ = list(val)[2:-3]
		valf = filter(None, map(lambda a,b: (a+':-'+b) if b else '', fil_list,vals_))
		final_to_update.append(', '.join(valf))
	return ' <> '.join(final_to_update)

    def colum (self, table, sk, inde):
	q5 = 'SELECT COLUMN_NAME FROM information_schema.columns where table_schema= "%s" and table_name = "%s"'%('FACEBOOK', table)
	self.cur.execute(q5)
	fields = self.cur.fetchall()
	fileds_list = list(fields)
	fil_list = list(chain.from_iterable(fileds_list))[2:-3]
	q6 = "select count(*)  from %s where date(modified_at)>= '%s' group by profile_sk order by count(*) desc limit 1"%(table, self.modified_at)
	self.cur.execute(q6)
	large_count = self.cur.fetchall()
	max_count = ''
	try: max_count = int(large_count[0][0])
	except: max_count = ''
	va = []
	if max_count:
		for fi in range(1,max_count+1):
			for fl in fil_list:
				va.append(fl+str(fi))
	if inde == 0: self.header_params.extend(va)
	q9  = 'select * from %s where profile_sk="%s" and date(modified_at)>= "%s"'%(table, sk, self.modified_at)
	self.cur.execute(q9)
	countrec = self.cur.fetchall()
	cntf_ = []
	if countrec:
		cntf = map(lambda x:(x[2:-3]), countrec)
		cntf_ = list(chain.from_iterable(cntf))
	if len(cntf_) != len(va):
		lnewln = len(va) - len(cntf_)
		cntf_.extend(['']*lnewln)
	return cntf_

    def metadesign(self, table, sk, inde):
	if inde == 0: self.header_params.extend(self.fil_list)
	q8 = 'select * from %s where sk ="%s" and date(modified_at)>= "%s"'%(table, sk, self.modified_at)
        self.cur.execute(q8)
        values = self.cur.fetchall()
	cntf_ = []
	if values:
        	vals_ = map(lambda x:(x[1:-3]), values)
		cntf_ = list(chain.from_iterable(vals_))
	if len(cntf_) != len(self.fil_list):
		lnewln = len(self.fil_list) - len(cntf_)
		cntf_.extend(['']*lnewln)
	return cntf_

    def send_xls(self):
	self.cur.execute(self.query2)
	records = self.cur.fetchall()
	for inde, rec in enumerate(records):
		values_final = []
		sk = list(rec)[0]
		sk = sk[:-7]
		url_re = rec[1]
                json_meta = json.loads(rec[2])
                given_url = json_meta.get('linkedin_url','')
                given_id = json_meta.get('id','')
                given_firstname = json_meta.get('firstname','')
                given_lastname = json_meta.get('lastname','')
		email_id = json_meta.get('email_address','')
		keysf = json_meta.get('key','')
		if not keysf: keysf = json_meta.get('keys','')
		status_url, data_avai = ['']*2
		genuni = 'GENUINE'
		if rec[3] == 1:
			status_url = 'Valid'
			data_avai = 'Available'
		elif rec[3] == 6:
			status_url = 'Valid'
			data_avai = 'Not Available'
		elif rec[3] == 10 or rec[3] == 5:
			status_url = 'Not Valid'
			data_avai = 'Not Available'
		if inde == 0: self.header_params.extend(['original_url','id', 'status of url','Data Available/UnAvailable', 'email_id', 'key'])
		values_final.extend([given_url, given_id, status_url, data_avai, email_id, keysf])
		callfun3 = self.metadesign('linkedin_meta', sk, inde)
		values_final.extend(callfun3)
					
		if values_final[8] == '':
			values_final[8] = "%s%s%s"%(given_firstname, ' ', given_lastname)
			values_final[9] = given_firstname
			values_final[10] = given_lastname
		if values_final[6] == '': values_final[6] = url_re
		for tabl in self.list_tables:
			callfun = self.querydesign(tabl, sk)
			values_final.extend([callfun])
		for tabl in self.list_tables1:
			calfun2 = self.colum(tabl, sk, inde)
			values_final.extend(calfun2)
		values_final =  [normalize(i) for i in values_final]
		if inde == 0:
			self.todays_excel_file.writerow(self.header_params)
		print inde, sk
		self.todays_excel_file.writerow(values_final)
		

    def main(self):
        self.send_xls()
if __name__ == '__main__':
	parser = optparse.OptionParser()
	parser.add_option('-m', '--modified-at', default='', help = 'modified_at')
	(options, args) = parser.parse_args()
        Licsvfilepremium(options)

