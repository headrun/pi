from juicer.utils import *
from juicer.items import *
from scrapy.http import Request, FormRequest
import re


class LybratehospitalsTerminal(JuicerSpider):
    name = 'lybrate_hospitals_terminal'
    handle_http_status_list = ['302', '504', '403', 403,'524','502']

    def __init__(self, *args, **kwargs):
        super(LybratehospitalsTerminal, self).__init__(*args, **kwargs)
        self.domain = "https://www.lybrate.com"
     
    def parse(self, response):
        sel = Selector(response)
        city_browse = response.meta.get('data').get('city', '')
        reference_url = response.meta.get('data').get('url', '')
        latitude = str("<>".join(sel.xpath('//div[contains(@id,"map")]//@data-clinic-latitude').extract()))
        longitude = str("<>".join(sel.xpath('//div[contains(@id,"map")]//@data-clinic-longitude').extract()))
        feedback_count = response.meta.get('data',{}).get('feedback_count','')
        hosp_name = extract_data(sel,'//h1[@itemprop="name"]//text()')
        price_range = extract_data(sel,'//div[@class="lybMar-btm--half fixed-hidden-sections"]//span[@itemprop="priceRange"]//text()')
        hosp_id = extract_data(sel,'//div[contains(@id,"ppview-seo-data")]//@data-clinicid')
        rating_count = response.meta.get('data',{}).get('star_rating','')
        clinic_location = extract_data(sel,'//span[@class="lybText--light lybText--bold lybText--body lybMar-btm--half"]//text()')
        medical_spec = extract_data(sel,'//h2[@itemprop="medicalSpecialty"]//text()')
        number_of_doctors = extract_data(sel,'//div[@class="lybMar-btm--half fixed-hidden-sections"]/text()')
        number_of_doctors = "".join(re.findall('\d+',number_of_doctors))
        hospt_description = extract_data(sel,'//div[@itemprop="description"]//text()').encode('utf8')
        timings = str("<>".join(sel.xpath('//div[contains(@itemprop,"openingHours")]//@datetime').extract()))
        other_centers = "<>".join(sel.xpath('//div[@class="grid__col-10 grid__col-lt-md-20 grid__col-xs-20 lybPad-right--half lybPad-top--half"]//a//text()').extract())

        no_of_beds = ''
        no_of_ambulances = ''
        method_of_payment = ''
        street_address =  extract_data(sel,'//span[@itemprop="streetAddress"]//text()')
        address_locality = extract_data(sel,'//span[@itemprop="addressLocality"]//text()')
        address_region = extract_data(sel,'//span[@itemprop="addressRegion"]//text()')
        postal_code = extract_data(sel,'//span[@itemprop="postalCode"]//text()')
        hospital_address = street_address+','+str(postal_code)+','+address_region 
        hospital_meta = HospitalMeta()
        hospital_meta['hospital_id']  = normalize(hosp_id)
        hospital_meta['hospital_name']  = normalize(hosp_name)
        hospital_meta['hospital_profile_link']  = normalize(response.url)
        hospital_meta['rating_count']  = ''
        hospital_meta['rating_value']  = ''
        hospital_meta['location']  = normalize(clinic_location)
        hospital_meta['medical_specialities']  = normalize(medical_spec)
        hospital_meta['number_of_doctors']  = normalize(number_of_doctors)
        hospital_meta['description']  = normalize(hospt_description)
        hospital_meta['no_of_beds']  = ''
        hospital_meta['no_of_ambulances'] = ''
        hospital_meta['method_of_payment']  = ''
        hospital_meta['address']  = normalize(hospital_address)
        hospital_meta['street_address']  = normalize(street_address)
        hospital_meta['locality']  = normalize(address_locality)
        hospital_meta['region']  = normalize(address_region)
        hospital_meta['postal_code']  = normalize(postal_code)
        hospital_meta['opening_timings']  = str(timings)
        hospital_meta['clinic_images']  = ''
        hospital_meta['amenities']  = ''
        hospital_meta['emergency_contact_number']  = ''
        hospital_meta['services']  = ''
        hospital_meta['longitude']  = normalize(latitude)
        hospital_meta['latitude']  = normalize(longitude)
        hospital_meta['establishment_data']  = ''
        hospital_meta['feedback_count']  = normalize(feedback_count)
        #hospital_meta['awards']  = normalize(awards)
        hospital_meta['other_centers']  = normalize(other_centers)
        hospital_meta['reference_url']  = normalize(response.url)
        slug = response.url.split('/')[-1]
        if slug :
            data = {"slug":str(slug),"slugType":"CPS","start":'0',"maxResults":'100',"cityPageUrl":str(city_browse)}
            headers = {'Host': 'www.lybrate.com', 'Accept-Language': 'en-US,en;q=0.5', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache', 'Referer': str(response.url), 'Content-Type': 'application/json', 'Connection': 'keep-alive', 'Accept': 'application/json, text/plain, */*', 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:56.0) Gecko/20100101 Firefox/56.0'}
            yield FormRequest('https://www.lybrate.com/get/doctor/treatments', headers=headers, body=json.dumps(data),method='POST',callback=self.other_center,meta= {'hospital_meta':hospital_meta})
        if number_of_doctors and hosp_id:
	        doctors_link = 'https://www.lybrate.com/get/cpview/uclms?clId='+str(hosp_id)+'&maxResults='+str(number_of_doctors)+'&start=0'
	        yield Request(doctors_link, callback=self.dct_hsp_meta_info, meta={"hsp_id":hosp_id,'city':city_browse,'ref_url':str(response.url)})

    def other_center(self,response):
        hospital_meta = response.meta['hospital_meta']
        jscsv_data = {}
        json21 =json.loads(response.body)
        other_cen = json21.get('items',{}).get('treatments',[])
        y='<>'.join([i.get('treatmentName','') for i in other_cen])
        hospital_meta.update({'services':normalize(y)})
        yield hospital_meta
        

    def dct_hsp_meta_info(self,response):
        hct_id = response.meta['hsp_id']
        ref_url = response.meta['ref_url']
        jscsv_data = {}
        json12=json.loads(response.body)
        doctor_nodes = json12.get('userClinicLocationMappings', [])
        for hnd in doctor_nodes:
            doc_id = str(hnd.get('userId', ''))
            doc_link = self.domain +'/'+ str(response.meta['city']) +'/doctor/'+str(hnd.get('username', '')) 
            doc_name = 'Dr.'+str(hnd.get('name'))
            print doc_name
            dot_qualifications = str(hnd.get('degrees'))
            doc_years_experience = str(hnd.get('experience',''))
            dct_photo = hnd.get('picUrl')
            if dct_photo : dct_photo = 'https://static.lybrate.com'+ str(dct_photo)
            doc_specialities =  str(hnd.get('specialityName',''))
            doc_rating = hnd.get('ratings','')
            doc_votes = ''
            doc_on_call = hnd.get('callDisabled','')
            doc_feedback = hnd.get('popularityScore',0)
            if doc_on_call == True : doc_on_call = 'Doctor available on call'
            else : doc_on_call = 'Not Available on call'
            pics = ''
            doc_availability = hnd.get('avlToday','')
            if doc_availability == 'True': doc_availability = 'Available Today'
            else : doc_availability == 'Not Available Today'
            name_prefix = hnd.get('namePrefix','')
            doc_fee_amount = str(hnd.get('consCharge',''))
            slug_id = hnd.get('doctor',{}).get('new_slug','')
            dct_booking_type = hnd.get('bAEnabled', '')
            if dct_booking_type == True:
                doc_booking_type = "Book Appointment"
            else:
                doc_booking_type = "Call Now"
            timings_dict = {}
            visit_times = hnd.get('userAvailabilities',[])
            for i in visit_times :
                day = i.get('day','')
                time = "<>".join(i.get('availabilities',''))
                timings_dict.update({day:time})
            doc_hosp_ = HospitalDoctor()
            doc_hosp_['sk'] = md5("%s%s%s" % (hct_id, doc_id, doc_name))
            doc_hosp_['hospital_id'] = normalize(hct_id)
            doc_hosp_['doctor_id'] = normalize(doc_id)
            doc_hosp_['doctor_name'] = normalize(doc_name)
            doc_hosp_['doctor_profile_link'] = normalize(doc_link)
            doc_hosp_['qualification'] = normalize(dot_qualifications)
            doc_hosp_['years_of_experience'] = normalize(doc_years_experience)
            doc_hosp_['specialization'] = normalize(doc_specialities)
            doc_hosp_['rating'] = str(doc_rating)
            doc_hosp_['vote_count'] = ''
            doc_hosp_['feedback_count'] = str(doc_feedback)
            doc_hosp_['consultation_fee'] = str(doc_fee_amount)
            doc_hosp_['doctor_image'] = normalize(pics)
            doc_hosp_['doctor_practo_gurantee'] = ''
            doc_hosp_['booking_type'] = normalize(doc_booking_type)
            doc_hosp_['doctor_monday_timing'] = str(timings_dict.get('Mon'))
            doc_hosp_['doctor_tuesday_timing'] = str(timings_dict.get('Tue',''))
            doc_hosp_['doctor_wednesday_timing'] = str(timings_dict.get('Wed',''))
            doc_hosp_['doctor_thursday_timing'] = str(timings_dict.get('Thu'))
            doc_hosp_['doctor_friday_timing'] = str(timings_dict.get('Fri'))
            doc_hosp_['doctor_saturday_timing'] = str(timings_dict.get('Sat'))
            doc_hosp_['doctor_sunday_timing'] = str(timings_dict.get('Sun'))
            doc_hosp_['doctor_on_call'] = normalize(doc_on_call)
            doc_hosp_['reference_url'] = normalize(ref_url)
            yield doc_hosp_
            self.got_page(hct_id, 1)
           



