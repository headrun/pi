from juicer.utils import *
from juicer.items import HospitalInfo
from practo_hospitals_xpaths import *
import requests

class Practohospitals(JuicerSpider):
    name = 'practo_hosp_crawl'
    handle_http_status_list = ['302', '500', '403']

    def __init__(self, *args, **kwargs):
        super(Practohospitals, self).__init__(*args, **kwargs)
        self.domain = "https://www.practo.com"
        self.hospitals = '/hospitals'
        self.pagenumber =  kwargs.get('page', '')
        self.pagenumber = '%s%s'%('?page=',self.pagenumber)
        self.pageend = kwargs.get('end', '')
        self.phone_post_url = "https://www.practo.com/health/api/vn/vnpractice"
        self.particular_city = kwargs.get('city','')
        if self.particular_city:
            #self.start_urls = ['https://www.practo.com/%s/hospitals'%self.particular_city]
            self.start_urls = ['https://www.practo.com/%s/hospitals?page=44'%self.particular_city]
        #else:
            #self.start_urls = ['https://www.practo.com/india']
            #self.start_urls = ['https://www.practo.com/chennai/hospitals?page=44']
        self.pattern1 = re.compile(r'\d+')

    def parse(self, response):
        sel = Selector(response)
        if not self.particular_city:
            city_links = sel.xpath(city_lks).extract()
            city_links1 = sel.xpath(city_lks1).extract()
            city_links.extend(city_links1)
            for city in city_links:
                city_url = "{}{}{}".format(self.domain, city, self.hospitals)
                #city_url = "{}{}{}{}".format(self.domain, city, self.hospitals, self.pagenumber)
                yield Request(city_url, callback=self.parse_cities, meta={'url':city_url})
        yield Request(response.url, callback=self.parse_cities, meta={'url': response.url}, dont_filter=True)


    def parse_cities(self, response):
        sel = Selector(response)
        url = response.meta.get('url','')
        city_url = response.url
        if '/ie/unsupported' not in city_url:
            cvss = sel.xpath('//script[contains(text(), "window.__REDUX_STATE__")]/text()').extract()[0].split('window.__REDUX_STATE__=')[1]
            other_info = response.xpath('//script[@type="application/ld+json"]//text()').extract()
            if len(other_info) >10:
                other_info = other_info[1:]
            else:
                other_info=other_info
            json_data = json.loads(cvss)
            listing =  json_data['listing']['list']
            for data,more_info in zip(listing,other_info) :
                more_info = json.loads(more_info)
                hosp_link = str(more_info.get('url',''))
                hosp_no_of_doctor = data.get('doctors_count','')
                hosp_book = str(data.get('status',''))
                if hosp_book=='vn':hosp_book='Call Now'
                else: hosp_book=''
                print hosp_link, hosp_no_of_doctor, hosp_book
