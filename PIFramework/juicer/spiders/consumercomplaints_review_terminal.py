from juicer.utils import *
from juicer.items import *

class Consumercomlaintsreviews(JuicerSpider):
    name = 'consumercomplaints_review_terminal'

    def __init__(self, *args, **kwargs):
        super(Consumercomlaintsreviews, self).__init__(*args, **kwargs)

    def parse(self, response):
        sel = Selector(response)
        sk = response.meta['sk']
        browse = response.meta.get('data','').get('browse','')
        title = extract_data(sel, '//h1[@property="v:itemreviewed"]/text()')
        rating = extract_data(sel, '//span[@typeof="v:Rating"]/meta[@property="v:average"]/@content')
        reviews = extract_data(sel, '//span[@typeof="v:Rating"]//text()[contains(., "Review")]')
        review_description = extract_data(sel, '//td[@class="compl-text"]/div[not(@*)]/text()')
        reviedw_by = extract_data(sel, '//td/a[contains(@href, "profile")]/text()')
        author_profile = extract_data(sel, '//td/a[contains(@href, "profile")][@class]/@href')
        if author_profile: author_profile = "https://www.consumercomplaints.in%s"%author_profile
        date_txt = extract_data(sel, '//td/a[contains(@href, "profile")]/../text()')
        comment = extract_data(sel, '//td/a/text()[contains(., "Comment")]')
        date1 = ''
        aux_info = {}
        aux_info.update({"browse":browse})
        if comment: aux_info.update({"comment":comment})
        if reviews: aux_info.update({"no_of_reviews":reviews})
        if author_profile: aux_info.update({"author_profile":author_profile})
        if date_txt:
            date1 = str(parse_date(date_txt))
        customerReviews = CustomerReviews()
        customerReviews.update({"sk":normalize(sk), "name":normalize(title), "product_id":normalize(sk),"reviewed_by":normalize(reviedw_by),"reviewed_on":normalize(date1),"review":normalize(review_description),"review_url":normalize(response.url),"review_rating":normalize(rating)})
        if aux_info: customerReviews.update({"aux_info":json.dumps(aux_info, ensure_ascii=False, encoding="utf-8")})
        yield customerReviews
        self.got_page(sk,1)


