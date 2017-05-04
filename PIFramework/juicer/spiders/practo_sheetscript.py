from linkedin_functions import *

class Practocsv(object):
    def __init__(self, *args, **kwargs):
        self.con, self.cur = get_mysql_connection('localhost', 'PRACTO', '')
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
        self.query1 = 'select * from %s'
        self.query2 = 'select * from %s where %s = "%s"'
        self.columns_query = 'SELECT COLUMN_NAME FROM information_schema.columns where table_schema= "PRACTO" and table_name = "%s"'
        self.max_count_query = "select count(*)  from %s group by doctor_id order by count(*) desc limit 1"
        doct_info_columns = fetchall(self.cur, self.columns_query%('DoctorInfo'))
        doc_info_list = list(doct_info_columns)
        self.doc_info_uplist = list(chain.from_iterable(doc_info_list))[:-3]
        doct_meta_columns = fetchall(self.cur, self.columns_query%('DoctorMeta'))
        doct_meta_ls = list(doct_meta_columns)
        self.doc_meta_uplist = list(chain.from_iterable(doct_meta_ls))[1:-3]
        hospital_columns = fetchall(self.cur, self.columns_query%('DoctorHospital'))
        doct_hospitals = list(hospital_columns)
        self.doct_hospitals = list(chain.from_iterable(doct_hospitals))[2:-4]
        feedback_columns = fetchall(self.cur, self.columns_query%('DoctorFeedback'))
        feed_col = list(feedback_columns)
        self.feedback_col = list(chain.from_iterable(feed_col))[2:-4]
        self.headerlisting = []
        self.headerprofiles = []
        self.main()


    def send_csv(self):
        records = fetchall(self.cur, self.query1%('DoctorInfo'))
        for inde, rec in enumerate(records):
            info_rec = list(rec)[:-3]
            if inde == 0:
                self.headerlisting.extend(self.doc_info_uplist)
                self.headerprofiles.extend(self.doc_meta_uplist)
                self.todays_excel_file.writerow(self.headerlisting)

            self.todays_excel_file.writerow(info_rec)
            values_final = []
            doctor_id = info_rec[0]
            meta_ = fetchall(self.cur, self.query2%("DoctorMeta", 'sk', doctor_id))
            meta_rec = list(meta_[0])[1:-3]
            values_final.extend(meta_rec)
            doctor_meta_id = meta_rec[0]
            doct_hospitals = self.values_for(inde, doctor_meta_id)
            values_final.extend(doct_hospitals)
            callfun = self.querydesign(doctor_meta_id, inde)
            if inde == 0: self.todays_excel_file1.writerow(self.headerprofiles)
            orig_vals = values_final
            countr=0
            for cf in callfun:
                countr+=1
                uptovalues_here = orig_vals
                uptovalues_here.extend(cf)
                uptovalues_here =  [normalize(i) for i in uptovalues_here]
                if len(self.headerprofiles) != len(uptovalues_here): import pdb;pdb.set_trace()
                self.todays_excel_file1.writerow(uptovalues_here)
                del orig_vals[-13:]

            """values_final.extend([callfun])
            if inde == 0: self.todays_excel_file1.writerow(self.headerprofiles)
            values_final =  [normalize(i) for i in values_final]
            self.todays_excel_file1.writerow(values_final)"""


    def querydesign(self, doctor_meta_id, hindex):
        if hindex == 0: self.headerprofiles.extend(self.feedback_col)
        final_to_update = []
        values = fetchall(self.cur, self.query2%("DoctorFeedback", 'doctor_id', doctor_meta_id))
        for ind, val in enumerate(values):
            vals_ = list(val)[2:-4]
            final_to_update.append(vals_)
        if not final_to_update:
            final_to_update.append(['' for i in self.feedback_col])
        return final_to_update
        """if hindex == 0:  self.headerprofiles.extend(['Feedback'])
        values = fetchall(self.cur, self.query2%("DoctorFeedback", 'doctor_id', doctor_meta_id))
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
        large_count = fetchall(self.cur, self.max_count_query%('DoctorHospital'))
        max_count = ''
        try: max_count = int(large_count[0][0])
        except: max_count = ''
        va = []
        if max_count:
            for fi in range(1,max_count+1):
                for fl in self.doct_hospitals:
                    va.append("%s%s%s%s"%('hospital_', str(fi), '_', fl.split('hospital_')[-1]))
        if inde == 0: self.headerprofiles.extend(va)
        countrec = fetchall(self.cur, self.query2%("DoctorHospital", 'doctor_id', doctor_meta_id))
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
        Practocsv(options)


