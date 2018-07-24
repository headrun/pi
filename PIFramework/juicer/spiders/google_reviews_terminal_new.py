import time
import re
import csv
import md5
import datetime
import MySQLdb
from scrapy.spider import BaseSpider
from scrapy.http import Request
import json
import requests

class GoogleReviewsTerminal(BaseSpider):

    name = 'google_reviews_crawl'

    def __init__(self):

        self.con = MySQLdb.connect(db='google_reviews', host='localhost', charset="utf8", use_unicode=True, user='root', passwd='root')
        self.cur = self.con.cursor()
        self.header_params = ['Main_keyword','Sub_keyword','reviewed_by', 'Review_text','Review_Star_Rating','Rating','No_of_Reviews','Time','reference_url', 'main_url', 'status']
        self.insert_qry2 = 'insert into Reviews_meta(sk, program_sk, main_keyword, sub_keyword, reviewed_by, Review_text, Review_Star_Rating, Rating, No_of_Reviews, Time, reference_url, main_url, status, created_at, modified_at) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(),now()) on duplicate key update modified_at = now()'
	self.select_query = "select sk,url,meta_data from reviewslink_crawl where crawl_status=10"
	self.upd_qry1 = "update reviewslink_crawl set crawl_status=1 where sk='%s'"
        self.upd_qry2 = "update reviewslink_crawl set crawl_status=2 where sk='%s'"
	self.excel_file_name = 'google_places_reviews_data_%s.csv'%str(datetime.datetime.now()).replace(' ', '_')
        oupf = open(self.excel_file_name, 'ab+')
        self.todays_excel_file  = csv.writer(oupf)
        self.todays_excel_file.writerow(self.header_params)

    def start_requests(self):
	self.cur.execute(self.select_query)
	rows = self.cur.fetchall()
	for row in rows:
		prg_sk, main_url, meta_data = row
		meta = json.loads(meta_data)
		reviews = meta['reviews_list']
		for review in reviews:
		    self.todays_excel_file.writerow(review)
		meta.pop('reviews_list')
		meta.update({'prg_sk':prg_sk, 'main_url':main_url})
		yield Request('https://www.justdial.com', callback=self.parse, meta=meta, dont_filter=True)

    def parse(self, response):

	meta = response.meta
	cookies = {
                'SID': 'MwbVsR65CXu_Gi29gTd9_-J-Q6S2vWHkx7YhdsTM1EwvqlOH82fZyk3llekSM2RH1YM83g.',
                'HSID': 'ATNWOBfp8bq9v21wa',
                'SSID': 'Ak80D8H3DIIrO7WpG',
                'APISID': '74DiOxa6vy-chcub/ABctrqz7bE30f5ANA',
                'SAPISID': 'GZ2hLtIeK0HsjfZk/AAz8PEj1Hm8bWwG0e',
                'NID': '134=dLcxqMY0OOubHg0cygNF-8O1CIudtkKMOOKkze4nqbjPDcDIUreMyliZknV3pWewW4-ntZ3p8hDdiDU_5x-gFicbIRqW7fryfjo-I9S79_eW-MttffxL5W9LW_0Skm9V2eduN-ES5G0a5_z57pJc_3emNAlXMsgW1YlirRXlAJ9AywHI-5uWNtM6k_L_y8mCYRY7_VGpLuQmRHzfkwdiO94e5izEDbBYmTnqct6V97jEchkhRnFh9Q_19X1eDsQejS7tYThyQn1aa4xZbGkXJzBapaNOPU0hjQ9kiHuH7pcHEuWw5fgKNh65GDb08PEuH88qYhnbLwpXPGKxMGedbmwSoxoIuU3GkDXOYag7XZJq6Dk6MxFroX7wG4wHM1lx153D',
                'CONSENT': 'YES+IN.en+20170402-16-0',
                '1P_JAR': '2018-07-13-06',
        }
        headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:61.0) Gecko/20100101 Firefox/61.0',
                'Accept': '*/*',
                'Accept-Language': 'en-GB,en;q=0.5',
                'Referer': 'https://www.google.co.in/',
                'Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
        }
	url = meta['main_url']
	prg_sk = meta['prg_sk']
	main_keyword = meta['main_keyword'].replace('\n', '')
        main_rating = meta['main_rating']
        main_url = meta['url']
	reviews = meta['reviews']
	try:
		data_text = ''.join(re.findall('data=(.*)', url)).split('!')
		for item in data_text:
		    if ':' in item:
			str1 = item
			break
		link = 'https://www.google.co.in/maps/preview/reviews?authuser=0&hl=en&gl=in&pb=!%s!%s'
		for num in range(8, int(reviews)+10, 10):
		    str2 = '2i{0}!3i10!4e6!7m4!2b1!3b1!5b1!6b1'.format(str(num))
		    url = link%(str1, str2)
		    response = requests.get(url, headers=headers, cookies=cookies)
		    data = json.loads(response.text.replace('\n', '').replace(")]}\'", ''))[0]
		    if data:
			    for review in data:
				r_url = review[0][0]
				reviewd_by = review[0][1]
				if reviewd_by:
				    reviewd_by = reviewd_by.decode('utf8', 'ignore').encode('utf8')
				time_ = review[1]
				rview = review[3]
				if rview:
				    rview =  rview.decode('utf8', 'ignore').encode('utf8')
				r_sk = review[6]
				r_rat = review[4]
				no_reviews =  review[12][1][1]
				vals = (r_sk, prg_sk, main_keyword, '', reviewd_by, rview, str(r_rat), main_rating, reviews, time_, r_url, main_url, 'Available')
				vals1 = (main_keyword, '', reviewd_by, rview,str(r_rat),main_rating,reviews,time_, r_url, main_url,'Available')
				self.cur.execute(self.insert_qry2, vals)
				self.con.commit()
				self.todays_excel_file.writerow(vals1)
		self.cur.execute(self.upd_qry1%prg_sk)
	except:
		self.cur.execute(self.upd_qry2%prg_sk)	

