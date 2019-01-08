import hashlib
import csv
import datetime
import datetime
import MySQLdb
import time
import scrapy
import json
import re
from datetime import timedelta
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from to_udrive import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib,ssl
import shutil
import os

class Openweathersheetscript(object):

    def __init__(self, *args, **kwargs):
        super(Openweathersheetscript, self).__init__(*args, **kwargs)
        self.con = MySQLdb.connect(db='accuweather',
        user='root', passwd='root',
        charset="utf8", host='localhost', use_unicode=True)
        self.cur = self.con.cursor()
        self.cur = self.con.cursor()
        self.excel_file_name = 'openweather_data_on_%s.csv'%str(datetime.datetime.now().date())
        header =['Key','customer_no','latitude','longitude','city_name','country','visibility','dt','base','wind_speed','wind_deg','cod','pressure','temp_min','temp_max','temp','humidity','cloud_data','weather_id','weather_main','icon','description','sunrise','sunset','message','sys_id','type_','response.url','crawled_time']
        self.oupf = open(self.excel_file_name, 'wb+')
        self.todays_excel_file  = csv.writer(self.oupf)
        self.todays_excel_file.writerow(header)
	self.select_qry = 'select * from openweather'        
        self.check_qry = 'select * from urlqueue_dev.openweather_crawl where crawl_status=9'
        self.update_qry = 'update urlqueue_dev.openweather_crawl set crawl_status=0 where crawl_status=9'
        self.del_qry = 'delete  from openweather'


    def run_main(self):
        self.cur.execute(self.check_qry)
        data = self.cur.fetchall()
        if data :
                self.cur.execute(self.update_qry)
                self.con.commit() 
		os.chdir('/root/PIFramework/juicer/spiders')
                os.system('scrapy crawl openweather_crawler_terminal -alimit=100')
        self.cur.execute(self.del_qry)
        self.con.commit()
	os.chdir('/root/PIFramework/juicer/scripts')
        os.system('python load_query_files_to_openweather_db.py')
        os.chdir('/root/PIFramework/juicer/spiders')
        self.cur.execute(self.select_qry)
        data = self.cur.fetchall()
        for row in data : 
            id_,cust_no,lat,lon,city_name,country,visibility,dt,base,wind_speed,wind_deg,cod,pressure,temp_min,temp_max,temp,humidity,cloud_data,weather_id,weather_main,icon,desc,sunrise,sunset,message,sys_id,type_,response_url,created_at,modified_at = row
            values = (str(id_),str(cust_no),str(lat),str(lon),self.normalize(city_name),self.normalize(country),str(visibility),str(dt),str(base),str(wind_speed),str(wind_deg),str(cod),str(pressure),str(temp_min),str(temp_max),str(temp),str(humidity),str(cloud_data),str(weather_id),self.normalize(weather_main),self.normalize(icon),self.normalize(desc),str(sunrise),str(sunset),str(message),str(sys_id),str(type_),response_url,modified_at) 
            self.todays_excel_file.writerow(values)
        statinfo = os.stat(self.excel_file_name)
        size = statinfo.st_size
        if size > 0  :
            self.oupf.close()
            email_from_list = ['anusha.boyina19@gmail.com']
            file_id = Googleupload().main('openweather', email_from_list, self.excel_file_name)
        os.system('mysql -uroot -proot urlqueue_dev  < openweather_crawl.sql')
        self.cur.close()
        self.con.close()

    def alert_mail(self, email_from_list, file_id, todays_excel_file) :
        sender_mail = 'positiveintegersproject@gmail.com'
        msg = MIMEMultipart('alternative')
        if email_from_list:
                receivers_mail_list = email_from_list
                msg['Subject'] = 'Openweather  data on %s' % self.crawler_start_time
                mas = '<p>File name : %s</p>'% str(paytm_file_name)
                mas += '<p>File is uploaded in paytm [sub-folder] of paytm_session_data [folder] in google drive of %s</p>' % sender_mail
                mas += '<p>Doc Link : "https://docs.google.com/spreadsheets/d/%s"</p>' % str(file_id)
        else:   
                receivers_mail_list = ['alekhya@headrun.com', 'kiranmayi@headrun.com','pi@headrun.com']
                #receivers_mail_list = ['alekhya@headrun.com']
                msg['Subject'] = 'Empty sheet of Bookmyshow Source'
                mas = '<p><h1>We got empty data for Bookmyshow Source</h1></p>'
                mas += '<p><h3>Please check on priority base</h3></p>'
        sender, receivers  = sender_mail, ','.join(receivers_mail_list)
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
 

    def xcode(self,text, encoding='utf8', mode='strict'):
        return text.encode(encoding, mode) if isinstance(text, unicode) else text

    def compact(self,text, level=0):
        if text is None: return ''

        if level == 0:
            text = text.replace("\n", " ")
            text = text.replace("\r", " ")
        compacted = re.sub("\s\s(?m)", " ", text)
        if compacted != text:
            compacted = compact(compacted, level+1)

        return compacted.strip()

    def clean(self,text):
        if not text: return text

        value = text
        value = re.sub("&amp;", "&", value)
        value = re.sub("&lt;", "<", value)
        value = re.sub("&gt;", ">", value)
        value = re.sub("&quot;", '"', value)
        value = re.sub("&apos;", "'", value)

        return value

    def normalize(self,text):
        return self.clean(self.compact(self.xcode(text)))
            
                    
        
if __name__ == '__main__':
     Openweathersheetscript().run_main()

        








