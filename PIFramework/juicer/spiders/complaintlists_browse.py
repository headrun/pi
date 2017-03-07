from juicer.utils import *
from juicer.items import *

class Complaintlistsb(JuicerSpider):
    name = "complaintlists_browse"
    start_urls = []
    def __init__(self, *args, **kwargs):
        super(Complaintlistsb, self).__init__(*args, **kwargs)
        self.search_url = 'http://www.complaintlists.com/?s=%s&searchsubmit=Search'
        self.domain = "http://www.complaintlists.com/"
        self.browse_list = 'Apollo hospitals'
        self.browse_list =  kwargs.get('search', self.browse_list)
        self.browse_list = self.browse_list.split(',')
        for br in self.browse_list:
            self.start_urls.append(self.search_url%br)

    def parse(self, response):
        sel = Selector(response)
        if not response.meta.get('browse',''):
            browse = textify(re.findall('\?s=(.*)&searchsubmit', response.url))
        else: browse = response.meta['browse']
        aux_info = {}
        aux_info.update({"browse":browse})
        nodes = get_nodes(sel, '//div[@class="main"]//article[contains(@class,"post")]')
        for nd in nodes:
            review_ur = extract_data(nd,'.//h2/a/@href')
            sk = md5(review_ur)
            self.get_page('complaintlists_review_terminal',review_ur, sk, aux_info)
        next_page = textify(sel.xpath('//div[@class="navigation"]//a[contains(text(),"Next")]/@href').extract())
        if next_page:
            if 'http' not in next_page: next_page_url = "{}{}".format(self.domain, next_page)
            else: next_page_url = next_page
            if next_page_url: yield Request(next_page_url, callback=self.parse, meta={"browse":browse})
