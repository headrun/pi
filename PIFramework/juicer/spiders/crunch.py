#Crunchbase Crawler
from juicer.utils import *

class Crunchbase(JuicerSpider):
    name = 'crunchbase_browse'
    start_urls = ['https://www.crunchbase.com/organization/blackbuck']

    def __init__(self, *args, **kwargs):
        super(Crunchbase, self).__init__(*args, **kwargs)
        #settings.overrides['DOWNLOADER_CLIENTCONTEXTFACTORY'] = 'juicer.contextfactory.MyClientContextFactory'
        settings.overrides['DOWNLOADER_CLIENTCONTEXTFACTORY'] = 'juicer.contextfactory.CustomClientContextFactory'

    def parse(self, response):
        import pdb;pdb.set_trace()
        print response.url

