"""from juicer.utils import *
from juicer.items import HospitalInfo
from practo_hospitals_xpaths import *
import requests

class LybrateHospitals(JuicerSpider):
    name = 'lybrate_hospitals_browse'
    handle_http_status_list = ['302', '500', '403']

    def __init__(self, *args, **kwargs):
        super(LybrateHospitals, self).__init__(*args, **kwargs)
        self.domain = "https://www.lybrate.com/"
        self.hospitals = '/hospitals'
        self.pagenumber =  kwargs.get('page', '')
        self.pagenumber = '%s%s'%('?page=',self.pagenumber)
        self.pageend = kwargs.get('end', '')
        self.phone_post_url = "https://www.practo.com/health/api/vn/vnpractice"
        self.particular_city = kwargs.get('city','')
        if self.particular_city:
            self.start_urls = ['https://www.lybrate.com/%s/hospitals'%self.particular_city]
        else:
            self.start_urls = ['https://www.practo.com/india']
           
        self.pattern1 = re.compile(r'\d+')

    def parse(self, response):
        sel = Selector(response)
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
        links = extract_list_data(sel,'//h2[@itemprop="name"]//a[@itemprop="url"]//@href')
        titles = extract_list_data(sel,'//h2[@itemprop="name"]//a[@itemprop="url"]//text()')
        for hosp_link,title in zip(links,titles) : 
            hosp_id = hosp_link.split('/')[-1]
            self.get_page('lybrate_hospitals_terminal', hosp_link, hosp_id,meta_data={"hospital_title":normalize(title),'url':response.url,'city':self.particular_city})
        next_page = extract_data(sel,'//a[@class="primary__inverted raised lybPull--right"][contains(@title,"Next")]//@href')
        if next_page :
            if next_page:
                yield Request(next_page, callback=self.parse_cities, meta={'url':response.url,'city':self.particular_city})

        #import pdb;pdb.set_trace()
        for i in range(10,1000):
            next_page = "https://www.lybrate.com/chennai/hospitals"+'?page='+str(i)
            #import pdb;pdb.set_trace()
            yield Request(next_page, callback=self.parse_data, meta={'url':response.url,'city':self.particular_city})

    def parse_data(self,response):
        sel = Selector(response)
        url = response.meta.get('url','')
        city_url = response.url
        links = extract_list_data(sel,'//h2[@itemprop="name"]//a[@itemprop="url"]//@href')
        titles = extract_list_data(sel,'//h2[@itemprop="name"]//a[@itemprop="url"]//text()')
        for hosp_link,title in zip(links,titles) :
            hosp_id = hosp_link.split('/')[-1]
            self.get_page('lybrate_hospitals_terminal', hosp_link, hosp_id,meta_data={"hospital_title":normalize(title),'url':response.url,'city':self.particular_city})"""




