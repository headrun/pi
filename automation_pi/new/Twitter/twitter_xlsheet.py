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
        self.selectqry =  'select screen_name,name,description,location,tweets,following,followers,likes,image,lists,timezone,language,is_verified,twitter_url,email_id,top_10_hashtags,top_5_mentioned_users,retweeted_percentage,retweeted_users, Most_referenced_domains,detected_sources, detected_languages, Avg_no_of_tweets_per_day from Twitter_latest where date(modified_at) >= "2018-04-10" and email_id=""'
	self.selectqry2 = 'select sk, url, meta_data from twitter_crawl where date(modified_at)>="2018-04-12" and crawl_status!=100 and crawl_status=9'

        self.excel_file_name = 'ash_enrichment_twitter_%s.xls'%str(datetime.datetime.now().date())
        self.todays_excel_file = xlwt.Workbook(encoding="utf-8")
        self.todays_excel_sheet1 = self.todays_excel_file.add_sheet("sheet1")
        header_params = ['sr no','payer','screen_name','name','description','location','tweets','following','followers','likes','image','listsi','timezone','language','is_verified','twitter_url','email_id','top_10_hashtags','top_5_mentioned_users','retweeted_percentage','retweeted_users', 'Most_referenced_domains','detected_sources', 'detected_languages', 'Avg_no_of_tweets_per_day','Status']
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
            con2_,cur2_ = self.create_cursor('FACEBOOK', 'root','root','localhost')
            #import pdb;pdb.set_trace()
            cur2_.execute(self.selectqry)
	
            records = cur2_.fetchall()
	    cur2_.execute(self.selectqry2)
	    records_2 = cur2_.fetchall()
            for record in records:
                screen_name,name,description,location,tweets,following,followers,likes,image,lists,timezone,language,is_verified,twitter_url,email_id,top_10_hashtags,top_5_mentioned_users,retweeted_percentage,retweeted_users, Most_referenced_domains,detected_sources, detected_languages, Avg_no_of_tweets_per_day = record
                retweeted_percentage = retweeted_percentage.replace('@@','@')
                twitter_url = twitter_url.replace('@','')
                retweeted_users = retweeted_users.replace('@@','')
		data = 'select meta_data from twitter_crawl where sk = "%s"' % screen_name
		cur2_.execute(data)
		sno_given1 = cur2_.fetchall()
		id_value, sno_given,payer = ['']*3
		if sno_given1:
		    try:
			sno_given = json.loads(sno_given1[0][0]).get('sno','')
			payer = json.loads(sno_given1[0][0]).get('payer','')
			id_value = json.loads(sno_given1[0][0]).get('id', '')
		    except: pass
		else:
			sno_given = ''

                values = [sno_given, payer,screen_name,name,description,location,tweets,following,followers,likes,image,lists,timezone,language,is_verified,twitter_url,email_id,top_10_hashtags,top_5_mentioned_users,retweeted_percentage,retweeted_users, Most_referenced_domains,detected_sources, detected_languages, Avg_no_of_tweets_per_day,'DataAvailable']
                

                for col_count, value in enumerate(values):
                    try : 
                        value = str(value)
                        value = normalize(value)
                    except :
                        value = normalize(value)

                    value = value.replace('\x1b[1m','').replace('\x1b[0m','')
                    if '{' in value : value = re.sub('\{.*?\}','',value)
                    self.todays_excel_sheet1.write(self.row_count, col_count, value)
                self.row_count = self.row_count+1
	    if records_2:
		for rec2 in records_2:
		    try :values = [json.loads(rec2[2]).get('srno',''),json.loads(rec2[2]).get('payer',''), rec2[0], '', '', '', '', '', '', '', '', '', '', '', '', rec2[1],json.loads(rec2[2]).get('email_address', ''), '', '', '', '', '', '', '', '', 'DataUnAvailable']
                    except : continue
                    
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
        Tixlsfile(options)


