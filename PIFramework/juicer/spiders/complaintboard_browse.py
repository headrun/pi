from juicer.utils import *
from juicer.items import *

class Complaintboardbrowse(JuicerSpider):
    name = "complaintboard_browse"
    start_urls = []
    def __init__(self, *args, **kwargs):
        super(Complaintboardbrowse, self).__init__(*args, **kwargs)
        self.search_url = 'http://www.complaintboard.in/?search='
        self.domain = "http://www.complaintboard.in"
        self.browse_list = 'Apollo hospitals'#comma seperated values
        self.browse_list =  kwargs.get('search', self.browse_list)
        self.browse_list = self.browse_list.split(',')
        for br in self.browse_list:
            self.start_urls.append("{}{}".format(self.search_url,br))

    def parse(self, response):
        sel = Selector(response)
        nodes = get_nodes(sel,'//table[@id="body"]//tr/td/div[@id="c"]')
        if not response.meta.get('browse',''):
            browse = textify(re.findall('search=(.*)', response.url))
        else: browse = response.meta['browse']
        for nd in nodes:
            review = extract_data(nd, './/td[@class="complaint"]//a/@href')
            review_title = extract_data(nd, './/td[@class="complaint"]//a//text()')
            post_date = extract_data(nd, './/td[@class="small"]/text()')
            author_name = extract_data(nd, './/td[@class="small"]/span/a/text()')
            author_url = extract_data(nd, './/td[@class="small"]/span/a/@href')
            if 'http' not in author_url.encode('utf8'): author_url = "{}{}".format(self.domain, author_url.encode('utf8'))
            if not review: continue
            if '#' in review: review = review.split('#')[0]
            if 'http' not in review.encode('utf8'): review = "{}{}".format(self.domain, review.encode('utf8'))
            sk = md5(review)
            aux_info = {}
            aux_info.update({"browse":browse})
            if review_title: aux_info.update({"review_title":review_title})
            if post_date: aux_info.update({"post_date": post_date})
            if author_name: aux_info.update({"author_name": author_name})
            if author_url: aux_info.update({"author_url":author_url})
            print review
            self.get_page('complaintboard_review_terminal',review, sk, aux_info)
        next_page = extract_data(sel, '//div[@class="pagelinks"]/a[contains(text(),"Next")]/@href')
        if next_page:
            if 'http' not in next_page: next_page = "{}{}".format(self.domain, next_page)
            if next_page: yield Request(next_page, callback=self.parse, meta={"browse":browse})
