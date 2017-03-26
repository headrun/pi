#import xlwt
import MySQLdb
import json
import datetime
import re
import sys
import optparse
import csv
from itertools import chain

class Lixlsfile(object):

    def __init__(self, options):
        self.db_list     = options.db_name
        self.types       = options.types
        self.row_count = 1
        self.db_list = self.db_list.split(',')
        #self.selectqry = 'select sk, flag, meta_data, crawl_status from linkedin_crawl30'
        #self.excel_file_name = 'linkedin30_data_%s.xls'%str(datetime.datetime.now().date())
        self.excel_file_name = 'linkedin30_data_%s.csv'%str(datetime.datetime.now().date())
        #self.todays_excel_file = xlwt.Workbook(encoding="utf-8")
        #self.todays_excel_sheet1 = self.todays_excel_file.add_sheet("sheet1")
        self.selectqry = ''
        header_params = []
        if not self.types == 'types':
            header_params = ['id','url', 'flag', 'clean_url']
            self.selectqry = 'select sk, flag, meta_data, crawl_status from linkedin_crawl30'
        else:
            header_params = ['id','given_url', 'name']
            self.selectqry = 'select sk, url, flag, meta_data, crawl_status, clean_url from linkedin_crawl30'

        self.updateqry = "update linkedin_crawl30 set clean_url = '%s' where sk = '%s'"
        """for i, row in enumerate(header_params):
            self.todays_excel_sheet1.write(0, i, row)"""
        oupf = open(self.excel_file_name, 'ab+')
        self.todays_excel_file  = csv.writer(oupf)
        if not self.types == 'types':
            self.todays_excel_file.writerow(header_params)

        self.main()

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


    def create_cursor(self, db_, user_, pswd_, host_):
        try:
            con = MySQLdb.connect(db   = db_,
                  user                      = user_,
                  passwd                    = pswd_,
                  charset                   = "utf8",
                  host                      = host_,
                  use_unicode               = True)
            cur = con.cursor()
        except:
            pass
        return con, cur

    def close_sql_connection(self, conn, cursor):
        if cursor: cursor.close()
        if conn: conn.close()

    def send_xlstwitter(self):
        dbs = self.db_list
        for db in dbs:
            con2_,cur2_ = self.create_cursor(db, 'root','hdrn59!','localhost')
            cur2_.execute(self.selectqry)
            records = cur2_.fetchall()
            for inde , record in enumerate(records):
                if not self.types == 'types':
                    sk , flag,  meta_data, crawl_status = record
                else:  sk, urlc, flag, meta_data, crawl_status, clean_url = record
                meta_data = json.loads(meta_data)
                id_ = meta_data.get('id','')
                url = meta_data.get('linkedin_url','')
                if not self.types == 'types':
                    urlclear = url
                    if 'http:' in urlclear: urlclear = urlclear.replace('http:','https:')
                    if 'id.www' in  urlclear: urlclear = urlclear.replace('id.www','https://www')
                    if 'www.linkedin.com' and 'https:' not in urlclear: urlclear = urlclear.replace('www.','https://www')
                    if urlclear.startswith('linkedin.com'): urlclear = urlclear.replace('linkedin.com','https://www.linkedin.com')
                    if 'https:' not in urlclear:
                        urlclear = re.sub('(\D+)\.linkedin.com','https://www.linkedin.com', urlclear)
                    urlclear = re.sub('https://(.*?).linkedin.com/','https://www.linkedin.com/',urlclear)
                    if not urlclear.startswith('https://www.linkedin.com') and crawl_status!=10: urlclear = ''.join(re.findall('.*(https://.*)', urlclear))
                    urlclear = urlclear.strip('"').strip().strip("'").strip()
                    if '/pub/' in urlclear:
                        if urlclear.endswith('/en'): urlclear = urlclear[:-3]
                        cv = ''.join(filter(None,re.split('https://www.linkedin.com/pub/.*?/(.*)',urlclear))).split('/')[::-1]
                        cv[0] = cv[0].zfill(3)
                        if cv[-1] == '0':
                            del cv[-1]
                        urlclear = ( '%s%s%s%s'%('https://www.linkedin.com/in/',''.join(re.findall('https://www.linkedin.com/pub/(.*?)/.*',urlclear)),'-',''.join(cv)))
                    #if '/pub/' in urlclear: urlclear = ( '%s%s%s%s'%('https://www.linkedin.com/in/',''.join(re.findall('https://www.linkedin.com/pub/(.*?)/.*',urlclear)),'-',''.join(''.join(filter(None,re.split('https://www.linkedin.com/pub/.*?/(.*)',urlclear))).split('/')[::-1])))
                    try: cur2_.execute(self.updateqry%(urlclear,sk))
                    except: import pdb;pdb.set_trace()
                    values = [id_, url, flag, urlclear]
                    values =  [self.normalize(i) for i in values]
                    self.todays_excel_file.writerow(values)
                else:
                    header_params = ['id','given_url', 'clean_url', 'flag']
                    values = [id_, url, clean_url, flag]
                    sk, urlc, flag, meta_data, crawl_status, clean_url
                    callfun3, headersv = self.metadesign('Linkedin', sk, cur2_)
                    if inde ==0: header_params.extend(headersv)
                    values.extend(callfun3)
                    callfun2, headersv2 = self.colum('Linkedinpositions', sk, cur2_)
                    if inde ==0: header_params.extend(headersv2)
                    if inde ==0: self.todays_excel_file.writerow(header_params)
                    values.extend(callfun2)
                    values =  [self.normalize(i) for i in values]
                    self.todays_excel_file.writerow(values)
                    print values
        self.close_sql_connection(con2_, cur2_)


    def colum (self, table, sk, cur):
        q5 = 'SELECT COLUMN_NAME FROM information_schema.columns where table_schema= "%s" and table_name = "%s"'%('FACEBOOK', table)
        cur.execute(q5)
        fields = cur.fetchall()
        fileds_list = list(fields)
        fil_list = list(chain.from_iterable(fileds_list))[2:-2]
        q6 = "select count(*)  from %s group by profile_sk order by count(*) desc limit 1"%table
        cur.execute(q6)
        large_count = cur.fetchall()
        max_count = ''
        try: max_count = int(large_count[0][0])
        except: max_count = ''
        va = []
        if max_count:
                for fi in range(1,max_count+1):
                        for fl in fil_list:
                                va.append(fl+str(fi))
        q9  = 'select * from %s where profile_sk="%s"'%(table, sk)
        cur.execute(q9)
        countrec = cur.fetchall()
        cntf_ = []
        if countrec:
                cntf = map(lambda x:(x[2:-2]), countrec)
                cntf_ = list(chain.from_iterable(cntf))
        if len(cntf_) != len(va):
                lnewln = len(va) - len(cntf_)
                cntf_.extend(['']*lnewln)
        return cntf_, va

    def metadesign(self, table, sk, cur):
        q0 = 'SELECT COLUMN_NAME FROM information_schema.columns where table_schema= "%s" and table_name = "%s"'%('FACEBOOK', table)
        cur.execute(q0)
        fields = cur.fetchall()
        fileds_list = list(fields)
        fil_list = list(chain.from_iterable(fileds_list))[1:-2]
        q8 = 'select * from %s where sk ="%s"'%(table, sk)
        cur.execute(q8)
        values = cur.fetchall()
        cntf_ = []
        if values:
                vals_ = map(lambda x:(x[1:-3]), values)
                cntf_ = list(chain.from_iterable(vals_))
        if len(cntf_) != len(fil_list):
                lnewln = len(fil_list) - len(cntf_)
                cntf_.extend(['']*lnewln)
        return cntf_, fil_list

    def main(self):
        self.send_xlstwitter()

if __name__ == '__main__':
        parser = optparse.OptionParser()
        parser.add_option('-d', '--db-name', default='', help = 'db_name')
        parser.add_option('-t', '--types', default = '', help = 'types')
        (options, args) = parser.parse_args()
        Lixlsfile(options)


