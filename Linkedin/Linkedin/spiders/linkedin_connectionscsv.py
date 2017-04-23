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
        self.excel_file_name = 'linkedinconnections_data_%s.csv'%str(datetime.datetime.now().date())
        self.selectqry = 'select connections_profile_url, member_id, headline, name, image_url, image_path, reference_url from linkedin_connections'
        self.header_params = ['name', 'headline', 'member_id','profile_url', 'image_url', 'image_path']
        oupf = open(self.excel_file_name, 'ab+')
	self.todays_excel_file  = csv.writer(oupf)
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
            con2_,cur2_ = self.create_cursor(db, 'root','root','localhost')
            cur2_.execute(self.selectqry)
            records = cur2_.fetchall()
            for inde , record in enumerate(records):
            	connections_profile_url, member_id, headline, name, image_url, image_path, reference_url = record
		values = [name, headline, member_id, connections_profile_url, image_url, image_path]
                values =  [self.normalize(i) for i in values]
		if inde == 0:
			self.todays_excel_file.writerow(self.header_params)
		self.todays_excel_file.writerow(values)
		print values
        self.close_sql_connection(con2_, cur2_)

    def main(self):
        self.send_xlstwitter()

if __name__ == '__main__':
        parser = optparse.OptionParser()
        parser.add_option('-d', '--db-name', default='', help = 'db_name')
        parser.add_option('-t', '--types', default = '', help = 'types')
        (options, args) = parser.parse_args()
        Lixlsfile(options)
