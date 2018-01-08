from linkedin_functions import *

class Medecurecsv(object):
    def __init__(self, *args, **kwargs):
        self.con, self.cur = get_mysql_connection('localhost', 'MEDECURE', '')
        self.excel_file_name = 'doctor_listing_%s.csv'%str(datetime.datetime.now().date())
        self.excel_file_name1 = 'doctor_profile_%s.csv'%str(datetime.datetime.now().date())
        if os.path.isfile(self.excel_file_name):
            os.system('rm %s'%self.excel_file_name)
        if os.path.isfile(self.excel_file_name1):
            os.system('rm %s'%self.excel_file_name1)
        oupf = open(self.excel_file_name, 'ab+')
        oupf1 = open(self.excel_file_name1, 'ab+')
        self.todays_excel_file  = csv.writer(oupf)
        self.todays_excel_file1 = csv.writer(oupf1)
        self.file_dirs = os.path.join(os.getcwd(),'OUTPUT')
        self.QUERY_FILES_DIR = os.path.join(self.file_dirs, 'load_script/processing')
        self.QUERY_FILES_CRAWLOUT_DIR = os.path.join(self.file_dirs, 'load_script/crawl_out')
        self.tableschema = 'INSERT INTO practo_final_table ('
        self.na = 'practo_final_table'
        self.tables_file = self.get_tables_file()
        self.query1 = 'select * from %s where date(modified_at) >= "2018-01-04"'
        self.query2 = 'select * from %s where %s = "%s"'
        self.columns_query = 'SELECT COLUMN_NAME FROM information_schema.columns where table_schema= "MEDECURE" and table_name = "%s"'
        self.max_count_query = "select count(*)  from %s group by doctor_id order by count(*) desc limit 1"
        doct_info_columns = fetchmany(self.cur, self.columns_query%('DoctorInfo'))
        doc_info_list = list(doct_info_columns)
        self.doc_info_uplist = list(chain.from_iterable(doc_info_list))[:-3]
        #self.doc_info_uplist.extend(['phone_number', 'extension', 'city', 'Availability Text'])
        self.doc_info_uplist.extend(['city'])
        doct_meta_columns = fetchmany(self.cur, self.columns_query%('DoctorMeta'))
        doct_meta_ls = list(doct_meta_columns)
        self.doc_meta_uplist = list(chain.from_iterable(doct_meta_ls))[1:-3]
        hospital_columns = fetchmany(self.cur, self.columns_query%('DoctorHospital'))
        doct_hospitals = list(hospital_columns)
        self.doct_hospitals = list(chain.from_iterable(doct_hospitals))[2:-4]
        feedback_columns = fetchmany(self.cur, self.columns_query%('DoctorFeedback'))
        feed_col = list(feedback_columns)
        self.feedback_col = list(chain.from_iterable(feed_col))[2:-4]
        self.columns_pft = ''

        self.headerlisting = []
        self.headerprofiles = []
        self.main()

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



    def send_csv(self):
        records = fetchall(self.cur, self.query1%('DoctorInfo'))
        counterpa = 0
        for inde, rec in enumerate(records):
            info_rec = list(rec)[:-2]
            '''phone_no, extension, city_name,avilability_text = ['']*4
            try:
                jsd = json.loads(info_rec[-1])
                if jsd:
                    phone_no = jsd.get('phone_number','')
                    extension = jsd.get('extension','')
                    city_name = jsd.get('city', '')
                    availability_text = jsd.get('doc_avilability_text','')
            except:
                pass

            info_rec[-1] = phone_no
            info_rec.extend([extension])
            info_rec.extend([city_name])
            info_rec.extend([availability_text])'''
            print info_rec[0], '>>>>'
            counterpa+=1
            print counterpa
            #if '316500' in info_rec[0]  or '555819' in info_rec[0]: continue
            if inde == 0:
                self.headerlisting.extend(self.doc_info_uplist)
                self.headerprofiles.extend(self.doc_meta_uplist)
                #import pdb;pdb.set_trace()
                self.headerprofiles.extend(['city'])
                self.todays_excel_file.writerow(self.headerlisting)
            info_rec = [normalize(i) for i in info_rec]
            self.todays_excel_file.writerow(info_rec)
            values_final = []
            doctor_id = info_rec[1]
            sk = info_rec[0]
            meta_ = fetchall(self.cur, self.query2%("DoctorMeta", 'sk', sk))
            meta_rec = []
            status = 'Available'
            if meta_:
                meta_rec = list(meta_[0])[1:-2]
                #meta_rec[-1] = json.loads(meta_rec[-2]).get('city', '')
            else:
                meta_rec = ['' for i in range(23)]
                meta_rec[0] = doctor_id
                status = 'Not Available'
            values_final.extend(meta_rec)
            doctor_meta_id = meta_rec[0]
            doct_hospitals = self.values_for(inde, doctor_meta_id)
            values_final.extend(doct_hospitals)
            callfun = self.querydesign(doctor_meta_id, inde)
            if inde == 0:
                self.headerprofiles.extend(['Status'])
                self.todays_excel_file1.writerow(self.headerprofiles)
                table_schema =  "%s%s%s"%("CREATE TABLE `practo_final_table` (`id` int(11) NOT NULL AUTO_INCREMENT, ",''.join(["%s%s%s%s"%('`' , i, '`',' text COLLATE utf8_unicode_ci, ') for i in self.headerprofiles]), "`created_at` datetime NOT NULL,   `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,   `last_seen` datetime NOT NULL,   PRIMARY KEY (`id`) ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci; ")
                execute_query(self.cur, table_schema)
                columns_pfinalt = fetchmany(self.cur, self.columns_query%('practo_final_table'))
                self.columns_pft = list(chain.from_iterable(list(columns_pfinalt)[1:-3]))
            orig_vals = values_final
            countr=0
            final_qryto = "%s%s%s%s%s%s"%(self.tableschema,', '.join(self.columns_pft), ', created_at, modified_at, last_seen) values (' , ', '.join(['%s' for i in range(len(self.columns_pft))]), ', now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(), ', ', '.join([str(i)+'=%s' for i in self.columns_pft]))
            for cf in callfun:
                countr+=1
                uptovalues_here = orig_vals
                uptovalues_here.extend(cf)
                uptovalues_here.extend([status])
                uptovalues_here =  [normalize(i) for i in uptovalues_here]
                if len(self.headerprofiles) != len(uptovalues_here):
                    print len(self.headerprofiles)
                    print len(uptovalues_here)
                self.todays_excel_file1.writerow(uptovalues_here)
                final_table_values = []
                final_table_values = uptovalues_here+uptovalues_here
                #execute_query(self.cur, "%s%s"%(final_qryto, tuple(final_table_values)))
                self.tables_file.write('%s\n%s\n' %(final_qryto, tuple(final_table_values)))
                self.tables_file.flush()
                del orig_vals[-13:]


            """values_final.extend([callfun])
            if inde == 0: self.todays_excel_file1.writerow(self.headerprofiles)
            values_final =  [normalize(i) for i in values_final]
            self.todays_excel_file1.writerow(values_final)"""
        self.close_all_opened_query_files()


    def querydesign(self, doctor_meta_id, hindex):
        if hindex == 0: self.headerprofiles.extend(self.feedback_col)
        final_to_update = []
        values = fetchmany(self.cur, self.query2%("DoctorFeedback", 'doctor_id', doctor_meta_id))
        for ind, val in enumerate(values):
            vals_ = list(val)[2:-4]
            final_to_update.append(vals_)
        if not final_to_update:
            final_to_update.append(['' for i in self.feedback_col])
        return final_to_update
        """if hindex == 0:  self.headerprofiles.extend(['Feedback'])
        values = fetchmany(self.cur, self.query2%("DoctorFeedback", 'doctor_id', doctor_meta_id))
        final_to_update = []
        for ind, val in enumerate(values):
                vals_ = list(val)[2:-4]
                indes = '%s%s'%('_',str(ind+1))
                feed_ = self.feedback_col
                feedb_= map(lambda x:x+indes, feed_)
                valf = filter(None, map(lambda a,b: (a+':-'+b) if b else '', feedb_,vals_))
                final_to_update.append(', '.join(valf))
        return ' <> '.join(final_to_update) """



    def values_for(self, inde, doctor_meta_id):
        large_count = fetchmany(self.cur, self.max_count_query%('DoctorHospital'))
        max_count = ''
        try: max_count = int(large_count[0][0])
        except: max_count = ''
        va = []
        if max_count:
            for fi in range(1,max_count+1):
                for fl in self.doct_hospitals:
                    va.append("%s%s%s%s"%('hospital_', str(fi), '_', fl.split('hospital_')[-1]))
        if inde == 0: self.headerprofiles.extend(va)
        countrec = fetchmany(self.cur, self.query2%("DoctorHospital", 'doctor_id', doctor_meta_id))
        cntf_ = []
        if countrec:
                cntf = map(lambda x:(x[2:-4]), countrec)
                cntf_ = list(chain.from_iterable(cntf))
        if len(cntf_) != len(va):
                lnewln = len(va) - len(cntf_)
                cntf_.extend(['']*lnewln)
        return cntf_

    def main(self):
        self.send_csv()

if __name__ == '__main__':
        parser = optparse.OptionParser()
        parser.add_option('-m', '--modified-at', default='', help = 'modified_at')
        (options, args) = parser.parse_args()
        Medecurecsv(options)
