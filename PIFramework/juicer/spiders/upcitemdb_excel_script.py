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
        self.excel_file_name = 'upc_itemdb.xls' 

    def xcode(self, text, encoding='utf8', mode='strict'):
        return text.encode(encoding, mode) if isinstance(text, unicode) else text

    def get_mysql_conn(self):
        self.conn = MySQLdb.connect(db = 'UPCITEMDB', user='root', host = 'localhost', passwd='root', charset   = "utf8", use_unicode=False)
        self.cur = self.conn.cursor()

    def excel_generation(self):
                header = ['UPC','ean', 'amazon_asin', 'country_of_registration', 'brand', 'model', 'size', 'color', 'weight','product_dimension','last_scanned', 'product_title', 'product_name_variations', 'isbn', 'isbn_identifier_group', 'isbn_publisher', 'isbn_title_id', 'isbn_check_digit', 'image', 'aux_info', 'reference_url']
                query = "select sk, upc, ean, amazon_asin, country_of_registration, brand, model, size, color, weight, product_dimension,last_scanned, product_title, product_name_variations, isbn, isbn_identifier_group, isbn_publisher, isbn_title_id, isbn_check_digit, image, aux_info, reference_url from upcitem_meta"
		self.cur.execute(query)
		rows = self.cur.fetchall()
		todays_excel_file = xlwt.Workbook(encoding="utf-8")
		todays_excel_sheet1 = todays_excel_file.add_sheet("sheet1")
		row_count = 1

		for i, row in enumerate(header):
			todays_excel_sheet1.write(0, i, row)
                
		for _row in rows:
		        sk, upc, ean, amazon_asin, country_of_registration, brand, model, size, color, weight, product_dimension,last_scanned, product_title, product_name_variations, isbn, isbn_identifier_group, isbn_publisher, isbn_title_id, isbn_check_digit, image, aux_info, reference_url = _row
			    
			values = [upc,ean,amazon_asin,country_of_registration,brand,model,size,color,weight,product_dimension,last_scanned,product_title,product_name_variations,isbn, isbn_identifier_group, isbn_publisher, isbn_title_id, isbn_check_digit,image,aux_info,reference_url]
	                   
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


