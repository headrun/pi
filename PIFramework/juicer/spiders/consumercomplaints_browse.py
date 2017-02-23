from juicer.utils import *
from juicer.items import *

class Consumerbrowse(JuicerSpider):
    name = "consumercomplaints_browse"
    start_urls = []
    def __init__(self, *args, **kwargs):
        super(Consumerbrowse, self).__init__(*args, **kwargs)
        self.search = kwargs.get('search', 'Apollo Hospitals')
        self.search_url = 'https://www.consumercomplaints.in/?search='
        self.domain = "https://www.consumercomplaints.in"
        #self.browse_list = ['apollo hospitals','apollo']
        self.browse_list = ['apollo hospitals']
        for br in self.browse_list:
            self.start_urls.append("{}{}".format(self.search_url,br))

    def parse(self, response):
        sel = Selector(response)
        if not response.meta.get('browse',''):
            browse = textify(re.findall('search=(.*)', response.url))
        else: browse = response.meta['browse']
        aux_info = {}
        aux_info.update({"browse":browse})
        review_urls = sel.xpath('//td[@class="complaint"]/a/@href').extract()
        for review in review_urls:
            review_ = "{}{}".format(self.domain, review)
            #sk = review.split('-')[-1].replace('.html','')
            sk = md5(review)
            self.get_page('consumercomplaints_review_terminal',review_, sk, aux_info)
        next_page = textify(sel.xpath('//nav[@class="pg"]/ul//li/a[contains(text(),"Next")]/@href').extract())
        if not response.meta.get('browse',''):
            self.got_page(sk,1)
        if next_page:
            next_page_url = "{}{}".format(self.domain, next_page)
            if next_page_url: yield Request(next_page_url, callback=self.parse, meta={"browse":browse})
