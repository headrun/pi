from juicer.utils import *
from juicer.items import DoctorInfo
from lybrate_doctors_xpaths import *
import requests

class LybrateDoctors(JuicerSpider):
    name = 'lybrate_doctors_browse'
    handle_http_status_list = ['302', '500', '403']

    def __init__(self, *args, **kwargs):
        super(LybrateDoctors, self).__init__(*args, **kwargs)
        self.domain = "https://www.lybrate.com/"
        self.doctors = '/doctors'
        self.pagenumber =  kwargs.get('page', '')
        self.pagenumber = '%s%s'%('?page=',self.pagenumber)
        self.pageend = kwargs.get('end', '')
        self.particular_city = kwargs.get('city','')
        if self.particular_city:
            self.start_urls = ['https://www.lybrate.com/%s/doctors'%self.particular_city]
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
                city_url = "{}{}{}".format(self.domain, city, self.doctors)
                yield Request(city_url, callback=self.parse_cities, meta={'url':city_url})
        yield Request(response.url, callback=self.parse_cities, meta={'url': response.url,'city': self.particular_city}, dont_filter=True)


    def parse_cities(self, response):
        sel = Selector(response)
        url = response.meta.get('url','')
        city_url = response.url
        nodes = get_nodes(sel, doc_nodes)
        for node in nodes:
            aux_info = {}
            photo = extract_data(node, photo_xpath)
            name = extract_data(node, name_xpath)
            link = extract_data(node, link_xpath)
            qua = extract_data(node, qua_xpath, '<>').replace(', ','<>')
            spe = extract_data(node, spe_xpath, '<>').replace(', ','<>')
            clic = extract_data(node, clic_xpath, '<>').replace(', ','<>')
            cic_img = extract_data(node, cic_img_xpath, '<>').replace(',','<>')
            st_ad = extract_data(node, st_ad_xpath)
            loc_ad = extract_data(node, loc_ad_xpath)
            ad_re = extract_data(node, ad_re_xpath)
            ad_cou = extract_data(node, ad_cou_xpath)
            ad_pos = extract_data(node, ad_pos_xpath)
            addr = normalize(st_ad)+' '+normalize(loc_ad)+' '+normalize(ad_re)+' '+normalize(ad_cou)+' '+normalize(ad_pos)
            consulted = extract_data(node, consulted_xpath, '<>').replace(', ','<>')
            lat = extract_data(node, lat_xpath)
            lon = extract_data(node, lon_xpath)
            rat = extract_data(node, rat_xpath)
            vote = extract_data(node, vote_xpath).replace('ratings','').strip('(').strip(')').strip()
            exp = extract_data(node, exp_xpath)
            cur = extract_data(node, cur_xpath)
            cur_mny = extract_data(node, cur_mny_xpath)
            avai = extract_data(node, avai_xpath)
            if avai:
                aux_info.update({"Available_status":normalize(avai)})
            sch = extract_data(node, sch_xpath)
            doc_id = link.split('/')[-1]
            feed =''
            if link and doc_id:
                self.get_page('lybrate_doctors_terminal', link, doc_id , meta_data={"doctor_name":normalize(name)})
            doctor_listing = DoctorInfo()
            doctor_listing['doctor_id'] = normalize(doc_id)
            doctor_listing['doctor_name'] = normalize(name)
            doctor_listing['doctor_profile_link'] = normalize(link)
            doctor_listing['qualification'] = normalize(qua)
            doctor_listing['years_of_experience'] = normalize(exp)
            doctor_listing['specialization'] = normalize(spe)
            doctor_listing['recently_visited_for'] = normalize(consulted)
            doctor_listing['rating'] = normalize(rat)
            doctor_listing['vote_count'] = normalize(vote)
            doctor_listing['feedback_count'] = normalize(feed)
            doctor_listing['location'] = normalize(loc_ad)
            doctor_listing['address'] = normalize(addr)
            doctor_listing['consultation_fee'] = normalize(cur_mny)
            doctor_listing['schedule_timeslot'] = normalize(sch)
            doctor_listing['doctor_image'] = normalize(photo)
            doctor_listing['clinic_names'] = normalize(clic)
            doctor_listing['clinic_images'] = normalize(cic_img)
            doctor_listing['location_latitude'] = normalize(lat)
            doctor_listing['location_longitude'] = normalize(lon)
            doctor_listing['region'] = normalize(ad_re)
            doctor_listing['fee_currency'] = normalize(cur)
            #doctor_listing['booking_type'] = normalize(doc_booking_type)
            doctor_listing['reference_url'] = normalize(city_url)
            if aux_info:
                doctor_listing['aux_info'] = json.dumps(aux_info)
            yield doctor_listing
            import pdb;pdb.set_trace()
        '''next_page = extract_data(sel,'//a[@class="primary__inverted raised lybPull--right"][contains(@title,"Next")]//@href')
        if next_page and self.crawl_type=='catchup':
                yield Request(next_page, callback=self.parse_cities, meta={'url':response.url})'''



