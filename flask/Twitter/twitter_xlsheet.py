import xlwt
import MySQLdb
import json
import datetime
import re
import sys
import optparse
from  linkedin_functions import *

class Tixlsfile(object):

    def get_primary(self):
        row_count = 1
        selectqry =  'select screen_name,name,description,location,tweets,following,followers,likes,image,lists,timezone,language,is_verified,twitter_url,email_id,top_10_hashtags,top_5_mentioned_users,retweeted_percentage,retweeted_users, Most_referenced_domains,detected_sources, detected_languages, Avg_no_of_tweets_per_day from Twitter_latest where screen_name = "%s"'
        excel_file_name = 'ash_enrichment_twitter_%s.xls'%str(datetime.datetime.now().date())
        todays_excel_file = xlwt.Workbook(encoding="utf-8")
        todays_excel_sheet1 = todays_excel_file.add_sheet("sheet1")
        header_params = ['screen_name','name','description','location','tweets','following','followers','likes','image','lists','timezone','language','is_verified','twitter_url','email_id','top_10_hashtags','top_5_mentioned_users','retweeted_percentage','retweeted_users', 'Most_referenced_domains','detected_sources', 'detected_languages', 'Avg_no_of_tweets_per_day','Status']
        for i, row in enumerate(header_params):
            todays_excel_sheet1.write(0, i, row)
        return row_count, selectqry, excel_file_name, todays_excel_file, todays_excel_sheet1,header_params

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

    def send_xlstwitter(self, screen_name):
        row_count, selectqry, excel_file_name, todays_excel_file, todays_excel_sheet1,header_params = self.get_primary()
        con2_,cur2_ = self.create_cursor('PROFILE_ANALYZER', 'root','hdrn59!','localhost')
        cur2_.execute(selectqry % screen_name)
        record = cur2_.fetchall()
        if record:
            screen_name,name,description,location,tweets,following,followers,likes,image,lists,timezone,language,is_verified,twitter_url,email_id,top_10_hashtags,top_5_mentioned_users,retweeted_percentage,retweeted_users, Most_referenced_domains,detected_sources, detected_languages, Avg_no_of_tweets_per_day = record[0]
            values = [screen_name,name,description,location,tweets,following,followers,likes,image,lists,timezone,language,is_verified,twitter_url,email_id,top_10_hashtags,top_5_mentioned_users,retweeted_percentage,retweeted_users, Most_referenced_domains,detected_sources, detected_languages, Avg_no_of_tweets_per_day,'DataAvailable']
            value_final_list = []
            for col_count, value in enumerate(values):
                try :
                    value = str(value)
                    value = normalize(value)
                except :
                    value = normalize(value)

                value = value.replace('\x1b[1m','').replace('\x1b[0m','')
                if '{' in value : value = re.sub('\{.*?\}','',value)
                if not value: value = 'NA'
                value_final_list.append(value)
                todays_excel_sheet1.write(row_count, col_count, value)
            row_count = row_count+1
            self.close_sql_connection(con2_, cur2_)
            todays_excel_file.save(excel_file_name)
            value_final_listbr = [vfl.replace('<>','; ') for vfl in value_final_list]
            finall_return = dict(itertools.izip(header_params,value_final_listbr))
            return finall_return
        else:
            return ''


    def main(self, screen_name):
        twitter_data = self.send_xlstwitter(screen_name)
        return twitter_data

if __name__ == '__main__':
        Tixlsfile().main('')


