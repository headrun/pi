from juicer.utils import *
from juicer.items import *
import dateparser

class Complaintsboardreviews(JuicerSpider):
    name = 'complaintsboard_review_terminal'
    def __init__(self, *args, **kwargs):
        super(Complaintsboardreviews, self).__init__(*args, **kwargs)
        self.domain = "https://www.complaintsboard.com"


    def replacefun(self, text):
        text = text.replace('"','<>#<>').replace("'","<>##<>").replace(',','###')
        return text

    def get_customer(self, sk, title, reviedw_by, date1, review_description, response_url, category, rev_rating, aux_info):
        customerReviews = CustomerReviews()
        customerReviews.update({"sk":normalize(sk), "name":normalize(title), "product_id":normalize(sk),"reviewed_by":normalize(reviedw_by),"reviewed_on":normalize(date1),"review":normalize(review_description),"review_url":normalize(response_url),"category":normalize(category),"review_rating":normalize(rev_rating)})
        if aux_info: customerReviews.update({"aux_info":normalize(json.dumps(aux_info, ensure_ascii=False, encoding="utf-8"))})
        return customerReviews

    def parse(self, response):
        sel = Selector(response)
        sk = response.meta['sk']
        if response.meta.get('data',''):
            browse = response.meta.get('data','').get('browse','')
        else: browse = response.meta['browse']
        title = extract_data(sel, '//td[@class="complaint"]/h1/text()')
        location = extract_data(sel, '//td[img[@title="Complaint country"]]/a//text()')
        no_of_comments = extract_data(sel, '//span[@itemprop="commentCount"]/text()')
        category = extract_data(sel, '//td[img[@title="Complaint category"]]/span/a//text()')
        review_description = extract_data(sel, '//div[@itemprop="reviewBody"]//text()')
        post_date = extract_data(sel, '//td[@class="small"]/span[@itemprop="dateCreated"]//text()')
        if post_date: post_date = str(dateparser.parse(post_date))
        author_name = extract_data(sel, '//div[@class="item-container"]//td[@class=small]//a[@itemprop="author"]/span[@itemprop="givenName"]//text()')
        review_rating = extract_data(sel, '//div[@class="item-container"]//div[@itemprop="reviewRating"]/span[@itemprop="ratingValue"]//text()')
        aggregate_rating_value = extract_data(sel, '//div[@class="item-container"]//div[@itemprop="aggregateRating"]/span[@itemprop="ratingValue"]//text()')
        if aggregate_rating_value: aggregate_rating_value = aggregate_rating_value.replace('%','').strip()
        aggregate_rating_count = extract_data(sel, '//div[@class="item-container"]//div[@itemprop="aggregateRating"]/span[@itemprop="ratingCount"]//text()')
        author_url = extract_data(sel,'//div[@class="item-container"]//td[@class="small"]//a[@itemprop="author"]/@href')
        post_text = extract_data(sel , '//div[@class="item-container"]//h1[@itemprop="about"]/text()')
        address = extract_data(sel, '//div[@class="item-container"]//div[@itemprop="contentLocation"]//text()[not(contains(.,"Contact information"))]',' ')
        sk_ = md5(sk+post_text+review_description+author_name+author_url+post_date+address+review_rating+category)
        aux_info = {}
        aux_info.update({"browse":self.replacefun(browse)})
        if location: aux_info.update({"location":self.replacefun(location)})
        if no_of_comments: aux_info.update({"no_comments":self.replacefun(no_of_comments)})
        if post_text: aux_info.update({"post_title":self.replacefun(post_text)})
        if aggregate_rating_value: aux_info.update({"aggregate_rating_value":aggregate_rating_value})
        if aggregate_rating_count: aux_info.update({"aggregate_rating_count":aggregate_rating_count})
        if address: aux_info.update({"address":self.replacefun(address)})
        if author_url:
            if 'http' not in author_url: author_url = "{}{}".format(self.domain, author_url)
            yield Request(author_url, callback=self.parse_next, meta={"sk":sk_, "title":title,"post_date":post_date,"review_description":review_description, "aux_info":aux_info,"response_url":response.url, 'category':category, "review_rating":review_rating}, dont_filter=True)

        else:
            if author_name: aux_info.update({"author_name":self.replacefun(author_name)})
            cus_rev = self.get_customer(sk_,title, author_name, post_date, review_description, response.url, category, review_rating, aux_info)
            if cus_rev: yield cus_rev
        comment_nodes = get_nodes(sel, '//div/table[@itemprop="comment"]')
        for cn in comment_nodes:
            comment_by = extract_data(cn, './/td[@class="comments"][not(@id)]//a[@itemprop="author"]/span[@itemprop="givenName"]/text()')
            comment_on = extract_data(cn, './/td[@class="comments"][not(@id)]//span[@itemprop="dateCreated"]/text()')
            if comment_on: comment_on = str(dateparser.parse(comment_on))
            commnt = extract_data(cn, './/td//div[@itemprop="text"]//text()')
            comment_votes = extract_data(cn, './/span[@class="small"][contains(text(),"Votes")]//text()')
            coment = Comments()
            sk_c = md5(sk_+commnt+comment_by+comment_on+comment_votes)
            coment.update({"sk":normalize(sk_c),"review_sk":normalize(sk_),"comment":normalize(commnt),"comment_by":normalize(comment_by),"comment_on":normalize(comment_on),"comment_votes":normalize(comment_votes)})
            yield coment



        if response.meta.get('data',''):
            self.got_page(sk,1)

    def parse_next(self, response):
        sel = Selector(response)
        sk_ = response.meta.get('sk','')
        title = response.meta.get('title','')
        aux_info = response.meta.get('aux_info','')
        post_date = response.meta.get('post_date','')
        review_rating = response.meta.get('review_rating','')
        category = response.meta.get('category','')
        response_url = response.meta.get('response_url','')
        review_description = response.meta.get('review_description','')
        author_name = extract_data(sel, '//div[@class="profile-head"]//h1//text()')
        reputation_points = extract_data(sel, '//div[@class="reputation"]/b/text()')
        author_location = extract_data(sel, '//div[@class="profile-cols"]//ul[@class="info"]/li[@class="location"]/text()')
        author_since_date = extract_data(sel,'//div[@class="profile-cols"]//ul[@class="info"]/li[@class="from"]/text()').replace('Member since','').strip()
        badges = get_nodes(sel,'//div[@class="badges"]/span')
        for i in badges:
            badge_name = extract_data(i,'./i/@class')
            badge_value = extract_data(i, './text()')
            if badge_value:
                aux_info.update({badge_name:badge_value})
        author_no_of_complaints = extract_data(sel,'//div[@class="right"][contains(text(),"Complaints")]/div/text()')
        author_no_of_comments = extract_data(sel,'//div[@class="right"][contains(text(),"Comments")]/div/text()')
        if author_no_of_complaints:
            aux_info.update({"author_no_of_complaints":author_no_of_complaints})
        if author_no_of_comments:
            aux_info.update({"author_no_of_comments":author_no_of_comments})
        if author_since_date: author_since_date = str(dateparser.parse(author_since_date))
        if author_since_date: aux_info.update({"author_since_date":author_since_date})
        if author_location: aux_info.update({"author_location":self.replacefun(author_location)})
        if reputation_points: aux_info.update({"author_reputation_points":self.replacefun(reputation_points)})
        if author_name: aux_info.update({"author_name":self.replacefun(author_name)})
        aux_info.update({"author_url":self.replacefun(response.url)})
        cus_rev = self.get_customer(sk_,title, author_name, post_date, review_description, response_url,category, review_rating,  aux_info)
        if cus_rev: yield cus_rev


