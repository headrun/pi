from w3lib.http import basic_auth_header
from scrapy.spider import BaseSpider
from scrapy.http import Request
import json
import MySQLdb
import requests

class deskcaseterminal(BaseSpider):
        name = "desk_case_terminal"
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
		self.select_query = "select sk, url, meta_data from desk_crawl where crawl_status=0"
		self.cases_insert = "INSERT INTO desk_cases(case_sk, case_id, filter_id, filter_name, case_assigned_group, case_active_at, case_active_attachments_count, case_active_notes_count, case_blurb, case_changed_at, case_label_ids, case_labels, case_language, case_locked_until, case_priority, case_opened_at, case_received_at, case_resolved_at, case_route_status, case_status, case_subject, case_type, case_updated_at, case_created_at, case_custom_fields, case_description, case_external_id, case_first_opened_at, case_first_resolved_at, case_has_failed_interactions, case_has_pending_interactions, case_customer_url, case_last_url, case_next_url, case_reference_url, created_at, modified_at, last_seen ) values(%s, %s, %s, %s, %s,  %s, %s, %s, %s, %s, %s, %s, %s, %s,  %s, %s, %s, %s, %s, %s, %s, %s, %s,  %s, %s, %s, %s, %s, %s, %s, %s, %s,  %s, %s, %s, now(), now(), now()) on duplicate key update modified_at = now(), case_sk=%s, case_id=%s, filter_id=%s, filter_name=%s, case_assigned_group=%s, case_active_at=%s, case_active_attachments_count=%s, case_active_notes_count=%s, case_blurb=%s, case_changed_at=%s, case_label_ids=%s, case_labels=%s, case_language=%s, case_locked_until=%s, case_priority=%s, case_opened_at=%s, case_received_at=%s, case_resolved_at=%s, case_route_status=%s, case_status=%s, case_subject=%s, case_type=%s, case_updated_at=%s, case_created_at=%s, case_custom_fields=%s, case_description=%s, case_external_id=%s, case_first_opened_at=%s, case_first_resolved_at=%s, case_has_failed_interactions=%s, case_has_pending_interactions=%s, case_customer_url=%s, case_last_url=%s, case_next_url=%s, case_reference_url=%s"
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
			yield Request(url, callback=self.parse, meta=meta, headers=self.headers, dont_filter=True)

	def parse(self, response):
		output = response.body
                output = json.loads(output.strip('\n'))
		values = response.meta['values']
		blurb = output.get('body', '')
		if blurb:
			values[8], values[43] = blurb, blurb
		self.cur.execute(self.cases_insert, values)
		value = ('1', values[0])
		self.cur.execute(self.update_query, value)
		self.conn.commit()		
