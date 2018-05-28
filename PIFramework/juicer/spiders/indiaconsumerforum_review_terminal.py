from juicer.utils import *
from juicer.items import *
#import dateparser

class Indiaconsumer(JuicerSpider):
    name = 'indiaconsumerforum_review_terminal'

    def __init__(self, *args, **kwargs):
        super(Indiaconsumer, self).__init__(*args, **kwargs)
        self.pattern1 = re.compile(r'(\d+\/\d+\/\d+)')

    def parse(self, response):
        sel = Selector(response)
        sk = response.meta['sk']
        browse = response.meta.get('data','').get('browse','')
        meta_data_from = response.meta.get('data','')
        category = meta_data_from.get('category','')
        author_url = meta_data_from.get('author_url','')
        author = meta_data_from.get('author','')
        if not category: category = extract_data(sel, '//div[@class="post-category"]/a/text()')
        if not author: author = extract_data(sel, '//span[@class="vcard author"]//a[@rel="author"]/text()')
        if not author_url: extract_data(sel, '//span[@class="vcard author"]//a[@rel="author"]/@href')
        title = extract_data(sel, '//h1[@class="entry-title"]/text()')
        location = extract_data(sel, '//cite//span[@class="location"]/text()')
        reviews = extract_data(sel,'//div[@class="entry-content"]/p//text()')
        details_check = sel.xpath('//div[@class="entry-content"]/p[contains(.,"Email: ")]/text()').extract()
        aux_info = {}
        aux_info.update({"browse":browse})
        if author_url: aux_info.update({"author_profile":author_url})
        if location: aux_info.update({"location":location})
        email_no = self.name_clean(extract_data(sel,'//div[@class="entry-content"]/p/text()[contains(.,"Email: ")]')).replace('Email:','')
        contact_no = self.name_clean(extract_data(sel,'//div[@class="entry-content"]/p/text()[contains(.,"Contact No")]'))
        if contact_no: contact_no = textify(re.findall('Contact No.*? (.*)', contact_no))
        author1, address, stampip, date1 = ['']*4
        if details_check:
            author1 = self.name_clean(details_check[0])
            if len(details_check) >1:
                address = self.name_clean(details_check[1])
                stampip = self.name_clean(details_check[-1])
            if 'Email:' in address or "Contact No" in address: address = ''
            if self.pattern1.search(stampip):
                if '/ ' in stampip:
                    stampip_cl = stampip.split('/ ')
                    try:
                        stampip_cl = stampip_cl[1:]
                        date1 = str(dateparser.parse(' '.join(stampip_cl)))
                    except: pass
            else:
                stampip = ''
        if author1: author = author1
        if address: aux_info.update({"address":address})
        if email_no: aux_info.update({"email":email_no})
        if contact_no: aux_info.update({"contact_no":contact_no})
        customerReviews = CustomerReviews()
        customerReviews.update({"sk":normalize(sk), "name":normalize(title), "product_id":normalize(sk),"reviewed_by":normalize(author),"reviewed_on":normalize(date1),"review":normalize(reviews),"review_url":normalize(response.url),"category":normalize(category)})
        if aux_info: customerReviews.update({"aux_info":json.dumps(aux_info, ensure_ascii=False, encoding="utf-8")})
        yield customerReviews
        self.got_page(sk,1)

    def name_clean(self, text):
        text = text.replace(u'\xa0','').replace(u'\u2013','').strip()
        return text
