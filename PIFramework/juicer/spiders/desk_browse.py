from juicer.utils import *
from w3lib.http import basic_auth_header

class deskbrowse(JuicerSpider):
	name = "desk_browse"
	start_urls = ('https://www.desk.com/',)

	def __init__(self, *args, **kwargs):
		super(deskbrowse, self).__init__(*args, **kwargs)
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
		self.filter_insert = "INSERT INTO desk_filter(filter_id, filter_name, filter_position, filter_routing_enabled, filter_sort_direction, filter_sort_field, filter_self_link, filter_cases_link, filter_reference_url, created_at, modified_at, last_seen) values(%s, %s, %s, %s,  %s, %s, %s, %s, %s, now(), now(), now()) on duplicate key update modified_at = now(), filter_id=%s, filter_name=%s, filter_position=%s, filter_routing_enabled=%s, filter_sort_direction=%s, filter_sort_field=%s, filter_self_link=%s, filter_cases_link=%s, filter_reference_url=%s"
		self.cases_insert = "INSERT INTO desk_cases(case_sk, case_id, filter_id, filter_name, case_assigned_group, case_active_at, case_active_attachments_count, case_active_notes_count, case_blurb, case_changed_at, case_label_ids, case_labels, case_language, case_locked_until, case_priority, case_opened_at, case_received_at, case_resolved_at, case_route_status, case_status, case_subject, case_type, case_updated_at, case_created_at, case_custom_fields, case_description, case_external_id, case_first_opened_at, case_first_resolved_at, case_has_failed_interactions, case_has_pending_interactions, case_customer_url, case_last_url, case_next_url, case_reference_url, created_at, modified_at, last_seen ) values(%s, %s, %s, %s, %s,  %s, %s, %s, %s, %s, %s, %s, %s, %s,  %s, %s, %s, %s, %s, %s, %s, %s, %s,  %s, %s, %s, %s, %s, %s, %s, %s, %s,  %s, %s, %s, now(), now(), now()) on duplicate key update modified_at = now(), case_sk=%s, case_id=%s, filter_id=%s, filter_name=%s, case_assigned_group=%s, case_active_at=%s, case_active_attachments_count=%s, case_active_notes_count=%s, case_blurb=%s, case_changed_at=%s, case_label_ids=%s, case_labels=%s, case_language=%s, case_locked_until=%s, case_priority=%s, case_opened_at=%s, case_received_at=%s, case_resolved_at=%s, case_route_status=%s, case_status=%s, case_subject=%s, case_type=%s, case_updated_at=%s, case_created_at=%s, case_custom_fields=%s, case_description=%s, case_external_id=%s, case_first_opened_at=%s, case_first_resolved_at=%s, case_has_failed_interactions=%s, case_has_pending_interactions=%s, case_customer_url=%s, case_last_url=%s, case_next_url=%s, case_reference_url=%s"

	def __del__(self):
        	self.conn.close()
	        self.cur.close()


	def parse(self, response):
                sel = Selector(response)
		url = "%s%s" % (self.main_url, '/api/v2/filters/')
		yield Request(url, callback=self.prase_login, headers = self.headers)

	def prase_login(self, response):
		output = response.body
		output = json.loads(output.strip('\n'))
		total_entries = output.get('_embedded',{}).get('entries', [])
		for total_filter_entries in total_entries:
			filter_active = total_filter_entries.get('active', '')
			filter_id = str(total_filter_entries.get('id', ''))
			filter_name = total_filter_entries.get('name', '')
			filter_position = str(total_filter_entries.get('position', ''))
			filter_routing_enabled = str(total_filter_entries.get('routing_enabled', ''))
			filter_sort_direction = total_filter_entries.get('sort_direction', '')
			filter_sort_field = total_filter_entries.get('sort_field', '')
			filter_self_link = total_filter_entries.get('_links',{}).get('self', {}).get('href', '')
			if filter_self_link:
				filter_self_link = "%s%s" %(self.main_url, filter_self_link)
			filter_cases_link = total_filter_entries.get('_links',{}).get('cases', {}).get('href', '')
			if filter_cases_link:
				filter_full_case_link = "%s%s%s" %(self.main_url, filter_cases_link, '?page=1&per_page=100')
				yield Request(filter_full_case_link, callback=self.parse_case, headers = self.headers, meta={"filter_id":filter_id, "filter_name":filter_name})
				values = (filter_id, filter_name, filter_position, filter_routing_enabled, filter_sort_direction, filter_sort_field, filter_self_link, filter_cases_link, response.url, filter_id, filter_name, filter_position, filter_routing_enabled, filter_sort_direction, filter_sort_field, filter_self_link, filter_cases_link, response.url)
				self.cur.execute(self.filter_insert, values)

	def parse_case(self, response):
		filter_id = response.meta.get('filter_id', '')
		filter_name = response.meta.get('filter_name', '')
		output = response.body
		output = json.loads(output.strip('\n'))
		next_page = output.get('_links', {}).get('next', {})
		if next_page:
			next_page = next_page.get('href', '')
		last_page = output.get('_links', {}).get('last', {})
		if last_page:
			last_page = last_page.get('href', '')
		if last_page:
			last_page = "%s%s" %(self.main_url, last_page)
		if next_page:
			next_page = "%s%s" %(self.main_url, next_page)
			yield Request(next_page, callback=self.parse_case, headers = self.headers, meta={"filter_id":filter_id, "filter_name":filter_name})
		total_entries = output.get('_embedded', {}).get('entries', [])
		for ttl_en in total_entries:
			customer_links = ttl_en.get('_links', {}).get('customer', {})
			customer_links = customer_links.get('href', '')
			if customer_links:
				customer_links = '%s%s' % (self.main_url, customer_links)
			attachment_links = ttl_en.get('_links', {}).get('assigned_group', {})
			if attachment_links:
				attachment_links = attachment_links.get('href', '')
			if attachment_links:
				attachment_links = '%s%s' % (self.main_url, attachment_links)
			active_at = ttl_en.get('active_at', '')
			active_attachments_count = str(ttl_en.get('active_attachments_count', ''))
			active_notes_count = str(ttl_en.get('active_notes_count', ''))
			blurb = normalize(ttl_en.get('blurb', ''))
			changed_at = ttl_en.get('changed_at', '')
			created_at = ttl_en.get('created_at', '')
			custom_fields = ttl_en.get('custom_fields', {})
			if not custom_fields:
				custom_fields = ''
			else:
				custom_fields = json.dumps(custom_fields)
			description = normalize(ttl_en.get('description', ''))
			external_id = ttl_en.get('external_id', '')
			first_opened_at = ttl_en.get('first_opened_at', '')
			first_resolved_at = ttl_en.get('first_resolved_at', '')
			has_failed_interactions = ttl_en.get('has_failed_interactions', '')
			has_pending_interactions = ttl_en.get('has_pending_interactions', '')
			id_ = str(ttl_en.get('id', ''))
			label_ids = '<>'.join([str(ld) for ld in ttl_en.get('label_ids', [])])
			labels = normalize('<>'.join(ttl_en.get('labels', [])))
			language = ttl_en.get('language', '')
			locked_until = ttl_en.get('locked_until', '')
			priority = ttl_en.get('priority', '')
			opened_at = ttl_en.get('opened_at', '')
			received_at = ttl_en.get('received_at', '')
			resolved_at = ttl_en.get('resolved_at', '')
			route_status = ttl_en.get('route_status', '')
			status = ttl_en.get('status', '')
			subject = normalize(ttl_en.get('subject', ''))
			type_ = ttl_en.get('type', '')
			updated_at = ttl_en.get('updated_at', '')
			case_sk = md5("%s%s%s%s" % (normalize(filter_name), id_, normalize(subject), normalize(blurb)))
			values = (case_sk, id_, filter_id, filter_name, attachment_links, active_at, active_attachments_count, active_notes_count, blurb, changed_at, label_ids, labels, language, locked_until, priority, opened_at, received_at, resolved_at, route_status, status, subject, type_, updated_at, created_at, custom_fields, description, external_id, first_opened_at, first_resolved_at, has_failed_interactions, has_pending_interactions, customer_links, last_page, next_page, response.url, case_sk, id_, filter_id, filter_name, attachment_links, active_at, active_attachments_count, active_notes_count, blurb, changed_at, label_ids, labels, language, locked_until, priority, opened_at, received_at, resolved_at, route_status, status, subject, type_, updated_at, created_at, custom_fields, description, external_id, first_opened_at, first_resolved_at, has_failed_interactions, has_pending_interactions, customer_links, last_page, next_page, response.url)
			self.cur.execute(self.cases_insert, values)
