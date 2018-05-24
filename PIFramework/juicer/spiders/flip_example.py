from juicer.utils import *
from juicer.items import *
from selenium import webdriver
import MySQLdb
import time
import scrapy
import json

class FlipkartBestsellersbrowse(JuicerSpider):
    name = "flipkart_browse"
    start_urls = ['https://www.flipkart.com/search?q=bestsellers&otracker=start&as-show=off&as=off']
    handle_httpstatus_list = [404, 302, 303, 403, 500, 999, 503]

    def __init__(self, *args, **kwargs):
        super(FlipkartBestsellersbrowse, self).__init__(*args, **kwargs)
        self.URL = "https://www.flipkart.com/"

    def parse(self, response):
        sel = Selector(response)
        url = 'https://www.flipkart.com/api/1/product/smart-browse/facets?store=search.flipkart.com&filters=facet-show=all&q=bestsellers'
        headers={'Referer' : 'https://www.flipkart.com/search?q=bestsellers&otracker=start&as-show=off&as=off',
        'User-Agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/53.0.2785.143 Chrome/53.0.2785.143 Safari/537.36',
        'x-user-agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/53.0.2785.143 Chrome/53.0.2785.143 Safari/537.36 FKUA/website/41/website/Desktop'}

        yield Request(url, self.parse_next,headers=headers)

    def parse_next(self,response):
        sel = Selector(response)
        body = json.loads(response.body)
         
        headers = {'Referer':response.url,
                        'User-Agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/53.0.2785.143 Chrome/53.0.2785.143 Safari/537.36','x-user-agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/53.0.2785.143 Chrome/53.0.2785.143 Safari/537.36 FKUA/website/41/website/Desktop'}
        payload = {"requestContext":{"store":'search.flipkart.com',"start":0,"disableProductData":'true',"count":60,"q":"bestsellers"}}
        link = 'https://www.flipkart.com/api/1/product/smart-browse'
        yield Request(link, self.parse_meta_links, method="POST", body=json.dumps(payload),headers=headers,meta={'headers':headers,'payload':payload})

    def parse_meta_links(self,response):
        sel = Selector(response)
        body = json.loads(response.body)
        try : product_count = body['RESPONSE']['pageContext']['searchMetaData']['metadata']['totalProduct']
        except : product_count = ''
        product_list = []
        try :
            data_ = body['RESPONSE']['pageContext']['searchMetaData']['productContextList']['products']
            for i in data_ :
                product_id = i[u'productId']
                product_list.append(product_id)
            headers = {'Referer':response.meta['url'],
                'User-Agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/53.0.2785.143 Chrome/53.0.2785.143 Safari/537.36','x-user-agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/53.0.2785.143 Chrome/53.0.2785.143 Safari/537.36 FKUA/website/41/website/Desktop'}

            link = 'https://www.flipkart.com/api/3/search/summary'
            payload = {"requestContext":{"products":data_}}
            yield Request(link, self.parse_meta_data_links, method="POST", body=json.dumps(payload),headers=headers,meta={'url':response.meta['url'],'title':response.meta['title'],'product_list':product_list})

        except :
            print response.meta['url']

        """if len(data_)>60 :
            for 
            nav_link  = response.url
            yield """

    def parse_meta_data_links(self,response):
        sel = Selector(response)
        body = json.loads(response.body)
        product_data = ''
        for product_id in response.meta['product_list']:
            try :
                meta_data  =  body.get('RESPONSE','').get(product_id,'').get('value','')
                product_link  = meta_data.get(u'smartUrl','')
                no_of_rating  = meta_data.get('rating',{}).get('count','')
                rating  = meta_data.get('rating',{}).get('average','')
                item_id = meta_data['itemId']
                reviews = meta_data.get('rating',{}).get('reviewCount','')
                title = meta_data.get('titles',{}).get('title','')
                price = meta_data.get('pricing',{}).get('finalPrice',{}).get('value','')
                discount = meta_data.get('pricing',{}).get('finalPrice',{}).get('discount','')
                currency = meta_data.get('pricing',{}).get('finalPrice',{}).get('currency','')
                category = meta_data.get('analyticsData',{}).get('category','')
                sub_title = meta_data.get('titles',{}).get('subtitle','')
                product_data = meta_data.get('keySpecs','')

            except : import pdb;pdb.set_trace()

            best_sellers = BestSellers()
            best_sellers.update({"product_id":str(product_id),"name":normalize(title),"star_rating":str(rating),"no_of_reviews":str(reviews),"price":str(price),"category":normalize(category),"product_url":normalize(product_link),"reference_url":normalize(response.meta['url'])})
            yield best_sellers

            
            images = meta_data.get('media',{}).get('images','')
            for image in images :
                image = image.get('url','')
                if image : image = image.replace('{@width}','832').replace('{@height}','832').replace('{@quality}','70')
                richmedia_item = RichMedia()
                richmedia_item.update({"sk":md5(image+response.meta['url']),"product_id":normalize(product_id), "category":normalize(category),"image_url":normalize(image),"reference_url":normalize(response.meta['url'])})
                yield  richmedia_item

            aux_info = {"category":category,"product_title":title,'price':price,'features':product_data,'sub_title':sub_title,'reference_url':response.meta['url'],'currency':currency,'discount':discount,'item_id':item_id}

            if title and product_link : self.get_page('flipkart_bestsellers_terminal', product_link, product_id, aux_info)
        








