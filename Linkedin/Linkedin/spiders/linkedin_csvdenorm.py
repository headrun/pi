from linkedin_voyager_functions import *
from linkedin_queries import *

class Lifilepde(object):

    def __init__(self, *args, **kwargs):
	self.modified_at     = options.modified_at
	self.table_flag = options.table_creation_needed
	self.limit = options.limit
	self.con, self.cur = get_mysql_connection(DB_HOST, DB_NAME_REQ, '')
        self.file_dirs = os.path.join(os.getcwd(),'OUTPUT')
        self.QUERY_FILES_DIR = os.path.join(self.file_dirs, 'processing')
        self.QUERY_FILES_CRAWLOUT_DIR = os.path.join(self.file_dirs, 'crawl_out')
        self.tables_file = self.get_tables_file()
	self.query2 = "select sk, url, meta_data, crawl_status from linkedin_crawl where date(created_at) >= '%s'"%(self.modified_at)
	self.quer1 = 'INSERT INTO %s ('%table_name_denor
	self.quer2 = quer2_denor
	self.member_id_track = 'select member_id from linkedin_track where sk = "%s"'
	if self.table_flag:
		self.check()
	if self.limit:
		self.main()

    def check(self):
	pattern_toc = "%s%s%s"%("%",table_name_denor,"%")
	table_check = fetchmany(self.cur, 'show tables like "%s"'%pattern_toc)
	if table_check:
		execute_query(self.cur, 'drop table %s'%table_name_denor)
	execute_query(self.cur, create_table_denor%table_name_denor)
	
    def querydesign(self,tble, sk, lasttbl, hindex):
	q2 = q0_denor%('FACEBOOK', tble)
	fields = fetchmany(self.cur, q2)
	fileds_list = list(fields)
	fil_list = list(chain.from_iterable(fileds_list))[2:-3]
	q1 = q9_denor%(tble, sk, self.modified_at)
	values =  fetchmany(self.cur, q1)
	final_to_update = []
	for val in values:
		vals_ = list(val)[2:-3]
		vals_ = [str(row) if isinstance(row, long) else row for row in vals_]
		valf = filter(None, map(lambda a,b: (a+':-'+b) if b else '', fil_list,vals_))
		final_to_update.append(', '.join(valf))
	if hindex == 0:
		if self.table_flag:
			execute_query(self.cur, altertable_denor%(table_name_denor, tble, 'longtext',lasttbl))
		self.quer2.extend([tble])
	return ' <> '.join(final_to_update)

    def colum (self, table, sk, inde, lastbln):
	q5 = q0_denor%('FACEBOOK', table)
	fields = fetchmany(self.cur, q5)
	fileds_list = list(fields)
	fil_list = list(chain.from_iterable(fileds_list))[2:-3]
	if 'linkedin_educations' in table:
		fil_list = list(chain.from_iterable(fileds_list))[2:-5]
	q6 = q6_denor%(table, self.modified_at)
	large_count = fetchmany(self.cur, q6)
	max_count = ''
	try: max_count = int(large_count[0][0])
	except: max_count = ''
	va = []
        if max_count:
                for fi in range(1,max_count+1):
                        for fl in fil_list:
                                va.append(fl+str(fi))
	if inde == 0 and va:
		for vac in va:
			try: 
				if self.table_flag: execute_query(self.cur, altertable_denor%(table_name_denor, vac, "text",lastbln))
			except: import pdb;pdb.set_trace()
			lastbln = vac
			self.quer2.extend([vac])
	q9  = q9_denor%(table, sk, self.modified_at)
	countrec =  fetchmany(self.cur, q9)
	cntf_ = []
	if countrec:
		cntf = map(lambda x:(x[2:-3]), countrec)
		if  'linkedin_educations' in table:
			cntf = map(lambda x:(x[2:-5]), countrec)
		cntf_ = list(chain.from_iterable(cntf))
	if len(cntf_) != len(va):
		lnewln = len(va) - len(cntf_)
		cntf_.extend(['']*lnewln)
	return cntf_, lastbln

    def metadesign(self, table, sk, inde):
	q0 = q0_denor%('FACEBOOK', table)
	fields = fetchmany(self.cur, q0)
        fileds_list = list(fields)
        fil_list = list(chain.from_iterable(fileds_list))[1:-3]
	q8 = q8_denor%(table, sk, self.modified_at)
	values = fetchmany(self.cur, q8)
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
        tables_queries_filename = os.path.join(self.QUERY_FILES_CRAWLOUT_DIR, "%s_%s_%s.queries" % (table_name_denor, self.limit,self.get_current_ts_with_ms()))
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
                get_meb_records = fetchmany(self.cur, self.member_id_track % rec[0])
                sk = get_meb_records[0][0]
                sk_crawl = list(rec)[0]
		url_re = rec[1]
                json_meta = json.loads(rec[2])
                given_url = json_meta.get('linkedin_url','')
                given_id = json_meta.get('id','')
                given_firstname = json_meta.get('firstname','')
                given_lastname = json_meta.get('lastname','')
		given_email = json_meta.get('email_address','')
                keysf = json_meta.get('key','')
                if not keysf: keysf = json_meta.get('keys','')
		status_url, data_avai = ['']*2
		if rec[3] == 1 or rec[3] == 9:
			status_url = 'Valid'
			data_avai = 'Available'
		elif rec[3] == 6:
			status_url = 'Valid'
			data_avai = 'Not Available'
		elif rec[3] == 10 or rec[3] == 5:
			status_url = 'Not Valid'
			data_avai = 'Not Available'
		values_final.extend([sk, given_url, given_id, status_url, data_avai, given_email, keysf])
		callfun3 = self.metadesign('linkedin_meta', sk, inde)
		values_final.extend(callfun3)
		lasttablename = ''
		for indes, tabl in enumerate(list_tables_denor):
			if indes == 0: lasttablename = 'image_path'
			callfun = self.querydesign(tabl, sk, lasttablename, inde)
			lasttablename = tabl
			values_final.extend([callfun])
		
		for indesm, tabl in enumerate(list_tables1_denor):
			if indesm == 0: lasttablenames = lasttablename
			calfun2, lastin = self.colum(tabl, sk, inde, lasttablenames)
			lasttablenames = lastin
			values_final.extend(calfun2)
		values_final = [str(row) if isinstance(row, long) else row for row in values_final]
		values_final =  [normalize(i) for i in values_final]
		final_qryto = "%s%s%s%s%s%s"%(self.quer1,', '.join(self.quer2), ', created_at, modified_at, last_seen) values (' , ', '.join(['%s' for i in range(len(self.quer2))]), ', now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(), ', ', '.join([str(i)+'=%s' for i in self.quer2]))
		values_final.extend(values_final)
                self.tables_file.write('%s\n%s\n' %(final_qryto, tuple(values_final)))
                self.tables_file.flush()
		print inde, sk
        self.close_all_opened_query_files()
	close_mysql_connection(self.con, self.cur)

    def main(self):
        self.send_xls()
if __name__ == '__main__':
	parser = optparse.OptionParser()
	parser.add_option('-m', '--modified-at', default='', help = 'modified_at')
	parser.add_option('-t','--table-creation-needed', default = '', help = 'table_creation_needed')
	parser.add_option('-l','--limit', default = '', help = 'limit')
	(options, args) = parser.parse_args()
	Lifilepde(options)

