import os, sys, datetime, subprocess, MySQLdb, codecs, json
import optparse, logging, logging.handlers
import xlwt, csv
import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
import string
import smtplib

class ExcelGenIOC():

    def __init__(self):
        self.load_dict = {}
        self.today_date = str(datetime.datetime.now()).split('.')[0].replace(' ','_')
        self.excel_file_name = 'tripadvisor_%s.csv'%self.today_date

    def xcode(self, text, encoding='utf8', mode='strict'):
        return text.encode(encoding, mode) if isinstance(text, unicode) else text

    def get_mysql_conn(self):
        self.conn = MySQLdb.connect(db = 'Trip_Advisor', user='root', host = 'localhost', passwd='root', charset   = "utf8", use_unicode=False)
        self.cur = self.conn.cursor()

    def excel_generation(self):
                header = ['sk', 'title', 'no_of_reviews', 'address', 'contact_number', 'image', ' reference_url', 'review_id','review_title','reviewed_on','reviewed_with','description','user_thank','user_likes', 'reviewed_by', 'location', 'contributor', 'votes', 'review_rating','review_image','excellent','very_good','average','poor','terrible','url']
		oupf = open(self.excel_file_name, 'ab+')
		todays_excel_file = xlwt.Workbook(encoding="utf-8")
		todays_excel_file  = csv.writer(oupf)
		todays_excel_file.writerow(header)
                query = "select sk, title, no_of_reviews, address, contact_number, image, reference_url from tripadvisor_meta where date(modified_at)>='2018-08-30'"
		self.cur.execute(query)
		rows = self.cur.fetchall()
		for _row in rows:
			sk, title, no_of_reviews, address, contact_number, image,reference_url = _row
                        qry = 'select review_id,review_title,reviewed_on,reviewed_with,description,user_thank, user_likes,reviewed_by, location, contributor, votes,review_rating,image,excellent,very_good,average,poor,terrible,reference_url from tripadvisor_review where program_sk ="%s" and date(modified_at)>="2018-08-30"'%str(sk)
                        self.cur.execute(qry)
                        data = self.cur.fetchall()
                        if data :
		       		for data_ in data :
					review_id,review_title,reviewed_on,reviewed_with,description,user_thank,user_likes,reviewed_by,location,contributor,votes,review_rating,review_image,excellent,very_good,average,poor,terrible,url = data_
	                                values = [sk, title, no_of_reviews, address, contact_number, image, reference_url,review_id,review_title,reviewed_on,reviewed_with,description,user_thank, user_likes,reviewed_by, location, contributor, votes, review_rating,review_image,excellent,very_good,average,poor,terrible,url]
					todays_excel_file.writerow(values)
			else:
				values = [sk, title, no_of_reviews, address, contact_number, image, reference_url, '','','','','','','','','','','','','','','','','','','']
				todays_excel_file.writerow(values)
		
    def main(self):
        self.get_mysql_conn()
        self.excel_generation()


if __name__ == '__main__':
    OBJ = ExcelGenIOC()
    OBJ.main()


