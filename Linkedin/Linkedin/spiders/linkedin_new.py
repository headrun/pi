# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http import FormRequest, Request


class LinkedinBrowseSpider(scrapy.Spider):
    name = "linkedin_new"
    allowed_domains = ["linkedin.com"]
    start_urls = (
        'https://www.linkedin.com/uas/login?goback=&trk=hb_signin',
    )

    def parse(self, response):
        sel = Selector(response)
        logincsrf = ''.join(sel.xpath('//input[@name="loginCsrfParam"]/@value').extract())
        csrf_token = ''.join(sel.xpath('//input[@name="csrfToken"]/@value').extract())
        source_alias = ''.join(sel.xpath('//input[@name="sourceAlias"]/@value').extract())
        return [FormRequest.from_response(response, formname = 'login_form',\
            formdata={'session_key':'meatproject05@gmail.com','session_password':'ram123123','isJsEnabled':'','source_app':'','tryCount':'','clickedSuggestion':'','signin':'Sign In','session_redirect':'','trk':'hb_signin','loginCsrfParam':logincsrf,'fromEmail':'','csrfToken':csrf_token,'sourceAlias':source_alias},callback=self.parse_next)]
            #formdata={'session_key':'imfacebookdummy01@gmail.com','session_password':'cheppanu','isJsEnabled':'','source_app':'','tryCount':'','clickedSuuggestion':'','signin':'Sign In','session_redirect':'','trk':'hb_signin','loginCsrfParam':logincsrf,'fromEmail':'','csrfToken':csrf_token,'sourceAlias':source_alias},callback=self.parse_next)]

    def parse_next(self, response):
        meatproject_headers = {
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36',
        'Accept': 'text/html,*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        }
        yield Request('https://www.linkedin.com/in/aravindrajanm/', callback=self.parse_again, headers=meatproject_headers)
        facebookdummy_headers = {
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'User-Agent': '"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0"',
        'Accept': 'text/html,*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        }
        #yield Request('https://www.linkedin.com/in/aravindrajanm/', callback=self.parse_again, headers=meatproject_headers)

    def parse_again(self, response):
	sel = Selector(response)
        import pdb;pdb.set_trace()
