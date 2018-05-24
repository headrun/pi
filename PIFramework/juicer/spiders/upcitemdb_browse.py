from juicer.utils import *
from upcitemdb_input import Company_names

class UpcitemdbBrowse(JuicerSpider):
    name = 'upcitemdb_company_browse' 
    start_urls = []
    for company in Company_names :
        start_urls.append('http://www.upcitemdb.com/query?s='+str(company)+'&type=2')

    def __init__(self, *args, **kwargs):
        super(UpcitemdbBrowse, self).__init__(*args, **kwargs)
        self.domain = 'http://www.upcitemdb.com'

    def parse(self, response):
        sel = Selector(response)
        nodes = sel.xpath('//div[@class="row"]//ul//li/div[@class="rImage"]')
        for node in nodes :
                 url = self.domain +''.join(node.xpath('./a[contains(@href,"upc")]/@href').extract())
                 title = "".join(node.xpath('./p/text()').extract())
                 sk = url.split('/')[-1]
                 self.get_page("upcitemdb_company_terminal", normalize(url), sk, meta_data={'title':normalize(title),'reference_url':normalize(response.url),'Search_keyword':response.url.split('=')[1].replace('&type','').replace('%20',' ')})

