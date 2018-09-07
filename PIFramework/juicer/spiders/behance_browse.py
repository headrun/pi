from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from scrapy.http import Request
import datetime
import csv
import time

class BehanceBrowse(BaseSpider):

    name = 'behance_browse'
    start_urls = []

    def __init__(self):
        self.today_date = str(datetime.datetime.now()).split('.')[0].replace(' ','_')
        self.excel_file_name = 'behance_data_%s.csv'%self.today_date
	self.headers = ['Url', 'First Name','Last Name','Summary','Location','Project Views','Appreciations','Followers','Following','Focus','About Me','Member Since','Projects','Collections','Appreciated','Project1_Name','Project1_type','Project1_likes','Project1_views','Project2_Name','Project2_type','Project2_likes','Project2_views','Project3_Name','Project3_type','Project3_likes','Project3_views','Project4_Name','Project4_type','Project4_likes','Project4_views','Project5_Name','Project5_type','Project5_likes','Project5_views','Project6_Name','Project6_type','Project6_likes','Project6_views','Project7_Name','Project7_type','Project7_likes','Project7_views','Project8_Name','Project8_type','Project8_likes','Project8_views','Project9_Name','Project9_type','Project9_likes','Project9_views','Project10_Name','Project10_type','Project10_likes','Project10_views','Project11_Name','Project11_type','Project11_likes','Project11_views','Project12_Name','Project12_type','Project12_likes','Project12_views','Project13_Name','Project13_type','Project13_likes','Project13_views','Project14_Name','Project14_type','Project14_likes','Project14_views','Project15_Name','Project15_type','Project15_likes','Project15_views','Project16_Name','Project16_type','Project16_likes','Project16_views','Project17_Name','Project17_type','Project17_likes','Project17_views','Project18_Name','Project18_type','Project18_likes','Project18_views','Project19_Name','Project19_type','Project19_likes','Project19_views','Project20_Name','Project20_type','Project20_likes','Project20_views','Project21_Name','Project21_type','Project21_likes','Project21_views','Project22_Name','Project22_type','Project22_likes','Project22_views','Project23_Name','Project23_type','Project23_likes','Project23_views','Project24_Name','Project24_type','Project24_likes','Project24_views','Project25_Name','Project25_type','Project25_likes','Project25_views']
    	self.oupf = open(self.excel_file_name, 'ab+')
        self.todays_excel_file  = csv.writer(self.oupf)
        self.todays_excel_file.writerow(self.headers)
    
    def start_requests(self):
	headers = {
    	'Connection': 'keep-alive',
    	'Cache-Control': 'max-age=0',
    	'Upgrade-Insecure-Requests': '1',
    	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    	'Accept-Encoding': 'gzip, deflate, br',
    	'Accept-Language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
	}
	cookies = {
    	'gk_suid': '28430579',
    	'bcp': '8072a411-1f5c-4477-8314-cb37f0d19aee',
    	'iat0': 'eyJ4NXUiOiJpbXNfbmExLWtleS0xLmNlciIsImFsZyI6IlJTMjU2In0.eyJpZCI6IjE1MzYxNDI1MDQ3NjVfZjMzMjg1NTItZGVjZC00MDZjLTg0ZmEtNjNmMzU0NjllMDU0X3VlMSIsImNsaWVudF9pZCI6IkJlaGFuY2VXZWJTdXNpMSIsInVzZXJfaWQiOiJFREU1MTNFMTVCNjgxNkI0MEE0OTVERjBAQWRvYmVJRCIsInN0YXRlIjoie1wiYWNcIjpcImJlaGFuY2UubmV0XCJ9IiwidHlwZSI6ImFjY2Vzc190b2tlbiIsImFzIjoiaW1zLW5hMSIsImZnIjoiU1hVQ1BBWDdYTEY3Q0hIR0NVQUFBQUFBRlU9PT09PT0iLCJzaWQiOiIxNTM2MTQyNTA0NzY1X2FlYjFiZjZmLTI5MTYtNDJlYS1hYmRhLTNlNDIzZTc1MmE5Y191ZTEiLCJtb2kiOiI5YTY0NjRmMCIsImMiOiJqRUdpcHhscWFHclN2bmNBQ2ZQWmN3PT0iLCJleHBpcmVzX2luIjoiODY0MDAwMDAiLCJzY29wZSI6IkFkb2JlSUQsb3BlbmlkLGduYXYsc2FvLmNjZV9wcml2YXRlLGNyZWF0aXZlX2Nsb3VkLGNyZWF0aXZlX3NkayxiZS5wcm8yLmV4dGVybmFsX2NsaWVudCxhZGRpdGlvbmFsX2luZm8ucm9sZXMiLCJjcmVhdGVkX2F0IjoiMTUzNjE0MjUwNDc2NSJ9.A5cIz9jSgSZxIot7wSWhRVj5Bl1xTo9hDmhymH5lKK5loz9YiRvAOX4Za7ytmcncNSq-S0-k-k343OTPfzrGDfZjwvgwEcbw4YKt3fNvhxbFIQlntFYOhNT_PrKAUafz83GWsDwxpNOntCELkL2r48oWZFe3tG7xSey0o1VK09wsSRBOjPvbN364O0rLjfXuWOxuywdAaSKomPAI2fE-4_1NrsuHIYsCYmItpglwBrqUV9u4PhFv8npuGoUttD4abFveb-nkNvoqmLord5AKB-RmJrK8a-mA0RFp2AZgWGtXyMsoIB7qogaAinDUL49KIgPPHTi1RjUxOh39o8q_DA',
}
	with open('behance_input.txt', 'r') as f:
            rows = f.readlines()
        for row in rows:
            row = row.replace('\n', '')
	    yield Request(row, self.parse, headers=headers, cookies=cookies)

    def parse(self, response):
	sel = Selector(response)
	name = ''.join(sel.xpath('//div[@id="profile-display-name"]/a/text()').extract())
	try:
	    f_name, l_name = name.split(' ')
	except:
	    f_name = name
	    l_name = ''
	summary = ' '.join(sel.xpath('//div[contains(@class, "qa-profile")]/text()').extract()).replace('\n', '').strip()
	location = ''.join(sel.xpath('//div[contains(@class, "profile-location")]/a/text()').extract())
	nodes = sel.xpath('//div[@class="profile-stat"]')
	dict_ = {}
	for node in nodes:
	    key = ''.join(node.xpath('./div[1]/span/text()').extract())
	    value = ''.join(node.xpath('.//div[@class="profile-stat-count"]/a/text()').extract())	
	    dict_.update({key:value})
	views = dict_.get('Project Views', '')
	appreciations = dict_.get('Appreciations', '')
	followers = dict_.get('Followers', '')
	following = dict_.get('Following', '')
	focus = ','.join(sel.xpath('//div[@id="profile-focus"]/a/text()').extract())
	about_me = ' '.join(sel.xpath('//div[@class="profile-section content-minor-section"][h3[contains(text(), "About")]]//text()').extract())
	if not about_me:
	    about_me = ' '.join(sel.xpath('//div[@class="profile-section content-minor-section"][h3[contains(text(), "about")]]//text()').extract())
	if 'Read More' in about_me:
	    about_me = about_me.split('Read More')[-1].replace('Read Less', '')
	about_me = about_me.replace('About Me', '').replace('about me', '').replace('About', '')
	member = ''.join(sel.xpath('//div[@id="profile-date"]/span/span/@data-timestamp').extract())
	member = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(member))).split(' ')[0]
	project = ''.join(sel.xpath('//a[@data-section="projects"]/@href').extract())
	collections = ''.join(sel.xpath('//a[@data-section="collections"]/@href').extract())
	appreciated = ''.join(sel.xpath('//a[@data-section="appreciated"]/@href').extract())
	p_nodes = sel.xpath('//div[@class="rf-project-cover__details"]')
	values = [response.url, f_name, l_name, summary, location, views, appreciations, followers, following, focus, about_me, member, project, collections, appreciated]
	for i in range(0, 25):
	    try:
	    	p_node = p_nodes[i]
	    	p_name = ''.join(p_node.xpath('./span[@class="rf-project-cover__title-wrap"]/a/text()').extract())
	    	p_type = ''.join(p_node.xpath('.//a[@class="rf-project-cover__field-link"]/text()').extract())
	    	p_likes,p_views = p_node.xpath('.//span[@class="rf-project-cover__stat-number"]/text()').extract()
	 	values.extend([p_name, p_type, p_likes, p_views])
	    except:
		values.extend(['', '', '', ''])
	self.todays_excel_file.writerow(values)
