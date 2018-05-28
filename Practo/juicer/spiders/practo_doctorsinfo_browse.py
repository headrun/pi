from juicer.utils import *
from practo_doctorsinfo_xpaths import *
from juicer.items import *
from scrapy.http import FormRequest
import requests

class Practoinfodoctor(JuicerSpider):
    name = 'practo_doctorsinfo_browse1'
    handle_http_status_list = ['302','404','403']

    def __init__(self, *args, **kwargs):
        super(Practoinfodoctor, self).__init__(*args, **kwargs)
        self.conn = MySQLdb.connect(host = 'localhost', user = 'root', passwd = 'hdrn59!', db = 'urlqueue_dev', charset = 'utf8', use_unicode = True)
        self.cur = self.conn.cursor()
 
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
                #city_url = "{}{}{}{}".format(self.domain, city, self.doctors, self.pagenumber)
                yield Request(city_url, callback=self.parse_cities, meta={'url':city_url, 'city':city})
        else:
            yield Request(response.url, callback=self.parse_cities, meta={'url': response.url, 'city': self.particular_city}, dont_filter=True)


    def parse_cities(self, response):
        sel = Selector(response)
        url = response.meta.get('url','')
        city_url = response.url
        if '/ie/unsupported' not in city_url:
                cvss = sel.xpath('//script[contains(text(), "window.__REDUX_STATE__")]/text()').extract()[0].split('window.__REDUX_STATE__=')[1]
                json_data = json.loads(cvss)
                listing =  json_data['listing']['list']
                for data in listing:
                    if not data: break
                    doctor_photos = data.get('photo_url','')
                    doc_ava_status = data.get('doctor_available_today','')
                    doc_ava_text = data.get('doctor_availability_text','')
                    doc_name = data.get('name','')
                    doc_link = data.get('profile_url','')
                    if doc_link : doc_link = self.domain + doc_link
                    doc_id = data.get('doctor_id','')
                    if doc_link and doc_id:
                        print doc_link,doc_id
                        #self.get_page('practo_doctorsinfo_terminal', doc_link, doc_id, json.dumps({'city':response.meta.get('city',''),'practice_id':practice_id}))
                        insert_qry = "insert into practo_duplicate_urls(doctor_id, doctor_name,doctor_url,reference_url) values (%s, %s, %s, %s)"
                        values = (str(doc_id),str(doc_name),str(doc_link),str(response.url))
                        self.cur.execute(insert_qry,values)
                        self.conn.commit()
        next_page = extract_data(sel, '//div[@data-qa-id="pagination_container"]/ul/li[@class="active"]//following-sibling::li[1]/a/@href')
        if self.crawl_type == 'catchup' and next_page:
                next_page = self.domain + self.particular_city +'/doctors'+str(next_page)
                yield Request(next_page, callback=self.parse_cities, meta={'url':response.url, 'city':response.meta.get('city','')},dont_filter = True)


      
