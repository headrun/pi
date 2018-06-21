import os
import scrapy
import re
import json
import csv
import datetime
import requests
import time
from scrapy.http import FormRequest, Request
from scrapy.selector import Selector
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from collections import OrderedDict
from generic_functions import * 
from dateutil import relativedelta

class Linkedinvoyagerpeoplesrp(scrapy.Spider):
	name = "linkedinapivoyagerpeople_srp"
	allowed_domains = ["linkedin.com"]
	start_urls = ('https://www.linkedin.com/uas/login?goback=&trk=hb_signin',)

	def __init__(self, *args, **kwargs):
		super(Linkedinvoyagerpeoplesrp, self).__init__(*args, **kwargs)
                self.login = kwargs.get('login', 'kiranmayi')
		self.keyword = kwargs.get('key', 'anand kishore')
		self.logins_dict = {'kiranmayi': ['cheedellach@gmail.com','cheedellach427']}
		self.filename = "LINKEDIN_KPMG.csv"
	        self.csv_file = self.is_path_file_name(self.filename)
		self.fields = ["Full Name", "First Name", "Last Name", "Title", "Location", "Role Tenure", "Company", "Website", "Keyword", "Profile url"]
		self.csv_file.writerow(self.fields)
                dispatcher.connect(self.spider_closed, signals.spider_closed)
                self.domain = "https://www.linkedin.com"

	def parse(self, response):
                sel = Selector(response)
                logincsrf = ''.join(sel.xpath('//input[@name="loginCsrfParam"]/@value').extract())
		csrf_token = ''.join(sel.xpath('//input[@id="csrfToken-login"]/@value').extract())
                source_alias = ''.join(sel.xpath('//input[@name="sourceAlias"]/@value').extract())
		login_account = self.logins_dict[self.login]
		account_mail, account_password = login_account
                data = [
                  ('isJsEnabled', 'true'),
                  ('source_app', ''),
                  ('tryCount', ''),
                  ('clickedSuggestion', 'false'),
                  ('session_key', account_mail),
                  ('session_password', account_password),
                  ('signin', 'Sign In'),
                  ('session_redirect', ''),
                  ('trk', 'hb_signin'),
                  ('loginCsrfParam', logincsrf),
                  ('fromEmail', ''),
                  ('csrfToken', csrf_token),
                  ('sourceAlias', source_alias),
                  ('client_v', '1.0.1'),
                ]
                headers = {
                    'cookie': response.headers.getlist('Set-Cookie'),
                    'origin': 'https://www.linkedin.com',
                    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                    'x-requested-with': 'XMLHttpRequest',
                    'x-isajaxform': '1',
                    'accept-encoding': 'gzip, deflate, br',
                    'pragma': 'no-cache',
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
                    'content-type': 'application/x-www-form-urlencoded',
                    'accept': '*/*',
                    'cache-control': 'no-cache',
                    'authority': 'www.linkedin.com',
                    'referer': 'https://www.linkedin.com/',
                }
                yield FormRequest('https://www.linkedin.com/uas/login-submit', callback=self.parse_next, formdata=data, headers = headers, meta = {"csrf_token":csrf_token})

	def is_path_file_name(self, excel_file_name):
		if os.path.isfile(excel_file_name):
    			os.system('rm %s' % excel_file_name)
		oupf = open(excel_file_name, 'ab+')
		todays_excel_file = csv.writer(oupf)
		return todays_excel_file

    	def spider_closed(self, spider):
		cv = requests.get('https://www.linkedin.com/logout/').text

        def get_start_end_date(self, data):
                start_date = data.get('startDate', {})
                end_date = data.get('endDate', {})
                start_year = start_date.get('year','')
                start_month = start_date.get('month','')
                end_year = end_date.get('year','')
                end_month = end_date.get('month','')
                return str(end_year), str(end_month), str(start_year), str(start_month)



	def parse_next(self, response):
                sel = Selector(response)
                cooki_list = response.request.headers.get('Cookie', [])
                li_at_cookie = ''.join(re.findall('li_at=(.*?); ', cooki_list))
                headers = {
                    'cookie': 'li_at=%s;JSESSIONID="%s"' % (li_at_cookie, response.meta['csrf_token']),
                    'x-requested-with': 'XMLHttpRequest',
                    'csrf-token': response.meta['csrf_token'],
                    'authority': 'www.linkedin.com',
                    'referer': 'https://www.linkedin.com/',
                }
		api_compid_url = "https://www.linkedin.com/voyager/api/search/cluster?blendedSrpEnabled=true&guides=List()&keywords=%s&origin=GLOBAL_SEARCH_HEADER&q=guided&count=10&start=0" % (self.keyword)
		api_url = "https://www.linkedin.com/voyager/api/search/cluster?blendedSrpEnabled=true&guides=List()&keywords=%s&origin=GLOBAL_SEARCH_HEADER&q=guided" % (self.keyword)
		api01 = "https://www.linkedin.com/voyager/api/search/cluster?blendedSrpEnabled=true&count=10&guides=List()&keywords=python&origin=GLOBAL_SEARCH_HEADER&q=guided&start=40"
		yield Request(api_compid_url, callback = self.parse_correct, meta = {
		    'csrf_token': response.meta['csrf_token'], 'headers':headers, 'api_url':api_url
		}, headers = headers)

	def parse_correct(self, response):
                data = json.loads(response.body)
		api_basic_url = response.meta.get('api_url', '')
		headers = response.meta.get('headers', {})
		data_elements = data.get('elements', [])
		inner_elements = []
		for datae in data_elements:
			inner_elements = datae.get('elements', [])
			for ine in inner_elements:
				hit_info = ine.get('hitInfo', {}).get('com.linkedin.voyager.search.SearchProfile', {})
				mini_p = hit_info.get('miniProfile', {})
				first_name = mini_p.get('firstName', '')
				last_name = mini_p.get('lastName', '')
				occupation = mini_p.get('occupation', '')
				location = hit_info.get('location', '')
				public_identifier = mini_p.get('publicIdentifier', '')
				member_id = mini_p.get('objectUrn', '')
				if member_id:
					member_id = member_id.split('urn:li:member:')[-1]
				urls = "https://www.linkedin.com/voyager/api/identity/profiles/%s" % public_identifier
				main_url =  "https://www.linkedin.com/in/%s/"%public_identifier
				positions = "%s%s" % (urls , "/positions")
				yield Request(positions, callback =  self.parse_main, headers = headers, meta = {"f_name":first_name, "l_name":last_name, "location":location, "profile_url":main_url, "name":("%s%s%s" % (first_name, ' ', last_name)).strip()})
					
		url_paging  = data.get('paging',[])
		if url_paging:
			count_data = url_paging.get('count','')
			start_data = url_paging.get('start','')
			total_data = url_paging.get('total','')
			if total_data > count_data+start_data:
				cons_part = ''
				if '?' not in api_basic_url:
					cons_part = "?count=%s&start=%s"%(count_data, start_data+count_data)
				else:
					cons_part = "&count=%s&start=%s"%(count_data, start_data+count_data)
				retrun_url = "%s%s"%(api_basic_url,cons_part)
				if inner_elements:
					yield Request(retrun_url, headers=headers, callback=self.parse_correct, meta={'api_url':api_basic_url, 'headers':headers})
	def parse_main(self, response):
		data = json.loads(response.body)
		data_elements_ = data.get('elements', [])
		end_year, end_month, start_year, start_month, exp_company_url, company_name, title = ['']*7
		if data_elements_:
			data_elements = data_elements_[0]
			if data_elements:
				title = data_elements.get('title','')
			        time_period = data_elements.get('timePeriod')
		                end_year, end_month, start_year, start_month, = ['']*4
                		if time_period:
		                        end_year, end_month, start_year, start_month = self.get_start_end_date(time_period)
                			start_date = '-'.join([start_year, start_month]).strip('-').strip()
			                end_date = '-'.join([end_year, end_month]).strip('-').strip()
				company_name = data_elements.get('companyName','')
				exp_company_beta = data_elements.get('companyUrn','')
                		if exp_company_beta:
		                        exp_company_beta = textify(re.findall('\d+',exp_company_beta))
                		        exp_company_url = "https://www.linkedin.com/company-beta/%s/"%exp_company_beta
		if not end_year:
			end_year = str(datetime.datetime.now().date().year)
		if not end_month:
			end_month = str(datetime.datetime.now().date().month)
		start_month = start_month.zfill(2)
		end_month = end_month.zfill(2)
		final_msg = ''
		if start_year and start_month:
			if start_month == "00":
				start_month = "01"
				end_month = "01"
			if end_month == "00":
				end_month = "01"
			full_e = datetime.datetime.strptime("%s%s%s" % (end_year, end_month, '01'), "%Y%m%d")
			full_start = datetime.datetime.strptime("%s%s%s" % (start_year, start_month, '01'), "%Y%m%d")
			realative_data = relativedelta.relativedelta(full_e, full_start)
			yrs = realative_data.years
			months = realative_data.months
			msg = 'year'
			msgq = 'month'
			if yrs > 1:
				msg = 'years'
			if months >1:
				msgq = 'months'
			if months < 12:
				months = months+1
			else:
				yrs = yrs+1
				months = 0
			yrs_msg = "%s%s%s" % (str(yrs), ' ', msg)
			months_msg = "%s%s%s" % (str(months), ' ',msgq)
			if months == 0:
				months_msg = ''
			if yrs == 0:
				yrs_msg = ''
			final_msg = ("%s%s%s" % (yrs_msg, ' ', months_msg)).strip()
		f_name = response.meta.get('f_name', '')
		l_name = response.meta.get('l_name', '')
		location = response.meta.get('location', '')
		profile_url = response.meta.get('profile_url', '')
		name = response.meta.get('name', '')
		values = [name, f_name, l_name, title, location, final_msg, company_name, exp_company_url, self.keyword, profile_url]
		values = [normalize(i) for i in values]
		self.csv_file.writerow(values)
		print f_name

