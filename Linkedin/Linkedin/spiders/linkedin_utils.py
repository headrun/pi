import scrapy
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest
from linkedin_functions import *
#import constants
from linkedin_queries import *


class Lgetlogin(scrapy.Spider):

    def __init__(self, name=None, **kwargs):
    	super(Lgetlogin, self).__init__(name, **kwargs)

    def start_requests(self):
	requests = []
	if 'terminal' in self.name:
		requests = self.get_terminal_requests(requests)
	return requests

    def get_terminal_requests(self, requests):
	yield Request('https://www.linkedin.com/uas/login?goback=&trk=hb_signin',self.login)

    def login(self, response):
	sel = Selector(response)
        logincsrf = ''.join(sel.xpath('//input[@name="loginCsrfParam"]/@value').extract())
        csrf_token = ''.join(sel.xpath('//input[@name="csrfToken"]/@value').extract())
        source_alias = ''.join(sel.xpath('//input[@name="sourceAlias"]/@value').extract())
	con, cur = get_mysql_connection(DB_HOST, REQ_DB_NAME, '')
	rec_va = fetchall(cur, selectmailparams)
	if rec_va and len(rec_va[0]) == 3:
		account_sk, account_mail, account_password = rec_va[0]
        #account_mail = constants.check
        #account_password = constants.check_by
	if account_mail:
		execute_query(cur, update_based_table%('linkedin_mails', 1, account_sk))
		return [FormRequest.from_response(response, formname = 'login_form',formdata={'session_key':account_mail,'session_password':account_password,'isJsEnabled':'','source_app':'','tryCount':'','clickedSuggestion':'','signin':'Sign In','session_redirect':'','trk':'hb_signin','loginCsrfParam':logincsrf,'fromEmail':'','csrfToken':csrf_token,'sourceAlias':source_alias}, callback=self.parse)]

