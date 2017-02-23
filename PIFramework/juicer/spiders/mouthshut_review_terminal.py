from juicer.utils import *
import requests
from juicer.items import *
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
             query_data = extract_list_data(node, './div[@class="row"]/div/script/text()')
             post_title = extract_data(node, './/strong/a/text()')
             post_text = extract_data(node, './/div[@class="more reviewdata"]/text()')
             post_t1 = textify(node.xpath('.//div[@class="more reviewdata"]/a/@onclick').extract())
             rating = len(extract_list_data(node, './/p[@class="rating"]/span/i[@class="icon-rating rated-star"]/@class'))
             if post_t1:
                reviewid, unknown, unknown1, fbmessage, catid, prodimg, twittermsg, twitterlink, catname, rating_str = ['']*10
                try:
                    li_params =  [i.replace("'",'') for i in re.findall('\((.*?)\)',post_t1)[0].split(',')]
                    reviewid, unknown, unknown1, fbmessage, catid, prodimg, twittermsg, twitterlink, catname, rating_str = li_params
                except: li_params =  ''
                headers1 = {
                'Origin': 'http://www.mouthshut.com',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en-US,en;q=0.8',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'text/plain, */*; q=0.01',
                'Referer': response.url,
                'X-Requested-With': 'XMLHttpRequest',
                'Connection': 'keep-alive',
                }
                data_form = {"type":"review","corp":"false","isvideo":"false","reviewid":reviewid,"fbmessage":fbmessage, "catid":catid, "prodimg":prodimg, "twittermsg":twittermsg, "twitterlink":twitterlink, "catname":catname, "rating_str":rating_str, "usession":0}
                post_text = self.get_parse_post(data_form, headers1)

             for q_data in query_data:
                 query_values = re.findall('(\d+),', q_data)
                 rev_id, user_id, post_s, tcount, is_del, review = query_values
                 user_url = self.profile_url%(rev_id, user_id, post_s, tcount, is_del, review)
                 yield Request(user_url, callback=self.parse_next, meta={'title':title,'post_title':post_title, 'post_text':post_text, "rating":rating, "ref_url":response.url, "sk":sk,"browse":browse})
        if not response.meta.get('next',''):
            self.got_page(sk,1)
        next_page = extract_list_data(sel, '//li[@class="next"]/a/@href')
        if next_page:
            yield Request(next_page, callback=self.parse, meta={'sk':sk, 'next':'yes'})

    def get_parse_post(self, data, headers1):
        tex = requests.post('http://www.mouthshut.com/review/CorporateResponse.ashx', headers=headers1, data=data).text
        data_temp = Selector(text=tex)
        return extract_data(data_temp, '//p/text()',' ')

    def parse_next(self, response):
        sel = Selector(response)
        sk = response.meta.get('sk','')
        title = response.meta.get('title', '')
        author_url = extract_data(sel,'//a[@style="background:none;"]/@href')
        reviewd_by = extract_data(sel, '//body/p/a/text()[not(contains(., "Review"))][not(contains(., "Followers"))]')
        #sel.xpath('//p/a[contains(@href,"%s")][not(@style="background:none;")][not(contains(@href,"reviews"))]/text()'%authour_url).extract()
        location = extract_data(sel,'//p[not(@*)]/text()')
        no_of_reviews = extract_data(sel, '//body/p/a/text()[contains(., "Reviews")]')
        followers = extract_data(sel, '//text()[contains(., "Followers")]')
        text = extract_data(sel, '//text()[contains(., "Comments")]')
        date1 = ''
        if text:
            views = ''.join(re.findall(r'(\d+) Views', text))
            likes = ''.join(re.findall('\^(\d+)$', text))
            time_stamp = ''.join(re.findall('Views\^(.*)\^Comments', text))
            if time_stamp:
                try: date1 = str(parse_date(time_stamp))
                except: date1 = ''
            no_comments = ''.join(re.findall(r'Comments \((\d+)', text))

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
        if response.meta.get('post_title',''): aux_info.update({"post_title": response.meta.get('post_title','')})
        customerReviews = CustomerReviews()
        customerReviews.update({"sk":normalize(sk_), "product_id":normalize(response.meta['sk']),"name":normalize(title), "reviewed_by": normalize(reviewd_by), "reviewed_on":normalize(date1), "review": normalize(response.meta.get('post_text','')), "review_url":normalize(response.meta['ref_url']),"review_rating":normalize(str(response.meta.get('rating',''))),"aux_info":json.dumps(aux_info, ensure_ascii=False, encoding="utf-8")})
        yield customerReviews

