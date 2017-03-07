from juicer.utils import *
from juicer.items import *
import dateparser

class Consumderdaddyreviews(JuicerSpider):
    name = 'consumerdaddy_review_terminal'
    def __init__(self, *args, **kwargs):
        super(Consumderdaddyreviews, self).__init__(*args, **kwargs)
        self.domain = "http://www.consumerdaddy.com/"


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
        sk = response.meta['sk']
        location = response.meta.get('data','').get('location','')
        browse = response.meta.get('data','').get('browse','')
        title = extract_data(sel,'//h1[contains(@id,"ProductName")][@title]/text()')
        review_nodes = get_nodes(sel, '//div[contains(@id,"LatestReviews")]//tr[@class="pdproductinfolist"]//table[contains(@id,"Panel_gvList")]/tr[td]')
        for nd in review_nodes:
            post_ti = extract_data(nd, './/tr[@style="text-align: left; vertical-align: top;"]/td[contains(text(),"by")]/a[1]/@title')
            post_enterprise = extract_data(nd, './/tr[@style="text-align: left; vertical-align: top;"]/td[contains(text(),"by")]/a[2]/@title')
            rated_score = extract_data(nd, './/span[contains(@id,"RatedScore")]/text()')
            if 'complaint' in rated_score.lower():rated_score = ''
            review_on = extract_data(nd, './/span[contains(@id,"Time")]/text()')
            post_date = ''
            if 'ago' not in review_on:
                post_date = dateparser.parse(review_on)
            product_score  = extract_data(nd, './/a[contains(@id,"ProductScore")]/text()')
            review_by = extract_data(nd, './/span[contains(@id,"User")]/@title')
            if not review_by: review_by = extract_data(nd, './/a[contains(@id,"User")]/@title')
            author_url = extract_data(nd, './/span[contains(@id,"User")]/@href')
            if not author_url: author_url = extract_data(nd, './/a[contains(@id,"User")]/@href')
            review_description = extract_data(nd, './/span[contains(@id,"Comments")]/text()')
            sk_ = md5(sk+post_ti+str(nd)+post_enterprise+rated_score+review_on+review_by+author_url+review_description)
            aux_info = {}
            aux_info.update({"browse":self.replacefun(browse)})
            if location: aux_info.update({"location":self.replacefun(location)})
            if rated_score: aux_info.update({"rated_score":self.replacefun(rated_score)})
            if review_on: aux_info.update({"review_on":self.replacefun(review_on)})
            if  product_score: aux_info.update({"product_score":self.replacefun(product_score)})
            if author_url:
                if 'http' not in author_url: author_url = "{}{}".format(self.domain, author_url)
            print author_url
            if author_url: aux_info.update({"author_url":self.replacefun(author_url)})
            if review_by: aux_info.update({"author_name":self.replacefun(review_by)})
            cus_rev = self.get_customer(sk_,title, review_by, post_date, review_description, response.url, aux_info)
            if cus_rev: yield cus_rev

        if response.meta.get('data',''):
            self.got_page(sk,1)

