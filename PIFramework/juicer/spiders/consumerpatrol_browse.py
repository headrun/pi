from juicer.utils import *
from juicer.items import *
#import dateparser

class Consumerpatrolbrowse(JuicerSpider):
    name = "consumerpatrol_browse"
    start_urls = []
    def __init__(self, *args, **kwargs):
        super(Consumerpatrolbrowse, self).__init__(*args, **kwargs)
        self.search_url = 'http://consumerpatrol.in/search?key='
        self.domain = "http://consumerpatrol.in/"
        self.browse_list = 'Apollo hospitals'#comma seperated values
        self.browse_list =  kwargs.get('search', self.browse_list)
        self.browse_list = self.browse_list.split(',')
        for br in self.browse_list:
            self.start_urls.append("{}{}".format(self.search_url,br))


    def replacefun(self, text):
        text = text.replace('"','<>#<>').replace("'","<>##<>").replace(',','###')
        return text

    def parse(self, response):
        sel = Selector(response)
        nodes = get_nodes(sel,'//div[@class="complaint_listing"][not(@style)]')
        if not response.meta.get('browse',''):
            browse = textify(re.findall('search\?key=(.*)', response.url))
        else: browse = response.meta['browse']
        for nd in nodes:
            review_title = extract_data(nd, './/div[@class="com_list_title"]/p/a/text()')
            company_name = extract_data(nd, './/div[@class="com_list_post_date"][@style]/p/span/text()')
            no_of_views = extract_data(nd, './/div[@class="com_list_post_date"][not(@style)]/p/text()[contains(.,"No.of.views")]/following-sibling::span[1]//text()').replace('(','').replace(')','')
            author = extract_data(nd, './/div[@class="com_list_post_date"][not(@style)]/p/text()[contains(.,"by")]/following-sibling::span[1]//text()')
            comment_desc = extract_data(nd, './/div[@class="com_list_post_date"][not(@style)]/comment()')
            post_date = textify(re.findall('Posted.* <span .*">(.*) </span>',comment_desc.replace('\n','')))
            if post_date: post_date = str(dateparser.parse(post_date))
            review_url = extract_data(nd, './/div[@class="com_list_title"]/p/a/@href')
            review = extract_data(nd, './/div[@class="com_list_detail"]/p//text()')
            category = extract_data(nd, './/div[@class="com_list_catego_repli"]/p/text()[contains(.,"Category")]/following-sibling::span[1]//text()')
            country = extract_data(nd, './/div[@class="com_list_catego_repli"]/p/text()[contains(.,"Country")]/following-sibling::span[1]//text()')
            replies = extract_data(nd, './/div[@class="com_list_catego_repli"]//p[span/a[contains(text(),"Replies")]]/text()').replace('(','').replace(')','')

            sk = md5(review+review_url+post_date+comment_desc+replies+country)
            aux_info = {}
            aux_info.update({"browse":browse})
            if review_url: aux_info.update({"review_main_url":review_url})
            if no_of_views: aux_info.update({"no_of_views":no_of_views})
            if company_name: aux_info.update({"company_name":self.replacefun(company_name)})
            if replies: aux_info.update({"no_of_replies":replies})
            if country: aux_info.update({"country":self.replacefun(country)})
            customerReviews = CustomerReviews()
            customerReviews.update({"sk":normalize(sk), "name":normalize(review_title), "product_id":normalize(sk),"reviewed_by":normalize(author),"reviewed_on":normalize(post_date),"review":normalize(review),"review_url":normalize(response.url),"category":normalize(category)})
            if aux_info: customerReviews.update({"aux_info":normalize(json.dumps(aux_info, ensure_ascii=False, encoding="utf-8"))})
            yield customerReviews

        next_page = extract_data(sel, '//a[@title="Go To Next Page"]/@href')
        if next_page:
            if 'http' not in next_page: next_page = "{}{}".format(self.domain, next_page)
            if next_page: yield Request(next_page, callback=self.parse, meta={"browse":browse})
