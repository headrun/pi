from juicer.utils import *
from juicer.items import HospitalInfo
from practo_hospitals_xpaths import *
import requests

class Practohospitals(JuicerSpider):
    name = 'practo_hospitalsapi_browse'
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
            self.start_urls = ['https://www.practo.com/%s/hospitals'%self.particular_city]
        else:
            self.start_urls = ['https://www.practo.com/india']

    def parse(self, response):
        sel = Selector(response)
        import pdb;pdb.set_trace()
        if not self.particular_city:
            city_links = sel.xpath(city_lks).extract()
            city_links1 = sel.xpath(city_lks1).extract()
            city_links.extend(city_links1)
            for city in city_links:
                city_url = "{}{}{}".format(self.domain, city, self.hospitals)
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
                doc_count = data.get('doctors_count','')
                hosp_book = str(data.get('status',''))
                if hosp_book=='vn':hosp_book='Call Now'
                else: hosp_book=''
                slug = hosp_link.split('/')[-1]
                hosp_id = data.get('id','')
                if hosp_link and doc_count and hosp_id : 
                    hospital_link = self.domain + hosp_link
                    api_link = 'https://www.practo.com/client-api/v1/profile/%s?slug=%s&profile_type=practices&with_relations=true&is_slug=true&platform=desktop_web&doctors_limit=%s&is_hospital=true&is_profile=true&city=%s&label=hospital&with_seo_data=true&all_amenities=true&mr=true'%(slug,slug,doc_count,self.particular_city)
                
                    self.get_page('practo_hospitalsapi_terminal', api_link, hosp_id, meta_data={"main_link":response.url,"hosp_link":hospital_link,'hosp_book':hosp_book})
            next_page = extract_data(sel, '//div[@data-qa-id="pagination_container"]/ul/li[@class="active"]//following-sibling::li[1]/a/@href')
            if next_page and self.crawl_type == 'catchup':
                next_page = self.domain+'/'+'chennai'+'/hospitals'+str(next_page) 
                if next_page:
                    yield Request(next_page, callback=self.parse_cities, meta={'url':response.url})
