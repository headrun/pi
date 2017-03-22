import requests

from juicer.utils import *

from juicer.items import *
""" starting amazon terminal"""


class AmazonBestsellersterminal(JuicerSpider):
    name = "amazon_bestsellers_terminal"
    handle_httpstatus_list = [404, 302, 303, 403, 500, 999,503]

    def __init__(self, *args, **kwargs):
        super(AmazonBestsellersterminal, self).__init__(*args, **kwargs)
        self.URL = "http://www.amazon.in"
        self.prod_detxpath = '//td[h2[contains(text(),"Product details")]]//li[b[contains(text(),"%s")]]/text()'
        self.pattern_int = re.compile(r'\d+')
        self.headers = {
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36',
        'Accept': 'text/html,*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        }

    def name_clean(self, text):
        text = re.sub('\((.*?)\)','',text)
        text = text.replace('#','').replace('(','').replace(')','').replace(u'\xc2\xa0','').replace(u'\xa0','').replace(u'\xf0\x9f\x92\x99','').replace(u'\U0001f499','').replace(u'\U0001f917','').replace(u'\U0001f44d','').replace('  <>','<>').replace(' <>','<>').strip().strip('<>').strip()
        return text

    def parse(self, response):
        sel = Selector(response)
        if self.headers.get('Referer',''):
            del self.headers['Referer']
        self.headers.update({"Referer":response.url})
        title = response.meta.get('data','').get('product_title','')
        category = response.meta.get('data','').get('category','')
        if not title: title = extract_data(sel,'//span[@id="productTitle"]/text()')
        sk = response.meta.get('sk','')
        features = normalize(extract_data(sel,'//div[@id="feature-bullets"]/ul/li//text()',', '))
        description = normalize(extract_data(sel,'//div[@id="productDescription"]/p//text()'))
        item_part_number = normalize(extract_data(sel,self.prod_detxpath%'Item part number'))
        product_dime = normalize(extract_data(sel,self.prod_detxpath%'Product Dimensions'))
        if not item_part_number: item_part_number = normalize(extract_data(sel,self.prod_detxpath%'Item model number'))
        if not item_part_number: item_part_number = extract_data(sel, '//td[h2[contains(text(),"Product details")]]//li[b[contains(text(),"item")][contains(text(),"number")]]/text()')
        date_first_avail = normalize(extract_data(sel,self.prod_detxpath%'Date first available at Amazon'))
        if not date_first_avail: date_first_avail = extract_data(sel,'//tr[@class="date-first-available"]/td[@class="value"]/text()')
        asin_number = normalize(extract_data(sel,self.prod_detxpath%'ASIN'))
        if not asin_number: asin_number = normalize(extract_data(sel, '//input[@id="ASIN"]/@value'))
        if not asin_number: asin_number = normalize(extract_data(sel,"//tr[td[@class='label'][contains(text(),'ASIN')]]/td[@class='value']/text()"))
        if not asin_number:
            try: asin_number =  json.loads(sel.xpath('//span[@class="a-declarative"][@data-action="a-modal"]/@data-a-modal').extract()[0]).get('asin','')
            except: pass
        seller_mrank = self.name_clean(extract_data(sel,self.prod_detxpath%'Amazon Bestsellers Rank'))
        seller_rank = self.name_clean(extract_data(sel, '//li[@class="zg_hrsr_item"]//text()',' '))
        seller_rk = ''
        if seller_mrank or seller_rank:
            seller_rk = normalize(self.name_clean("%s%s%s"%(seller_mrank,'<>',seller_rank)))
        if not seller_rk: seller_rk = extract_data(sel, '//tr[@id="SalesRank"]/td[@class="value"]//text()', ' ').replace('\n','').replace('  ',' ').replace(u'\xa0','').replace('#','<>')
        if date_first_avail:
            date_first_avail = str(parse_date(date_first_avail))
        customer_reviews = extract_list_data(sel, '//td[h2[contains(text(),"Product details")]]//a[contains(text(), "customer reviews")]/@href')
        if not customer_reviews:
            customer_reviews = extract_list_data(sel,'//tr[@class="average_customer_reviews"]//a[contains(text(), "customer reviews")]/@href')
        if not customer_reviews:
            customer_reviews = extract_list_data(sel, '//a[id="acrCustomerReviewLink"]/@href')
        if customer_reviews: customer_reviews[0]
        produ_aux = {}
        original_price = extract_data(sel,'//div[@id="price"]//span[@class="a-text-strike"]/text()').strip()
        if not original_price: original_price = extract_data(sel, '//div[@id="price"]//span[@id="priceblock_ourprice"]/text()').strip()
        discount_price = extract_data(sel, '//div[@id="price"]//span[@id="priceblock_saleprice"]/text()').strip()
        if product_dime: produ_aux.update({"product_dimensions":product_dime})
        extra_technical_info = get_nodes(sel, '//div[contains(@class,"techD")][div[span[contains(text(),"Technical Details")]]]/div[contains(@class,"content")]//table//tr[td[@class="label"]]')
        for tech in extra_technical_info:
            tech_key = extract_data(tech, './td[@class="label"]/text()')
            tech_value = extract_data(tech, './td[@class="value"]/text()')
            if tech_key and tech_value:
                produ_aux.update({tech_key:tech_value})
        products_item = Products()
        products_item.update({"id":normalize(sk),"name":normalize(title),"original_price":normalize(original_price),"discount_price":normalize(discount_price),"features":normalize(features),"description":normalize(description),"item_number":normalize(item_part_number),"date_available":normalize(date_first_avail),"best_sellerrank":normalize(seller_rk),"reference_url":normalize(response.url)})
        if produ_aux:
            products_item.update({"aux_info":normalize(json.dumps(produ_aux, ensure_ascii=False, encoding="utf-8"))})
        yield products_item
        if customer_reviews: yield Request(customer_reviews, callback=self.parse_reviews, meta= {"sk":sk, "title":title, 'category':category})
        script_images = extract_data(sel,'//script[@type="text/javascript"]/text()[contains(.,"colorImages\': { \'initial\'")]')
        if script_images:
            images_final = re.findall('"hiRes":"(.*?)"', script_images)
            if not images_final: images_final = sel.xpath('//div[@class="imgTagWrapper"]/img/@src').extract()
            for img in images_final:
                get_rich_meida = self.parse_richmedia(img, sk, response.url, title, category)
                if get_rich_meida: yield get_rich_meida
        seller_main_av = extract_data(sel,'//div[@id="availability"]/span/text()')
        seller_main_name = extract_data(sel, '//div[@id="merchant-info"]/a[contains(@href,"merchant")]/text()')
        seller_main_ratings = extract_data(sel, '//div[@id="merchant-info"]//text()[contains(.,"ratings")]')
        seller_main_rat, star_seller_m = '', ''
        if seller_main_ratings:
            seller_main_rat = textify(self.pattern_int.findall(seller_main_ratings)).replace(' ','')
        star_seller_main = extract_data(sel,'//div[@id="merchant-info"]//text()[contains(.,"out of")]')
        if star_seller_main:
            star_seller_m = textify(re.findall('(.*?) out',star_seller_main)).replace('(','').strip()
        aux_relatedsel1 = {}
        if seller_main_ratings:
            aux_relatedsel1.update({"star_rating":star_seller_main})
        if seller_main_name:
            relatedsellersitem = RelatedSellers()
            relatedsellersitem.update({"related_sk":md5(seller_main_name+response.url+seller_main_av),"product_id":normalize(sk),"name":normalize(title),"category":normalize(category),"product_condition":normalize(seller_main_av),"seller_name":normalize(seller_main_name),"seller_no_of_rating":normalize(seller_main_rat),"seller_rating_percentage":'',"seller_price":normalize(original_price)})
            if aux_relatedsel1:
                relatedsellersitem.update({"aux_info":normalize(json.dumps(aux_relatedsel1, ensure_ascii=False, encoding="utf-8"))})
            yield relatedsellersitem

        other_sellers_nodes = get_nodes(sel,'//div[div[h5[span[contains(text(),"Other Sellers on Amazon")]]]]/following-sibling::div[contains(@class,"box")]')
        for seller_nd in other_sellers_nodes:
            price_pop = extract_data(seller_nd,'.//span[contains(@class,"color-price")]/text()')
            prod_state = extract_data(seller_nd,'.//span[contains(@class,"color-secondary")][not(contains(text(),"Sold"))]/text()')
            merchant_name = extract_data(seller_nd, './/span[contains(@class,"MerchantName")]/text()')
            inner_pop = extract_data(seller_nd,'.//span[@data-action]/@data-a-popover')
            if inner_pop:
                in_pop = json.loads(inner_pop)
                url = in_pop.get('url','')
                if url:
                    url1 = "{}{}".format(self.URL,url)
                    get_relatedseller_item = self.parse_related(url1, price_pop, prod_state, merchant_name, response.url, sk, title, category)
                    if get_relatedseller_item: yield get_relatedseller_item
        self.got_page(sk, 1)

    def parse_reviews(self, response):
        sel = Selector(response)
        sk = response.meta.get('sk','')
        title = response.meta.get('title','')
        category = response.meta.get('category','')
        review_nodes = get_nodes(sel, '//div[contains(@id, "review_list")]//div[@data-hook="review"]')
        for rnd in review_nodes:
            revie_by = extract_data(rnd, './/a[@data-hook="review-author"]/text()')
            review_on = extract_data(rnd, './/span[@data-hook="review-date"]/text()')
            review_format = extract_data(rnd, './/a[@data-hook="format-strip"]//text()')
            review_tit = extract_data(rnd, './/a[@data-hook="review-title"]/text()')
            review_vot = extract_data(rnd, './/span[@class="review-votes"]/text()')
            review_purchase = extract_data(rnd,'.//span[@data-hook="avp-badge"]/text()')
            purchase_flag = '0'
            if 'purchase' in review_purchase.lower():
                purchase_flag = '1'
            reviw_aux  = {}
            if review_format:
                reviw_aux.update({"review_format":review_format.replace(u'\xf0\x9f\x92\x99','').replace(u'\U0001f499','').replace(u'\U0001f917','').replace(u'\U0001f44d','')})
            if review_tit: reviw_aux.update({"review_title":review_tit.replace(u'\xf0\x9f\x92\x99','').replace(u'\U0001f499','').replace(u'\U0001f917','').replace(u'\U0001f44d','')})
            if review_vot: reviw_aux.update({"review_votes":review_vot.replace(u'\xf0\x9f\x92\x99','').replace(u'\U0001f499','').replace(u'\U0001f917','').replace(u'\U0001f44d','')})
            review_ond = ''
            if review_on: review_ond = str(parse_date(review_on))
            reveiw_body = extract_data(rnd, './/span[@data-hook="review-body"]/text()').replace(u'\xf0\x9f\x92\x99','').replace(u'\U0001f499','').replace(u'\U0001f917','').replace(u'\U0001f44d','')
            review_rating = extract_data(rnd, './/i[@data-hook="review-star-rating"]/span/text()')
            stars_ratings = textify(re.findall('(.*?) out',review_rating))
            review_item = CustomerReviews()
            if revie_by:
                reviw_sk = md5(sk+category+revie_by+review_ond)
                review_item.update({"sk":normalize(reviw_sk),"product_id":normalize(sk),"name":normalize(title),"reviewed_by":normalize(revie_by),"reviewed_on":normalize(review_ond),"review":normalize(reveiw_body),"category":normalize(category),"review_url":normalize(response.url),"review_rating":normalize(stars_ratings),"verified_purchase_flag":purchase_flag})
                if reviw_aux:
                    review_item.update({"aux_info":normalize(json.dumps(reviw_aux, ensure_ascii=False, encoding="utf-8"))})
                yield review_item

        next_review_link = extract_data(sel, '//li[@class="a-last"]/a/@href')
        if next_review_link:
            next_review_url = "{}{}".format(self.URL,next_review_link)
            yield Request(next_review_url, callback=self.parse_reviews, meta= {"sk":sk, "title":title, 'category':category})

    def parse_richmedia(self, images_final, sk, responseurl, title, category):
        richmedia_item = RichMedia()
        richmedia_item.update({"sk":md5(images_final+responseurl),"product_id":normalize(sk), "category":normalize(category),"image_url":normalize(images_final),"reference_url":normalize(responseurl)})
        return richmedia_item

    def parse_related(self, url1, price_pop, prod_state, merchant_name, responseurl, sk, title, category):
        data = requests.get(url1, headers=self.headers).text
        hxs = Selector(text=data)
        #whole_txt = extract_data(hxs, '//div//text()',',').replace(',,','').replace(',',' ')
        whole_txt = extract_data(hxs, '//div//text()[not(ancestor::style)][not(ancestor::script)]',',').replace(',,',' ').replace(',',' ')
        seller_rat_inte, seller_rat_per = '', ''
        seller_ratings = extract_data(hxs,'//a[contains(text(),"seller ratings")]/text()')
        seller_rat_perc = extract_data(hxs, '//div[b[contains(text(),"%")]]/b/text()')
        prod_st = extract_data(hxs, '//span[@class="availGreen"]/text()').strip().strip('.')
        if seller_ratings:
            seller_rat_inte = textify(self.pattern_int.findall(seller_ratings))
        if seller_rat_perc:
             seller_rat_per = textify(self.pattern_int.findall(seller_rat_perc))
        aux_relatedsel = {}
        if whole_txt: aux_relatedsel.update({"information":whole_txt})
        if prod_state: aux_relatedsel.update({"product_info": prod_state})
        relatedsellersitem = RelatedSellers()
        relatedsellersitem.update({"related_sk":md5(merchant_name+responseurl),"product_id":normalize(sk),"name":normalize(title),"category":normalize(category),"product_condition":normalize(prod_st),"seller_name":normalize(merchant_name),"seller_no_of_rating":normalize(seller_rat_inte),"seller_rating_percentage":normalize(seller_rat_per),"seller_price":normalize(price_pop)})
        if aux_relatedsel:
            relatedsellersitem.update({"aux_info":normalize(json.dumps(aux_relatedsel, ensure_ascii=False, encoding="utf-8"))})
        return relatedsellersitem
