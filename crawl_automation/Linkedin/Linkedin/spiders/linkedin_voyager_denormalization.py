from linkedin_voyager_functions import *
from linkedin_voyager_db_operations import *
from db_qry2 import*
import ast

class Licsdenormalization(object):

    def __init__(self, *args, **kwargs):
        self.dirs = ['OUTPUT', 'OUTPUT/crawl_out', 'OUTPUT/processing']
        for dirs in self.dirs:
            make_dir(dirs)
        self.con, self.cur = get_mysql_connection(DB_HOST, 'CRAWL_AUTOMATION', '')
        self.file_dirs = os.path.join(os.getcwd(), 'OUTPUT')
        self.QUERY_FILES_DIR = os.path.join(self.file_dirs, 'processing')
        self.QUERY_FILES_CRAWLOUT_DIR = os.path.join(
            self.file_dirs, 'crawl_out')
        self.tables_file = self.get_tables_file()
        self.tables_file1 = self.get_tables_file1()
        self.sk = options.sk
        self.inner_dict = {}
        self.main()

    def __del__(self):
        self.con.close()
        self.cur.close()

    def get_current_ts_with_ms(self):
        dt = datetime.datetime.now().strftime("%Y%m%dT%H%M%S%f")
        return dt
    

    def get_tables_file(self):
        tables_queries_filename = os.path.join(self.QUERY_FILES_CRAWLOUT_DIR, "%s_%s.queries" % (
            'linkedin_aws_csv1', self.get_current_ts_with_ms()))
        self.tables_file = open(tables_queries_filename, 'w')

        return self.tables_file

    def get_tables_file1(self):
        tables_queries_filename1 = os.path.join(self.QUERY_FILES_CRAWLOUT_DIR, "%s_%s.queries" % (
            'linkedin_pi_csv1', self.get_current_ts_with_ms()))

        self.tables_file2 = open(tables_queries_filename1, 'w')
        return self.tables_file2


    def move_file(self, source, dest):
        cmd = "mv %s %s" % (source, dest)
        os.system(cmd)
        

    def close_all_opened_query_files(self):
        files_list = [self.tables_file,self.tables_file2]
        for f in files_list:
            if not isinstance(f, file):
                continue
            f.flush()
            f.close()
            self.move_file(f.name, self.QUERY_FILES_DIR)

    def querydesign(self, tble, sk):
        q1 = q1_querydesign % (tble, sk)
        values = fetchmany(self.cur, q1)
        final_to_update = []
        for val in values:
            vals_ = list(val)[2:-3]
            vals_ = [str(row) if isinstance(
                row, long) else row for row in vals_]
            valf = filter(
                None, map(lambda a, b: (a + ':-' + b) if b else '', dict_of_fields[tble], vals_))
            final_to_update.append(', '.join(valf))
        return ' <> '.join(final_to_update)


    def colum(self, table, sk, inde):
        v1_, v2_, v3_, v4_ = lnkd_limit_querydict[table]
        q9 = lnkd_limit_query % (table, sk, v1_)
        countrec = fetchmany(self.cur, q9)
        cntf_ = []
        if countrec:
            cntf = []
            if 'linkedin_honors' in table:
                cntf = map(lambda x: (x[2:5]+x[6:7]), countrec)
            elif 'linkedin_experiences' in table:
                cntf = map(lambda x: (x[2:4]+x[5:10]+x[12:13]), countrec)
            else:
                cntf = map(lambda x: (x[v2_:v3_]), countrec)
            cntf_ = list(chain.from_iterable(cntf))
        if len(cntf_) != v4_:
            lnewln = v4_ - len(cntf_)
            cntf_.extend([''] * lnewln)
        return cntf_


    def metadesign(self, table, sk):
        q8 = q1_meta_few_results % (
            sk)
        values = fetchmany(self.cur, q8)
        cntf_ = []
        if values:
            cntf_ = list(values[0])
        else:
            lnewln = 19 # length of records for meta table
            cntf_.extend([''] * lnewln)
        return cntf_

    def get_json_data(self, record_json):
        json_meta = {}
        try:
            json_meta = json.loads(record_json)
        except:
            try:
                json_meta = ast.literal_eval(record_json)
            except:
                try:
                    json_meta = ast.literal_eval(
                        normalize(record_json).replace('\\', ''))
                except:
                    pass
        return json_meta


    def main(self):
        sk = options.sk.split(',')
        if len(sk) == 1 : query2 = crawl_table_query1 % "".join(sk)
        else : query2 =  crawl_table_query + str(tuple(sk))
        records = fetchmany(self.cur, query2)
        counter = 0
        for inde, rec in enumerate(records):
	    counter += 1
	    values_final = []
	    get_meb_records = fetchmany(
		self.cur, member_id_track % rec[0])
	    sk = get_meb_records[0][0]
	    sk_crawl = list(rec)[0]
	    url_re = rec[1]
	    json_meta = self.get_json_data(rec[2])
	    given_url = json_meta.get('linkedin_url', '')
	    status_url, data_avai = [''] * 2
	    if rec[3] == 1:
		status_url = 'Valid'
		data_avai = 'Available'
	    elif rec[3] == 6:
		status_url = 'Valid'
		data_avai = 'Not Available'
	    elif rec[3] == 10 or rec[3] == 5:
		status_url = 'Not Valid'
		data_avai = 'Not Available'
	    values_final = ['', given_url,  status_url, data_avai]
	    callfun3 = self.metadesign('linkedin_meta', sk)
	    values_final.extend(callfun3)
	    for tabl in list_tables_denormalization:
		callfun = self.querydesign(tabl, sk)
		values_final.extend([callfun])
	    for tabl in list_tables1:
		calfun2 = self.colum(tabl, sk, inde)
		values_final.extend(calfun2)
	    values_final = [str(row) if isinstance(
		row, long) else row for row in values_final]
	    values_final.extend(['' for r in range(63)])
	    values_final = [normalize(i) for i in values_final]
	    values_final.extend(values_final)

	    self.tables_file.write(
		'%s\n%s\n' % (insert_query_aws_csv1, tuple(values_final)))
            self.tables_file1.write(
                '%s\n%s\n' % (insert_query_pi_csv1, tuple(values_final)))
	    self.tables_file.flush()
            self.tables_file1.flush()
       
        self.close_all_opened_query_files()

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-s','--sk',default='', help='sk')
    (options, args) = parser.parse_args()
    Licsdenormalization(options)
