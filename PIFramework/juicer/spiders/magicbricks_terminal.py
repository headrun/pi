from juicer.utils import *
from juicer.items import *
import scrapy
import hashlib
import csv
import datetime
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest
import datetime
city = 'chennai'


class MagicBrowse(JuicerSpider):
    name = "magic_data_terminal"
    start_urls = ['https://www.magicbricks.com/propertyDetails/2-BHK-985-Sq-ft-Multistorey-Apartment-FOR-Rent-Oragadam-in-Chennai-r1&id=4d423132383536333233']

    def __init__(self, *args, **kwargs):
        super(MagicBrowse, self).__init__(*args, **kwargs)

    def parse(self, response):
        sel = Selector(response)
        data_dict = {}
        if response.status==200 :  
		title =  normalize("".join(response.xpath('//h1//span[@class="p_bhk"]//text()').extract()))
		image = "<>".join(sel.xpath('//div[@class="bigImage"]//img//@data-src').extract())
		if 'Detail_no_img2' in image : image = ''
		price = "".join(response.xpath('//div[@id="priceSv"]//text()').extract()).replace('\n','')
                headers = sel.xpath('//div[@class="p_title"]/text()').extract()
                for header in headers : 
                        header = normalize(header)
                        if 'Super area' in header or 'Carpet' in header : continue
			value = normalize("".join(response.xpath('//div[contains(text(),"%s")]/following-sibling::div[@class="p_value"]/text()'%header).extract()))
                        if 'Amenti' in value  : value = normalize(",".join(response.xpath('//div[contains(text(),"Amenities")]/following-sibling::div[@class="p_value"]//ul//li//text()').extract()))
                        
                        if 'Rental Value' in header : value = "".join(response.xpath('//div[@class="p_infoRow"]//div[contains(text(),"Rental Value")]/following-sibling::div//text()').extract()).replace('See Other Charges','').replace('\n','')
                        if 'Bedroom' in header : value = normalize("".join(response.xpath('//div[@class="seeBedRoomDimen"]/text()').extract()))
                        if 'Security Deposit' in header : value = "".join(response.xpath('//div[contains(text(),"Security Deposit")]/following-sibling::div[@class="p_value"]//text()').extract()).replace('\n','')
                        if 'Society' in header :  value = "".join(response.xpath('//div[contains(text(),"Society")]/following-sibling::div[@class="p_value"]//a//text()').extract())
                        if header == 'Floor' : value = "".join(response.xpath('//div[contains(text(),"Floor")]/following-sibling::div[@class="p_value truncated"]/text()').extract())
                        if 'Furnishing Details' in header : value = normalize(",".join(response.xpath('//div[contains(text(),"Furnishing Details")]/following-sibling::div[@class="p_value"]//ul//li//text()').extract()))
                        if header == 'Status' : value = normalize("".join(response.xpath('//div[@class="p_infoRow"]/div[contains(text(),"Status")]/following-sibling::div/text()').extract()))
                        header = header.replace(' ','_')
                        data_dict.update({header:value})
		super_area = "".join(response.xpath('//span[@id="coveredAreaDisplay"]/text()').extract())
		if super_area : 
                    super_area = super_area+' sqft'
                    data_dict.update({'Super_area': super_area})
		carpet_area = "".join(response.xpath('//span[@id="carpetAreaDisplay"]/text()').extract())
		if carpet_area : 
                    carpet_area = carpet_area+' sqft'
                    data_dict.update({'carpet_area':carpet_area})             
		desc = normalize("".join(response.xpath('//div[@id="prop-detail-desc"]//text()').extract())).replace('"','')
		if not desc : 
		    desc = normalize("".join(response.xpath('//div[@class="descriptionCont"]//following-sibling::div/text()').extract())).replace('"','')
		try : owner_name  = normalize("".join(sel.xpath('//div[@class="agentName"]/div[@class="nameValue"]/text()').extract()[0]))
		except : 
			try : owner_name = normalize("".join(sel.xpath('//div[@class="CAName"]//text()').extract()))
			except : owner_name = ''
                sk = response.url.split('=')[-1]
                data_dict.update({'owner_name':owner_name,'description':desc,'title':title,'price':price,'image':image})
                magic_data = Magicbricks()
                magic_data.update({'sk':sk,'data_dict':str(data_dict),'reference_url':response.url})
                
                yield magic_data
		self.got_page(sk,1)

        
        
         
        
	


