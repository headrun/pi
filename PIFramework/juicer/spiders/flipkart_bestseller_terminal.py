import requests
from juicer.items import *
from juicer.utils import *

class FlipkartBestsellersterminal(JuicerSpider):
    name = "flipkart_bestsellers_terminal"
    handle_httpstatus_list = [404, 302, 303, 403, 500, 999,503,400]

    def __init__(self, *args, **kwargs):
        super(FlipkartBestsellersterminal, self).__init__(*args, **kwargs)
        self.URL = "http://www.flipkart.com"



    def name_clean(self, text):
        text = re.sub('\((.*?)\)','',text)
        text = text.replace('#','').replace('(','').replace(')','').replace(u'\xc2\xa0','').replace(u'\xa0','').replace(u'\xf0\x9f\x92\x99','').replace(u'\U0001f499','').replace(u'\U0001f917','').replace(u'\U0001f44d','').strip().strip('<>').strip()
        return text

    def parse(self, response):
        sel = Selector(response)
        print response.meta
        page_value = response.meta.get('page',1)
        start_count = response.meta.get('start',0)
        data = {}
        try : data  = json.loads(sel.xpath('//script[@type="application/ld+json"]//text()').extract()[0])[0]
        except : print "NO data Available and format has changed"
        reviews = data.get('aggregateRating',{}).get('reviewCount','')
        rating = data.get('aggregateRating',{}).get('ratingValue','')
        image = "<>".join(sel.xpath('//div[@class="_4m8kDI"]//img//@src').extract())
        title = normalize("".join(sel.xpath('//div[@class="_29OxBi"]//h1//text()').extract()))
        sub_title = normalize("".join(sel.xpath('//div[@class="_3xgqrA"]//text()').extract()))
        item_id = response.url.split('?')[0].split('/')[-1]
        price =  normalize("".join(sel.xpath('//div[@class="_1vC4OE _3qQ9m1"]//text()').extract()))
        currency = 'INR'
        discount =  normalize("".join(sel.xpath('//div[@class="_2XDAh9"]//span//text()').extract()))
        features = "<>".join(sel.xpath('//div[@class="_3WHvuP"]//ul//li[@class="_2-riNZ"]//text()').extract())
        category = 'Tvs&Appliances < Washing_machine'
        sk = response.meta.get('sk','')
        description = normalize("".join(sel.xpath('//div[@class="_3rQFTN"]//text()').extract()))
        specifications = ''
        aux_info = {}
        spec = json.loads(sel.xpath('//script[@id="is_script"]//text()').extract()[0].split('window.__INITIAL_STATE__ =')[-1].replace(';\n','')).get('productPage').get('productDetails').get('data').get('product_specification_1').get('data')[0].get('value').get('attributes')
        for spec_node in spec :
                key  = normalize(spec_node.get('name',{}))
                vals = normalize("<>".join(spec_node.get('values',{})))
                aux_info.update({key:vals})

        best_sellers = BestSellers()
        best_sellers.update({"product_id":str(sk),"name":normalize(title),"star_rating":str(rating),"no_of_reviews":str(reviews),"price":str(price),"category":normalize(category),"product_url":normalize(response.url),"reference_url":response.url})
        yield best_sellers
        if image : 
                image = image.replace('{@width}','832').replace('{@height}','832').replace('{@quality}','70')
                richmedia_item = RichMedia()
                richmedia_item.update({"sk":md5(image+response.url),"product_id":normalize(sk), "category":normalize(category),"image_url":normalize(image),"reference_url":normalize(response.url)})
                yield  richmedia_item

        if sub_title : aux_info.update({'sub_title':sub_title})
        products_item = Products()
        products_item.update({"id":str(sk),"name":normalize(title),"original_price":str(price),"discount_price":str(discount),"features":features,"description":normalize(description),"reference_url":normalize(response.url),'aux_info':json.dumps(aux_info)})
        yield products_item
        self.got_page(sk,1)
        seller_link =  "".join(sel.xpath('//a[contains(@href, "seller")]/@href').extract())
        if seller_link :
                seller_link = self.URL+seller_link
                headers = {
        'x-user-agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/53.0.2785.143 Chrome/53.0.2785.143 Safari/537.36 FKUA/website/41/website/Desktop',
        'Origin': 'https://www.flipkart.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.8',
        'content-type': 'application/json',
        'Accept': '*/*',
        'Cache-Control': 'max-age=0',
        'Referer': str(seller_link),
        'Connection': 'keep-alive'}
                url = 'https://www.flipkart.com/api/3/page/dynamic/product-sellers'
                payload = {"requestContext":{"productId":str(sk)}}
                yield Request(url, callback=self.parse_sellers,headers=headers,method="POST",body=json.dumps(payload), meta= {"sk":sk, "title":title, 'category':category,'ref_url':response.url,'seller_url':seller_link})

      
        customer_reviews = "".join(sel.xpath('//a[contains(@href, "product-reviews")]/@href').extract())
 
        if customer_reviews : 
                customer_review_url = self.URL+customer_reviews
                rev_url = customer_review_url.split('?')[0]+'?page='+str(page_value)+'&'+str(sk)
                headers = {
        'x-user-agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/53.0.2785.143 Chrome/53.0.2785.143 Safari/537.36 FKUA/website/41/website/Desktop',
        'Origin': 'https://www.flipkart.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.8',
        'content-type': 'application/json',
        'Accept': '*/*',
        'Cache-Control': 'max-age=0',
        'Referer': str(rev_url),
        'Connection': 'keep-alive'}
                req_url = 'https://www.flipkart.com/api/3/product/reviews?productId='+str(sk)+'&start='+str(start_count)+'&count=10&ratings=ALL&reviewerType=ALL&sortOrder=MOST_HELPFUL'
                yield Request(req_url, callback=self.parse_reviews,headers=headers, meta= {"sk":sk, "title":title, 'category':category,'ref_url':response.url,'rev_url':rev_url,'headers':headers})
        else : 
            try : 
                data_ = json.loads(sel.xpath('//script[@id="is_script"]//text()').extract()[0].split('window.__INITIAL_STATE__ =')[-1].replace(';\n','')).get('productPage',{}).get('productDetails',{}).get('data',{}).get('product_review_page_default_1',{}).get('data',[])
                for data in data_:
                    rev_text = meta_data.get('value',{}).get('text','')
                    rev_title = meta_data.get('value',{}).get('title','')
                    rating = meta_data.get('value',{}).get('rating','')
                    rev_sk = meta_data.get('value',{}).get('id','')
                    review_by = meta_data.get('value',{}).get('author','')
                    review_url = meta_data.get('value',{}).get('url','')
                    review_on = meta_data.get('value',{}).get('created','')
                    try : rev_on = datetime.datetime.strptime(str(review_on.replace(',','')), '%d %B %Y')
                    except : rev_on = ''
                    review_item = CustomerReviews()
                    review_item.update({"sk":str(rev_sk),"product_id":str(sk),"name":normalize(title),"reviewed_by":normalize(review_by),"reviewed_on":str(rev_on),"review":normalize(rev_text),"category":normalize(category),"review_url":normalize(rev_url),"review_rating":str(rating)})
                    yield review_item
            except : data = {}   


    def parse_reviews(self, response):
        sel = Selector(response)
        try : data = json.loads(response.body)
        except : print response.body
        sk = response.meta.get('sk','')
        try :
            total_count = data['RESPONSE']['params']['totalCount']
            nav_page = total_count/int(10)
        except : 
            total_count = ''
            nav_page = 0
        start_count = response.meta.get('start',10)
        page_value  =  response.meta.get('page',2)
        rev_url = response.meta.get('rev_url','')
        rev_url = rev_url.split('?')[0]+'?page='+str(page_value)+'&pid='+str(sk)
        headers = response.meta.get('headers','')
        headers.update({'Referer':rev_url})
        title = response.meta.get('title','')
        category = response.meta.get('category','')
        try : rev_data = data.get('RESPONSE',{}).get('data','')
        except :rev_data = ''
        if rev_data :         
            for meta_data in rev_data : 
                rev_text = meta_data.get('value',{}).get('text','')
                rev_title = meta_data.get('value',{}).get('title','')
                rating = meta_data.get('value',{}).get('rating','')
                rev_sk = meta_data.get('value',{}).get('id','')
                review_by = meta_data.get('value',{}).get('author','')
                review_url = meta_data.get('value',{}).get('url','')
                review_on = meta_data.get('value',{}).get('created','')
                try : rev_on = datetime.datetime.strptime(str(review_on.replace(',','')), '%d %B %Y')
                except : rev_on = ''
	        review_item = CustomerReviews()
	        review_item.update({"sk":str(rev_sk),"product_id":str(sk),"name":normalize(title),"reviewed_by":normalize(review_by),"reviewed_on":str(rev_on),"review":normalize(rev_text),"category":normalize(category),"review_url":normalize(rev_url),"review_rating":str(rating)})
                yield review_item

        next_review_link = 'https://www.flipkart.com/api/3/product/reviews?productId='+str(sk)+'&start='+str(start_count)+'&count=10&ratings=ALL&reviewerType=ALL&sortOrder=MOST_HELPFUL'
       
        if page_value > nav_page: 
            next_review_link = '' 

        if next_review_link :
            yield Request(next_review_link, callback=self.parse_reviews,headers=headers, meta= {"sk":sk, "title":title, 'category':category,'page':int(page_value)+int(1),'start':int(start_count)+int(10),'rev_url':rev_url,'headers':headers})

    

    def parse_sellers(self,response):
        sel = Selector(response)
        sk = response.meta.get('sk','')
        title = response.meta.get('title','')
        category = response.meta.get('category','')
        ref_url = response.meta.get('ref_url','')
        seller_link  = response.meta.get('seller_url','')
        try : data = json.loads(response.body)
        except : print "no data"
        meta_data = data.get('RESPONSE',{}).get('data',{}).get('product_seller_detail_1',{}).get('data','')
        if meta_data :
            for metadata in meta_data : 
		    seller_info = metadata.get('value','').get('sellerInfo','')
		    if seller_info :
			seller_id = seller_info.get('action',{}).get('params',{}).get('sellerId','')
			name = seller_info.get('value',{}).get('name','')
			seller_rating_per = seller_info.get('value',{}).get('rating',{}).get('average','')
                        seller_rating_inte = seller_info.get('value',{}).get('rating',{}).get('base','')
		    try : delivery_info = metadata.get('value',{}).get('deliveryMessages','')[0].get('text','')
		    except : delivery_info = ''
		    price = metadata.get('value',{}).get('metadata',{}).get('price','')
		    try : 
                        offer_info = metadata.get('value','').get('offerInfo','').get('offers','')
                        offer_desc = []
                        for desc in offer_info :
                            desc = desc.get('description',{})
                            offer_desc.append(desc)
                            descri = "".join(offer_desc)
                    except : offer_info = ''
                    aux_info = {}
                    if descri :aux_info.update({'offer_info':descri})
                    if 'delivery_info': aux_info.update({'delivery_info':delivery_info})
                    relatedsellersitem = RelatedSellers()
                    relatedsellersitem.update({"related_sk": str(seller_id),"product_id":str(sk),"name":normalize(title),"category":normalize(category),"seller_name":normalize(name),"seller_no_of_rating":str(seller_rating_inte),"seller_rating_percentage":str(seller_rating_per),"seller_price":str(price)})
                    if aux_info : relatedsellersitem.update({"aux_info":normalize(json.dumps(aux_info, ensure_ascii=False, encoding="utf-8"))})
                    yield relatedsellersitem

