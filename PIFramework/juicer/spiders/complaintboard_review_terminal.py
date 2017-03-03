from juicer.utils import *
from juicer.items import *
import dateparser

class Complaintboardreviews(JuicerSpider):
    name = 'complaintboard_review_terminal'
    def __init__(self, *args, **kwargs):
        super(Complaintboardreviews, self).__init__(*args, **kwargs)
        self.domain = "http://www.complaintboard.in"


    def replacefun(self, text):
        text = text.replace('"','<>#<>').replace("'","<>##<>").replace(',','###')
        return text


    def get_customer(self, sk, title, reviedw_by, date1, review_description, response_url, aux_info):
        customerReviews = CustomerReviews()
        customerReviews.update({"sk":normalize(sk), "name":normalize(title), "product_id":normalize(sk),"reviewed_by":normalize(reviedw_by),"reviewed_on":normalize(date1),"review":normalize(review_description),"review_url":normalize(response_url)})
        if aux_info: customerReviews.update({"aux_info":normalize(json.dumps(aux_info, ensure_ascii=False, encoding="utf-8"))})
        return customerReviews

    def parse(self, response):
        sel = Selector(response)
        #print response.url
        sk = response.meta['sk']
        if response.meta.get('data',''):
            browse = response.meta.get('data','').get('browse','')
        else: browse = response.meta['browse']
        title = extract_data(sel, '//td[h1[div]]/h1/text()')
        location = extract_data(sel, '//td[@class="wmm"]//td[h1[@*]]/h1[not(div)]/text()')
        nodes = get_nodes(sel, '//table//tr/td/div[@id][@style]')
        for nd in nodes:
            author_name = extract_data(nd, './/td[@class="small"][contains(@style,"align:left")]/a[not(@rel)]/text()')
            author_url = extract_data(nd, './/td[@class="small"][contains(@style,"align:left")]/a[not(@rel)]/@href')
            if not author_name: author_name = extract_data(nd, './/td[@class="small"][contains(@style,"align:left")]/text()')
            post_date = extract_data(nd, './/td[@class="small"][contains(@style,"align:right")]/text()')
            if post_date: post_date = str(dateparser.parse(post_date))
            post_text = extract_data(nd , './/td[@class="complaint"]//h4/text()')
            #if 'apollo hospital' not in post_text.lower(): continue
            review_description = extract_data(nd , './/td[@class="complaint"]/div/div//text()',' ')
            sk_ = md5(sk+post_text+review_description+author_name+author_url+post_date)
            aux_info = {}
            aux_info.update({"browse":self.replacefun(browse)})
            aux_info.update({"location":self.replacefun(location)})
            if post_text: aux_info.update({"post_title":self.replacefun(post_text)})
            if author_url:
                if 'http' not in author_url: author_url = "{}{}".format(self.domain, author_url)
                yield Request(author_url, callback=self.parse_next, meta={"sk":sk_, "title":title,"post_date":post_date,"review_description":review_description, "aux_info":aux_info,"response_url":response.url}, dont_filter=True)
            else:
                if author_url: aux_info.update({"author_url":self.replacefun(author_url)})
                if author_name: aux_info.update({"author_name":self.replacefun(author_name)})
                cus_rev = self.get_customer(sk_,title, author_name, post_date, review_description, response.url, aux_info)
                if cus_rev:
                    yield cus_rev
        if response.meta.get('data',''):
            self.got_page(sk,1)
        next_page = extract_data(sel, '//div[@class="pagelinks"]/a[contains(text(),"Next")]/@href')
        if next_page:
            if 'http' not in next_page: next_page = "{}{}".format(self.domain, next_page)
            if next_page: yield Request(next_page, callback=self.parse, meta={"sk":sk,"browse":browse})

    def parse_next(self, response):
        sel = Selector(response)
        sk_ = response.meta.get('sk','')
        title = response.meta.get('title','')
        aux_info = response.meta.get('aux_info','')
        post_date = response.meta.get('post_date','')
        response_url = response.meta.get('response_url','')
        review_description = response.meta.get('review_description','')
        author_name = extract_data(sel, '//span[@class="displname"]/text()')
        aux_info.update({"author_url":self.replacefun(response.url)})
        author_location = extract_data(sel, '//td[@class="wmm"]//div[contains(text(),"Location")]/following-sibling::div/text()')
        author_since_date = extract_data(sel,'//td[@class="wmm"]//span[@class="grey-normal"]/text()').replace('Member since','').strip()
        if author_since_date: author_since_date = str(dateparser.parse(author_since_date))
        if author_since_date: aux_info.update({"author_since_date":author_since_date})
        if author_location: aux_info.update({"author_location":self.replacefun(author_location)})
        if author_name: aux_info.update({"author_name":self.replacefun(author_name)})
        aux_info.update({"author_url":self.replacefun(response.url)})
        cus_rev = self.get_customer(sk_,title, author_name, post_date, review_description, response_url, aux_info)
        if cus_rev: yield cus_rev


