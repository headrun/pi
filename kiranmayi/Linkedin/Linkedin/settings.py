# -*- coding: utf-8 -*-

# Scrapy settings for Linkedin project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Linkedin'

SPIDER_MODULES = ['Linkedin.spiders']
NEWSPIDER_MODULE = 'Linkedin.spiders'
#ITEM_PIPELINES=['Linkedin.pipelines.LinkedinPipeline']
ITEM_PIPELINES = {'Linkedin.pipelines.LinkedinPipeline': 400,
		'scrapy.pipelines.images.ImagesPipeline':1,}
		#'Linkedin.pipelines.MyImagesPipeline': 1,}

IMAGES_STORE = '/root/Linkedin/Linkedin/spiders/images'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Pibot (+http://www.positiveintegers.com)'
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 10
DOWNLOAD_DELAY = 8 
DOWNLOAD_TIMEOUT = 360
RANDOMIZE_DOWNLOAD_DELAY = True

# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'Linkedin.middlewares.LinkedinSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
    #'Linkedin.middlewares.MyCustomDownloaderMiddleware': 543,
     #'Linkedin.middlewares.CustomHttpProxyMiddleware': 543,
    #'Linkedin.middlewares.CustomUserAgentMiddleware': 545,
#}
#HTTP_PROXY = 'http://176.9.181.34:3279'
#HTTP_PROXY = 'http://zproxy.lum-superproxy.io:22225'
'''HTTP_PROXY = [#'http://lum-customer-hl_75a24c21-zone-zone1-ip-38.131.153.31:rbjphacd6nn6@zproxy.lum-superproxy.io:22225']
		#'http://lum-customer-hl_75a24c21-zone-zone1-ip-38.131.153.141:rbjphacd6nn6@zproxy.lum-superproxy.io:22225']
		#'http://lum-customer-hl_75a24c21-zone-zone1-ip-38.131.153.178:rbjphacd6nn6@zproxy.lum-superproxy.io:22225']
		#'http://lum-customer-hl_75a24c21-zone-zone1-ip-38.131.154.13:rbjphacd6nn6@zproxy.lum-superproxy.io:22225']
		#'http://lum-customer-hl_75a24c21-zone-zone1-ip-38.131.154.32:rbjphacd6nn6@zproxy.lum-superproxy.io:22225']
		'http://lum-customer-hl_75a24c21-zone-zone1-ip-38.131.149.225:rbjphacd6nn6@zproxy.lum-superproxy.io:22225']
		#'http://lum-customer-hl_75a24c21-zone-zone1-ip-38.131.149.251:rbjphacd6nn6@zproxy.lum-superproxy.io:22225']
		#'http://lum-customer-hl_75a24c21-zone-zone1-ip-38.131.150.90:rbjphacd6nn6@zproxy.lum-superproxy.io:22225']
		#'http://lum-customer-hl_75a24c21-zone-zone1-ip-38.131.151.30:rbjphacd6nn6@zproxy.lum-superproxy.io:22225',
		#'http://lum-customer-hl_75a24c21-zone-zone1-ip-38.131.151.48:rbjphacd6nn6@zproxy.lum-superproxy.io:22225']'''
'''HTTP_PROXY = ['http://lum-customer-hl_75a24c21-zone-zone1-ip-38.131.154.132:rbjphacd6nn6@zproxy.lum-superproxy.io:22225',
		'http://lum-customer-hl_75a24c21-zone-zone1-ip-38.131.154.44:rbjphacd6nn6@zproxy.lum-superproxy.io:22225',
		'http://lum-customer-hl_75a24c21-zone-zone1-ip-38.131.154.177:rbjphacd6nn6@zproxy.lum-superproxy.io:22225',
		'htpp://lum-customer-hl_75a24c21-zone-zone1-ip-38.131.154.209:rbjphacd6nn6@zproxy.lum-superproxy.io:22225',
		'http://lum-customer-hl_75a24c21-zone-zone1-ip-38.131.154.206:rbjphacd6nn6@zproxy.lum-superproxy.io:22225']'''
'''HTTP_PROXY = ['http://lum-customer-hl_75a24c21-zone-zone1-ip-38.131.156.106:rbjphacd6nn6@zproxy.lum-superproxy.io:22225',
		'http://lum-customer-hl_75a24c21-zone-zone1-ip-38.131.156.230:rbjphacd6nn6@zproxy.lum-superproxy.io:22225',
		'http://lum-customer-hl_75a24c21-zone-zone1-ip-38.131.156.238:rbjphacd6nn6@zproxy.lum-superproxy.io:22225',
		'http://lum-customer-hl_75a24c21-zone-zone1-ip-38.131.157.55:rbjphacd6nn6@zproxy.lum-superproxy.io:22225',
		'http://lum-customer-hl_75a24c21-zone-zone1-ip-38.131.157.119:rbjphacd6nn6@zproxy.lum-superproxy.io:22225',
		'http://lum-customer-hl_75a24c21-zone-zone1-ip-38.131.158.144:rbjphacd6nn6@zproxy.lum-superproxy.io:22225',
		'http://lum-customer-hl_75a24c21-zone-zone1-ip-38.131.159.8:rbjphacd6nn6@zproxy.lum-superproxy.io:22225',
		'http://lum-customer-hl_75a24c21-zone-zone1-ip-38.131.159.46:rbjphacd6nn6@zproxy.lum-superproxy.io:22225',
		'http://lum-customer-hl_75a24c21-zone-zone1-ip-38.131.159.75:rbjphacd6nn6@zproxy.lum-superproxy.io:22225',
		'http://lum-customer-hl_75a24c21-zone-zone1-ip-38.145.76.21:rbjphacd6nn6@zproxy.lum-superproxy.io:22225']'''
'''HTTP_PROXY = ['http://lum-customer-hl_75a24c21-zone-zone1-ip-38.145.76.25:rbjphacd6nn6@zproxy.lum-superproxy.io:22225',
		'http://lum-customer-hl_75a24c21-zone-zone1-ip-38.145.76.37:rbjphacd6nn6@zproxy.lum-superproxy.io:22225',
		'http://lum-customer-hl_75a24c21-zone-zone1-ip-38.145.76.44:rbjphacd6nn6@zproxy.lum-superproxy.io:22225',
		'http://lum-customer-hl_75a24c21-zone-zone1-ip-38.145.76.55:rbjphacd6nn6@zproxy.lum-superproxy.io:22225',
		'http://lum-customer-hl_75a24c21-zone-zone1-ip-38.145.76.90:rbjphacd6nn6@zproxy.lum-superproxy.io:22225',
		'http://lum-customer-hl_75a24c21-zone-zone1-ip-38.145.77.10:rbjphacd6nn6@zproxy.lum-superproxy.io:22225',
		'http://lum-customer-hl_75a24c21-zone-zone1-ip-38.145.77.106:rbjphacd6nn6@zproxy.lum-superproxy.io:22225',
		'http://lum-customer-hl_75a24c21-zone-zone1-ip-38.145.77.112:rbjphacd6nn6@zproxy.lum-superproxy.io:22225',
		'http://lum-customer-hl_75a24c21-zone-zone1-ip-38.145.78.11:rbjphacd6nn6@zproxy.lum-superproxy.io:22225',
		'http://lum-customer-hl_75a24c21-zone-zone1-ip-38.145.78.41:rbjphacd6nn6@zproxy.lum-superproxy.io:22225']'''
HTTP_PROXY = ['http://lum-customer-hl_75a24c21-zone-zone1-ip-38.145.78.117:rbjphacd6nn6@zproxy.lum-superproxy.io:22225',
		'http://lum-customer-hl_75a24c21-zone-zone1-ip-38.145.79.56:rbjphacd6nn6@zproxy.lum-superproxy.io:22225',
		'http://lum-customer-hl_75a24c21-zone-zone1-ip-38.145.79.157:rbjphacd6nn6@zproxy.lum-superproxy.io:22225',
		'http://lum-customer-hl_75a24c21-zone-zone1-ip-38.145.80.200:rbjphacd6nn6@zproxy.lum-superproxy.io:22225',
		'http://lum-customer-hl_75a24c21-zone-zone1-ip-38.145.81.27:rbjphacd6nn6@zproxy.lum-superproxy.io:22225',
		'http://lum-customer-hl_75a24c21-zone-zone1-ip-38.145.81.145:rbjphacd6nn6@zproxy.lum-superproxy.io:22225',
		'http://lum-customer-hl_75a24c21-zone-zone1-ip-38.145.81.195:rbjphacd6nn6@zproxy.lum-superproxy.io:22225',
		'http://lum-customer-hl_75a24c21-zone-zone1-ip-38.145.82.203:rbjphacd6nn6@zproxy.lum-superproxy.io:22225',
		'http://lum-customer-hl_75a24c21-zone-zone1-ip-38.145.82.244:rbjphacd6nn6@zproxy.lum-superproxy.io:22225',
		'http://lum-customer-hl_75a24c21-zone-zone1-ip-38.145.82.245:rbjphacd6nn6@zproxy.lum-superproxy.io:22225']
#HTTP_PROXY = 'htthp://lum-customer-hl_75a24c21-zone-zone1-ip-78.136.200.21:rbjphacd6nn6@zproxy.lum-superproxy.io:22225'
DOWNLOADER_MIDDLEWARES = {
      'Linkedin.middlewares.ProxyMiddleware':410
}
#DOWNLOADER_MIDDLEWARES = {
#    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
#    'Linkedin.middlewares.ProxyMiddleware': 100,
#}##others

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
    #'Linkedin.pipelines.LinkedinPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 6#60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


