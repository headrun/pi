import os
import urllib
import random

PROJECT_DIR = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

BOT_NAME = 'practo' #'juicer'
BOT_VERSION = '2.0'

SPIDER_MODULES = ['juicer.spiders']
NEWSPIDER_MODULE = 'juicer.spiders'
DEFAULT_ITEM_CLASS = 'juicer.items.JuicerItem'

#USER_AGENT = "Mozilla/5.0 (Linux; Pibot; + http://positiveintegers.com/) AppleWebKit/535.21 (KHTML, like Gecko) Chrome/19.0.1042.0"
#USER_AGENT_LIST = [i.strip() for i in list(open('/root/PIFramework/juicer/useragents2.list'))]

USER_AGENT_LIST = ["Mozilla/5.0 (Linux; Pibot; + http://positiveintegers.com/) AppleWebKit/535.21 (KHTML, like Gecko) Chrome/19.0.1042.0",\
                   "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785",\
                   "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",\
                   "Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3"]

#USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/53.0.2785.143 Chrome/53.0.2785.143 Safari/537.36"
#USER_AGENT =  'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'
#USER_AGENT =  'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'

ITEM_PIPELINES = {
    #'juicer.validations_pipeline.ValidateRecordPipeline': 300,
    'juicer.pipelines.JuicerPipeline': 400,
}

#HTTPCACHE_ENABLED = True                                    # Note: Disable Cache Option in Prod setup.
#HTTPCACHE_DIR = '%s/cache/' % PROJECT_DIR
#HTTPCACHE_DIR= '/root/pi_crawling/PIFramework/juicer'
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_STORAGE = 'juicer.cache.LevelDBCacheStorage'

ROBOTSTXT_OBEY = 1
#DOWNLOAD_DELAY = 2
DOWNLOAD_TIMEOUT = 360
RANDOMIZE_DOWNLOAD_DELAY = True

DOWNLOAD_DELAY = 1
#DOWNLOAD_DELAY = 0.25
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 6
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_DEBUG = False

LOG_FILE = None
LOG_LEVEL = 'INFO' #'DEBUG'
#LOG_LEVEL = 'DEBUG'

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

CONCURRENT_REQUESTS_PER_IP = 3

RETRY_TIMES = 4
#RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408, 200]

SPIDER_MIDDLEWARES = {
    'juicer.utils.SpiderMiddleware': 10000,
    #'juicer.randomproxy.RandomProxy': 100,
    #'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
}

DOWNLOADER_MIDDLEWARES = {
    'juicer.middlewares.CustomRetryMiddleware':600, 
    #'juicer.middlewares.CustomUserAgentMiddleware':500,
    'juicer.utils.RandomUserAgentMiddleware': 401,
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
#USER_AGENT_LIST = [#"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785",\
                   #"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",\
                   #"Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3"
                   #]

#USER_AGENT_LIST = ["Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/53.0.2785.143 Chrome/53.0.2785.143 Safari/537.36",\
#                   "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0"]
#USER_AGENT_LIST = [i.strip() for i in list(open('/root/pi_crawling/Practo/juicer/useragents.list'))]
#PROXIES_LIST = ['http://%s:3279' % random.choice(list(open('/root/PIFramework/juicer/proxy.list'))).strip()]
#PROXIES_LIST = ["https://melb.au.torguardvpnaccess.com:6060","https://melb.au.torguardvpnaccess.com:6060","https://bul.torguardvpnaccess.com:6060",'https://au.torguardvpnaccess.com:6060','https://ro.torguardvpnaccess.com:6060','https://ru.torguardvpnaccess.com:6060','https://mos.ru.torguardvpnaccess.com:6060',"https://swe.torguardvpnaccess.com:6060",'https://swiss.torguardvpnaccess.com:6060','https://bg.torguardvpnaccess.com:6060',"https://hk.torguardvpnaccess.com:6060",'https://ind.torguardvpnaccess.com:6060','https://thai.torguardvpnaccess.com:6060','https://turk.torguardvpnaccess.com:6060','https://mx.torguardvpnaccess.com:6060','https://singp.torguardvpnaccess.com:6060','https://saudi.torguardvpnaccess.com:6060','https://fr.torguardvpnaccess.com:6060','https://pl.torguardvpnaccess.com:6060','https://czech.torguardvpnaccess.com:6060','https://it.torguardvpnaccess.com:6060','https://sp.torguardvpnaccess.com:6060','https://no.torguardvpnaccess.com:6060','https://por.torguardvpnaccess.com:6060','https://za.torguardvpnaccess.com:6060','https://den.torguardvpnaccess.com:6060','https://vn.torguardvpnaccess.com:6060','https://pa.torguardvpnaccess.com:6060','https://sk.torguardvpnaccess.com:6060','https://lux.torguardvpnaccess.com:6060','https://nz.torguardvpnaccess.com:6060','https://md.torguardvpnaccess.com:6060','https://uae.torguardvpnaccess.com:6060','https://slk.torguardvpnaccess.com:6060','https://fl.east.usa.torguardvpnaccess.com:6060','https://atl.east.usa.torguardvpnaccess.com:6060','https://ny.east.usa.torguardvpnaccess.com:6060','https://sa.west.usa.torguardvpnaccess.com:6060','https://nj.east.usa.torguardvpnaccess.com:6060','https://east.usa.torguardvpnaccess.com:6060','https://egy.torguardvpnaccess.com:6060','https://cn.torguardvpnaccess.com:6060','https://la.west.usa.torguardvpnaccess.com:6060','https://west.usa.torguardvpnaccess.com:6060','https://dal.central.usa.torguardvpnaccess.com:6060','https://cp.torguardvpnaccess.com:6060','https://chi.central.usa.torguardvpnaccess.com:6060','https://cr.torguardvpnaccess.com:6060','https://tun.torguardvpnaccess.com:6060','https://bul.torguardvpnaccess.com:6060','https://hg.torguardvpnaccess.com:6060','https://my.torguardvpnaccess.com:6060','https://lv.torguardvpnaccess.com:6060','https://cp.torguardvpnaccess.com:6060','https://gre.torguardvpnaccess.com:6060','https://central.usa.torguardvpnaccess.com:6060','https://dal.central.usa.torguardvpnaccess.com:6060','https://lv.west.usa.torguardvpnaccess.com:6060','https://lv.west.usa.torguardvpnaccess.com:6060','https://eastusa.torguardvpnaccess.com:6060','https://westusa.torguardvpnaccess.com:6060','https://centralusa.torguardvpnaccess.com:6060']

#PROXIES_LIST = [i.strip() for i in list(open('/root/PIFramework/juicer/proxy.list'))]
PROXIES_LIST = ['http://zproxy.lum-superproxy.io:22225']
#HTTP_PROXY = '%s'

