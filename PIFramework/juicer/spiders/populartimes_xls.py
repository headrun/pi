import os, sys, datetime, subprocess, MySQLdb, codecs, json
import optparse, logging, logging.handlers
import glob
import xlwt
import csv
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
        self.excel_file_name = 'populartimes2.xls' 

    def xcode(self, text, encoding='utf8', mode='strict'):
        return text.encode(encoding, mode) if isinstance(text, unicode) else text

    def get_mysql_conn(self):
        self.conn = MySQLdb.connect(db = 'Popular_times2', user='root', host = 'localhost', passwd='', charset   = "utf8", use_unicode=False)
        self.cur = self.conn.cursor()

    def excel_generation(self):
                header = ['search_keyword','Name','Address','Phone','Rating','day','timings','status','processed_time','keyword_popular_times_availability','search_state','reference_url','main_url']

                query = "select search_keyword,Name,Address,Phone,Rating,day,timings,status,processed_time,\
				keyword_popular_times_availability, search_state,reference_url,main_url from Popular_meta"
                 
		self.cur.execute(query)
		rows = self.cur.fetchall()
		todays_excel_file = xlwt.Workbook(encoding="utf-8")
		todays_excel_sheet1 = todays_excel_file.add_sheet("sheet1")
		row_count = 1

		for i, row in enumerate(header):
			todays_excel_sheet1.write(0, i, row)
                   	  
                
		for _row in rows:
		        
                	search_keyword,Name,Address,Phone,Rating,day,timings,status,processed_time,\
				keyword_popular_times_availability, search_state,reference_url,main_url = _row
			values = [search_keyword,Name,Address,Phone,Rating,day,timings,status,processed_time,keyword_popular_times_availability, search_state,reference_url,main_url]
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


