from juicer.utils import *
from upcitemdb_input import Company_names

class UpcitemdbBrowse(JuicerSpider):
    name = 'upcitemdb_company_browse' 
    start_urls = []
    for company in Company_names :
        start_urls.append('http://www.upcitemdb.com/upc/'+str(company))

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
                 self.get_page("upcitemdb_company_terminal", url, sk, meta_data={'title':title})

