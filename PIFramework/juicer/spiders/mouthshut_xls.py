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

    def xcode(self, text, encoding='utf8', mode='strict'):
        return text.encode(encoding, mode) if isinstance(text, unicode) else text

    def get_mysql_conn(self):
        self.conn = MySQLdb.connect(db = 'MOUTHSHUT', user='root', host = 'localhost', passwd='root', charset   = "utf8", use_unicode=False)
        self.cur = self.conn.cursor()

    def excel_generation(self):
		header = ['product_id', 'product_title', 'reviewed_by', 'reviewed_on', 'review', 'category', 'product_url', 'review_rating', 'verified_purchase_flag', 'review_title', 'no_comments', 'review_likes', 'user_likes', 'views', 'keyword', 'useful', 'very_useful', 'not_useful', 'fake', 'no_of_reviews', 'location', 'author_url']
                query = "select sk, product_id, name, reviewed_by, reviewed_on, review, category, review_url, review_rating, verified_purchase_flag, aux_info from CustomerReviews where date(modified_at)='2018-06-11'"
                excel_file_name = 'mouthshut_data_%s.csv' % str(datetime.datetime.now().date()) 
		oupf = open(excel_file_name, 'ab+')
		todays_excel_file = xlwt.Workbook(encoding="utf-8")
		todays_excel_file  = csv.writer(oupf)
		todays_excel_file.writerow(header)
		self.cur.execute(query)
		rows = self.cur.fetchall()
                   	  
		for _row in rows:
		        sk, product_id, name, reviewed_by, reviewed_on, review, category, review_url, review_rating, verified_purchase_flag, aux_info = _row
		        aux_info = json.loads(aux_info)
			post_title = self.xcode(aux_info.get('post_title', ''))
			no_comments = aux_info.get('no_comments', '')
			review_likes = aux_info.get('review_likes', '')
			user_likes = aux_info.get('user_likes', '')
			views = aux_info.get('views', '')
			keyword = self.xcode(aux_info.get('browse', '')).replace('%20', ' ')
			useful = aux_info['useful'].get('Useful', '')
			very_useful = aux_info['useful'].get('Very Useful', '')
			not_useful = aux_info['useful'].get('Not Useful', '')
			fake = aux_info.get('fake', '')
			no_of_reviews = aux_info.get('no_of_reviews', '').replace('Review', '')
			location = self.xcode(aux_info.get('location', ''))
			author_url = aux_info.get('author_url', '')
			if 'page' in review_url:
				product_id = review_url.split('-')[-3]
			else:
				product_id = review_url.split('-')[-1]
			values = [product_id, self.xcode(name), self.xcode(reviewed_by), str(reviewed_on), self.xcode(review), category, review_url, review_rating, verified_purchase_flag, post_title, no_comments, review_likes, user_likes, views, keyword, useful, very_useful, not_useful, fake, no_of_reviews, location, author_url]
			todays_excel_file.writerow(values)

    def main(self):
        self.get_mysql_conn()
        self.excel_generation()


if __name__ == '__main__':
    OBJ = ExcelGenIOC()
    OBJ.main()


