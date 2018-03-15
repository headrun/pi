from linkedin_voyager_functions import *
import json
import requests

class Lprofileimage(scrapy.Spider):
	name = 'profiles_image_browse'
	start_urls=['https://www.linkedin.com/pulse-fe/api/v1/followableEntity?vanityName']
	
	def parse(self,response):
		headers = {
    'pragma': 'no-cache',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'cache-control': 'no-cache',
    'authority': 'www.linkedin.com',
    'cookie': 'bcookie="v=2&b614f28e-965d-4a07-8b5e-9bdfdfb395bb"; bscookie="v=1&201802070537032478b629-bacc-453e-8fe5-0608d173f39cAQHLiq_OTf3o6zMS62oqrDu-FCq8lpNe"; lidc="b=SGST08:g=10:u=1:i=1518500914:t=1518587314:s=AQHgUjgTq29ERxvNKq_gTCHOLH2yVy_d"; visit="v=1&G"; join_wall=v=2&AQECv4vC-c6negAAAWGNwKwEnWw1e1_BU7azXrw2G1h8k_AkhlS8GjkX6m18FoqfI3vgGCxqg8XKyu6W5NxGj3UAoAKCH1oCT9epWoIe8KKBpcoQn4Mrhi9zVWHR_XdcL3b1_RGiZah7LzCcym9C3xnWAj0DkSga; _ga=GA1.2.1587069347.1518501672; JSESSIONID=ajax:5168498028091499714; lang=v=2&lang=en-us',
			}

		params = (
    			('vanityName', 'chimango-chikwanda-56a2b7a'),
			)

		yield Request('https://www.linkedin.com/pulse-fe/api/v1/followableEntity', callback=self.parse_next,headers=headers, params=params)

	def parse_next(self,response):
		import pdb;pdb.set_trace()
