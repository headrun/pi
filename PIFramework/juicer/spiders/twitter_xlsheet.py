import xlwt
import MySQLdb
import json
import datetime
import re
import sys
import optparse

class Tixlsfile(object):

    def __init__(self, options):
        self.db_list     = options.db_name
        self.row_count = 1
        self.db_list = self.db_list.split(',')
        self.selectqry = 'select sk,screen_name,name,description,location,tweets,following,followers,likes,image,lists,timezone,language,is_verified,twitter_url, aux_info from Twitter'
        self.excel_file_name = 'twitter_data_%s.xls'%str(datetime.datetime.now().date())
        self.todays_excel_file = xlwt.Workbook(encoding="utf-8")
        self.todays_excel_sheet1 = self.todays_excel_file.add_sheet("sheet1")
        header_params = ['ScreenName', 'Name', 'Description', 'Location', 'Tweets', 'Following', 'Followers','Likes', 'Image', 'Lists', 'TimeZone', 'Language', 'IsVerified', 'Twitter URL']
        for i, row in enumerate(header_params):
            self.todays_excel_sheet1.write(0, i, row)
        self.main()

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
            for record in records:
                sk , screen_name,name,description,location,tweets,following,followers,likes,image,lists,timezone,language,is_verified,twitter_url, aux_info = record
                values = [screen_name,name,description,location,tweets,following,followers,likes,image,lists,timezone,language,is_verified,twitter_url]
                for col_count, value in enumerate(values):
                    self.todays_excel_sheet1.write(self.row_count, col_count, value)
                    print self.row_count, col_count, value
                self.row_count = self.row_count+1
            self.close_sql_connection(con2_, cur2_)
        self.todays_excel_file.save(self.excel_file_name)

    def main(self):
        self.send_xlstwitter()

if __name__ == '__main__':
        parser = optparse.OptionParser()
        parser.add_option('-d', '--db-name', default='', help = 'db_name')
        (options, args) = parser.parse_args()
        Tixlsfile(options)


