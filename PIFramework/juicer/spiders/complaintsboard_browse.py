from juicer.utils import *

class ComplaintsBoardComBrowse(JuicerSpider):
    name = 'complaintsboardcom_browse'
    handle_httpstatus_list = [301]

    def __init__(self, *args, **kwargs):
        super(ComplaintsBoardComBrowse, self).__init__(*args, **kwargs)
        self.search_url = "https://www.complaintsboard.com/?search="
        self.domain = "https://www.complaintsboard.com"
        self.browse_list = 'apollo+hospitals'
        self.browse_list =  kwargs.get('search', self.browse_list)
        self.browse_list = self.browse_list.split(',')
        for br in self.browse_list:
            self.start_urls.append("{}{}".format(self.search_url,br))

    def parse(self, response):
        sel = Selector(response)
        nodes = get_nodes(sel,'//table//tr/td/div[@class="item-row"][@id]')
        if not response.meta.get('browse',''):
            browse = textify(re.findall('search=(.*)', response.url))
        else: browse = response.meta['browse']
        for nd in nodes:
            review = extract_data(nd, './/td[@class="complaint"]//a/@href')
            review_title = extract_data(nd, './/td[@class="complaint"]//a//text()')
            if not review: continue
            if '#' in review: review = review.split('#')[0]
            if 'http' not in review.encode('utf8'): review = "{}{}".format(self.domain, review.encode('utf8'))
            sk = md5(review)
            aux_info = {}
            aux_info.update({"browse":browse})
            if review_title: aux_info.update({"review_title":review_title})
            self.get_page('complaintsboard_review_terminal',review, sk, aux_info)
        next_page = extract_data(sel, '//nav[@class="pages"]/a[contains(text(),"Next")]/@href')
        if next_page:
            if 'http' not in next_page: next_page = "{}{}".format(self.domain, next_page)
            if next_page: yield Request(next_page, callback=self.parse, meta={"browse":browse})


