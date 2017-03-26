import scrapy
import md5
import json
import re
import requests
import MySQLdb
import hashlib
import time
from scrapy import signals
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest
from scrapy.xlib.pydispatch import dispatcher
from linkedin_queries import *
from Linkedin.items import *
class LinkedinauthBrowse(scrapy.Spider):
    name = "linkedinauth_browse"
    allowed_domains = ["linkedin.com"]
    start_urls = ('https://www.linkedin.com/uas/login?goback=&trk=hb_signin',)

    def __init__(self, *args, **kwargs):
	super(LinkedinauthBrowse, self).__init__(*args, **kwargs)
        self.login = kwargs.get('login', 'ramanujan')
        self.con = MySQLdb.connect(db   = 'FACEBOOK', \
        host = 'localhost', charset="utf8", use_unicode=True, \
        user = 'root', passwd = 'root')
	self.cur = self.con.cursor()
	get_query_param = "select sk, url from linkedin_crawl where crawl_status=6 and url like '%authToken%' and url  like '%id=%' limit 2"
	self.cur.execute(get_query_param)
	self.profiles_list = [i for i in self.cur.fetchall()]
	dispatcher.connect(self.spider_closed, signals.spider_closed)
	self.auth2 = "https://www.linkedin.com/profile/mappers?x-a=profile_v2_browse_map&x-p=profile_v2_connections.distance%3A1%2Ctop_card.profileContactsIntegrationStatus%3A0%2Cprofile_v2_right_fixed_discovery.records%3A12%2Cprofile_v2_right_fixed_discovery.offset%3A0%2Cprofile_v2_browse_map.pageKey%3Anprofile_view_nonself%2Cprofile_v2_discovery.offset%3A0%2Cprofile_v2_discovery.records%3A12%2Cprofile_v2_discovery.records%3A12%2Ctop_card.tc%3Atrue%2Cprofile_v2_discovery.offset%3A0%2Cprofile_v2_summary_upsell.summaryUpsell%3Atrue&x-oa=bottomAliases&id="
	self.auth1 = "&locale=en_US&snapshotID=&authType=name&invAcpt=&promoId=&notContactable=&primaryAction=&isPublic=false&sfd=true"
	self.domain = "https://www.linkedin.com"


    def parse(self, response):
	sel = Selector(response)
	logincsrf = ''.join(sel.xpath('//input[@name="loginCsrfParam"]/@value').extract())
	csrf_token = ''.join(sel.xpath('//input[@name="csrfToken"]/@value').extract())
	source_alias = ''.join(sel.xpath('//input[@name="sourceAlias"]/@value').extract())
	account_mail, account_password = '', ''
	if self.login == 'raja':
		account_mail = 'rajaqx@gmail.com'
		account_password = 'linkedinpw'
	if account_mail:	
	        return [FormRequest.from_response(response, formname = 'login_form',\
                    formdata={'session_key':account_mail,'session_password':account_password,'isJsEnabled':'','source_app':'','tryCount':'','clickedSuggestion':'','signin':'Sign In','session_redirect':'','trk':'hb_signin','loginCsrfParam':logincsrf,'fromEmail':'','csrfToken':csrf_token,'sourceAlias':source_alias},callback=self.parse_next)]

    def spider_closed(self, spider):
	cv = requests.get('https://www.linkedin.com/logout/').text
	
    def parse_next(self, response):
	sel = Selector(response)
	for li in self.profiles_list:
            sk = li[0]
	    member_idjson = ''.join(re.findall('id=(.*?)&',li[1]))
	    url_p = "%s%s%s"%(self.auth2, member_idjson, self.auth1)
	    #sk = self.md5(li[1])
	    #self.cur.execute(update_get_params%(9,sk))
            #yield Request(li[1], callback=self.parse_again, headers=meat_headers,meta={"sk":sk, 'email_address':email_address})
	    yield Request(url_p, callback=self.parse_ajax, meta={"sk":sk})


    def parse_ajax(self, response):
	temp = json.loads(response.body)
 	all_keys_url = temp.get('content',{}).get('browse_map',{}).get('url_current_profile_view','')
	sk = response.meta.get('sk','')
	query = "update linkedin_crawl set crawl_status=0, url = '%s' where sk = '%s'"%(all_keys_url, sk)
	print query
	
					
		
		
	
	    



	

