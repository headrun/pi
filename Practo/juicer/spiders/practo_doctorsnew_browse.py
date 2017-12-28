from juicer.utils import *
from practo_doctorsinfo_xpaths import *
from juicer.items import *
from scrapy.http import FormRequest
import requests

class Practoinfodoctor(JuicerSpider):
    name = 'practo_doctorsnew_browse'
    handle_http_status_list = ['302','404','403']

    def __init__(self, *args, **kwargs):
        super(Practoinfodoctor, self).__init__(*args, **kwargs)
        self.domain = "https://www.practo.com/"
        self.doctors = '/doctors'
        self.pagenumber =  kwargs.get('page', '')
        self.pagenumber = '%s%s'%('?page=',self.pagenumber)
        self.pageend = kwargs.get('end', '')
        self.doctors_domain = 'https://www.practo.com/doctors'
        self.phone_post_url = "https://www.practo.com/health/api/vn/vnpractice"
        self.particular_city = kwargs.get('city','')
        if self.particular_city:
            self.start_urls = ['https://www.practo.com/%s/doctors'%self.particular_city]
        else:
            self.start_urls = ['https://www.practo.com/india']

    def parse(self, response):
        sel = Selector(response)
        if not self.particular_city:
            city_links = sel.xpath(city_lks).extract()
            city_links1 = sel.xpath(city_lks1).extract()
            city_links.extend(city_links1)
            for city in city_links:
                city_url = "{}{}{}".format(self.domain, city, self.doctors)
                yield Request(city_url, callback=self.parse_cities, meta={'url':city_url, 'city':city})
        else:
            yield Request(response.url, callback=self.parse_cities, meta={'url': response.url, 'city': self.particular_city}, dont_filter=True)


    def parse_cities(self, response):
        sel = Selector(response)
        url = response.meta.get('url','')
        city_url = response.url
        if '/ie/unsupported' not in city_url:
            links = sel.xpath('//div[@class="c-card-info"]/a[contains(@href,"/chennai/doctor")]/@href').extract()
            for doc_link in links :     
                doc_link = self.domain + str(doc_link)
                doc_id =  doc_link.split('=')[-1]
                slug =  doc_link.split('/')[-1].split('?')[0]
                api_link = "https://www.practo.com/client-api/v1/profile/%s?slug=%s&profile_type=doctors&with_relations=true&with_locality=true&is_slug=true&with_seo_data=true&is_profile=true&city=%s&label=doctor&query=pediatrician&platform=desktop_web&mr=true&with_ad=true&show_recommended_reviews=true&with_service_enquiry=true" %(slug,slug,self.particular_city)
                if doc_link :
                    self.get_page('practo_doctorsnew_terminal',api_link,doc_id, json.dumps({'city':response.meta.get('city',''),'doc_link':doc_link,'main_link':response.url}))            
                    
            next_page = next_page = extract_data(sel, '//div[@data-qa-id="pagination_container"]/ul/li[@class="active"]//following-sibling::li[1]/a/@href')
            if next_page and self.crawl_type == 'catchup':
                next_page = self.domain + self.particular_city +'/doctors'+str(next_page)
                yield Request(next_page, callback=self.parse_cities, meta={'url':response.url, 'city':response.meta.get('city','')},dont_filter = True)


      
