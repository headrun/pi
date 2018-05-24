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
        self.today_date = datetime.datetime.now().date()
        self.excel_file_name = 'tripadvisor.xls' 

    def xcode(self, text, encoding='utf8', mode='strict'):
        return text.encode(encoding, mode) if isinstance(text, unicode) else text

    def get_mysql_conn(self):
        self.conn = MySQLdb.connect(db = 'Trip_Advisor', user='root', host = 'localhost', passwd='root', charset   = "utf8", use_unicode=False)
        self.cur = self.conn.cursor()

    def excel_generation(self):
                header = ['sk', 'title', 'no_of_reviews', 'address', 'contact_number', 'image', ' reference_url', 'review_id','review_title','reviewed_on','reviewed_with','description','user_thank','user_likes', 'reviewed_by', 'location', 'contributor', 'votes', 'review_rating','review_image','excellent','very_good','average','poor','terrible','url']

                query = "select sk, title, no_of_reviews, address, contact_number, image, reference_url from tripadvisor_meta where date(modified_at)='2017-10-27'"
                 
		self.cur.execute(query)
		rows = self.cur.fetchall()
		todays_excel_file = xlwt.Workbook(encoding="utf-8")
		todays_excel_sheet1 = todays_excel_file.add_sheet("sheet1")
		row_count = 1

		for i, row in enumerate(header):
			todays_excel_sheet1.write(0, i, row)
                   	  
                
		for _row in rows:
		        
                        sk, title, no_of_reviews, address, contact_number, image,reference_url = _row
                        qry = 'select review_id,review_title,reviewed_on,reviewed_with,description,user_thank, user_likes,reviewed_by, location, contributor, votes,review_rating,image,excellent,very_good,average,poor,terrible,reference_url from tripadvisor_review where program_sk ="%s" and date(modified_at)="2017-10-27"'%str(sk)
                        self.cur.execute(qry)
                        data = self.cur.fetchall()
                        if data :
                            for data_ in data :
			        #review_title,reviewd_on,reviewed_with,description,user_thank, reviewed_by, location, contributor, votes, extra_info,url = data_
				review_id,review_title,reviewed_on,reviewed_with,description,user_thank,user_likes,reviewed_by,location,contributor,votes,review_rating,review_image,excellent,very_good,average,poor,terrible,url = data_

			        values = [sk, title, no_of_reviews, address, contact_number, image, reference_url,review_id,review_title,reviewed_on,reviewed_with,description,user_thank, user_likes,reviewed_by, location, contributor, votes, review_rating,review_image,excellent,very_good,average,poor,terrible,url]

		                for col_count, value in enumerate(values):
	                            todays_excel_sheet1.write(row_count, col_count, value)
	                        row_count = row_count+1 
                        
	        todays_excel_file.save(self.excel_file_name)
			
		  
            

    def main(self):
        self.get_mysql_conn()
        self.excel_generation()


if __name__ == '__main__':
    OBJ = ExcelGenIOC()
    OBJ.main()


