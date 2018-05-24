import xlwt
import MySQLdb
import json
import datetime
import re
import sys
import optparse
from  table_schemas.generic_functions import *
from table_schemas.to_udrive import *
from table_schemas.pi_db_operations import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import smtplib
from email import encoders

class Tixlsfile(object):

    def __init__(self, options):
        self.db_list     = options.db_name
	self.email_from_list = options.email_from_list
	self.modified_at_cmd = options.modified_at
	self.modified_at_cmd = self.modified_at_cmd.replace('#', ' ')
        self.row_count = 1
        self.db_list = self.db_list.split(',')
        self.selectqry =  'select screen_name,name,description,location,tweets,following,followers,likes,image,lists,timezone,language,is_verified,twitter_url,email_id,top_10_hashtags,top_5_mentioned_users,retweeted_percentage,retweeted_users, Most_referenced_domains,detected_sources, detected_languages, Avg_no_of_tweets_per_day from Twitter_latest where modified_at = "%s"' % self.modified_at_cmd

	self.selectqry2 = 'select sk, url, meta_data from twitter_crawl where modified_at = "%s" and crawl_status != 1;'%self.modified_at_cmd

        self.excel_file_name = 'twitter_data_on_%s.xls'%str(datetime.datetime.now())
	self.excel_file_name = self.excel_file_name.replace(' ','_')
        self.todays_excel_file = xlwt.Workbook(encoding="utf-8")
        self.todays_excel_sheet1 = self.todays_excel_file.add_sheet("sheet1")
        header_params = ['id', 'sno', 'payer','screen_name','name','description','location','tweets','following','followers','likes','image','listsi','timezone','language','is_verified','twitter_url','email_id','top_10_hashtags','top_5_mentioned_users','retweeted_percentage','retweeted_users', 'Most_referenced_domains','detected_sources', 'detected_languages', 'Avg_no_of_tweets_per_day','Status']
        for i, row in enumerate(header_params):
            self.todays_excel_sheet1.write(0, i, row)
        self.main()

    def close_sql_connection(self, conn, cursor):
        if cursor: cursor.close()
        if conn: conn.close()

    def send_xlstwitter(self):
            con2_,cur2_ = get_mysql_connection(DB_HOST, DB_NAME_REQ, '')
            cur2_.execute(self.selectqry)
            records = cur2_.fetchall()
	    cur2_.execute(self.selectqry2)
	    records_2 = cur2_.fetchall()
            for record in records:
                screen_name,name,description,location,tweets,following,followers,likes,image,lists,timezone,language,is_verified,twitter_url,email_id,top_10_hashtags,top_5_mentioned_users,retweeted_percentage,retweeted_users, Most_referenced_domains,detected_sources, detected_languages, Avg_no_of_tweets_per_day = record
		sno_given1 = fetchmany(cur2_, 'select meta_data from twitter_crawl where sk = "%s"' % screen_name)
		id_value, sno_given,payer = ['']*3
		if sno_given1:
			try:
				#sno_given = json.loads(sno_given1[0][0]).get('sno','')
				sno_given = json.loads(sno_given1[0][0]).get('srno','')
				payer = json.loads(sno_given1[0][0]).get('payer','')
				id_value = json.loads(sno_given1[0][0]).get('id', '')
			except: pass
		else:
			sno_given = ''
                values = [id_value, sno_given, payer,screen_name,name,description,location,tweets,following,followers,likes,image,lists,timezone,language,is_verified,twitter_url,email_id,top_10_hashtags,top_5_mentioned_users,retweeted_percentage,retweeted_users, Most_referenced_domains,detected_sources, detected_languages, Avg_no_of_tweets_per_day,'DataAvailable']
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
		    values = [json.loads(rec2[2]).get('id',''),json.loads(rec2[2]).get('sno',''), rec2[0], '', '', '', '', '', '', '', '', '', '', '', '', rec2[1],json.loads(rec2[2]).get('email_address', ''), '', '', '', '', '', '', '', '', 'DataUnAvailable']
		    for col_count, value in enumerate(values):
			self.todays_excel_sheet1.write(self.row_count, col_count, value)
		    self.row_count = self.row_count+1
            self.close_sql_connection(con2_, cur2_)
            self.todays_excel_file.save(self.excel_file_name)
  	    return len(records), len(records_2)

    def main(self):
        avai, unava = self.send_xlstwitter()
	file_id = Googleupload().main('Twitter', self.email_from_list.split(','), self.excel_file_name)	
	self.alert_mail(avai, unava, file_id)
	self.mv_file(self.excel_file_name)

    def mv_file(self, file_name):
        current_path = os.path.dirname(os.path.abspath(__file__))
        cuex = os.path.join(current_path, 'twitter_sheet_files')
        make_dir(cuex)
        cmd = 'mv "%s" %s' % (file_name, cuex)
        os.system(cmd)


    def alert_mail(self, avai, unava,  file_id):
	sender_mail = sender_mail_pi
	receivers_mail_list = self.email_from_list.split(',')
	sender, receivers  = sender_mail, ','.join(receivers_mail_list)
	msg = MIMEMultipart('alternative')
	msg['Subject'] = 'Data for Twitter'
	mas = '<h4>Stats for Twitter<h4></br>'
	mas += '<p>Total : %s</p>' % str(avai+unava)
	mas += '<p>Available : %s</p>' % avai
	mas += '<p>UnAvailable : %s</p>' % unava
        mas += '<p>File name : %s</p>'% str(self.excel_file_name)
	mas += '<p>File is uploaded in Twitter sub-folder of  PositiveIntegers folder in google drive of %s</p>' % sender_mail_pi
	mas += '<p>Doc Link: "https://docs.google.com/spreadsheets/d/%s"</p>' % str(file_id)
	msg['From'] = sender
	msg['To'] = receivers
	#part = MIMEBase('application', "octet-stream")
	#part.set_payload(open(self.excel_file_name, "rb").read())
	#encoders.encode_base64(part)
	#part.add_header('Content-Disposition', 'attachment; filename=%s' % self.excel_file_name)
	#msg.attach(part)
	tem = MIMEText(''.join(mas), 'html')
	msg.attach(tem) 
	s = smtplib.SMTP('smtp.gmail.com:587')
	s.ehlo()
	s.starttls()
	s.login(sender_mail, sender_pwd_pi)
	s.sendmail(sender, receivers_mail_list, msg.as_string())
	s.quit()


if __name__ == '__main__':
        parser = optparse.OptionParser()
        parser.add_option('-d', '--db-name', default = '', help = 'db_name')
	parser.add_option('-m', '--modified_at', default = '', help = 'modified_at' )
	parser.add_option('-p', '--email_from_list', default = '', help = 'email_from_list')
        (options, args) = parser.parse_args()
        Tixlsfile(options)


