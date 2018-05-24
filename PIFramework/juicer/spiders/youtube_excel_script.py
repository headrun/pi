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
        self.excel_file_name = 'youtube_video_comments3.xlsx' 

    def xcode(self, text, encoding='utf8', mode='strict'):
        return text.encode(encoding, mode) if isinstance(text, unicode) else text

    def get_mysql_conn(self):
        self.conn = MySQLdb.connect(db = 'youtube_comments', user='root', host = 'localhost', passwd='root', charset   = "utf8", use_unicode=False)
        self.cur = self.conn.cursor()

    def excel_generation(self):
                query = 'select a.sk ,a.title, a.description,a.video_link ,a.reference_url ,b.channel_sk,b.comment,b.author_name,b.reference_url,b.no_of_comments,b.published_at,b.updated_at,b.auth_channel_url,b.auth_channel_id,b.auth_image_url from Video_Info a, comments b where a.sk=b.program_sk limit 60000,40000'
                self.cur.execute(query)
                rows = self.cur.fetchall()
               
                header = ['channel_id', 'video_id', 'video_title', 'video_description', 'video_link', 'ref_url', 'comment', 'author_name', 'reference_url', 'no_of_comments', 'auth_channel_url', 'auth_channel_id', 'auth_image_url', 'published_at', 'updated_at']
                todays_excel_file = xlwt.Workbook(encoding="utf-8")
                todays_excel_sheet1 = todays_excel_file.add_sheet("sheet1")

                row_count = 1

                for i, row in enumerate(header):
                        todays_excel_sheet1.write(0, i, row)

                for _row in rows:
                   
                    video_id, video_title, video_description, video_link, ref_url, channel_sk, comment, author_name, reference_url, no_of_comments, published_at, updated_at, auth_channel_url, auth_channel_id, auth_image_url  = _row
                    values = [channel_sk, video_id, video_title, video_description, video_link, ref_url, comment, author_name, reference_url, no_of_comments, auth_channel_url, auth_channel_id, auth_image_url, str(published_at.date()), str(updated_at.date())]
                    
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


