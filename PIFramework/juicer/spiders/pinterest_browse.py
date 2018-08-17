from scrapy.spider import BaseSpider
from scrapy.selector import Selector
import json
from scrapy.http import Request
import datetime
import csv

class PinterestBrowse(BaseSpider):
    
    name = 'pinterest_browse'
    start_urls = []

    def __init__(self):
        self.today_date = str(datetime.datetime.now()).split('.')[0].replace(' ','_')
        self.excel_file_name = 'pinterest_data_%s.csv'%self.today_date
	#self.header = ['Url', 'First Name','Last Name','followers','following','Location','Board_cnt','Pin_cnt','Board1_name','Board1_pin_cnt','Board1_last_saved','Board2_name','Board2_pin_cnt','Board2_last_saved','Board3_name','Board3_pin_cnt','Board3_last_saved','Board4_name','Board4_pin_cnt','Board4_last_saved','Board5_name','Board5_pin_cnt','Board5_last_saved','Board6_name','Board6_pin_cnt','Board6_last_saved','Board7_name','Board7_pin_cnt','Board7_last_saved','Board8_name','Board8_pin_cnt','Board8_last_saved','Board9_name','Board9_pin_cnt','Board9_last_saved','Board10_name','Board10_pin_cnt','Board10_last_saved','Board11_name','Board11_pin_cnt','Board11_last_saved','Board12_name','Board12_pin_cnt','Board12_last_saved','Board13_name','Board13_pin_cnt','Board13_last_saved','Board14_name','Board14_pin_cnt','Board14_last_saved','Board15_name','Board15_pin_cnt','Board15_last_saved','Board16_name','Board16_pin_cnt','Board16_last_saved','Board17_name','Board17_pin_cnt','Board17_last_saved','Board18_name','Board18_pin_cnt','Board18_last_saved','Board19_name','Board19_pin_cnt','Board19_last_saved','Board20_name','Board20_pin_cnt','Board20_last_saved']
	self.header = ['Url', 'First Name','Last Name','followers','following','Location','Board_cnt','Pin_cnt','Board1_name','Board1_pin_cnt','Board2_name','Board2_pin_cnt','Board3_name','Board3_pin_cnt','Board4_name','Board4_pin_cnt','Board5_name','Board5_pin_cnt','Board6_name','Board6_pin_cnt','Board7_name','Board7_pin_cnt','Board8_name','Board8_pin_cnt','Board9_name','Board9_pin_cnt','Board10_name','Board10_pin_cnt','Board11_name','Board11_pin_cnt','Board12_name','Board12_pin_cnt','Board13_name','Board13_pin_cnt','Board14_name','Board14_pin_cnt','Board15_name','Board15_pin_cnt','Board16_name','Board16_pin_cnt','Board17_name','Board17_pin_cnt','Board18_name','Board18_pin_cnt','Board19_name','Board19_pin_cnt','Board20_name','Board20_pin_cnt']
	self.oupf = open(self.excel_file_name, 'ab+')
        self.todays_excel_file  = csv.writer(self.oupf)
        self.todays_excel_file.writerow(self.header)

    def start_requests(self):
        with open('pinterest_input.txt', 'r') as f:
            rows = f.readlines()
        for row in rows:
            row = row.replace('\n', '')
            yield Request(row, callback=self.parse)
    
    def parse(self, response):
	sel = Selector(response)
	script_data = ''.join(sel.xpath("//script[@id='initial-state']/text()").extract())
	if script_data:
	    data = json.loads(script_data)
	    data = data['resources']['data']['UnauthReactUserProfileResource'].values()[0]['data']
	    profile_info = data['profile']
	    full_name = profile_info['full_name']
	    try:
		f_name, l_name = full_name.split(' ')
	    except:
		f_name = full_name
		l_name = ''
	    followers = profile_info['follower_count']
	    following = profile_info['following_count']
	    location = profile_info['location']
	    boards_cnt = ''.join(sel.xpath('//meta[@name="pinterestapp:boards"]/@content').extract())
	    pins_cnt = ''.join(sel.xpath('//meta[@property="pinterestapp:pins"]/@content').extract())
	    boards = data['boards']
	    values = [response.url, f_name, l_name, followers, following, location, boards_cnt, pins_cnt]
	    for i in range(0, 20):
		try:
		    board = boards[i]
		    b_name = board['name']
		    b_pin_cnt = board['pin_count']
		    values.extend([b_name, b_pin_cnt])
		except:
		    values.extend(['', ''])
	    self.todays_excel_file.writerow(values)
