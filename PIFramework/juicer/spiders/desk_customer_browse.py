from juicer.utils import *
from w3lib.http import basic_auth_header

class deskcustomerbrowse(JuicerSpider):
	name = "desk_customer_browse"
	start_urls = ('https://www.desk.com/',)

	def __init__(self, *args, **kwargs):
		super(deskcustomerbrowse, self).__init__(*args, **kwargs)
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
		get_query_param = "select case_customer_url from desk_cases where case_customer_url not in (select customer_link from desk_customer) order by rand() limit 50000"
		self.cur.execute(get_query_param)
		self.profiles_list = [i for i in self.cur.fetchall()]
		self.customer_insert = "INSERT INTO desk_customer(customer_link, customer_id, customer_company_link, customer_twitter_user, customer_access_company_cases, customer_access_private_portal, customer_addresses, customer_avatar, customer_background, customer_company, customer_company_name, customer_created_at, customer_custom_fields, customer_display_name, customer_emails, customer_external_id, customer_first_name, customer_label_ids, customer_language, customer_last_name, customer_locked_until, customer_phone_numbers, customer_title, customer_uid, customer_updated_at, created_at, modified_at, last_seen ) values(%s, %s,  %s, %s, %s, %s, %s, %s, %s, %s, %s,  %s, %s, %s, %s, %s, %s, %s, %s, %s,  %s, %s, %s, %s, %s, now(), now(), now()) on duplicate key update modified_at = now(), customer_link=%s, customer_id=%s, customer_company_link=%s, customer_twitter_user=%s, customer_access_company_cases=%s, customer_access_private_portal=%s, customer_addresses=%s, customer_avatar=%s, customer_background=%s, customer_company=%s, customer_company_name=%s, customer_created_at=%s, customer_custom_fields=%s, customer_display_name=%s, customer_emails=%s, customer_external_id=%s, customer_first_name=%s, customer_label_ids=%s, customer_language=%s, customer_last_name=%s, customer_locked_until=%s, customer_phone_numbers=%s, customer_title=%s, customer_uid=%s, customer_updated_at=%s"

	def __del__(self):
        	self.conn.close()
	        self.cur.close()


	def parse(self, response):
                sel = Selector(response)
		if self.profiles_list:
			for cus in self.profiles_list:
				yield Request(cus[0], callback=self.parse_customer, headers = self.headers, meta = {"customer_link": cus[0]})

	def parse_customer(self, response):
		customer_links = response.meta.get('customer_link', '')
                output = response.body
                import pdb;pdb.set_trace()
                output = json.loads(output.strip('\n'))
		total_entries = output.get('_embedded', {}).get('entries', [])
		if not total_entries:
			if isinstance(output, dict):
				toal_en = []
				toal_en.append(output)
				total_entries = toal_en
		for ttl_en in total_entries:
			company_links = ttl_en.get('_links', {}).get('company', {})
			if company_links:
				company_links = company_links.get('href', '')
			twitter_user = ttl_en.get('_links', {}).get('twitter_user', {})
			if twitter_user:
				twitter_user = twitter_user.get('href', '')
			if company_links:
				company_links  = "%s%s" %(self.main_url, company_links)
			if twitter_user:
				twitter_user = "%s%s" %(self.main_url, twitter_user)
			access_company_cases = ttl_en.get('access_company_cases', '')
			access_private_portal = ttl_en.get('access_private_portal', '')
			addresses = '<>'.join(ttl_en.get('addresses', []))
			avatar = ttl_en.get('avatar', '')
			background = ttl_en.get('background', '')
			company = ttl_en.get('company', '')
			company_name = ttl_en.get('company_name', '')
			created_at = ttl_en.get('created_at', '')
			custom_fields = ttl_en.get('custom_fields', {})
                        if not custom_fields:
                                custom_fields = ''
                        else:
                                custom_fields = json.dumps(custom_fields)
			display_name = ttl_en.get('display_name', '')
			emails = ttl_en.get('emails', [])
			if emails:
				emails = '<>'.join(["%s%s%s" % (te.get('type'), ':-', te.get('value')) for te in emails])
			else:
				emails = ''
			external_id = ttl_en.get('external_id', '')
			first_name = ttl_en.get('first_name', '')
			id_ = str(ttl_en.get('id', ''))
			label_ids = '<>'.join([str(ld) for ld in ttl_en.get('label_ids', [])])
			language = ttl_en.get('language', '')
			last_name = ttl_en.get('last_name', '')
			locked_until = ttl_en.get('locked_until', '')
			phone_numbers = '<>'.join(ttl_en.get('phone_numbers', []))
			title = ttl_en.get('title', '')
			uid = ttl_en.get('uid', '')
			updated_at = ttl_en.get('updated_at', '')
			values = (customer_links, id_, company_links, twitter_user, access_company_cases, access_private_portal, addresses, avatar, background, company, company_name, created_at, custom_fields, display_name, emails, external_id, first_name, label_ids, language, last_name, locked_until, phone_numbers, title, uid, updated_at, customer_links, id_, company_links, twitter_user, access_company_cases, access_private_portal, addresses, avatar, background, company, company_name, created_at, custom_fields, display_name, emails, external_id, first_name, label_ids, language, last_name, locked_until, phone_numbers, title, uid, updated_at)
			#self.cur.execute(self.customer_insert, values)	
