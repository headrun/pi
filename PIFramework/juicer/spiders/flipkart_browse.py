from juicer.utils import *
from juicer.items import *
from selenium import webdriver
import MySQLdb
import time
import scrapy
import json

class FlipkartBestsellersbrowse(JuicerSpider):
    name = "flipkart_bestsellers_browse"
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
        import pdb;pdb.set_trace()
        body = json.loads(response.body)
        start = response.meta.get('start_count',0)
        data = body['RESPONSE']['storeMetaInfoList']
        for uri in data :
            url = "https://www.flipkart.com"+uri[u'uri'] 
            id_ = uri[u'id']
            url = str(url)
            title = uri[u'title']
            headers = {'Referer':url,
                        'User-Agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/53.0.2785.143 Chrome/53.0.2785.143 Safari/537.36','x-user-agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/53.0.2785.143 Chrome/53.0.2785.143 Safari/537.36 FKUA/website/41/website/Desktop'}
            payload = {"requestContext":{"store":str(id_),"start":int(start),"disableProductData":'true',"count":60,"q":"bestsellers"}}
            link = 'https://www.flipkart.com/api/1/product/smart-browse'
            yield Request(link, self.parse_meta_links, method="POST", body=json.dumps(payload),headers=headers,meta={'title':title,'url':url,'headers':headers,'payload':payload, 'start':start, 'id_':id_})

    def parse_meta_links(self,response):
        sel = Selector(response)
        try : body = json.loads(response.body)
        except :print response.body
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
          
            yield Request(link, self.parse_meta_data_links, method="POST", body=json.dumps(payload),headers=headers,meta={'url':response.meta['url'],'title':response.meta['title'],'product_list':product_list},dont_filter = True)

        except : pass
        if product_count >= 60 and self.crawl_type=='catchup':
             try : range_ = int(product_count)/40
             except : pass
             try : 
                 for i in range(1,range_):
                     title = str(response.meta['title'].replace(' ','-'))
                     headers = response.meta['headers']
                     start = int(response.meta['start']) + 40
                     payload = {"requestContext":{"store":str(response.meta['id_']),"start":str(start),"disableProductData":"true","count":60,"q":"bestsellers"}}
                     link_ = 'https://www.flipkart.com/'+str(title)+'/pr?page='+str(i)+'&q=bestsellers&sid='+response.meta['id_']+'&viewType=grid'
                     links = 'https://www.flipkart.com/api/1/product/smart-browse'
                     headers['Referer'] = str(link_)
                     headers.update({'Origin': 'https://www.flipkart.com'})
                     yield Request(links, self.parse_meta_links, method="POST", body=json.dumps(payload),headers=headers,meta={'title':response.meta['title'],'url':response.meta['url'],'headers':headers,'payload':payload, 'start': start, 'id_':response.meta['id_']})
             except  : print "Navigation is Done succesfully"

    def parse_meta_data_links(self,response):
        sel = Selector(response)
        try : body = json.loads(response.body)
        except : print response.body
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
        








