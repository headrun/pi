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

class CSVGenIOC():

    def __init__(self):
        self.load_dict = {}
        self.excel_file_name = 'baby_names_%s.csv'%str(datetime.datetime.now().date())
        oupf = open(self.excel_file_name, 'ab+')
        self.todays_excel_file  = csv.writer(oupf)
        self.headers = ['name','gender','similar_names','meaning_of_name','popularity','name_usage','origin','famous_names','reference_url']
        self.query = 'select sk from baby_names'

    def get_mysql_conn(self):
        self.conn = MySQLdb.connect(db = 'Baby_Names', user='root', host = 'localhost', passwd='root', charset   = "utf8", use_unicode=False)
        self.cur = self.conn.cursor()

    def csv_generation(self):
        self.cur.execute(self.query)
        sks = self.cur.fetchall()
        for index, sk1 in enumerate(sks):
            sk2 = sk1[0]
            sel_query = 'select name,gender,similar_names,meaning_name,popularity,name_usage,origin_usage,famous_names,reference_url from baby_names where date(modified_at)>="2018-02-02" and sk="%s"'%(sk2)
            self.cur.execute(sel_query)
            rows = self.cur.fetchall()
            for _row in rows:
                name,gender,similar_names,meaning_name,popularity,name_usage,origin_usage,famous_names,reference_url=_row
                values = [name,gender,similar_names,meaning_name,popularity,name_usage,origin_usage,famous_names,reference_url]
                values =  [i for i in values]
                if index == 0:
                    self.todays_excel_file.writerow(self.headers)
                self.todays_excel_file.writerow(values)

    def main(self):
        self.get_mysql_conn()
        self.csv_generation()

if __name__ == '__main__':
    OBJ = CSVGenIOC()
    OBJ.main()


