from juicer.utils import *
import csv
import datetime

class MWCTERMINAL(JuicerSpider):
    name = "mwc_exhibitors_terminal"

    def __init__(self, *args, **kwargs):
        super(MWCTERMINAL, self).__init__(*args, **kwargs)
	self.domain_url = 'https://www.mwcbarcelona.com/'
        self.excel_file_name = 'MWC_data_on_%s.csv'%str(datetime.datetime.now().date())
	self.header_params = ['Title','location','location_url','description','contact','mail_id','website_link','fb_link','linkedin_link','tags','Reference_url']
        oupf = open(self.excel_file_name, 'wb+')
        self.todays_excel_file  = csv.writer(oupf)
        self.todays_excel_file.writerow(self.header_params)	

    def parse(self, response):
        sel = Selector(response)
	location = normalize("<>".join(response.xpath('//p[@class="list-location"]//text()').extract()))
	location_url = normalize("<>".join(response.xpath('//p[@class="list-location"]//a//@href').extract()))
	description = normalize("".join(response.xpath('//div[@class="mod-content api-description"]//p//text()').extract()))
	contact = normalize("".join(response.xpath('//div[@class="mod-title"]//p[@class="tag-title"][contains(text(),"Contact Details")]//..//following-sibling::div/p/text()').extract()))
	mail_id = normalize("".join(response.xpath('//div[@class="social-exhibitors"]//a[contains(@class,"email-link")]/@href').extract()))
	website_link = normalize("".join(response.xpath('//div[@class="social-exhibitors"]//a[contains(@class,"web-site-link")]/@href').extract()))
	fb_link = normalize("".join(response.xpath('//div[@class="social-exhibitors"]//a[contains(@class,"social-fb")]/@href').extract()))
	linkedin_link = normalize("".join(response.xpath('//div[@class="social-exhibitors"]//a[contains(@class,"social-li")]/@href').extract()))
	tags = normalize(",".join(response.xpath('//div[@class="mod-title"]//p[@class="tag-title"][contains(text(),"Tags")]//..//following-sibling::div//text()').extract())).replace('\xc2\xa0','').strip(',').strip().strip(',')
	title = normalize("".join(response.xpath('//div[@class="top-area-container"]//h2//text()').extract()))
 	values = [title,location,location_url,description,contact,mail_id,website_link,fb_link,linkedin_link,tags,response.url]	
	self.todays_excel_file.writerow(values)

		
	


