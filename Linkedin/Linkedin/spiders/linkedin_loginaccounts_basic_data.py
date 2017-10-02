from stats_gen_functions import *
import os
import datetime

class FacebookScript1(object):
    def __init__(self):
        self.con = MySQLdb.connect(db='FACEBOOK',user='root',passwd='root',
                      charset="utf8",host='localhost',use_unicode=True)
	self.excel_file_name = 'linkedin_login_connections_data_%s.csv' % (str(datetime.datetime.now().date()))
	if os.path.isfile(self.excel_file_name):
		os.system('rm %s'%self.excel_file_name)
	oupf = open(self.excel_file_name, 'ab+')
	self.todays_excel_file  = csv.writer(oupf)
	self.header_params =  ['first_name', 'last_name', 'profile_url', 'connection_first_name', 'connection_last_name', 'connection_profile_url']
	self.todays_excel_file.writerow(self.header_params)
        self.cur = self.con.cursor()
	self.cur.execute("select profile_sk from linkedin_connections where profile_sk!='368972887kiranmayi-cheedella-b87699a3' and profile_sk!='24983769rajaemmela' group by profile_sk")
	dic = self.cur.fetchall()
	dic_sks = [di[0] for di in dic]
	self.dic_acconts = {}
	for dic_sk in dic_sks:
		member_id = re.findall('(\d+)', dic_sk)[0]
		profile_u = dic_sk.split(member_id)[-1]
		prof_co = 'https://www.linkedin.com/in/%s' % profile_u
		self.cur.execute('select first_name, last_name from linkedin_meta where member_id="%s" order by last_seen desc limit 1' % member_id)
		tow = self.cur.fetchall()
		firs,last = tow[0]
		values = [member_id, prof_co, firs,last]
		self.dic_acconts.update({dic_sk:values})
	self.select_query = "Select member_id, connections_profile_url, name from linkedin_connections where profile_sk='%s'"
	self.meta = "Select first_name,last_name, profile_url from linkedin_meta where member_id='%s' order by last_seen desc limit 1"
	self.main()

    def main(self):
	counter = 0
	for keys, values in self.dic_acconts.iteritems():
		self.cur.execute(self.select_query % keys)
		all_sk_records = self.cur.fetchall()
		for index, dats in enumerate(all_sk_records):
		    mem_id = normalize(dats[0])
		    connections_profile_url = dats[1]
		    name = normalize(dats[2])
		    details = self.meta%(mem_id)
		    self.cur.execute(details)
		    dat1 = self.cur.fetchall()
		    c_first_name, c_last_name = ['']*2
		    if dat1:
			c_first_name = dat1[0][0]
			c_last_name = dat1[0][1]
			connections_profile_url = dat1[0][2]
		    vm, vu, vf, vn = self.dic_acconts.get(keys)
		    values = [vf, vn, vu, c_first_name, c_last_name, connections_profile_url]
		    values =  [normalize(i) for i in values]
		    counter += 1
		    self.todays_excel_file.writerow(values)
		    print counter

if __name__ == '__main__':
    FacebookScript1()
