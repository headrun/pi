from juicer.utils import *
from juicer.items import *
import dateparser

class Consumercourtreviews(JuicerSpider):
    name = 'consumercourt_review_terminal'

    def __init__(self, *args, **kwargs):
        super(Consumercourtreviews, self).__init__(*args, **kwargs)
        self.domain = "https://www.consumercourt.in/"

    def parse(self, response):
        sel = Selector(response)
        bro_meta = {}
        if response.meta.get('data',''):
            bro_meta = response.meta.get('data','')
        else: bro_meta = response.meta
        sk = response.meta.get('sk','')
        browse = bro_meta.get('browse','')
        last_post_author_name = bro_meta.get('last_post_author_name','')
        last_post_author_url = bro_meta.get('last_post_author_url','')
        forum_url = bro_meta.get('forum_url','')
        forum_views = bro_meta.get('forum_views','')
        forum_title = bro_meta.get('forum_title','')
        forum_text = bro_meta.get('forum_text','')
        forum_replies = bro_meta.get('forum_replies','')
        last_post_date = bro_meta.get('last_post_date','')
        nodes = get_nodes(sel, "//ol[@id='posts']/li[contains(@class,'postbit')]")
        for nd in nodes:
            post_date = extract_data(nd, './/span[@class="date"]//text()')
            if post_date: post_date = str(dateparser.parse(post_date))
            author_name = extract_data(nd, './/div[@class="username_container"]//a[contains(@class,"username")]//text()')
            if not author_name: author_name = extract_data(nd, './/div[@class="username_container"]/span[@class="username guest"]/text()')
            author_url = extract_data(nd, './/div[@class="username_container"]//a[contains(@class,"username")]//@href')
            author_title = extract_data(nd, './/span[@class="usertitle"]//text()')
            post_title = extract_data(nd, './/h2[contains(@class,"posttitle")]/text()').replace(u'\xc2\xa0','').replace(u'\xa0','').replace(u'\xf0\x9f\x92\x99','').replace(u'\U0001f499','').replace(u'\U0001f917','').replace(u'\U0001f44d','').replace(u'\U0001f4f6','')
            post_text = extract_data(nd, './/blockquote[contains(@class,"postcontent")]//text()',' ')
            reputation_image = extract_data(nd, './/span[@class="postbit_reputation"]/img[@class="repimg"]/@src')
            if reputation_image:
                if 'http' not in reputation_image: reputation_image = "{}{}".format(self.domain, reputation_image)
            aux_info = {}
            aux_info.update({"browse":browse})
            if last_post_author_name: aux_info.update({"last_post_author_name":last_post_author_name})
            if last_post_author_url: aux_info.update({"last_post_author_url":last_post_author_url})
            if forum_url: aux_info.update({"forum_url":forum_url})
            if forum_views: aux_info.update({"forum_views":forum_views})
            if forum_title: aux_info.update({"forum_title":forum_title})
            if forum_text: aux_info.update({"forum_name":forum_text})
            if forum_replies: aux_info.update({"forum_replies":forum_replies})
            if author_title: aux_info.update({"author_title":author_title})
            if reputation_image: aux_info.update({"user_reputation_image":reputation_image})
            if author_url: aux_info.update({"author_profile":author_url})
            if last_post_date: aux_info.update({"last_post_date":last_post_date})
            sk_ = md5(forum_title+sk+forum_text+response.url+author_title+author_name+post_title+reputation_image+post_date+post_text)
            customerReviews = CustomerReviews()
            customerReviews.update({"sk":normalize(sk_),"product_id":normalize(sk_), "name":normalize(post_title), "reviewed_by":normalize(author_name),"reviewed_on":normalize(post_date),"review":normalize(post_text),"review_url":normalize(response.url)})
            if aux_info: customerReviews.update({"aux_info":normalize(json.dumps(aux_info, ensure_ascii=False, encoding="utf-8"))})
            yield customerReviews
        if response.meta.get('data',''):
            self.got_page(sk,1)
        next_page = extract_data(sel,'//div[@id="pagination_top"]//span//a[@rel="next"]/@href')
        if next_page:
            if 'http' not in next_page: next_page = "{}{}".format(self.domain, next_page.encode('utf8'))
            if next_page:
                yield Request(next_page, callback=self.parse, meta={"browse":browse,"sk":sk,"last_post_author_name":last_post_author_name,"last_post_author_url":last_post_author_url,"forum_url":forum_url,"forum_views":forum_views,"forum_title":forum_title,"forum_text":forum_text,"forum_replies":forum_replies,"last_post_date":last_post_date})


