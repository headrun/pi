from multiprocessing import Process
import sys
import os
import re
import time
import datetime
from scrapy.xlib.pydispatch import dispatcher
from to_udrive import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib,ssl
import csv
import datetime
import sys
from scrapy.mail import MailSender
reload(sys)
sys.setdefaultencoding('UTF8')
import MySQLdb
from datetime import timedelta
import shutil
sys.path.insert(0, '../')
def run_scraper(p, k, path):
    os.chdir(path)
    os.system(p)
    print p, k, datetime.datetime.now()

class MultiProcess(object):

    def __init__(self):
	self.path = '/root/PIFramework/juicer/spiders'
	self.conn = MySQLdb.connect(db = 'paytm_movie', user='root', host='localhost', passwd='root', charset="utf8", use_unicode=False)
        self.cur = self.conn.cursor()
        self.header_params = ['movie_code','Movie_title','image_url','censor','genre','content','duration','trailor_url','language','opening_date','Reference_url']
        self.header_params1 = ['session_id','Movie_code','theater_name','provider_name','address','latitude','longitude','multiple_ticket','real_show_time','free_seating','token_fee_only','token_fee_pickup_time','grouped_seats','max_tickets','seats_avail','seats_unavail','seats_total','ticket_type','ticket_price', 'crawler_start_time','crawler_end_time','reference_url']
        self.crawler_start_time  = str(datetime.datetime.now() + timedelta(hours=9,minutes=34)).split('.')[0]
        self.excel_file_name1 = 'paytm_session_data_ON_%s.csv'% self.crawler_start_time
        self.excel_file_name = 'paytm_Movie_data_ON_%s.csv'% self.crawler_start_time
	self.processed_path = '/root/PIFramework/juicer/spiders/paytm_csv_files'
	self.oupf = open(self.excel_file_name, 'ab+')
	self.oupf1 = open(self.excel_file_name1, 'ab+')
        self.todays_movieef  = csv.writer(self.oupf)
        self.todays_excel_file1  = csv.writer(self.oupf1)
        self.todays_excel_file1.writerow(self.header_params1)
        self.todays_movieef.writerow(self.header_params)
        self.select_qry = 'select session_id,Movie_code,theater_name,provider_name,address,latitude,longitude,multiple_ticket,audi,real_show_time,free_seating,token_fee_only,token_fee_pickup_time,grouped_seats,max_tickets,seats_avail,seats_unavail,seats_total,ticket_type,ticket_price,crawler_starttime,reference_url from Movie_sessions'
        self.movie_query = 'select Movie_code,Movie_title,image_url,censor,genres,content,duration,trailor_url,language,opening_date,reference_url from Movie'
        self.r_list = ['export PATH=$PATH:/usr/local/bin;scrapy crawl paytm_browse -a min_=0 -a max_=10', 'export PATH=$PATH:/usr/local/bin;scrapy crawl paytm_browse -a min_=10 -a max_=20', 'export PATH=$PATH:/usr/local/bin;scrapy crawl paytm_browse -a min_=20 -a max_=30']
        self.main()

    def run_script(self):
	crawler_end_time =  str(datetime.datetime.now() + timedelta(hours=9,minutes=34)).split('.')[0]
        self.cur.execute(self.movie_query)
        data_ = self.cur.fetchall()
        for row_ in data_ :
            movie_id,movie_title,image_url,censor,genre,content,duration,trailor_url,language,opening_date,reference_url = row_
            vals_data = [movie_id,movie_title,image_url,censor,genre,content,duration,trailor_url,language,opening_date,reference_url]
            self.todays_movieef.writerow(vals_data)
        self.cur.execute(self.select_qry)
        data = self.cur.fetchall()
        for row in data :
            session_id,Movie_code,theater_name,provider_name,address,latitude,longitude,multiple_ticket,audi,real_show_time,free_seating,token_fee_only,token_fee_pickup_time,grouped_seats,max_tickets,seats_avail,seats_unavail,seats_total,ticket_type,ticket_price,crawler_start_time,reference_url = row
            values = [session_id,Movie_code,theater_name,provider_name,address,latitude,longitude,multiple_ticket,real_show_time,free_seating,token_fee_only,token_fee_pickup_time,grouped_seats,max_tickets,seats_avail,seats_unavail,seats_total,ticket_type,ticket_price,crawler_start_time,crawler_end_time,reference_url]
            self.todays_excel_file1.writerow(values)
        statinfo = os.stat(self.excel_file_name1)
        size = statinfo.st_size
        self.oupf.close()
        self.oupf1.close()
        if size > 0 :
	    email_from_list = ['anushab@headrun.com']
            files = [self.excel_file_name1,self.excel_file_name]
            for file_ in files :
                file_id = Googleupload().main('Paytm_Availability', email_from_list, file_)
		cmd = 'mv /root/PIFramework/juicer/spiders/"%s" /root/PIFramework/juicer/spiders/paytm_csv_files'%file_
		os.system(cmd)
        self.cur.close()
        self.conn.close()

    def alert_mail(self, email_from_list, file_id, paytm_file_name):
	try:
	    sender_mail = 'positiveintegersproject@gmail.com'
	    receivers_mail_list = email_from_list
	    sender, receivers  = sender_mail, ','.join(receivers_mail_list)
	    msg = MIMEMultipart('alternative')
	    msg['Subject'] = 'paytm session data on %s' % self.crawler_start_time
	    mas = '<p>File name : %s</p>'% str(paytm_file_name)
	    mas += '<p>File is uploaded in paytm [sub-folder] of paytm_session_data [folder] in google drive of %s</p>' % sender_mail
	    mas += '<p>Doc Link : "https://docs.google.com/spreadsheets/d/%s"</p>' % str(file_id)
	    msg['From'] = sender
	    msg['To'] = receivers
	    tem = MIMEText(''.join(mas), 'html')
	    msg.attach(tem)
	    s = smtplib.SMTP('smtp.gmail.com:587')
	    s.ehlo()
	    s.starttls()
	    s.login(sender_mail, 'integers')
	    s.sendmail(sender, receivers_mail_list, msg.as_string())
	    s.quit()
	except:
	    sender_mail = 'positiveintegersproject@gmail.com'
            receivers_mail_list = email_from_list
            sender, receivers  = sender_mail, ','.join(receivers_mail_list)
            msg = MIMEMultipart('alternative')
            msg['Subject'] = 'paytm session data on %s' % self.crawler_start_time
            mas = '<p>File name : %s</p>'% str(paytm_file_name)
            mas += '<p>File is uploaded in paytm [sub-folder] of paytm_session_data [folder] in google drive of %s</p>' % sender_mail
            mas += '<p>Doc Link : "https://docs.google.com/spreadsheets/d/%s"</p>' % str(file_id)
            msg['From'] = sender
            msg['To'] = receivers
            tem = MIMEText(''.join(mas), 'html')
            msg.attach(tem)
            s = smtplib.SMTP('smtp.gmail.com:587')
            s.ehlo()
            s.starttls()
            s.login(sender_mail, 'integers')
            s.sendmail(sender, receivers_mail_list, msg.as_string())
            s.quit()


    def main(self):
        processes = []
        for m in range(1, 2):
            for j in self.r_list:
                n = m + 1
                p = Process(target=run_scraper, args=(str(j),str(m), self.path))
                p.start()
                processes.append(p)
        for p in processes:
            p.join()
        self.run_script()

if __name__ == '__main__':
	MultiProcess()
