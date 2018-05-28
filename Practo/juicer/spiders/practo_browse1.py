from juicer.utils import *
from practo_xpaths import *
from juicer.items import *
from scrapy.http import FormRequest
import requests

class Practo(JuicerSpider):
    name = 'practo_browse1'
    handle_http_status_list = ['302']

    def __init__(self, *args, **kwargs):
        super(Practo, self).__init__(*args, **kwargs)
        self.domain = "https://www.practo.com"
        self.doctors = '/doctors'
        self.pagenumber =  kwargs.get('page', '')
        self.pagenumber = '%s%s'%('?page=',self.pagenumber)
        self.pageend = kwargs.get('end', '')
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

    def phoneno(self, url, docid):
        headers = {
            'referer': url,
                'authority': 'www.practo.com',
                }
        params = (
            ('practice_doctor_id', docid),
                ('speciality', ''),
                )
        data = requests.get(self.phone_post_url,headers=headers, params=params).text
        extension, phone_numbe = ['']*2
        if data:
            jsdata = {}
            try:
                jsdata = json.loads(data)
            except:
                jsdata = {}
            if jsdata:
                extension = jsdata.get('extension','')
                phone_numbe = jsdata.get('vn_phone_number',{}).get('number','')
        return phone_numbe, extension

    def parse_cities(self, response):
        sel = Selector(response)
        url = response.meta.get('url','')
        city_url = response.url
        import pdb;pdb.set_trace()
        if '/ie/unsupported' not in city_url:
            nodes = response.xpath('//div[@data-qa-id="doctor_listing_cards"]//div[@class="c-card"]')
            for node in nodes :
                import pdb;pdb.set_trace()
            '''nodes = get_nodes(sel, doc_nodes)
            for nd in nodes:
                details_nodes = nd.xpath(details_block)
                doctor_photos = extract_data(nd, doctor_photos_xpath)
                doc_name = extract_data(details_nodes, name_xpath)
                doc_link = extract_data(details_nodes, url_xpath)
                doc_qualifications = extract_data(details_nodes, qual_, '<>')
                doc_years_experience = extract_data(details_nodes, exp_)
                doc_specialities = extract_data(details_nodes, specialities_, '<>')
                doc_clinic_names = extract_data(details_nodes, clinic_name, '<>').strip('<>')
                doc_id = extract_data(details_nodes,id_xpath)
                aux_infos = {}
                if doc_id:
                    #phone_numer, extension = self.phoneno(response.url, doc_id)
                    phone_numer, extension = ['']*2 
                    if phone_numer:
                        aux_infos.update({"phone_number":phone_numer})
                    if extension:
                        aux_infos.update({"extension": extension})
                if response.meta.get('city'):
                        aux_infos.update({"city": response.meta.get('city','')})
                doc_clinic_images = extract_data(details_nodes, clinic_photos,'<>')
                doc_recently_visited = extract_data(details_nodes, doc_recently_visited_xpath)
                doc_availability = nd.xpath(doc_availability_xpath)
                doc_rating = extract_data(doc_availability, doc_rating_xpath)
                doc_votes = extract_data(doc_availability, doc_votes_xpath)
                doc_loc_latitude = extract_data(doc_availability, doc_loc_latitude_xpath)
                doc_loc_longitude = extract_data(doc_availability, doc_loc_longitude_xpath)
                doc_feedback_count = extract_data(doc_availability, doc_feedback_count_xpath)
                doc_addr_locality = extract_data(doc_availability, doc_addr_locality_xpath)
                doc_addr_region = extract_data(doc_availability, doc_addr_region_xpath)
                doc_add_both = extract_data(doc_availability, doc_add_both_xpath ,', ')
                doc_fee_amount = extract_data(doc_availability, doc_fee_amount_xpath)
                doc_price_range = extract_data(doc_availability, doc_price_range_xpath)
                doc_price_currency = extract_data(doc_availability, doc_price_currency_xpath)
                doc_booking_type = extract_data(doc_availability, doc_booking_type_xpath)
                sch_list = []
                doc_schedule_nodes = doc_availability.xpath(doc_schedule_nodes_xpath)
                for sch in doc_schedule_nodes:
                    sch_days = extract_data(sch, sch_days_xpath, ', ')
                    sch_timings = extract_data(sch, sch_timings_xpath,', ')
                    sch_slot = ("%s%s%s"%(sch_days,':-',sch_timings)).strip('<>')
                    if sch_slot:
                        sch_list.append(sch_slot)
                sch_list = '<>'.join(sch_list)
                if doc_link and doc_id:
                    self.get_page('practo_doctor_terminal', doc_link, doc_id, json.dumps({'city':response.meta.get('city','')}))
                doctor_listing = DoctorInfo()
                doctor_listing['doctor_id'] = normalize(doc_id)
                doctor_listing['doctor_name'] = normalize(doc_name)
                doctor_listing['doctor_profile_link'] = normalize(doc_link)
                doctor_listing['qualification'] = normalize(doc_qualifications)
                doctor_listing['years_of_experience'] = normalize(doc_years_experience)
                doctor_listing['specialization'] = normalize(doc_specialities)
                doctor_listing['recently_visited_for'] = normalize(doc_recently_visited)
                doctor_listing['rating'] = normalize(doc_rating)
                doctor_listing['vote_count'] = normalize(doc_votes)
                doctor_listing['feedback_count'] = normalize(doc_feedback_count)
                doctor_listing['location'] = normalize(doc_add_both)
                doctor_listing['address'] = normalize(doc_addr_locality)
                doctor_listing['consultation_fee'] = normalize(doc_fee_amount)
                doctor_listing['schedule_timeslot'] = normalize(sch_list)
                doctor_listing['doctor_image'] = normalize(doctor_photos)
                doctor_listing['clinic_names'] = normalize(doc_clinic_names)
                doctor_listing['clinic_images'] = normalize(doc_clinic_images)
                doctor_listing['location_latitude'] = normalize(doc_loc_latitude)
                doctor_listing['location_longitude'] = normalize(doc_loc_longitude)
                doctor_listing['region'] = normalize(doc_addr_region)
                doctor_listing['fee_currency'] = normalize(doc_price_currency)
                doctor_listing['booking_type'] = normalize(doc_booking_type)
                doctor_listing['reference_url'] = normalize(city_url)
                if aux_infos:
                    doctor_listing['aux_info'] = json.dumps(aux_infos)
                yield doctor_listing'''

            next_page = extract_data(sel, next_page_xpath)
            #if 'page=%s'%self.pageend in response.url: next_page = ''
            if next_page and  self.crawl_type=="catchup":
                yield Request(next_page, callback=self.parse_cities, meta={'url':response.url, 'city':response.meta.get('city','')})
