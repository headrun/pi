import xlwt
import MySQLdb
import json
import datetime
from itertools import chain

class Lixlsfilepremium(object):

    def __init__(self, *args, **kwargs):
        self.con = MySQLdb.connect(db   = 'FACEBOOK', \
        host = 'localhost', charset="utf8", use_unicode=True, \
        user = 'root', passwd ='root')
        self.cur = self.con.cursor()
        self.row_count = 1
        self.excel_file_name = 'linkedin_profiles_premium_%s.xls'%str(datetime.datetime.now().date())
        self.todays_excel_file = xlwt.Workbook(encoding="utf-8")
        self.todays_excel_sheet1 = self.todays_excel_file.add_sheet("sheet1")
	self.header_params = ['profile_url', 'profileview_url', 'name', 'first_name', 'last_name', 'member_id', 'headline', 'no_of_followers', 'profile_post_url', 'summary', 'number_of_connections', 'industry', 'location', 'languages', 'emails', 'websites', 'addresses', 'message_handles', 'phone_numbers', 'birthday', 'birth_year', 'birth_month', 'twitter_accounts', 'profile_image', 'interests']
	self.query1 = "select sk,profile_url,profileview_url,name,first_name,last_name,member_id,headline,no_of_followers,profile_post_url,summary,number_of_connections,industry,location,languages,emails,websites,addresses,message_handles,phone_numbers,birthday,birth_year,birth_month,twitter_accounts,profile_image,interests from linkedin_meta"

	self.list_tables = ['linkedin_certifications','linkedin_courserecommendations','linkedin_following_channels','linkedin_following_companies','linkedin_following_influencers','linkedin_following_schools','linkedin_given_recommendations','linkedin_groups','linkedin_organizations','linkedin_posts','linkedin_projects','linkedin_received_recommendations','linkedin_skills','linkedin_volunteer_experiences']
	self.list_tables1 = ['linkedin_educations','linkedin_experiences','linkedin_honors']
        #for i, row in enumerate(header_params):
            #self.todays_excel_sheet1.write(0, i, row)

    def restore(self, text):
        text = text.replace('<>#<>','"').replace("<>##<>","'").replace('###',',').replace('\\','')
        if '<>' in text:
            text = set(text.split('<>'))
            text = '<>'.join(text)
        return text

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
		#valf = map(lambda x,y:x+':- '+y if y,fil_list,vals_)
		#valf = map(lambda x,y:x+':- '+y, fil_list,vals_)
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
	

    def send_xls(self):
	self.cur.execute(self.query1)
	records = self.cur.fetchall()
	for inde, rec in enumerate(records):
		values_final = []
		rec_f = list(rec)[1:]
		values_final.extend(rec_f)
		sk = list(rec)[0]
		for tabl in self.list_tables:
			callfun = self.querydesign(tabl, sk)
			values_final.extend([callfun])
		for tabl in self.list_tables1:
			calfun2 = self.colum(tabl, sk, inde)
			values_final.extend(calfun2)
		if inde == 0:
			for i, row in enumerate(self.header_params):
				self.todays_excel_sheet1.write(0, i, row)
		for col_count, value in enumerate(values_final):
			self.todays_excel_sheet1.write(self.row_count, col_count, value)
		self.row_count = self.row_count+1
	self.todays_excel_file.save(self.excel_file_name)

def main():
        obj = Lixlsfilepremium()
        obj.send_xls()
if __name__ == '__main__':
        main()

