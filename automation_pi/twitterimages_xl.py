import os, sys, datetime, subprocess, MySQLdb, codecs, json
import optparse, logging, logging.handlers
import xlwt, csv

class CSVGenIOC():

    def __init__(self):
        self.load_dict = {}
        self.excel_file_name = 'twitter_images_%s.csv'%str(datetime.datetime.now().date())
        oupf = open(self.excel_file_name, 'ab+')
        self.todays_excel_file  = csv.writer(oupf)
        self.headers = ['profile_url','image_path','image_url','image_size','image_width','image_height','reference_url','email_id','status']
        self.query = 'select sk from twitter_profilepic_meta where date(modified_at)="2018-02-15" limit 1'

    def get_mysql_conn(self):
        self.conn = MySQLdb.connect(db = 'twitter_profic', user='root', host = 'localhost', passwd='root', charset   = "utf8", use_unicode=False)
        self.cur = self.conn.cursor()

    def csv_generation(self):
        self.cur.execute(self.query)
        sks = self.cur.fetchall()
        for index, sk1 in enumerate(sks):
            sk2 = sk1[0]
            sel_query = 'select sk,url,image_path,image_url,data_size,image_width,image_height,reference_url,email_id,status from twitter_profilepic_meta where date(modified_at)>="2018-02-15" and sk="%s"'%(sk2)
            self.cur.execute(sel_query)
            rows = self.cur.fetchall()
            for _row in rows:
                sk,profile_url,image_path,image_url,data_size,image_width,image_height,reference_url,email_id,status=_row
                values = [profile_url,image_path,image_url,data_size,image_width,image_height,reference_url,email_id,status]
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


