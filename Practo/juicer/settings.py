import os
import urllib
import random

PROJECT_DIR = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

BOT_NAME = 'practo' #'juicer'
BOT_VERSION = '2.0'

SPIDER_MODULES = ['juicer.spiders']
NEWSPIDER_MODULE = 'juicer.spiders'
DEFAULT_ITEM_CLASS = 'juicer.items.JuicerItem'

#SER_AGENT = "Mozilla/5.0 (Linux; Pibot; + http://positiveintegers.com/) AppleWebKit/535.21 (KHTML, like Gecko) Chrome/19.0.1042.0"

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/53.0.2785.143 Chrome/53.0.2785.143 Safari/537.36"
#USER_AGENT =  'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'
#USER_AGENT =  'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'

ITEM_PIPELINES = {
    #'juicer.validations_pipeline.ValidateRecordPipeline': 300,
    'juicer.pipelines.JuicerPipeline': 400,
}

HTTPCACHE_ENABLED = True                                    # Note: Disable Cache Option in Prod setup.
HTTPCACHE_DIR = '%s/cache/' % PROJECT_DIR
#HTTPCACHE_DIR= '/root/pi_crawling/PIFramework/juicer'
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_STORAGE = 'juicer.cache.LevelDBCacheStorage'

ROBOTSTXT_OBEY = 1
#DOWNLOAD_DELAY = 2
DOWNLOAD_TIMEOUT = 360
RANDOMIZE_DOWNLOAD_DELAY = True

DOWNLOAD_DELAY = 10
#DOWNLOAD_DELAY = 0.25
'''AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 6
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_DEBUG = False'''

LOG_FILE = None
LOG_LEVEL = 'INFO' #'DEBUG'

# DB Details
DB_HOST ='localhost'
DB_USERNAME = 'root'
DB_PASSWORD = 'root'
URLQ_DATABASE_NAME = 'urlqueue_dev'                         # Fill with actual DATABASE NAME.

SCRIPT_LOG_FILE = 'juicer.log'
LOGS_DIR = '%s/logs/' % PROJECT_DIR

TELNETCONSOLE_ENABLED = False
WEBSERVICE_ENABLED = False

NUM_ITEMS_TO_CONSUME = 10000

CONCURRENT_SPIDERS = 5

RETRY_TIMES = 10
RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]

SPIDER_MIDDLEWARES = {
    'juicer.utils.SpiderMiddleware': 10000,
    #'juicer.randomproxy.RandomProxy': 100,
    #'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
}

DOWNLOADER_MIDDLEWARES = {
    'juicer.utils.RandomUserAgentMiddleware': 400,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    #'scrapy.contrib.downloadermiddleware.redirect.RedirectMiddleware': 123,G
    #'juicer.middlewares.InterfaceRoundRobinMiddleware' : 1
}

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
    'Accept-Encoding': '*'
}

RANDOM_SCHEDULING = True

DUMPSTORE_DIR = "%s/output_dir/" % PROJECT_DIR

DEFAULT_CRAWLER_PRIORITY = 5

MIN_URLS_TO_GET = 10

NO_ITEMS_TO_PROCESS = 100
NO_URLS_TO_PROCESS = 10000
NO_DUMPSTORE_ITEMS_TO_PROCESS = 10000

COUNTER_PREFIX  = "services.intervod.stats"

#USER_AGENT_LIST = #["Mozilla/5.0 (Linux; Pibot; + http://positiveintegers.com/) AppleWebKit/535.21 (KHTML, like Gecko) Chrome/19.0.1042.0",\
USER_AGENT_LIST = ["Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785",\
                   #"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",\
                   #"Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3"
                   ]

#USER_AGENT_LIST = ["Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/53.0.2785.143 Chrome/53.0.2785.143 Safari/537.36",\
#                   "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0"]

#PROXIES_LIST = ['http://%s:3279' % random.choice(list(open('/root/pi_crawling/Practo/juicer/proxy.list'))).strip()]
PROXIES_LIST = [i.strip() for i in list(open('/root/Practo/juicer/proxy.list'))]
