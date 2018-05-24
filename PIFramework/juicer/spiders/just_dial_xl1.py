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

class ExcelGenIOC1():

    def __init__(self):
        self.load_dict = {}
        self.today_date = datetime.datetime.now().date()
        self.excel_file_name = 'just_dialarc.xls' 

    def xcode(self, text, encoding='utf8', mode='strict'):
        return text.encode(encoding, mode) if isinstance(text, unicode) else text

    def get_mysql_conn(self):
        self.conn = MySQLdb.connect(db = 'AGENTS1', user='root', host = 'localhost', passwd='root', charset   = "utf8", use_unicode=False)
        self.cur = self.conn.cursor()

    def excel_generation(self):
                header = ['name', 'city', 'ref_url_city', 'photos', 'image', 'address','Category', 'payment_mode','rating_val','votes','telephone','time', 'year', 'available_services', 'buisness_info', 'place','website_link','doctor_availability','distance','number_of_ratings','reviewed_by', 'reviewed_on','review','review_rating','reference_url','Main_url']

                query = 'select sk,name, city, ref_url_city, photos, image, address ,medicalspecialty, payment_mode,rating_val,rating_count,telephone,time, year, available_services, buisness_info, place,website_link,book_appointment,distance,number_of_ratings,reference_url,main_url from justdail_meta where date(modified_at)>="2018-01-26"'
                 
		self.cur.execute(query)
		rows = self.cur.fetchall()
		todays_excel_file = xlwt.Workbook(encoding="utf-8")
		todays_excel_sheet1 = todays_excel_file.add_sheet("sheet1")
		row_count = 1

		for i, row in enumerate(header):
			todays_excel_sheet1.write(0, i, row)
                   	  
                
		for _row in rows:
		        sk = _row[0]
                        sk, name, city, ref_url_city, photos, image, address ,medicalspecialty, payment_mode,rating_val,rating_count,telephone,time, year, available_services, buisness_info, place,website_link,doctor_availability,distance,number_of_ratings,reference_url, main_url = _row
                        qry = 'select reviewed_by, reviewed_on,review,rating_value from Reviews where program_sk ="%s"'%sk
                        self.cur.execute(qry)
                        data = self.cur.fetchall()
                        if data :
                            for data_ in data :
			        reviewed_by, reviewed_on,review,rating_value = data_

			        values = [name, city, ref_url_city, photos, image, address ,medicalspecialty, payment_mode,rating_val,rating_count,telephone,time, year, available_services, buisness_info, place,website_link,doctor_availability,distance,number_of_ratings,reviewed_by, str(reviewed_on),review,rating_value,reference_url,main_url]

		                for col_count, value in enumerate(values):
	                            todays_excel_sheet1.write(row_count, col_count, value)
	                        row_count = row_count+1 
                        else : 
                             
                             reviewed_by, reviewed_on,review,rating_value = '','','',''

                             values = [name,city, ref_url_city, photos, image, address ,medicalspecialty, payment_mode,rating_val,rating_count,telephone,time, year, available_services, buisness_info, place,website_link,doctor_availability,distance,number_of_ratings,reviewed_by, reviewed_on, review, rating_value,reference_url, main_url]

                             for col_count, value in enumerate(values):
                                    todays_excel_sheet1.write(row_count, col_count, value)

                             row_count = row_count+1

                        
	        todays_excel_file.save(self.excel_file_name)
			
		  
            

    def main(self):
        self.get_mysql_conn()
        self.excel_generation()


if __name__ == '__main__':
    OBJ = ExcelGenIOC1()
    OBJ.main()


