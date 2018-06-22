from juicer.utils import *
from scrapy.http import FormRequest

class TripAvisorTerminal(JuicerSpider):
	name = 'tripadvisor_search_terminal'
	start_urls = ['https://www.tripadvisor.in/Restaurant_Review-g293924-d12593669-Reviews-Duong_s_2_Restaurant_Cooking_Class-Hanoi.html']
	handle_httpstatus_list = [302,301]

	def __init__(self, *args, **kwargs):
	    super(TripAvisorTerminal, self).__init__(*args, **kwargs)
	    self.insert_query1 = "INSERT INTO tripadvisor_meta(sk,title,no_of_reviews,address,contact_number,image,reference_url,created_at,modified_at,last_seen) values(%s,%s,%s,%s,%s,%s,%s,now(),now(),now()) on duplicate key update modified_at = now(), title=%s, no_of_reviews=%s, address=%s, contact_number=%s, image=%s"
	    self.insert_query2 = "INSERT INTO tripadvisor_review(sk,program_sk,review_id,review_title,reviewed_on, reviewed_with,description,user_thank,user_likes,reviewed_by, location, contributor, votes, review_rating, image, excellent, very_good, average, poor, terrible, reference_url, created_at,modified_at,last_seen) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),now(),now()) on duplicate key update modified_at = now()"

            self.conn = MySQLdb.connect(db='Trip_Advisor',user='root',passwd='root',
                                charset="utf8",host='localhost',use_unicode=True)
            self.cur = self.conn.cursor()

	def parse(self, response):
	    sel = Selector(response)
	    sk = "-".join(response.url.split('-')[1:3])
	    title = normalize(''.join(sel.xpath('//h1[@class="heading_title"]/text()').extract()))
	    if not title:
		title = normalize(''.join(sel.xpath('//h1[@id="HEADING"]/text()').extract()))
	    no_of_reviews = normalize(''.join(sel.xpath('//div[@class="rs rating"]/a/span/text()').extract())) 
	    if not no_of_reviews:
		no_of_reviews = normalize(''.join(sel.xpath('//div[@class="ratingContainer"]/a/span/text()').extract()))
	    no_of_reviews = normalize(''.join(re.findall('(\d+) of ', no_of_reviews)))
	    streetadress = normalize(''.join(sel.xpath('//div[@class="blRow"]/div//span[@class="street-address"]/text()').extract()))
	    extend_ad = normalize(''.join(sel.xpath('//div[@class="blRow"]/div//span[@class="extended-address"]/text()').extract()))
	    locality= normalize(''.join(sel.xpath('//div[@class="blRow"]/div//span[@class="locality"]/text()').extract()))
	    coun = normalize(''.join(sel.xpath('//div[@class="blRow"]/div//span[@class="country-name"]/text()').extract()))
	    tes = normalize(''.join(sel.xpath('//div[@class="blRow"]/div/text()').extract())).strip(',').strip(' ')
	    full_address = streetadress+extend_ad+locality+coun+tes
	    full_address1 = full_address.strip('|')
	    contact_no = normalize(''.join(sel.xpath('//div[@class="blEntry phone"]//span/text()').extract()))
	    images = normalize('<>'.join(sel.xpath('//div[@class="prw_rup prw_common_location_photos photos"]//img//@src').extract()))
	    if not images:
		images = normalize('<>'.join(sel.xpath('//div[@class="carousel_images"]//img//@data-lazyurl').extract()))
	    if not images:
		images = normalize('<>'.join(sel.xpath('//div[@class="carousel_images"]//img//@data-src').extract()))
	    images = images.replace('https://static.tacdn.com/img2/x.gif', '').replace('<><>', '<>').strip('<>')
	    values1 =(normalize(sk),title,no_of_reviews,full_address1,contact_no,images,normalize(response.url), title,no_of_reviews,full_address1,contact_no,images)
	    self.cur.execute(self.insert_query1 , values1)
            headers = {
            'Origin': 'https://www.tripadvisor.in',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.8,fil;q=0.6',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'text/html, */*',
            'Cache-Control': 'no-cache',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
        	}
            data = [
            ('returnTo', '#REVIEWS'),
            ('filterLang', 'ALL'),
            ('filterSeasons', ''),
            ('filterSegment', ''),
            ('filterRating', ''),
            ('reqNum', '1'),
            ('changeSet', 'REVIEW_LIST'),
            	]
            yield FormRequest(response.url, callback=self.details, formdata = data, headers=headers,meta={"sk":sk})

	def details(self,response):
	    sel = Selector(response)
	    sk = response.meta['sk']
	    rating_num = sel.xpath('//div[@id="ratingFilter"]/ul/li[@class="filterItem"]/label//span/text()').extract()
	    urls1 = sel.xpath('//div[@class="quote"]/a/@href').extract()  
	    urls2 = sel.xpath('//div[@class="quote isNew"]//a//@href').extract()
	    urls1.extend(urls2)
	    for url in urls1:
		url1 = 'https://www.tripadvisor.in'+(''.join(url))
	        yield Request(normalize(url1), callback=self.parse_next, meta={"sk":sk})
	    offset = normalize(''.join(response.xpath('//div[@class="unified ui_pagination north_star "]/a[@class="nav next taLnk ui_button primary"]/@data-offset').extract()[:1]))
	    if offset:
            	    links = response.url.split('-Reviews-')
		    links1 = ''.join(links[0])+'-Reviews-'+'or'+offset+'-'+''.join(links[1])
		    extra = "-".join(links1.split('-or')[-1].split('-')[1:])
		    main_link = ''.join(links[0])+'-Reviews-'+'or'+offset+'-'+extra
		    yield Request(normalize(main_link), callback=self.details, meta={'sk':sk}, dont_filter=True)
	
	def parse_next(self, response):
	    sel = Selector(response)
	    sk = response.meta['sk']
	    try:	
	    	review_id = normalize(''.join(sel.xpath('//div[contains(@class, "prw_rup prw_reviews")]/div/@data-reviewid').extract()[0]))
	    except:
	    	review_id = normalize(''.join(sel.xpath('//div[@class="prw_rup prw_reviews_basic_review_responsive"]/div/@data-reviewid').extract()[0])) 
	    rating_num = sel.xpath('//div[@id="ratingFilter"]/ul/li[@class="filterItem"]/label//span/text()').extract()
            if rating_num:
            	excellent = rating_num[0]
           	very_good = rating_num[1]
            	average = rating_num[2]
            	poor = rating_num[3]
            	terrible = rating_num[4]
	    else:
		excellent = normalize(''.join(sel.xpath('//div[@data-tracker="Excellent"]//span/text()').extract()[0]))
		very_good = normalize(''.join(sel.xpath('//div[@data-tracker="Very good"]//span/text()').extract()[0]))
		average = normalize(''.join(sel.xpath('//div[@data-tracker="Average"]//span/text()').extract()[0]))
		poor = normalize(''.join(sel.xpath('//div[@data-tracker="Poor"]//span/text()').extract()[0]))
		terrible = normalize(''.join(sel.xpath('//div[@data-tracker="Terrible"]//span/text()').extract()[0]))
	    r_rating = normalize(''.join(sel.xpath('//div[@class="rating"]/span/span/@alt').extract()))
	    if r_rating: r_rat = normalize(''.join(re.findall('(\d+) of ', r_rating)))
	    else: r_rat = ''
	    if review_id:
		url = "https://www.tripadvisor.in/OverlayWidgetAjax?Mode=EXPANDED_HOTEL_REVIEWS&metaReferer=ShowUserReviewsRestaurants&contextChoice=SUR&reviews=%s" %review_id
		if url:
		    yield Request(url, callback=self.parse_meta, meta={'sk':sk,'r_rat':r_rat,'r_id':review_id,
					'excellent':excellent,'very_good':very_good,'average':average,'poor':poor,'terrible':terrible,'ref_url':normalize(response.url)})

	def parse_meta(self, response):
	    sel = Selector(response)
	    sk = response.meta['sk']
	    r_rat = response.meta['r_rat']
	    r_id = response.meta['r_id']
	    excellent = response.meta['excellent']
	    very_good = response.meta['very_good']
	    average = response.meta['average']
	    poor = response.meta['poor']
	    terrible = response.meta['terrible']
	    ref_url = response.meta['ref_url']
	    image = normalize(''.join(sel.xpath('//div[@class="ui_avatar large"]/img/@src').extract()))
	    contributor = normalize(''.join(sel.xpath('//div[@class="memberBadgingNoText"]/span[@class="ui_icon pencil-paper"]/following-sibling::span[1]//text()').extract()))
	    votes = normalize(''.join(sel.xpath('//div[@class="memberBadgingNoText"]/span[@class="ui_icon thumbs-up-fill"]/following-sibling::span[1]//text()').extract()))
	    reviewed_by = normalize(''.join(sel.xpath('//div[@class="username mo"]/span/text()').extract()))
	    location = normalize(''.join(sel.xpath('//div[@class="location"]/span/text()').extract()))
	    reviewed_on = normalize(''.join(sel.xpath('//div[@class="rating reviewItemInline"]/span/@title').extract()))
	    review_title = normalize(''.join(sel.xpath('//div[@class="quote"]/a/span/text()').extract()))
	    if not review_title:
		review_title = normalize(''.join(sel.xpath('//div[@class="quote isNew"]/a/span/text()').extract()))
	    review_sk = md5(review_title+normalize(response.url))
	    description = normalize(''.join(sel.xpath('//div[@class="prw_rup prw_reviews_text_summary_hsx"]/div/p//text()').extract()))
	    thank_user = normalize(''.join(sel.xpath('//span[@class="helpful_text"]/span[@class="thankUser"]/text()').extract()))
	    thank_likes = normalize(''.join(sel.xpath('//span[@class="helpful_text"]/span[@class="numHelp emphasizeWithColor"]/text()').extract()))
	    reviewed_with = normalize(''.join(sel.xpath('//div[@class="rating reviewItemInline"]//a/text()').extract())).strip('via').strip(' ')
	    values2 = (normalize(review_sk),normalize(sk),normalize(r_id),review_title,reviewed_on,reviewed_with,description,thank_user,thank_likes,\
			reviewed_by,location,contributor,votes,r_rat,image,normalize(excellent),normalize(very_good),\
			normalize(average),normalize(poor),normalize(terrible),normalize(ref_url))
	    self.cur.execute(self.insert_query2 , values2)
	    self.got_page(sk, '1')
