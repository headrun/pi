from w3lib.http import basic_auth_header
from scrapy.spider import BaseSpider
from scrapy.http import Request
import json
import MySQLdb
import requests

class deskrepliesterminal(BaseSpider):
    name = "desk_replies_terminal"
    handle_httpstatus_list = [401]
        
    def __init__(self, *args, **kwargs):
        self.auth = basic_auth_header('chetan.m@positiveintegers.com', 'Welcome@123')
        self.main_url = 'https://sathyamcinemas.desk.com'
        self.headers = {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json',
                        'Authorization': self.auth
                        }
        self.conn = MySQLdb.connect(user="root", host = "localhost", db="DESKCASES", passwd='root', use_unicode=True)
        self.cur  = self.conn.cursor()
        self.conn.set_character_set('utf8')
        self.cur.execute('SET NAMES utf8;')
        self.cur.execute('SET CHARACTER SET utf8;')
        self.cur.execute('SET character_set_connection=utf8;')
	self.select_query = "select sk, url, meta_data from desk_crawl"
	self.cases_insert = "INSERT INTO desk_replies(reply_id, case_sk, case_id, filter_id, reply, reply_from, reply_updated_at, created_at, modified_at) values(%s, %s, %s, %s, %s, %s, %s, now(), now()) on duplicate key update modified_at = now()"
	self.update_query = 'update desk_crawl set crawl_status=%s where sk=%s'
	
    def __del__(self):
        self.conn.close()
        self.cur.close()
	
    def start_requests(self):
	self.cur.execute(self.select_query)
	rows = self.cur.fetchall()
	for row in rows:
	    case_sk, url, meta_data = row
	    meta = json.loads(meta_data)
	    url = url.replace('message', 'replies')
	    yield Request(url, callback=self.parse, meta=meta, headers=self.headers, dont_filter=True)

    def parse(self, response):
        output = response.body
	output = json.loads(output.strip('\n'))
	values = response.meta['values']
	body = output.get('_embedded', {}).get('entries', [])
	if body:
	    for lst in body:
		if 'event_type' not in lst.keys():
	            reply = lst['body']
		    id_ = lst['id']
		    from_ = lst.get('from', '')
		    if not from_:
                        from_ = lst.get('from_facebook_name', '')
		    updated_at = lst.get('updated_at', '')
		    case_sk = values[0]
		    case_id = values[1]
		    filter_id = values[2]
		    c_values = (id_, case_sk, case_id, filter_id, reply, from_, updated_at)
		    self.cur.execute(self.cases_insert, c_values)
		    self.conn.commit()
