from scrapy import log
from proxy import PROXIES
from agents import AGENTS
from scrapy.downloadermiddlewares.retry import RetryMiddleware
import time
import random

"""
Custom proxy provider. 
"""
class CustomHttpProxyMiddleware(object):
    
    def process_request(self, request, spider):
        # TODO implement complex proxy providing algorithm
        if self.use_proxy(request):
            p = random.choice(PROXIES)
            try:
                request.meta['proxy'] = "http://%s" % p['ip_port']
		print request.meta['proxy'] 
            except Exception, e:
                log.msg("Exception %s" % e, _level=log.CRITICAL)
                
    
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

from scrapy.downloadermiddlewares.retry import RetryMiddleware
import time
class CustomRetryMiddleware(RetryMiddleware):
    def process_response(self, request, response, spider):
        url = response.url
        if request.meta.get('retry', ''):
                url = response.url
                #check_xpath = response.xpath('//p//text').extract()
                check_xpath = response.xpath('//div[@class="quote"]/a/@href').extract() or response.xpath('//div[@class="quote isNew"]//a//@href').extract()
                if not check_xpath:
                        return self._retry(request, 'meta', spider) or response

        return response

