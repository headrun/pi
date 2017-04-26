import xlwt
import MySQLdb
import json
import datetime
import re
import sys
import optparse
import ast

class Tixlsfilecrawl(object):

    def __init__(self, options):
        self.db_list     = options.db_name
        self.row_count = 1
        self.db_list = self.db_list.split(',')
        self.selectqry = 'select sk, screen_name, name, description, location, tweets, following, followers, likes, image, lists, timezone, language, is_verified, twitter_url, email_id, aux_info from Twitter where screen_name="%s"'
        self.selectqry1 = 'select sk, meta_data from urlqueue_dev.twitter_crawl where date(modified_at) >= "2017-04-21"'
        self.excel_file_name = 'twitter_data_%s.xls'%str(datetime.datetime.now().date())
        self.todays_excel_file = xlwt.Workbook(encoding="utf-8")
        self.todays_excel_sheet1 = self.todays_excel_file.add_sheet("sheet1")
        header_params = ['ScreenName', 'Name', 'Description', 'Location', 'Tweets', 'Following', 'Followers','Likes', 'Image', 'Lists', 'TimeZone', 'Language', 'IsVerified', 'Twitter URL', 'Email Id', 'Status', 'Key']
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
            cur2_.execute(self.selectqry1)
            records1 = cur2_.fetchall()
            for rec in records1:
                keyf = ast.literal_eval(rec[1]).get('key','')
                if not keyf: keyf = ast.literal_eval(rec[1]).get('keys','')
                cur2_.execute(self.selectqry%rec[0])
                records = cur2_.fetchall()
                sk , screen_name,name,description,location,tweets,following,followers,likes,image,lists,timezone,language,is_verified,twitter_url, email_id, aux_info, status = ['']*18
                if records:
                    record = records[0]
                    sk , screen_name,name,description,location,tweets,following,followers,likes,image,lists,timezone,language,is_verified,twitter_url, email_id,  aux_info = record
                    status = 'Available'
                else:
                    screen_name = rec[0]
                    status = 'Not Available'
                    twitter_url = ast.literal_eval(rec[1]).get('twitter_url','')
                values = [screen_name,name,description,location,tweets,following,followers,likes,image,lists,timezone,language,is_verified,twitter_url, email_id, status, keyf]
                for col_count, value in enumerate(values):
                        self.todays_excel_sheet1.write(self.row_count, col_count, value)
                self.row_count = self.row_count+1
            self.close_sql_connection(con2_, cur2_)
        self.todays_excel_file.save(self.excel_file_name)

    def main(self):
        self.send_xlstwitter()

if __name__ == '__main__':
        parser = optparse.OptionParser()
        parser.add_option('-d', '--db-name', default='', help = 'db_name')
        (options, args) = parser.parse_args()
        Tixlsfilecrawl(options)


