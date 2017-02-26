from juicer.utils import *
from juicer.items import *

class Indiaconsume(JuicerSpider):
    name = "indiaconsumerforum_browse"
    start_urls = []
    def __init__(self, *args, **kwargs):
        super(Indiaconsume, self).__init__(*args, **kwargs)
        self.search_url = 'http://www.indiaconsumerforum.org/?s='
        self.domain = "http://www.indiaconsumerforum.org/"
        #self.browse_list = 'Apollo hospitals'#comma seperated values
        self.browse_list = 'Apollo hospitals'
        self.browse_list =  kwargs.get('search', self.browse_list)
        self.browse_list = self.browse_list.split(',')
        for br in self.browse_list:
            self.start_urls.append("{}{}".format(self.search_url,br))

    def parse(self, response):
        sel = Selector(response)
        if not response.meta.get('browse',''):
            browse = textify(re.findall('s=(.*)', response.url))
        else: browse = response.meta['browse']
        aux_info = {}
        aux_info.update({"browse":browse})
        nodes = get_nodes(sel, '//section[@id="primary"]/article')
        for nd in nodes:
            review_ur = extract_data(nd,'.//h2[contains(@class,"entry-title")]/a/@href')
            category = extract_data(nd, './/div[@class="post-category"]/a/text()')
            author = extract_data(nd, './/span[@class="vcard author"]//a[@rel="author"]/text()')
            author_url = extract_data(nd, './/span[@class="vcard author"]//a[@rel="author"]/@href')
            aux_info = {}
            aux_info.update({"browse":browse})
            if category: aux_info.update({"category":category})
            if author: aux_info.update({"author":author})
            if author_url:aux_info.update({"author_url":author_url})
            if 'http' not in review_ur: review_ur = "{}{}".format(self.domain,review_ur)
            print review_ur
            sk = md5(review_ur)
            self.get_page('indiaconsumerforum_review_terminal',review_ur, sk, aux_info)
        next_page = textify(sel.xpath('//div[@id="pagination"]/a[@class="next page-numbers"]/@href').extract())
        if not response.meta.get('browse',''):
            self.got_page(sk,1)
        if next_page:
            if 'http' not in next_page: next_page_url = "{}{}".format(self.domain, next_page)
            else: next_page_url = next_page
            if next_page_url: yield Request(next_page_url, callback=self.parse, meta={"browse":browse})
