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
            browse = response.meta.get('data',{}).get('browse','')
        title = extract_data(sel, '//h1[@id="prodTitle1"]/a/text()')
        nodes = get_nodes(sel, '//div[@id="dvreview-listing"]/div[@class="row review-article"]')
        for node in nodes:
	    
            post_url = extract_data(node, './/div[contains(@id, "reviewdetails")]//strong/a/@href')
            post_text = extract_data(node, './/div[@class="more reviewdata"]/text()')
            post_title = extract_data(node, './/strong/a/text()')
            comment_t = extract_data(node, './/div[@class="comment-clk"]//span[@id]/text()')
            query_data = extract_data(node, './div[@class="row"]/div/script/text()')
            u_likes = self.parse_query(query_data)
	    r_id = extract_data(node, './/div[@class="rar-rate"]/a/@reviewid')
	    u_id = extract_data(node, './/div[@class="rar-rate"]/a/@userid')
	    _id = extract_data(node, './/div[@class="rar-rate"]/a/@id')
	    rat_id = response.url.split('-')[-1]
	    cat_nam = title.replace(' ','+')
	    res_id = extract_data(node, './/div[@class="rar-rate"]/a/@divCorpid')
	    likes_link = 'https://www.mouthshut.com/review/CorporateResponse.ashx?type=like&OverallGraph=%s&u=%s&Random=0.8851791636685369&arateid=%s&corp=false&Session=0&corpname=&catid=%s&catname=%s&sessionname=Guest&divcorprespid=%s'%(r_id, u_id, _id, rat_id, cat_nam, res_id)
	    dat = requests.get(likes_link).text
	    dt = Selector(text=dat)
	    txt = extract_data(dt, '//text()')
	    review_likes  = ''.join(re.findall('\((\d+)\)', txt))
            comment = ''
            if comment_t:
                comment = textify(re.findall('\((.*?)\)',comment_t))
            yield Request(post_url, callback=self.parse_next, meta={'title':title,"ref_url":response.url, "sk":sk,"browse":browse, "post_text": post_text,"comment":comment, "user_likes":u_likes,"post_title":post_title, 'review_likes':review_likes})

        if not response.meta.get('next',''):
            self.got_page(sk,1)
        next_page = extract_list_data(sel, '//li[@class="next"]/a/@href')
        if next_page:
            yield Request(next_page, callback=self.parse, meta={'sk':sk, 'next':'yes', "browse":browse})

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
	cooki = {'G_ENABLED_IDPS': 'google','ASP.NET_SessionId': 'odl2l14c3wam2wjdcxririhz'}
	headerp = {
    	'Connection': 'keep-alive',
    	'Cache-Control': 'max-age=0',
    	'Upgrade-Insecure-Requests': '1',
    	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    	'Accept-Encoding': 'gzip, deflate, br',
    	'Accept-Language': 'en-US,en;q=0.9',
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
        u_likes = response.meta.get('user_likes','')
	review_likes = response.meta.get('review_likes', '')
        rating = len(extract_list_data(sel, '//i[@class="icon-rating rated-star"]/@class'))
        views = extract_data(sel, '//div[@id="firstReview"]//span[@class="views"]//text()')
        sk_ = md5(response.meta['ref_url']+response.meta['post_title']+reviewd_by+no_of_reviews)
        aux_info = {}
        if followers: aux_info.update({"followers":followers})
        if author_url: aux_info.update({"author_url":author_url})
        if location: aux_info.update({"location":location})
        if views: aux_info.update({"views":views.replace('views', '')})
        if u_likes: aux_info.update({"user_likes":u_likes})
        aux_info.update({"browse":response.meta['browse']})
        if no_comments:  aux_info.update({"no_comments":no_comments})
	if review_likes: aux_info.update({"review_likes":review_likes})
        if no_of_reviews: aux_info.update({"no_of_reviews":no_of_reviews.replace('Reviews', '').replace('Review', '')})
        aux_info.update({"fake":icon_fake1})
        if response.meta.get('post_title',''): aux_info.update({"post_title": normalize(response.meta.get('post_title','')).replace('"', '')})
        if useful:  aux_info.update({"useful":json.loads(useful)})
        customerReviews = CustomerReviews()
        customerReviews.update({"sk":normalize(sk_), "product_id":normalize(response.meta['sk']),"name":normalize(title), "reviewed_by": normalize(reviewd_by), "reviewed_on":normalize(date1), "review": normalize(post_text), "review_url":normalize(response.meta['ref_url']),"review_rating":normalize(str(rating)),"aux_info":json.dumps(aux_info)})
        yield customerReviews

