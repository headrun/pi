from juicer.utils import *

class TnreraBrowse(JuicerSpider):
    name = 'tnrera_browse' 
    start_urls = ["https://www.tnrera.in/index.php"]
    

    def __init__(self, *args, **kwargs):
        super(TnreraBrowse, self).__init__(*args, **kwargs)
     

    def parse(self, response):
        import pdb;pdb.set_trace()
        sel = Selector(response)
        nodes = sel.xpath('//div[@class="row"]//ul//li/div[@class="rImage"]')
        for node in nodes :
                 url = self.domain +''.join(node.xpath('./a[contains(@href,"upc")]/@href').extract())
                 title = "".join(node.xpath('./p/text()').extract())
                 sk = url.split('/')[-1]
                 self.get_page("upcitemdb_company_terminal", normalize(url), sk, meta_data={'title':normalize(title),'reference_url':normalize(response.url),'Search_keyword':response.url.split('=')[1].replace('&type','').replace('%20',' ')})

