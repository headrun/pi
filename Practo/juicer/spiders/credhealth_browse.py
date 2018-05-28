from juicer.utils import *
from juicer.items import *

class CredhealthDoctors(JuicerSpider):
    name = 'credihealth_doctors_browse'
    handle_http_status_list = ['302', '500', '403']

    def __init__(self, *args, **kwargs):
        super(CredhealthDoctors, self).__init__(*args, **kwargs)
        self.domain = "https://www.credihealth.com"
        self.doctors = '/doctors'
        self.particular_city = kwargs.get('city','')
        if self.particular_city:
            self.start_urls = ['https://www.credihealth.com/doctors/%s'%self.particular_city]
        else:
            self.start_urls = ['https://www.credihealth.com/doctors/india']

    def parse(self, response):
        sel = Selector(response)
        if not self.particular_city:
            city_links = sel.xpath(city_lks).extract()
            city_links1 = sel.xpath(city_lks1).extract()
            city_links.extend(city_links1)
            for city in city_links:
                city_url = "{}{}{}".format(self.domain, city, self.doctors)
                yield Request(city_url, callback=self.parse_cities, meta={'url':city_url})
        yield Request(response.url, callback=self.parse_speciality, meta={'url': response.url,'city': self.particular_city}, dont_filter=True)

    def parse_speciality(self, response):
        sel = Selector(response)
        spe_links = extract_list_data(sel,'//a[contains(@href,"doctors/chennai/")]//@href')
        for link in spe_links :
            link = self.domain + str(link)
            yield Request(link, callback=self.parse_cities, meta={'url': response.url,'city': self.particular_city}, dont_filter=True)

    def parse_cities(self, response):
        sel = Selector(response)
        url = response.meta.get('url','')
        city_url = response.url
        nodes = sel.xpath('//div[@class="doctor-list-wrapper"]//div[@class="row"]')
        for node in nodes :
            inner_nodes1 = node.xpath('.//div[@class="sp-d-content"]')
            for inner_node1 in inner_nodes1 : 
                doc_link = self.domain + extract_data(inner_node1,'./a/@href')
                doc_name = normalize(extract_data(inner_node1,'./a/h2/text()'))
                doc_degree = normalize(extract_data(inner_node1,'.//p[@class="sp-d-degree"]//text()'))
                doc_desig = normalize(extract_data(inner_node1,'./p[@class="sp-d-designation"]//text()'))
                doc_hosp_link = "<>".join(extract_list_data(inner_node1,'./div[@class="sp-d-hospital-aff"]//ul//li//a//@href'))
                doc_hosp_name = "<>".join(extract_list_data(inner_node1,'./div[@class="sp-d-hospital-aff"]//ul//li//a//text()'))
                doc_speciality = normalize(extract_data(inner_node1,'./p[@class="sp-d-speciality"]//text()'))
                doc_exp = normalize(extract_data(inner_node1,'./div[@class="sp-achievements"]//p/text()')).split('Award')[-1].replace('s','')
                doc_image = extract_data(inner_node1,'./div[@class="sp-d-photo-shot"]//a//img//@src')
                doc_id = doc_link.split('/')[-2]
            inner_nodes2 = node.xpath('.//div[@class="col-sm-4 doc-content-sidebar"]')
            for inner_node2 in inner_nodes2 :
                rating_per = normalize(extract_data(inner_node2,'.//div[@class="sp-rec-btn-inner-sec"]//span//text()'))
                book_app = normalize(extract_data(inner_node2,'.//div[@class="sp-cta-buttons"]//a//button//text()'))
                doc_fee = extract_data(inner_node2,'.//div[@class="sp-money"]//span//text()')
            doctor_listing = DoctorInfo()
	    doctor_listing['doctor_id'] = str(doc_id)
	    doctor_listing['doctor_name'] = str(doc_name)
	    doctor_listing['doctor_profile_link'] = str(doc_link)
	    doctor_listing['qualification'] = str(doc_degree)
	    doctor_listing['years_of_experience'] = str(doc_exp)
	    doctor_listing['specialization'] = str(doc_speciality)
	    doctor_listing['rating'] = str(rating_per)
	    doctor_listing['vote_count'] = ''
	    doctor_listing['feedback_count'] = ''
	    doctor_listing['location'] = ''
	    doctor_listing['address'] = ''
	    doctor_listing['consultation_fee'] = str(doc_fee)
	    doctor_listing['doctor_image'] = str(doc_image)
	    doctor_listing['clinic_names'] = str(doc_hosp_name)
	    doctor_listing['clinic_images'] = ''
	    doctor_listing['location_latitude'] = ''
	    doctor_listing['location_longitude'] = ''
	    doctor_listing['region'] = ''
	    doctor_listing['fee_currency'] = ''
	    doctor_listing['booking_type'] = str(book_app)
	    doctor_listing['reference_url'] = str(city_url)
            if 'request_callback' in doc_link : continue
            self.get_page('credihealth_doctors_terminal', doc_link, doc_id , meta_data={'doctor_listing':doctor_listing})
        next_page = extract_data(sel,'//div[@class="sp-pagination"]//ul[@class="pagination pagination"]//a[@rel="next"][contains(text(),"Next")]//@href')
        if next_page :
                next_page = self.domain + next_page
                yield Request(next_page, callback=self.parse_cities, meta={'url':response.url})



