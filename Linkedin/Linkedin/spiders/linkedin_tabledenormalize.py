import MySQLdb
import json
import datetime
import md5
from itertools import chain
import re
import os

class Litablespremium(object):

    def __init__(self, *args, **kwargs):
        self.con = MySQLdb.connect(db   = 'FACEBOOK', \
        host = 'localhost', charset="utf8", use_unicode=True, \
        user = 'root', passwd ='root')
        self.cur = self.con.cursor()
	self.file_dirs = os.path.join(os.getcwd(),'OUTPUT')
	self.QUERY_FILES_DIR = os.path.join(self.file_dirs, 'processing')
	self.QUERY_FILES_CRAWLOUT_DIR = os.path.join(self.file_dirs, 'crawl_out')
	self.na = 'linkedin_all'
	self.tables_file = self.get_tables_file()
	self.query2 = "select sk, url, meta_data, crawl_status from linkedin_crawl where date(modified_at)>= '2017-03-27'"
	self.list_tables = ['linkedin_educations', 'linkedin_experiences', 'linkedin_honors','linkedin_certifications','linkedin_courserecommendations','linkedin_following_channels','linkedin_following_companies','linkedin_following_influencers','linkedin_following_schools','linkedin_given_recommendations','linkedin_groups','linkedin_organizations','linkedin_posts','linkedin_projects','linkedin_received_recommendations','linkedin_volunteer_experiences', 'linkedin_skills']
	self.quer = 'INSERT INTO linkedin_all(sk,  original_url,  id,  status_of_url,  data_available_flag, profile_url, profileview_url, name, first_name, last_name, member_id, headline, no_of_followers, profile_post_url, summary, number_of_connections, industry, location, languages, emails, websites, addresses, message_handles, phone_numbers, birthday, birth_year, birth_month, twitter_accounts, profile_image, interests, linkedin_educations, linkedin_experiences, linkedin_honors, linkedin_certifications, linkedin_courserecommendations, linkedin_following_channels, linkedin_following_companies, linkedin_following_influencers, linkedin_following_schools, linkedin_given_recommendations, linkedin_groups, linkedin_organizations, linkedin_posts, linkedin_projects, linkedin_received_recommendations, linkedin_volunteer_experiences, linkedin_skills, created_at, modified_at, last_seen) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(), sk=%s, original_url=%s, id=%s, status_of_url=%s, data_available_flag=%s, profile_url=%s, profileview_url=%s, name=%s, first_name=%s, last_name=%s, member_id=%s, headline=%s, no_of_followers=%s, profile_post_url=%s, summary=%s, number_of_connections=%s, industry=%s, location=%s, languages=%s, emails=%s, websites=%s, addresses=%s, message_handles=%s, phone_numbers=%s, birthday=%s, birth_year=%s, birth_month=%s, twitter_accounts=%s, profile_image=%s, interests=%s, linkedin_educations=%s, linkedin_experiences=%s, linkedin_honors=%s, linkedin_certifications=%s, linkedin_courserecommendations=%s, linkedin_following_channels=%s, linkedin_following_companies=%s, linkedin_following_influencers=%s, linkedin_following_schools=%s, linkedin_given_recommendations=%s, linkedin_groups=%s, linkedin_organizations=%s, linkedin_posts=%s, linkedin_projects=%s, linkedin_received_recommendations=%s, linkedin_volunteer_experiences=%s, linkedin_skills=%s'


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


    def restore(self, text):
        text = text.replace('<>#<>','"').replace("<>##<>","'").replace('###',',')
        return text
    def get_current_ts_with_ms(self):
    	dt = datetime.datetime.now().strftime("%Y%m%dT%H%M%S%f")
	return dt


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
        #text = text.replace('"','<>#<>').replace("'","<>##<>").replace(',','###')
	text = text.replace(' :- ','').replace('<br>','').replace('</br>','').replace('  ','').strip()
        return text

    def colum (self, table, sk ):
	q5 = 'SELECT COLUMN_NAME FROM information_schema.columns where table_schema= "%s" and table_name = "%s"'%('FACEBOOK', table)
	self.cur.execute(q5)
	fields = self.cur.fetchall()
	fileds_list = list(fields)
	fil_list = list(chain.from_iterable(fileds_list))[2:-3]
	q9  = 'select * from %s where profile_sk="%s"'%(table, sk)
	self.cur.execute(q9)
	countrec = self.cur.fetchall()
	cntf_ = {}
	if countrec:
		cntf = map(lambda x:(x[2:-3]), countrec)
		for ind_, recv in enumerate(cntf, start=1):
			inner_cntf = {}
			list_con = list(recv)
			lis_key  = filter(None, map(lambda a,b: (a+' :--- '+self.replacefun(b)) if b else '', fil_list, recv))	
			for innerky in lis_key:
				keyf, valuef =  innerky.split(' :--- ')
				inner_cntf.update({keyf:valuef})
			cntf_.update({ind_:inner_cntf})
	if not cntf_: cntf_ = ''
	else: cntf_ = json.dumps(cntf_)
	return cntf_


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

    def send_tables(self):
	counter = 0
	self.cur.execute(self.query2)
	records = self.cur.fetchall()
	for inde, rec in enumerate(records):
		values_final = []
		sk = list(rec)[0]
		as_sk = sk
		sk = sk[:-7]
                json_meta = json.loads(rec[2])
                given_url = json_meta.get('linkedin_url','')
                given_id = json_meta.get('id','')
                given_firstname = json_meta.get('firstname','')
                given_lastname = json_meta.get('lastname','')
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
		values_final.extend([as_sk, given_url, given_id, status_url, data_avai])
		callfun3 = self.metadesign('linkedin_meta', sk, inde)
		values_final.extend(callfun3)
		if values_final[7] == '':
			values_final[7] = "%s%s%s"%(given_firstname, ' ', given_lastname)
			values_final[8] = given_firstname
			values_final[9] = given_lastname
		for tabl in self.list_tables:
			calfun2 = self.colum(tabl, sk)
			values_final.append(calfun2)
		values_final =  [self.normalize(i) for i in values_final]
		values_final.extend(values_final)
		#self.cur.execute(self.quer%tuple(values_final))
		self.tables_file.write('%s\n%s\n' %(self.quer, tuple(values_final)))
		self.tables_file.flush()
		print inde
	self.close_all_opened_query_files()
		
		
    def main(self):
	self.send_tables()

if __name__ == '__main__':
        Litablespremium().main()

