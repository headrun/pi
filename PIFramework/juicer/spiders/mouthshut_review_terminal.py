from juicer.utils import *
import requests
from juicer.items import *
from scrapy.http.cookies import CookieJar

class Mouthshutreviewterminal(JuicerSpider):
    name = 'mouthshut_review_terminal'

    def __init__(self, *args, **kwargs):
        super(Mouthshutreviewterminal, self).__init__(*args, **kwargs)
        self.profile_url = "http://www.mouthshut.com/review/CorporateResponse.ashx?type=GetProfileData&rev_id=%s&user_id=%s&post_s=%s&tcount=%s&is_del=%s&img=.jpg&review=%s&corp=false"

    def parse(self, response):
        sel = Selector(response)
        if response.meta.get('next',''):
            sk = response.meta.get('sk','')
            browse = response.meta.get('browse','')
        else:
            sk = response.meta['sk']
            browse = response.meta.get('data','').get('browse','')
        title = extract_data(sel, '//h1[@id="prodTitle1"]/a/text()')
        nodes = get_nodes(sel, '//div[@id="dvreview-listing"]/div[@class="row review-article"]')
        for node in nodes:
            post_url = extract_data(node, './/div[contains(@id, "reviewdetails")]//strong/a/@href')
            post_text = extract_data(node, './/div[@class="more reviewdata"]/text()')
            post_title = extract_data(node, './/strong/a/text()')
            comment_t = extract_data(node, './/div[@class="comment-clk"]//span[@id]/text()')
            query_data = extract_data(node, './div[@class="row"]/div/script/text()')
            likes = self.parse_query(query_data)
            comment = ''
            if comment_t:
                comment = textify(re.findall('\((.*?)\)',comment_t))
            yield Request(post_url, callback=self.parse_next, meta={'title':title,"ref_url":response.url, "sk":sk,"browse":browse, "post_text": post_text,"comment":comment, "likes":likes,"post_title":post_title})

        if not response.meta.get('next',''):
            self.got_page(sk,1)
        next_page = extract_list_data(sel, '//li[@class="next"]/a/@href')
        if next_page:
            yield Request(next_page, callback=self.parse, meta={'sk':sk, 'next':'yes'})

    def parse_query(self, q_data):
        likes = ''
        query_values = re.findall('(\d+),', q_data)
        rev_id, user_id, post_s, tcount, is_del, review = query_values
        user_url = self.profile_url%(rev_id, user_id, post_s, tcount, is_del, review)
        data= requests.get(user_url).text
        sel = Selector(text=data)
        text = extract_data(sel, '//text()[contains(., "Comment")]')
        if text:  likes = ''.join(re.findall('\^(\d+)$', text))
        return likes

    def parse_useful(self, use, urls):
        data= requests.get(use).text
        sel = Selector(text=data)
        session = requests.Session()
        res = session.get(use)
        cook = session.cookies.get_dict()
        cook.update({"G_ENABLED_IDPS":"google"})
        cooki = {'ASP.NET_SessionId': 'hnioleeeqtppby14shrasmev', 'G_ENABLED_IDPS': 'google'}
        headerp = {
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36',
        'Accept': '*/*',
        'Referer': urls,
        'Connection': 'keep-alive',
        }
        data=  requests.get(use, headers=headerp, cookies=cooki).text
        sel = Selector(text=data)
        dict1 = {}
        nodes = sel.xpath('//div[@id="pnlGraph"]//div[@class="col-4"]/p[not(@*)]')
        for nd in nodes:
            spu = extract_data(nd,'./span[1]/text()')
            spi = extract_data(nd,'./span[2]/text()')
            spi = textify(re.findall('\((.*?)\)',spi))
            dict1.update({spu:spi})
        return json.dumps(dict1)



    def parse_next(self, response):
        sel = Selector(response)
        sk = response.meta.get('sk','')
        title = response.meta.get('title', '')
        author_url = extract_data(sel,'//div[@id="firstReview"]//div[@class="profile-img"]/a/@href')
        time_stamp = extract_data(sel, '//div[@id="firstReview"]//div[@class="small-text rating"]/small[not(@*)]/text()')
        icon_fake = extract_data(sel,'//div[@id="firstReview"]//span[@class="icon-fake"]')
        post_text = extract_data(sel, '//div[@id="firstReview"]//div[@class="row summary"]/following-sibling::p[not(@*)]/text()')
        icon_fake1 = '0'
        if icon_fake: icon_fake1 = '1'
        date1 = ''
        if time_stamp:
            try: date1 = str(parse_date(time_stamp))
            except: pass
        reviewd_by = extract_data(sel, '//div[@id="firstReview"]//label[contains(@id, "linkrevname")]//text()')
        location = extract_data(sel,'//div[@id="firstReview"]//p[contains(@id, "city")]/text()')
        no_of_reviews = extract_data(sel, '//div[@id="firstReview"]//p/a[contains(@href, "/review")]/text()')
        followers = extract_data(sel, '//div[@id="firstReview"]//p/a[contains(@id, "linkTrust")]/text()')
        var_rid = extract_data(sel, '//script[contains(.,"var Rid")]')
        var_rid = textify(re.findall('var Rid = "(.*?)"', var_rid))
        urk_use = "http://www.mouthshut.com/review/reviewratingrestaurant.aspx?OverallGraph=%s"%var_rid
        useful = self.parse_useful(urk_use, response.url)
        no_comments = response.meta.get('comment','')
        likes = response.meta.get('likes','')
        rating = len(extract_list_data(sel, '//div[@id="firstReview"]//span[contains(@span,"litMemRating")]/span/i[@class="icon-rating rated-star"]/@class'))
        views = extract_data(sel, '//div[@id="firstReview"]//span[@class="views"]//text()')
        sk_ = md5(response.meta['ref_url']+response.meta['post_title']+reviewd_by+no_of_reviews)
        aux_info = {}
        if followers: aux_info.update({"followers":followers})
        if author_url: aux_info.update({"author_url":author_url})
        if location: aux_info.update({"location":location})
        if views: aux_info.update({"views":views})
        if likes: aux_info.update({"likes":likes})
        aux_info.update({"browse":response.meta['browse']})
        if no_comments:  aux_info.update({"no_comments:":no_comments})
        if no_of_reviews: aux_info.update({"no_of_reviews":no_of_reviews})
        aux_info.update({"fake":icon_fake1})
        if response.meta.get('post_title',''): aux_info.update({"post_title": response.meta.get('post_title','')})
        if useful:  aux_info.update({"useful":useful})
        customerReviews = CustomerReviews()
        customerReviews.update({"sk":normalize(sk_), "product_id":normalize(response.meta['sk']),"name":normalize(title), "reviewed_by": normalize(reviewd_by), "reviewed_on":normalize(date1), "review": normalize(post_text), "review_url":normalize(response.meta['ref_url']),"review_rating":normalize(str(rating)),"aux_info":json.dumps(aux_info, ensure_ascii=False, encoding="utf-8")})
        yield customerReviews

