from linkedin_voyager_functions import *
from linkedin_voyager_db_operations import *
import ast

class Licsvoyager(object):
    def is_path_file_name(self, excel_file_name):
        if os.path.isfile(excel_file_name):
            os.system('rm %s' % excel_file_name)
        oupf = open(excel_file_name, 'ab+')
        todays_excel_file = csv.writer(oupf)
        return todays_excel_file

    def __init__(self, *args, **kwargs):
        self.con, self.cur = get_mysql_connection(DB_HOST, 'FACEBOOK', '')
        self.modified_at = options.modified_at
        self.limit = options.limit
        self.excel_file_name = sheet_name % (self.limit, str(datetime.datetime.now().date()))
        todays_excel_file = self.is_path_file_name(self.excel_file_name)
        self.todays_excel_file = todays_excel_file
        self.header_params = header_params_list
        self.query2 = crawl_table_query % (self.modified_at, self.limit)
        self.inner_dict = {}
        self.main()

    def __del__(self):
        self.con.close()
        self.cur.close()

    def querydesign(self, tble, sk):
        q1 = q1_querydesign % (tble, sk, self.modified_at)
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

    def colum_max_count(self, table):
        q6 = q6_column_maxcount % (table, self.modified_at)
        large_count = fetchmany(self.cur, q6)
        max_count = ''
        try:
            max_count = int(large_count[0][0])
        except:
            max_count = ''
        va = []
        if max_count:
            for fi in range(1, max_count + 1):
                for fl in dict_of_fields[table]:
                    va.append(fl + str(fi))
        self.header_params.extend(va)
        self.inner_dict.update({table : va})
        return va

    def colum(self, table, sk, inde, va):
        q9 = q1_querydesign % (table, sk, self.modified_at)
        countrec = fetchmany(self.cur, q9)
        cntf_ = []
        if countrec:
            cntf = map(lambda x: (x[2:-3]), countrec)
            cntf_ = list(chain.from_iterable(cntf))
        if len(cntf_) != len(va):
            lnewln = len(va) - len(cntf_)
            cntf_.extend([''] * lnewln)
        return cntf_

    def metadesign(self, table, sk):
        q8 = q8_metadesign % (
            table, sk, self.modified_at)
        values = fetchmany(self.cur, q8)
        cntf_ = []
        if values:
            vals_ = map(lambda x: (x[1:-3]), values)
            cntf_ = list(chain.from_iterable(vals_))
        if len(cntf_) != 29: # number of fields in meta table
            lnewln = 29 - len(cntf_)
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
        records = fetchmany(self.cur, self.query2)
        counter = 0
        for inde, rec in enumerate(records):
            counter += 1
            print counter
            values_final = []
            get_meb_records = fetchmany(
                self.cur, member_id_track % rec[0])
            sk = get_meb_records[0][0]
            sk_crawl = list(rec)[0]
            url_re = rec[1]
            json_meta = self.get_json_data(rec[2])
            given_url = json_meta.get('linkedin_url', '')
            given_id = json_meta.get('id', '')
            given_firstname = json_meta.get('firstname', '')
            given_lastname = json_meta.get('lastname', '')
            email_id = json_meta.get('email_address', '')
            keysf = json_meta.get('key', '')
            if not keysf:
                keysf = json_meta.get('keys', '')
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
            values_final = [given_url, given_id, status_url, data_avai, email_id, keysf]
            callfun3 = self.metadesign('linkedin_meta', sk)
            values_final.extend(callfun3)
            for tabl in list_tables:
                callfun = self.querydesign(tabl, sk)
                values_final.extend([callfun])
            for tabl in list_tables1:
                va = ''
                if inde == 0:
                    va = self.colum_max_count(tabl)
                else:
                    va = self.inner_dict[tabl]
                calfun2 = self.colum(tabl, sk, inde, va)
                values_final.extend(calfun2)
            values_final = [str(row) if isinstance(
                row, long) else row for row in values_final]
            values_final = [normalize(i) for i in values_final]
            if inde == 0:
                self.todays_excel_file.writerow(self.header_params)
                print len(self.header_params)
            print len(values_final)
            self.todays_excel_file.writerow(values_final)

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-m', '--modified-at', default='', help='modified_at')
    parser.add_option('-l', '--limit', default='', help='limit')
    (options, args) = parser.parse_args()
    Licsvoyager(options)
