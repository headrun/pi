from juicer.utils import *
from juicer.items import *
import dateparser

class Complaintlistsreview(JuicerSpider):
    name = 'complaintlists_review_terminal'

    def __init__(self, *args, **kwargs):
        super(Complaintlistsreview, self).__init__(*args, **kwargs)
        self.domain = "http://www.complaintlists.com/"

    def parse(self, response):
        sel = Selector(response)
        sk = response.meta.get('sk','')
        browse = response.meta.get('data','').get('browse','')
        aux_info = {}
        aux_info.update({"browse":browse})
        title = extract_data(sel,'//div[@class="main"]/article[contains(@id,"post")]/h1/text()')
        post_date = extract_data(sel, '//p[@class="post-meta"]/span[@class="icon date"]/following::text()[1]').strip().strip(',')
        if post_date: post_date = str(dateparser.parse(post_date))
        author = extract_data(sel, '//p[@class="post-meta"]/span[@class="icon author"]/following::text()[1]').strip().strip(',')
        commentss = (extract_data(sel, '//span[@class="icon comments"]/following::text()[1]')).strip()
        review = textify(sel.xpath('//div[@class="main"]//p[not(@*)]/text()').extract()).strip(', ').strip(',').strip().replace(u'\u2026','...')
        city = extract_data(sel, '//div[@class="taxonomy"]/text()[contains(.,"Town/City")]/following::a[1]/text()')
        state = extract_data(sel, '//div[@class="taxonomy"]/text()[contains(.,"Union Territory/State")]/following::a[1]/text()')
        country = extract_data(sel, '//div[@class="taxonomy"]/text()[contains(.,"Country")]/following::a[1]/text()')
        category = extract_data(sel, '//p[span[@class="icon cats"]]/a/text()')
        if city: aux_info.update({"city":city})
        if state: aux_info.update({"state":state})
        if country: aux_info.update({"country":country})
        if commentss: aux_info.update({"no_of_comments":commentss})
        sk_ = md5(title+post_date+author+sk+review+commentss)
        customerReviews = CustomerReviews()
        customerReviews.update({"sk":normalize(sk_),"product_id":normalize(sk_), "name":normalize(title), "reviewed_by":normalize(author),"reviewed_on":normalize(post_date),"review":normalize(review),"review_url":normalize(response.url),"category":normalize(category)})
        if aux_info: customerReviews.update({"aux_info":normalize(json.dumps(aux_info, ensure_ascii=False, encoding="utf-8"))})
        yield customerReviews
        if response.meta.get('data',''):
            self.got_page(sk,1)


