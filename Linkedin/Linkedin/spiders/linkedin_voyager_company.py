from linkedin_logins import *
from linkedin_voyage_queries import *
from linkedin_voyager_utils import *

class Linkedinpremiumapivoyagercompany(Voyagerapi):
	name = "linkedinapivoyager_company_browse"
	allowed_domains = ["linkedin.com"]
	start_urls = ('https://www.linkedin.com/uas/login?goback=&trk=hb_signin',)

	def __init__(self, *args, **kwargs):
		super(Linkedinpremiumapivoyagercompany, self).__init__(*args, **kwargs)
                self.login = kwargs.get('login', 'ramanujan')
		self.upcpqu = "update linkedin_company_crawl set crawl_status='%s' where sk = '%s'"
                self.con, self.cur = get_mysql_connection(DB_HOST, DB_NAME_REQ, '')
                get_query_param = "select sk, url, meta_data from linkedin_company_crawl where crawl_status=0 limit 100"
                self.cur.execute(get_query_param)
                self.profiles_list = [i
                    for i in self.cur.fetchall()
                ]
                dispatcher.connect(self.spider_closed, signals.spider_closed)
                self.domain = domain_premium

	def parse(self, response):
                sel = Selector(response)
                command_prxy = cvs = response.meta.get('proxy','')\
                .replace('http://','').replace(':3279','')\
                .replace('https://','')
                logincsrf = ''.join(sel.xpath('//input[@name="loginCsrfParam"]/@value').extract())
                csrf_token = ''.join(sel.xpath('//input[@name="csrfToken"]/@value').extract())
                source_alias = ''.join(sel.xpath('//input[@name="sourceAlias"]/@value').extract())
		if self.profiles_list:
			logind_date = "%s%s"%(str(datetime.datetime.now().date()), ' 00:00:00')
			sk_login_self = self.login
			login_account = mails_dict[self.login]
			account_mail, account_password = login_account
			yes_s, skf_login_self = self.checking_for_limit(account_mail, logind_date, sk_login_self, command_prxy)
			if skf_login_self:
				login_account = mails_dict[skf_login_self]
				account_mail, account_password = login_account
				if account_mail and self.profiles_list:
					return [FormRequest.from_response(response, formname = 'login_form',\
				formdata={'session_key':account_mail,'session_password':account_password,'isJsEnabled':'','source_app':'','tryCount':'','clickedSuggestion':'','signin':'Sign In','session_redirect':'','trk':'hb_signin','loginCsrfParam':logincsrf,'fromEmail':'','csrfToken':csrf_token,'sourceAlias':source_alias},callback=self.parse_next, meta={'csrf_token':csrf_token, 'login_mail':account_mail, 'count_from_': yes_s, 'logind_date':logind_date, 'sk_login_self': skf_login_self, 'command_prxy':command_prxy})]

		
    	def spider_closed(self, spider):
		cv = requests.get('https://www.linkedin.com/logout/').text
		#yield Request('https://www.linkedin.com/logout/', callback=self.close_yield)
		close_mysql_connection(self.con, self.cur)

	def parse_next(self, response):
                sel = Selector(response)
		command_prxy = response.meta.get('command_prxy','')
                count_from_ = response.meta.get('count_from_', '')
                logind_date = response.meta.get('logind_date', '')
                cooki_list = response.request.headers.get('Cookie', [])
                li_at_cookie = ''.join(re.findall('li_at=(.*?); ', cooki_list))
                headers = {
                    'cookie': 'li_at=%s;JSESSIONID="%s"' % (li_at_cookie, response.meta['csrf_token']),
                    'x-requested-with': 'XMLHttpRequest',
                    'csrf-token': response.meta['csrf_token'],
                    'authority': 'www.linkedin.com',
                    'referer': 'https://www.linkedin.com/',
                }
                sk_login_self = response.meta.get('sk_login_self', '')
                for li in self.profiles_list:
                        count_from_ += 1
                        update_count_from = execute_query(self.cur, "update linkedin_loginlimit set count='%s' where sk = '%s' and login_date='%s' and proxy_ip='%s'" % (count_from_, sk_login_self, logind_date, command_prxy))
                	meta_data = json.loads(li[2])
	                company_url = meta_data.get('company_url', '')
			sno = meta_data.get('sno','')
			company_given_name = meta_data.get('company_given_name', '')
        	        sk, profile_url, m_data = li
                	meta_data = json.loads(m_data)
			execute_query(self.cur, self.upcpqu % (9, sk))
			api_compid_url = 'https://www.linkedin.com/voyager/api/organization/companies/%s' % (profile_url.strip().strip('/').split('/')[-1])
			
                	yield Request(api_compid_url, callback = self.parse_correct, meta = {
	                    "sk": sk,
                	    'csrf_token': response.meta['csrf_token'],
			    'command_prxy': command_prxy,
			    'company_given_name' : company_given_name,
			    'm_data':json.dumps(meta_data),
			    'sno':sno,
			    'company_url':company_url
	                }, headers = headers)

	def parse_correct(self, response):
                sel = Selector(response)
		m_data = response.meta.get('m_data','')
		sno = str(response.meta.get('sno',''))
		company_url = str(response.meta.get('company_url',''))
		company_given_name = str(response.meta.get('company_given_name', '').encode('utf-8'))
                sk = response.meta.get('sk', '')
		execute_query(self.cur, self.upcpqu % (1, sk))
		tmp = {}
		try:
			tmp = json.loads(response.body)
		except:
			tmp = {}
		if tmp:
			company_name = tmp.get('name','')
			company_page_url = tmp.get('companyPageUrl','')
			no_of_employees = str(tmp.get('staffCount', ''))
			followers_count = str(tmp.get('followingInfo',{}).get('followerCount',''))
			headquater = tmp.get('headquarter', {})
			city = headquater.get('city', '')
			country = headquater.get('country', '')
			geogrep_area = headquater.get('geographicArea', '')
			line1 = headquater.get('line1', '')
			line2 = headquater.get('line2', '')
			postalcode = headquater.get('postalCode', '')
			industries = tmp.get('industries', [])
			industries = '<>'.join(industries).strip().strip('<>')
			company_type = tmp.get('companyType', {}).get('localizedName', '')
			company_description = tmp.get('description', '')
			comp_time = Linkedincompanymeta()
			comp_time['sk'] = normalize(sk)
			comp_time['company_given_url'] = normalize(company_url)
			comp_time['company_given_sno'] = normalize(sno)
			comp_time['company_given_name'] = normalize(company_given_name)
			comp_time['company_name'] = normalize(company_name)
			comp_time['company_page_url'] = normalize(company_page_url)
			comp_time['number_of_employees'] = normalize(no_of_employees)
			comp_time['no_of_followers'] = normalize(followers_count)
			comp_time['industry'] = normalize(industries)
			comp_time['city'] = normalize(city)
			comp_time['geographic_area'] = normalize(geogrep_area)
			comp_time['line1'] = normalize(line1)
			comp_time['line2'] = normalize(line2)
			comp_time['postal_code'] = normalize(postalcode)
			comp_time['company_type'] = normalize(company_type)
			comp_time['company_description'] = normalize(company_description)
			yield comp_time
