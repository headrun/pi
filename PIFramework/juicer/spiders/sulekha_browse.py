# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest, Request
from scrapy.http import FormRequest
import requests
import json
import MySQLdb
from juicer.utils import *
import csv
import re
class SULEKHA2(JuicerSpider):
    name = "sulekha_browse"
    start_urls = ['https://www.sulekha.com/interior-designers-decorators/bangalore']


    def __init__(self, *args, **kwargs):
        super(SULEKHA2, self).__init__(*args, **kwargs)
        self.header_params = ['Name','contact_person', 'Address','Working_hours','pincode', 'contact', 'Description','Email','Images','Website','Sulekha_score','Rating','Social_media_links','Services_offered','Services_offered_link','no_of_reviews','Reference_url']
        self.excel_file_name = 'Sulekha_bangalore_Metadata_on_%s.csv'%str(datetime.datetime.now().date())
        oupf = open(self.excel_file_name, 'wb+')
        self.todays_excel_file  = csv.writer(oupf)
        self.todays_excel_file.writerow(self.header_params)
        self.header_params2 = ['Reviewed_By','Review_Date','Review_text','Review_rating','No_of_reviews','reference_url']
        self.excel_file_name2 = 'Sulekha_bangalore_Reviewsdata_on_%s.csv'%str(datetime.datetime.now().date())
        oupf2 = open(self.excel_file_name2, 'wb+')
        self.todays_excel_file2  = csv.writer(oupf2)
        self.todays_excel_file2.writerow(self.header_params2)


    def parse(self, response):
        sel = Selector(response)
        links = response.xpath('//div[@class="busi-name"]/h3/a/@href').extract()
        for link in links:
            link = "https:"+str(link) 
            yield Request(str(link),self.parse_details,response,meta={'Main_page':response.url})

        for i in range(2,1500):
            data = (('PartialPageData', 'eyIkaWQiOiIxIiwiQ2l0eUlkIjo0LCJBcmVhSWQiOjAsIkNhdGVnb3J5SWQiOjEzNzYsIk5lZWRJZCI6MCwiTmVlZEZpbHRlclZhbHVlcyI6IiIsIlJvdXRlTmFtZSI6IkludGVyaW9yIERlc2lnbmVycyIsIlBhZ2VWaWV3VHlwZSI6NCwiSGFzTGNmIjp0cnVlLCJCcmVhZENydW1iVGl0bGUiOiJJbnRlcmlvciBEZXNpZ25lcnMiLCJJc09ubHlQcmltYXJ5VGFnIjpmYWxzZSwiQ2xlYXJDYWNoZSI6ZmFsc2V9'), ('Category', '1376'), ('Filter', '{}'), ('PageNr', str(i)), ('Sort', ''), ('getQuoteVisiblity', ''), ('aboutEnabled', ''), ('CategoryName', 'Interior Designers & Decorators'), ('CityName', 'Bangalore'), ('IsAboutEnabled', 'False'))
            get_response = requests.post('https://www.sulekha.com/mvc5/lazy/v1/Listing/get-business-list', data=data)
            data_1 = Selector(text = get_response.text)
            links = data_1.xpath('//div[@class="busi-name"]/h3/a/@href').extract()
            for link in links:
                link = "https:"+str(link)
                yield Request(link,self.parse_details)


     

    def parse_details(self,response):
        sel = Selector(response)   
        name =  normalize("".join(response.xpath('//h1[@class="span9"]/text()').extract()))
        contact_person = ''.join(response.xpath('//label[@class="icon-person"]/../span/text()').extract())
        Address = normalize("".join(response.xpath('//address[@class="ellips"]//text()').extract()))
        work_hours = normalize("".join(sel.xpath('//label[@class="icon-time"]/../span//text()').extract()))
        pincode = ''.join(Address).split('-')[-1]
        contact = "".join(response.xpath('//span[@class="icon-mobile ph-no"]//text()').extract())
        desc = normalize("".join(response.xpath('//div[@class="scontent"]/text()').extract()))
        email = normalize("<>".join(response.xpath('//label[@class="icon-email"]/../a//text()').extract()))
        images = ''
        try : images = "<>".join([i.get('MediaUrl', '')for i  in json.loads(sel.xpath('//input[@type="hidden"][@value][@class="mediadata"]/@value').extract()[0])])
        except : print "no images"
        website = normalize('<>'.join(response.xpath('//div[@class="social-icons"]/a/@href').extract()))
        suleka_score = "".join(response.xpath('//span[@class="sulekha-score"]//strong//text()').extract())
        rating = "".join(response.xpath('//span[@class="rating-count"]/text()').extract())
        soc_links = "<>".join(response.xpath('//div[@class="social-links"]//a//@href').extract())
        services_offered_text = normalize("<>".join(response.xpath('//h2[@class="icon-services"]//..//a//text()').extract()))
        services_offered_link = "<>".join(response.xpath('//h2[@class="icon-services"]//..//a//@href').extract())
        no_of_reviews = "<>".join(response.xpath('//div[@class="review-rate"]//span//text()').extract())
        vals = [name,contact_person,Address,work_hours,pincode,contact,desc,email,images,website,suleka_score,rating,soc_links,services_offered_text,services_offered_link,no_of_reviews,response.url]      
        self.todays_excel_file.writerow(vals)

        rev_nodes = response.xpath('//div[@class="reviews"]//ul//li')
        
        for node in rev_nodes :
            date = "".join(node.xpath('./@data-date').extract())
            desc_ = normalize("".join(node.xpath('./p//text()').extract()))
            rev_by = normalize("".join(node.xpath('./@data-name').extract()))
            data_rat = "".join(node.xpath('./@data-rating').extract())
            values = [rev_by,date,desc_,data_rat,no_of_reviews,response.url]
            self.todays_excel_file2.writerow(values)
        counter = 2  
        id_ = "".join(response.xpath('//a//@data-cid').extract())
        if id_ : 
            params = (('PartialPageData', 'eyIkaWQiOiIxIiwiQ2l0eUlkIjo0LCJBcmVhSWQiOjE5NTU0LCJDYXRlZ29yeUlkIjoxMzc2LCJOZWVkSWQiOjAsIlJvdXRlTmFtZSI6IkludGVyaW9yIERlc2lnbmVycyIsIlBhZ2VWaWV3VHlwZSI6NywiSGFzTGNmIjpmYWxzZSwiSXNPbmx5UHJpbWFyeVRhZyI6ZmFsc2UsIkFyZWFOYW1lIjoiSG9yYW1hdnUiLCJDbGVhckNhY2hlIjpmYWxzZX0='), ('BusinessId', str(id_)), ('PageNr', '2'))
            yield FormRequest('https://www.sulekha.com/mvc5/lazy/v1/profile/get-review-list',  dont_filter = True, callback = self.parse_rev,formdata=params,meta={'counter':counter,'reference_url':response.url})

    def parse_rev(self,response):
            sel = Selector(response)
            counter = response.meta.get('counter','')
            response_url = response.meta.get('reference_url','')
            counter = counter + 1
            no_of_reviews = "".join(response.xpath('//div[@class="review-rate"]//span//text()').extract())
            rev_nodes = response.xpath('//div[@class="reviews"]//ul//li')
            for node in rev_nodes :
                date = "".join(node.xpath('.//@data-date').extract())
                desc_ = normalize("".join(node.xpath('.//p//text()').extract()))
                rev_by = normalize("".join(node.xpath('.//@data-name').extract()))
                data_rat = "".join(node.xpath('.//@data-rating').extract())
                values = [rev_by,date,desc_,data_rat,no_of_reviews,response_url]
                self.todays_excel_file2.writerow(values)
            id_ = "".join(response.xpath('//a//@data-cid').extract())
            if not id_ : x = "".join(sel.xpath('//@onclick').extract()).split(';')[0]
            try : id_ = "".join(re.findall('\d+',x)[0])
            except : print "no id"
            if id_ : 
                 print id_
                 params = (('PartialPageData', 'eyIkaWQiOiIxIiwiQ2l0eUlkIjo0LCJBcmVhSWQiOjE5NTU0LCJDYXRlZ29yeUlkIjoxMzc2LCJOZWVkSWQiOjAsIlJvdXRlTmFtZSI6IkludGVyaW9yIERlc2lnbmVycyIsIlBhZ2VWaWV3VHlwZSI6NywiSGFzTGNmIjpmYWxzZSwiSXNPbmx5UHJpbWFyeVRhZyI6ZmFsc2UsIkFyZWFOYW1lIjoiSG9yYW1hdnUiLCJDbGVhckNhY2hlIjpmYWxzZX0='), ('BusinessId', str(id_)), ('PageNr', str(counter)))
                 yield FormRequest('https://www.sulekha.com/mvc5/lazy/v1/profile/get-review-list',  dont_filter = True, callback = self.parse_rev,formdata=params,meta={'counter':counter,'reference_url':response_url})


             


            
      

