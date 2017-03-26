import xlwt
import MySQLdb
import json
import datetime
import md5
from itertools import chain
import re
import csv

class Licsvfilepremium(object):

    def __init__(self, *args, **kwargs):
        self.con = MySQLdb.connect(db   = 'FACEBOOK', \
        host = 'localhost', charset="utf8", use_unicode=True, \
        user = 'root', passwd ='root')
        self.cur = self.con.cursor()
        self.row_count = 1
        self.excel_file_name = 'linkedin_profiles_premium_%s.csv'%str(datetime.datetime.now().date())
	oupf = open(self.excel_file_name, 'ab+')
	self.todays_excel_file  = csv.writer(oupf)
	self.header_params =  []
	self.query2 = "select sk, url, meta_data, crawl_status from linkedin_crawl"
	self.list_tables = ['linkedin_certifications','linkedin_courserecommendations','linkedin_following_channels','linkedin_following_companies','linkedin_following_influencers','linkedin_following_schools','linkedin_given_recommendations','linkedin_groups','linkedin_organizations','linkedin_posts','linkedin_projects','linkedin_received_recommendations','linkedin_skills','linkedin_volunteer_experiences']
	self.list_tables1 = ['linkedin_educations','linkedin_experiences','linkedin_honors']

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
    def querydesign(self,tble, sk):
	q2 = 'SELECT COLUMN_NAME FROM information_schema.columns where table_schema= "%s" and table_name = "%s"'%('FACEBOOK', tble)
	self.cur.execute(q2)
	fields = self.cur.fetchall()
	fileds_list = list(fields)
	fil_list = list(chain.from_iterable(fileds_list))[2:-3]
	self.header_params.extend([tble])
	q1 = 'select * from %s where profile_sk="%s"'%(tble, sk)
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
	q6 = "select count(*)  from %s group by profile_sk order by count(*) desc limit 1"%table
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
	q9  = 'select * from %s where profile_sk="%s"'%(table, sk)
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
	q0 = 'SELECT COLUMN_NAME FROM information_schema.columns where table_schema= "%s" and table_name = "%s"'%('FACEBOOK', table)
        self.cur.execute(q0)
        fields = self.cur.fetchall()
        fileds_list = list(fields)
        fil_list = list(chain.from_iterable(fileds_list))[1:-3]
	if inde == 0: self.header_params.extend(fil_list)
	q8 = 'select * from %s where sk ="%s"'%(table, sk)
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

    def send_xls(self):
	self.cur.execute(self.query2)
	records = self.cur.fetchall()
	for inde, rec in enumerate(records):
		values_final = []
		sk = list(rec)[0]
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
		elif rec[3] == 10:
			status_url = 'Not Valid'
			data_avai = 'Not Available'
		if '/profile/view?id' in given_url: genuni = 'DOUBT'
		if inde == 0: self.header_params.extend(['original_url','id', 'status of url','Data Available/UnAvailable','GENUINITY'])
		values_final.extend([given_url, given_id, status_url, data_avai, genuni])
		callfun3 = self.metadesign('linkedin_meta', sk, inde)
		values_final.extend(callfun3)
		if values_final[7] == '':
			values_final[7] = "%s%s%s"%(given_firstname, ' ', given_lastname)
			values_final[8] = given_firstname
			values_final[9] = given_lastname
		for tabl in self.list_tables:
			callfun = self.querydesign(tabl, sk)
			values_final.extend([callfun])
		for tabl in self.list_tables1:
			calfun2 = self.colum(tabl, sk, inde)
			values_final.extend(calfun2)
		values_final =  [self.normalize(i) for i in values_final]
		if inde == 0:
			self.todays_excel_file.writerow(self.header_params)
		self.todays_excel_file.writerow(values_final)

def main():
        obj = Licsvfilepremium()
        obj.send_xls()
if __name__ == '__main__':
        main()

