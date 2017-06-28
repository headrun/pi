import xlwt
import MySQLdb
import json
import datetime
import re
import sys
import optparse
from  linkedin_functions import *

class Tixlsfile(object):

    def __init__(self, options):
        self.db_list     = options.db_name
        self.row_count = 1
        self.db_list = self.db_list.split(',')
        self.selectqry =  'select screen_name,name,description,location,tweets,following,followers,likes,image,lists,timezone,language,is_verified,twitter_url,email_id,top_10_hashtags,top_5_mentioned_users,retweeted_percentage,retweeted_users, Most_referenced_domains,detected_sources, detected_languages, Avg_no_of_tweets_per_day from Twitter_latest where date(created_at) >= "2017-06-19"'

        self.excel_file_name = 'ash_enrichment_twitter_%s.xls'%str(datetime.datetime.now().date())
        self.todays_excel_file = xlwt.Workbook(encoding="utf-8")
        self.todays_excel_sheet1 = self.todays_excel_file.add_sheet("sheet1")
        header_params = ['screen_name','name','description','location','tweets','following','followers','likes','image','listsi','timezone','language','is_verified','twitter_url','email_id','top_10_hashtags','top_5_mentioned_users','retweeted_percentage','retweeted_users', 'Most_referenced_domains','detected_sources', 'detected_languages', 'Avg_no_of_tweets_per_day','Status']
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
            #import pdb;pdb.set_trace()
            cur2_.execute(self.selectqry)

            records = cur2_.fetchall()
            for record in records:
                screen_name,name,description,location,tweets,following,followers,likes,image,lists,timezone,language,is_verified,twitter_url,email_id,top_10_hashtags,top_5_mentioned_users,retweeted_percentage,retweeted_users, Most_referenced_domains,detected_sources, detected_languages, Avg_no_of_tweets_per_day = record
                values = [screen_name,name,description,location,tweets,following,followers,likes,image,lists,timezone,language,is_verified,twitter_url,email_id,top_10_hashtags,top_5_mentioned_users,retweeted_percentage,retweeted_users, Most_referenced_domains,detected_sources, detected_languages, Avg_no_of_tweets_per_day,'DataAvailable']
                

                for col_count, value in enumerate(values):
                    try : 
                        value = str(value)
                        value = normalize(value)
                        print value
                    except :
                        value = normalize(value)

                    value = value.replace('\x1b[1m','').replace('\x1b[0m','')
                    if '{' in value : value = re.sub('\{.*?\}','',value)
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
        Tixlsfile(options)


