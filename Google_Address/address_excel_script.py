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
        self.excel_file_name = 'cleaned_permutations.xls' 

    def xcode(self, text, encoding='utf8', mode='strict'):
        return text.encode(encoding, mode) if isinstance(text, unicode) else text

    def get_mysql_conn(self):
        self.conn = MySQLdb.connect(db = 'address_components', user='root', host = 'localhost', passwd='root', charset   = "utf8", use_unicode=False)
        self.cur = self.conn.cursor()

    def excel_generation(self):
                #query = 'select sk, key_value, old_address, address_new, formatted_address, geometry_bounds_ne_lat, geometry_bounds_ne_lng, geometry_bounds_sw_lat, geometry_bounds_sw_lng, location_lat, location_lng, location_type, viewport_ne_lat, viewport_ne_lng, viewport_sw_lat, viewport_sw_lng, partial_match, place_id, types, status,         reference_url,long_name, short_name, component_type from  address_pincode order by id '
                query = 'select * from Permutations order by id'
           
                self.cur.execute(query)
                rows = self.cur.fetchall()
             
                header = ['id','sk','s_no','key_value','old_address','new_address','address','formatted_address','geometry_bounds_ne_lat','geometry_bounds_ne_lng','geometry_bounds_sw_lat','geometry_bounds_sw_lng','location_lat','location_lng','location_type','viewport_ne_lat','viewport_ne_lng','viewport_sw_lat','viewport_sw_lng','partial_match','place_id','types','status','reference_url','long_name','short_name','component_type']
                todays_excel_file = xlwt.Workbook(encoding="utf-8")
                todays_excel_sheet1 = todays_excel_file.add_sheet("sheet1")

                row_count = 1

                for i, row in enumerate(header):
                        todays_excel_sheet1.write(0, i, row)

                for _row in rows:
                   
                    id_, sk, s_no, key_value, old_address, new_address, address, formatted_address,geometry_bounds_ne_lat,geometry_bounds_ne_lng,geometry_bounds_sw_lat, geometry_bounds_sw_lng,location_lat, location_lng,location_type, viewport_ne_lat,viewport_ne_lng, viewport_sw_lat,viewport_sw_lng,partial_match, place_id, types,status,reference_url,long_name,short_name,component_type = _row
		    new_address  = new_address.decode('string_escape')
                    old_address = old_address.decode('string_escape')
		    address = address.decode('string_escape')
                    values = [id_, sk, s_no , key_value, old_address, new_address,  address, formatted_address, geometry_bounds_ne_lat, \
			      geometry_bounds_ne_lng, geometry_bounds_sw_lat, geometry_bounds_sw_lng, location_lat,\
			      location_lng, location_type, viewport_ne_lat, viewport_ne_lng, viewport_sw_lat,\
			      viewport_sw_lng, partial_match, place_id, types, status,reference_url,long_name,short_name,component_type ]
                    
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


