import xlwt
import MySQLdb
import json
import datetime
import md5
from itertools import chain
import re
import os

class Lifilepde(object):

    def __init__(self, *args, **kwargs):
        self.con = MySQLdb.connect(db   = 'FACEBOOK', \
        host = 'localhost', charset="utf8", use_unicode=True, \
        user = 'root', passwd ='root')
        self.cur = self.con.cursor()
        self.file_dirs = os.path.join(os.getcwd(),'OUTPUT')
        self.QUERY_FILES_DIR = os.path.join(self.file_dirs, 'processing')
        self.QUERY_FILES_CRAWLOUT_DIR = os.path.join(self.file_dirs, 'crawl_out')
        self.na = 'linkedin_newless'
        self.tables_file = self.get_tables_file()
	#self.query2 = "select sk, url, meta_data, crawl_status from linkedin_crawl where date(modified_at)>= '2017-03-27' and date(modified_at) < '2017-04-07'"
	self.query2 = "select sk, url, meta_data, crawl_status from linkedin_crawl where date(modified_at) >= '2017-04-12'"
	self.list_tables = ['linkedin_certifications','linkedin_courserecommendations','linkedin_following_channels','linkedin_following_companies','linkedin_following_influencers','linkedin_following_schools','linkedin_given_recommendations','linkedin_groups','linkedin_organizations','linkedin_posts','linkedin_projects','linkedin_received_recommendations','linkedin_skills','linkedin_volunteer_experiences']
	self.list_tables1 = ['linkedin_educations','linkedin_experiences','linkedin_honors']
	self.altertable = 'alter table linkedin_newless add column %s %s COLLATE utf8_unicode_ci after %s'
	self.altertable1 = 'alter table linkedin_newless add column %s %s after %s'
	self.quer1 = 'INSERT INTO linkedin_newless ('
	self.quer2 = ['sk', 'original_url', 'id', 'status_of_url', 'data_available_flag', 'email_id','profile_url', 'profileview_url', 'name', 'first_name', 'last_name', 'member_id', 'headline', 'no_of_followers', 'profile_post_url', 'summary', 'number_of_connections', 'industry', 'location', 'languages', 'emails', 'websites', 'addresses', 'message_handles', 'phone_numbers', 'birthday', 'birth_year', 'birth_month', 'twitter_accounts', 'profile_image', 'interests']

    def restore(self, text):
        text = text.replace('<>#<>','"').replace("<>##<>","'").replace('###',',').replace('\\','')
        if '<>' in text:
            text = set(text.split('<>'))
            text = '<>'.join(text)
        return text

    def xcode(self, text, encoding='utf8', mode='strict'):
        return text.encode(encoding, mode) if isinstance(text, unicode) else text

    def md5(self, x):
        return hashlib.md5(self.xcode(x)).hexdigest()

    def replacefun(self, text):
        text = text.replace('"','<>#<>').replace("'","<>##<>").replace(',','###').replace(u'\u2013','').strip()
        return text

    def restore(self, text):
        text = text.replace('<>#<>','"').replace("<>##<>","'").replace('###',',')
        return text

    def clean(self, text):
        if not text: return text
        value = text
        value = re.sub("&amp;", "&", value)
        value = re.sub("&lt;", "<", value)
        value = re.sub("&gt;", ">", value)
        value = re.sub("&quot;", '"', value)
        value = re.sub("&apos;", "'", value)

        return value

    def normalize(self, text):
        return self.clean(self.compact(self.xcode(text)))

    def compact(self, text, level=0):
        if text is None: return ''
        if level == 0:
            text = text.replace("\n", " ")
            text = text.replace("\r", " ")
        compacted = re.sub("\s\s(?m)", " ", text)
        if compacted != text:
            compacted = self.compact(compacted, level+1)
	return compacted.strip()


    def replacefun(self, text):
        text = text.replace('"','<>#<>').replace("'","<>##<>").replace(',','###')
        return text

    def querydesign(self,tble, sk, lasttbl, hindex):
	q2 = 'SELECT COLUMN_NAME FROM information_schema.columns where table_schema= "%s" and table_name = "%s"'%('FACEBOOK', tble)
	self.cur.execute(q2)
	fields = self.cur.fetchall()
	fileds_list = list(fields)
	fil_list = list(chain.from_iterable(fileds_list))[2:-3]
	q1 = 'select * from %s where profile_sk="%s" and date(modified_at)>= "2017-03-27"'%(tble, sk)
	self.cur.execute(q1)
	values = self.cur.fetchall()
	final_to_update = []
	for val in values:
		vals_ = list(val)[2:-3]
		valf = filter(None, map(lambda a,b: (a+':-'+b) if b else '', fil_list,vals_))
		final_to_update.append(', '.join(valf))
	if hindex == 0:
		"""try: self.cur.execute(self.altertable%(tble, 'longtext',lasttbl))
		except: pass"""
		try: self.cur.execute(self.altertable%(tble, 'longtext',lasttbl))
		except: import pdb;pdb.set_trace()
		
		self.quer2.extend([tble])
	return ' <> '.join(final_to_update)

    def colum (self, table, sk, inde, lastbln):
	q5 = 'SELECT COLUMN_NAME FROM information_schema.columns where table_schema= "%s" and table_name = "%s"'%('FACEBOOK', table)
	self.cur.execute(q5)
	fields = self.cur.fetchall()
	fileds_list = list(fields)
	fil_list = list(chain.from_iterable(fileds_list))[2:-3]
	q6 = "select count(*)  from %s where date(modified_at)>= '2017-04-12' group by profile_sk order by count(*) desc limit 1"%table
	self.cur.execute(q6)
	large_count = self.cur.fetchall()
	max_count = ''
	try: max_count = int(large_count[0][0])
	except: max_count = ''
	"""vatab = []
	if max_count:
		for fi in range(1,max_count+1):
			vatab.append(table+str(fi))"""
	va = []
        if max_count:
                for fi in range(1,max_count+1):
                        for fl in fil_list:
                                va.append(fl+str(fi))
	#if vatab: lastbln = vatab[-1]	
	if inde == 0 and va:
		for vac in va:
			"""try:
				if 'summary' in vac or 'logo' in vac:
 					self.cur.execute(self.altertable%(vac, "text",lastbln))
					print self.altertable%(vac, "text",lastbln)
				else:
					self.cur.execute(self.altertable1%(vac, "varchar(255) NOT NULL DEFAULT ''",lastbln))
					print self.altertable1%(vac, "varchar(255) NOT NULL DEFAULT ''",lastbln)
				lastbln = vac
			except: pass"""

			self.cur.execute(self.altertable%(vac, "text",lastbln))
			#print self.altertable%(vac, "text",lastbln)
			lastbln = vac

			self.quer2.extend([vac])
	q9  = 'select * from %s where profile_sk="%s" and date(modified_at)>= "2017-03-27"'%(table, sk)
	self.cur.execute(q9)
	countrec = self.cur.fetchall()
	cntf_ = []
	if countrec:
		cntf = map(lambda x:(x[2:-3]), countrec)
		cntf_ = list(chain.from_iterable(cntf))
		"""for recv in cntf:
			inner_cntf = []
			list_con = list(recv)
			lis_key  = filter(None, map(lambda a,b: (a+':- '+b) if b else '', fil_list, recv))
			cntf_.append(', '.join(lis_key))"""
	if len(cntf_) != len(va):
		lnewln = len(va) - len(cntf_)
		cntf_.extend(['']*lnewln)
	return cntf_, lastbln

    def metadesign(self, table, sk, inde):
	q0 = 'SELECT COLUMN_NAME FROM information_schema.columns where table_schema= "%s" and table_name = "%s"'%('FACEBOOK', table)
        self.cur.execute(q0)
        fields = self.cur.fetchall()
        fileds_list = list(fields)
        fil_list = list(chain.from_iterable(fileds_list))[1:-3]
	q8 = 'select * from %s where sk ="%s" and date(modified_at)>= "2017-03-27"'%(table, sk)
        self.cur.execute(q8)
        values = self.cur.fetchall()
	cntf_ = []
	if values:
        	vals_ = map(lambda x:(x[1:-3]), values)
		cntf_ = list(chain.from_iterable(vals_))
	if len(cntf_) != len(fil_list):
		lnewln = len(fil_list) - len(cntf_)
		cntf_.extend(['']*lnewln)
	return cntf_

    def get_current_ts_with_ms(self):
        dt = datetime.datetime.now().strftime("%Y%m%dT%H%M%S%f")
        return dt
    def get_tables_file(self):
        tables_queries_filename = os.path.join(self.QUERY_FILES_CRAWLOUT_DIR, "%s_%s.queries" % (self.na, self.get_current_ts_with_ms()))
        self.tables_file = open(tables_queries_filename, 'w')
        return self.tables_file

    def move_file(self, source, dest):
        cmd = "mv %s %s" % (source, dest)
        os.system(cmd)


    def close_all_opened_query_files(self):
        files_list = [self.tables_file]

        for f in files_list:
            if not isinstance(f, file): continue
            f.flush()
            f.close()
            self.move_file(f.name, self.QUERY_FILES_DIR)



    def send_xls(self):
	counter = 0
	self.cur.execute(self.query2)
	records = self.cur.fetchall()
	for inde, rec in enumerate(records):
		values_final = []
		sk = list(rec)[0]
		old_sk = sk
		sk = sk[:-7]
                json_meta = json.loads(rec[2])
                given_url = json_meta.get('linkedin_url','')
                given_id = json_meta.get('id','')
                given_firstname = json_meta.get('firstname','')
                given_lastname = json_meta.get('lastname','')
		given_email = json_meta.get('email_address','')
		status_url, data_avai = ['']*2
		genuni = 'GENUINE'
		if rec[3] == 1 or rec[3] == 9:
			status_url = 'Valid'
			data_avai = 'Available'
		elif rec[3] == 6:
			status_url = 'Valid'
			data_avai = 'Not Available'
		elif rec[3] == 10 or rec[3] == 5:
			status_url = 'Not Valid'
			data_avai = 'Not Available'
		values_final.extend([old_sk, given_url, given_id, status_url, data_avai, given_email])
		callfun3 = self.metadesign('linkedin_meta', sk, inde)
		values_final.extend(callfun3)
		"""her_values = values_final
		her_values.extend(her_values)
		self.cur.execute(self.quer%tuple(her_values))"""
		if values_final[7] == '':
			values_final[7] = "%s%s%s"%(given_firstname, ' ', given_lastname)
			values_final[8] = given_firstname
			values_final[9] = given_lastname
		lasttablename = ''
		for tabl in self.list_tables:
			if inde == 0: lasttablename = 'interests'
			callfun = self.querydesign(tabl, sk, lasttablename, inde)
			lasttablename = tabl
			values_final.extend([callfun])
		for tabl in self.list_tables1:
			if inde == 0: lasttablenames = lasttablename
			calfun2, lastin = self.colum(tabl, sk, inde, lasttablenames)
			lasttablenames = tabl
			values_final.extend(calfun2)
		values_final =  [self.normalize(i) for i in values_final]
		final_qryto = "%s%s%s%s%s%s"%(self.quer1,', '.join(self.quer2), ', created_at, modified_at, last_seen) values (' , ', '.join(['%s' for i in range(len(self.quer2))]), ', now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(), ', ', '.join([str(i)+'=%s' for i in self.quer2]))
		values_final.extend(values_final)
                self.tables_file.write('%s\n%s\n' %(final_qryto, tuple(values_final)))
                self.tables_file.flush()
		print inde, sk
		print counter
        self.close_all_opened_query_files()

def main():
        obj = Lifilepde()
        obj.send_xls()
if __name__ == '__main__':
        main()

