from juicer.utils import *
from practo_doctorsinfo_xpaths import *
from juicer.items import *
from scrapy.http import FormRequest
import requests

class Practoinfodoctor(JuicerSpider):
    name = 'practo_doctorsinfo_browse'
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
                    doc_qualifications = data.get('qualifications','').replace(',','<>')
                    doc_years_experience = str(data.get('experience_years','')) + ' '+ 'years experience'
                    spec_list = []
                    doc_specialities = data.get('specialization','')
                    if doc_specialities :
                        for i in doc_specialities :
                            spec = i.get('label','')
                            spec_list.append(spec)
                        doc_specialities = '<>'.join(spec_list)
                    else : doc_specialities = ''
                    doc_clinic_names = data.get('clinic_name','')
                    doc_id = data.get('doctor_id','')
                    aux_infos = {}
                    if response.meta.get('city'):
                         aux_infos.update({"city": response.meta.get('city','')})
                    if doc_ava_text :aux_infos.update({'doc_avilability_text':doc_ava_text})
                    doc_clinic_images = data.get('clinic_photos','')
                    if doc_clinic_images : doc_clinic_images = doc_clinic_images[0].get('photo_url','')
                    else : doc_clinic_images = ''
                    doc_availability = data.get('doctor_available_today','')
                    if doc_availability : aux_infos.update({"Doctor_availability": doc_availability})
                    doc_rating = data.get('recommendation',{}).get('percent','')
                    doc_votes = ''
                    if doc_rating:
                        doc_votes = data.get('recommendation',{}).get('votes','')
                    doc_loc_latitude = data.get('latitude','')
                    doc_loc_longitude = data.get('longitude','')
                    doc_feedback_count = str(data.get('reviews_count','')) +' '+'Feedback'
                    doc_addr_locality = data.get('locality','' )
                    doc_addr_region = self.particular_city
                    doc_add_both = str(doc_addr_locality) + ','+str(doc_addr_region)
                    doc_fee_amount = data.get('consultation_fees','')
                    doc_price_currency = data.get('currency','')
                    practice_id = data.get('practice_id','')
                    if practice_id:aux_infos.update({"practice_id": practice_id})
                    on_call = data.get('on_call','')
                    if on_call == 'True' : doc_booking_type = 'Call Now'
                    else : doc_booking_type = 'Book Appointment'
                    if doc_link and doc_id:
                        self.get_page('practo_doctorsinfo_terminal', doc_link, doc_id, json.dumps({'city':response.meta.get('city',''),'practice_id':practice_id}))
                    doctor_listing = DoctorInfo()
                    doctor_listing['doctor_id'] = str(doc_id)
                    doctor_listing['doctor_name'] = str(doc_name)
                    doctor_listing['doctor_profile_link'] = str(doc_link)
                    doctor_listing['qualification'] = str(doc_qualifications)
                    doctor_listing['years_of_experience'] = str(doc_years_experience)
                    doctor_listing['specialization'] = str(doc_specialities)
                    doctor_listing['rating'] = str(doc_rating)
                    doctor_listing['vote_count'] = str(doc_votes)
                    doctor_listing['feedback_count'] = str(doc_feedback_count)
                    doctor_listing['location'] = str(doc_add_both)
                    doctor_listing['address'] = str(doc_addr_locality)
                    doctor_listing['consultation_fee'] = str(doc_fee_amount)
                    doctor_listing['doctor_image'] = str(doctor_photos)
                    doctor_listing['clinic_names'] = str(doc_clinic_names)
                    doctor_listing['clinic_images'] = str(doc_clinic_images)
                    doctor_listing['location_latitude'] = str(doc_loc_latitude)
                    doctor_listing['location_longitude'] = str(doc_loc_longitude)
                    doctor_listing['region'] = str(doc_addr_region)
                    doctor_listing['fee_currency'] = str(doc_price_currency)
                    doctor_listing['booking_type'] = str(doc_booking_type)
                    doctor_listing['reference_url'] = str(city_url)
                    if aux_infos:
                        doctor_listing['aux_info'] = json.dumps(aux_infos)
                    yield doctor_listing
        next_page =  sel.xpath('//div[@data-qa-id="pagination_container"]//li//a//@href').extract()
        for i in next_page :
            if 'page=0' in i : continue
            next_page = self.domain + self.particular_city +'/doctors'+str(i)
            yield Request(next_page, callback=self.parse_citie, meta={'url':response.url, 'city':response.meta.get('city','')},dont_filter = True)
    def parse_citie(self, response):
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
                    doc_ava_text = data.get('doctor_availability_text','')
                    doc_name = data.get('name','')
                    doc_link = data.get('profile_url','')
                    if doc_link : doc_link = self.domain + doc_link
                    doc_qualifications = data.get('qualifications','').replace(',','<>')
                    doc_years_experience = str(data.get('experience_years','')) + ' '+ 'years experience'
                    spec_list = []
                    doc_specialities = data.get('specialization','')
                    if doc_specialities : 
                        for i in doc_specialities :
                            spec = i.get('label','')
                            spec_list.append(spec)
                        doc_specialities = '<>'.join(spec_list)
                    else : doc_specialities = ''
                    doc_clinic_names = data.get('clinic_name','')
                    doc_id = data.get('doctor_id','')
                    aux_infos = {}
                    if response.meta.get('city'):
                         aux_infos.update({"city": response.meta.get('city','')})
                    if doc_ava_text :aux_infos.update({'doc_avilability_text':doc_ava_text})
                    doc_clinic_images = data.get('clinic_photos','')
                    if doc_clinic_images : doc_clinic_images = doc_clinic_images[0].get('photo_url','')
                    else : doc_clinic_images = ''
                    doc_availability = data.get('doctor_available_today','')
                    if doc_availability : aux_infos.update({"Doctor_availability": doc_availability})
                    doc_rating = data.get('recommendation',{}).get('percent','')
                    doc_votes = ''
                    if doc_rating:
                        doc_votes = data.get('recommendation',{}).get('votes','')
                    doc_loc_latitude = data.get('locality_latitude','')
                    doc_loc_longitude = data.get('locality_longitude','')
                    doc_feedback_count = str(data.get('reviews_count','')) +' '+'Feedback'
                    doc_addr_locality = data.get('locality','' )
                    doc_addr_region = self.particular_city
                    doc_add_both = str(doc_addr_locality) + ','+str(doc_addr_region)
                    doc_fee_amount = data.get('consultation_fees','')
                    doc_price_currency = data.get('currency','')
                    practice_id = data.get('practice_id','')
                    if practice_id:aux_infos.update({"practice_id": practice_id})
                    on_call = data.get('on_call','')
                    if on_call == 'True' : doc_booking_type = 'Call now'
                    else : doc_booking_type = 'Book Appointment'
                    if doc_link and doc_id:
                        self.get_page('practo_doctorsinfo_terminal', doc_link, doc_id, json.dumps({'city':response.meta.get('city',''),'practice_id':practice_id}))
                    doctor_listing = DoctorInfo()
                    doctor_listing['doctor_id'] = str(doc_id)
                    doctor_listing['doctor_name'] = str(doc_name)
                    doctor_listing['doctor_profile_link'] = str(doc_link)
                    doctor_listing['qualification'] = str(doc_qualifications)
                    doctor_listing['years_of_experience'] = str(doc_years_experience)
                    doctor_listing['specialization'] = str(doc_specialities)
                    doctor_listing['rating'] = str(doc_rating) 
                    doctor_listing['vote_count'] = str(doc_votes)
                    doctor_listing['feedback_count'] = str(doc_feedback_count)
                    doctor_listing['location'] = str(doc_add_both)
                    doctor_listing['address'] = str(doc_addr_locality)
                    doctor_listing['consultation_fee'] = str(doc_fee_amount)
                    doctor_listing['doctor_image'] = str(doctor_photos)
                    doctor_listing['clinic_names'] = str(doc_clinic_names)
                    doctor_listing['clinic_images'] = str(doc_clinic_images)
                    doctor_listing['location_latitude'] = str(doc_loc_latitude)
                    doctor_listing['location_longitude'] = str(doc_loc_longitude)
                    doctor_listing['region'] = str(doc_addr_region)
                    doctor_listing['fee_currency'] = str(doc_price_currency)
                    doctor_listing['booking_type'] = str(doc_booking_type)  
                    doctor_listing['reference_url'] = str(city_url)
                    if aux_infos:
                        doctor_listing['aux_info'] = json.dumps(aux_infos)
                    yield doctor_listing'''

      
