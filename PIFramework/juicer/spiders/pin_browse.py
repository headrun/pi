from juicer.utils import *
import requests

class PinterestBrowse(JuicerSpider):
    name ='pin_movie_spider'
    allowed_domains = ['pinterest.com']
    start_urls = ['http://pinterest.com/search/people/?q=Ieva+Mazeikaite']

    def parse(self,response):
        sel=Selector(response)
	headers = {
 		'Accept-Encoding': 'gzip, deflate, br',
     		'Accept-Language': 'en-US,en;q=0.9',
     		'Upgrade-Insecure-Requests': '1',
     		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
     		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
     		'Cache-Control': 'max-age=0',
    		'Connection': 'keep-alive',
 		}
	cookies = {
   		'_pinterest_cm': 'TWc9PSZsTU5mV29mWjUrRXBrUVl1MkNNRWhKTC9WSXJ3dVNrR2diUll5WkZpYisrRmhhZjVsS1JmYTlHdDYyYXFlRjl4OVlZL1hzSHI3eHd4TmdUQVFJOEdqQlN2aDVjbXNPV1lPdFJQVis5SHBNelR4dDFqUWNqUmd0Mk9zUkVxdDlDVSZkWk1remJ4aE1QTjlWZ3NNbkt0WWFwdWkxWkk9',
     		'_pinterest_referrer': 'https://www.google.co.in/',
     		'c_dpr': '1',
     		'c_vh': '678',
     		'c_vw': '1286',
     		'sessionFunnelEventLogged': '1',
     		'_b': 'AS/6k8yTEfNLqYDoi5DMIQACRlr5jRxqdXcViMW/me4hP1i/Rwbha1ZTbTayrUHOwvw=',
     		'_auth': '1',
     		'csrftoken': 'yd1rPhTwOJICCba9UqyD4OUsPzSdTqX3',
     		'_pinterest_sess': 'TWc9PSYwdkpEWS93QkhsaUt4N2VJOUM2RkpHSFdkOW01TGxETDZhNmhudEJLcFZ2VmJQVnhHVDIyVUxkMFV4eWNtTzFoTnE2Rm5DU08xZzhCUk1oYytSZmJ3ZjVUVERNeXF4YldXSmVUeVY5d1l5dTgzaVg5QTVBR1E2TDcrSFBMWWdzTTNqQS8yYW5ETVRXSjBCam9oeTJSRlZCZHZOaFJjMW9qVXFhYlc5ZUJUWTdNcTViK3d3TmFOOXc0eGNQMGwwYk1zN3huRnRFdjIvc28zRVoxWE5xWW9PYTFuUUZJTzJLbW9NUDZDdFFDR2JGN0krUVM1bUw5SmZjdGsvMzhaZ3ZjeXliZW0zTE1EVVZINWpCcUFHZXg0T3VKVU5qVVZDbTErZytrN2ZwV2J3N1ArTzM5QjFOY25XRzhCWU5PWkptMkZpay9qY1ppL04zT3FJYnNmWTdqTGIzUnZCTTk4Vmd1Z3BPNHpwSEVSTTB3bHloQ05RK0pTVUV3VnBQN3J0YkFyQ0QzS000aGV2L09GU0Z6eHRsVzZSWEo1azJTSGYrUUU0T2FXam9BeWM0QTFhR1ZmeU1LT3Y0ZXllQ0ZCYWJ6bHdLWnRTUnFGUWd2MzZpck5OVndTSlNhNzBzUWtJUXJuTC9vOWlJd0ZFcz0mYTNMTnBZMVREb3N4dDUyLzl0L1NXNWFoTHZvPQ==',
     		'_pinterest_pfob': 'disabled',
     		'bei': 'false',
     		'cm_sub': 'none',
     		'_ga': 'GA1.2.531761451.1513679818',
     		'_gid': 'GA1.2.1467195468.1513679818',
 		}
	params = (
		('q', 'Ieva Mazeikaite'),
		)
	yield Request('https://in.pinterest.com/search/people/', callback=self.parse_next,headers=headers, params=params, cookies=cookies)
	
	def parse_next(self,response):
        	import pdb;pdb.set_trace()

