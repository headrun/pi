from juicer.spiders import *
from juicer.utils import *
from practo_xpaths import *
from juicer.items import *
#import requests

class Practo(JuicerSpider):
    name = 'practo_browse'
    start_urls = ['https://www.practo.com/india']
    handle_http_status_list = ['302']

    def __init__(self, *args, **kwargs):
        super(Practo, self).__init__(*args, **kwargs)
        self.domain = "https://www.practo.com"
        self.doctors = '/doctors'
    def parse(self, response):
        sel = Selector(response)
        city_links = sel.xpath(city_lks).extract()
        city_links1 = sel.xpath(city_lks1).extract()
        city_links.extend(city_links1)
        city_links = ['/chennai']
        for city in city_links:
            city_url = "{}{}{}".format(self.domain, city, self.doctors)
            #requs = self.parse_cities(city_url)
            yield Request(city_url, callback=self.parse_cities, meta={'url':city_url})

    def parse_function(self, dic):
        if dic:
            import pdb;pdb.set_trace()
            yield dic

    def parse_cities(self, response):
        sel = Selector(response)
        url = response.meta.get('url','')
        city_url = response.url
        """data = requests.get(city_url,timeout=None).text
        sel = Selector(text=data)"""
        print response.url
        if '/ie/unsupported' in city_url:
            print url, response.url, '--> Error'
            import pdb;pdb.set_trace()
        else:
            nodes = get_nodes(sel, doc_nodes)
            for nd in nodes:
                details_nodes = nd.xpath(details_block)
                doctor_photos = extract_data(nd,'.//div[@class="doc-photo-container"]//img/@data-originalsrc')
                doc_name = extract_data(details_nodes, name_xpath)
                doc_link = extract_data(details_nodes, url_xpath)
                doc_qualifications = extract_data(details_nodes, qual_, '<>')
                doc_years_experience = extract_data(details_nodes, exp_)
                doc_specialities = extract_data(details_nodes, specialities_, '<>')
                doc_clinic_names = extract_data(details_nodes, clinic_name, '<>').strip('<>')
                doc_id = extract_data(details_nodes,id_xpath)
                doc_clinic_images = extract_data(details_nodes, clinic_photos,'<>')
                doc_recently_visited = extract_data(details_nodes, './/span[@class="doc-last-visited-text"]/text()')
                doc_availability = nd.xpath('.//div[@class="doc-availability-block"]')
                doc_rating = extract_data(doc_availability,'./div[contains(@class,"patient_experience_score")]/text()')
                doc_votes = extract_data(doc_availability,'./div[contains(@class,"patient_experience_score")]/span[@class="doctor-votes"]/text()')
                doc_loc_latitude = extract_data(doc_availability, './/span[@itemprop="geo"]/meta[@itemprop="latitude"]/@content')
                doc_loc_longitude = extract_data(doc_availability, './/span[@itemprop="geo"]/meta[@itemprop="longitude"]/@content')
                doc_feedback_count = extract_data(doc_availability, './p[@class="reviews-count"]//text()')
                doc_addr_locality = extract_data(doc_availability,'./p[@itemprop="address"]//span[@itemprop="addressLocality"]/text()')
                doc_addr_region = extract_data(doc_availability,'./p[@itemprop="address"]//span[@itemprop="addressRegion"]/text()')
                doc_add_both = extract_data(doc_availability,'./p[@itemprop="address"]//span[@itemprop]/text()',', ')
                doc_fee_amount = extract_data(doc_availability,'./p[@class="fees"]//span[@class="fees-amount"]/text()')
                doc_price_range = extract_data(doc_availability,'./p[@class="fees"]//meta[@itemprop="priceRange"]/@content')
                doc_price_currency = extract_data(doc_availability,'./p[@class="fees"]//meta[@itemprop="currenciesAccepted"]/@content')
                doc_booking_type = extract_data(doc_availability,'.//span[@class="button-text vn-call-button"]/text()')
                #doc_avail_schedule = extract_data(doc_availability,'./div[@class="timings"]//span[@class="strong days-timing"]/text()')
                #doc_time_slots = extract_data(doc_availability,'./div[@class="timings"]//span[@class="hours-timing"]/text()','<>')
                sch_list = []
                doc_schedule_nodes = doc_availability.xpath('./div[@class="timings"]/div[@class="timings-block"]/p')
                for sch in doc_schedule_nodes:
                    sch_days = extract_data(sch, './span[contains(@class,"strong days-timing")]/text()', ', ')
                    sch_timings = extract_data(sch, './span[contains(@class,"hours-timing")]/text()',', ')
                    sch_slot = ("%s%s%s"%(sch_days,':-',sch_timings)).strip('<>')
                    if sch_slot:
                        sch_list.append(sch_slot)
                sch_list = '<>'.join(sch_list)
                if doc_link and doc_id:
                    self.get_page('practo_doctor_terminal', doc_link, doc_id)
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
                yield doctor_listing

            next_page = extract_data(sel, '//div[@class="paginator"]//a[@class="page_link page_link_next"]/@href')
            if next_page and  self.crawl_type=="catchup":
                import pdb;pdb.set_trace()
                yield Request(next_page,callback = self.parse_cities)
                #self.parse_cities(next_page)
