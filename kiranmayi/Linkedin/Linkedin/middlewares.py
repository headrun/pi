# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random

class LinkedinSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

from scrapy import log
#from proxy import PROXIES
#from agents import AGENTS

import random

"""
Custom proxy provider. 
"""
class CustomHttpProxyMiddleware(object):
    def process_request(self, request, spider):
        # TODO implement complex proxy providing algorithm
        if self.use_proxy(request):
            #p = random.choice(PROXIES)
            try:
                #request.meta['proxy'] = "http://%s" % p['ip_port']
		request.meta['proxy'] = "http://176.9.181.45:3279"
            except Exception, e:
                log.msg("Exception %s" % e, _level=log.CRITICAL)
	    print request.meta['proxy']
                
    
    def use_proxy(self, request):
        """
        using direct download for depth <= 2
        using proxy with probability 0.3
        """
        if "depth" in request.meta and int(request.meta['depth']) <= 2:
            return False
        i = random.randint(1, 10)
        return i <= 2
    
    
"""
change request header nealy every time
"""
class CustomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        agent = random.choice(AGENTS)
        request.headers['User-Agent'] = agent

import base64

from scrapy.conf import settings
class ProxyMiddleware(object):
    def process_request(self, request, spider):
	#import pdb;pdb.set_trace()
        request.meta['proxy'] = random.choice(settings.get('HTTP_PROXY'))
	"""if '103.224.241.217' in settings.get('HTTP_PROXY'):
		request.dont_filter= True
		proxy_user_pass = "hr@headrun.com:hdrn^123!"
		encoded_user_pass = base64.encodestring(proxy_user_pass)
		request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass 
	
	proxy_user_pass = "lum-customer-hl_75a24c21-zone-zone1-ip-45.73.171.131:rbjphacd6nn6"
	encoded_user_pass = base64.encodestring(proxy_user_pass)
	print encoded_user_pass
	request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass.strip()"""	

