from juicer.utils import *
from practo_hospitals_xpaths import *
from juicer.items import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Practohospitals(JuicerSpider):
    name = 'practo_hospitalinfo_terminal'
    handle_http_status_list = ['302', '504', '403', 403,'524','502']

    def __init__(self, *args, **kwargs):
        super(Practohospitals, self).__init__(*args, **kwargs)
        self.domain = "https://www.practo.com"
        self.week_list = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
        self.pattern1 = re.compile(r'\((.*?)\)')
        self.pattern2 = re.compile('(.*) (.*)')
        self.feedjson1 = "https://www.practo.com/wave/reviewmoderations/clinicreviews.json?show_recommended_reviews&practice_id="
        self.feedjson2 = "&with_doctor=true&mr=true&page="
        self.feedjson3 = "&show_feedback_summary_tags=true"

    def parse(self, response):
        sel = Selector(response)
        day1= normalize(extract_data(sel, '//p[@data-qa-id="clinic-timings-day"]/span/span[1]/text()'))
        day2=normalize(extract_data(sel, '//p[@data-qa-id="clinic-timings-day"]/span/span[2]/text()'))
        day = day1+'-'+day2
        sa =normalize(extract_data(sel,'//p[@data-qa-id="clinic-timings-session"]/span/span[1]/text()'))+' '+'AM'
        sb = normalize(extract_data(sel,'//p[@data-qa-id="clinic-timings-session"]/span/span[2]/text()'))+' '+'PM'
        sc = sa+'-'+sb
        if day and sc:
            opening_timings1 = day+':-'+sc
        jscsv_data = {}
        try :
            cvss = sel.xpath('//script[contains(text(), "window.__REDUX_STATE__")]/text()').extract()[0].split('window.__REDUX_STATE__=')[1]
            jscsv_data = json.loads(cvss)
        except :
            jscsv_data = {}

        profile_payload = jscsv_data.get('analyticsData', {}).get('profilePayload', {})
        hosp_id = response.meta['sk']
        feedback_count = response.meta['data']['hsp_feed_count']
        hosp_name =  profile_payload.get('name','')
        slug = profile_payload.get('new_slug','')
        doc_ref = 'https://www.practo.com/chennai/hospital/'+normalize(slug)+'/doctors'
        rating_count = str(profile_payload.get('clinic_score',{}).get('number_of_rating_responses',''))
        clinic_location = str(profile_payload.get('locality','').get('name','')) + ', ' + str(profile_payload.get('city','').get('name',''))
        medical_spec = str(profile_payload.get('seo_data',{}).get('clinicKeyword',''))
        number_of_doctors = str(profile_payload.get('relations_count',''))
        hospt_description = ''.join(profile_payload.get('summary', '')).encode('ascii', 'ignore').decode('ascii')
        no_of_beds = str(profile_payload.get('bed_count',''))
        no_of_ambulances = str(profile_payload.get('ambulance_count',''))
        method_of_payment = "<>".join(profile_payload.get('payment_mode',''))
        hospital_address =  str(profile_payload.get('street_address',{})).encode('ascii', 'ignore').decode('ascii') + str(profile_payload.get('landmark',{})).encode('ascii', 'ignore').decode('ascii')
        street_address =  str(profile_payload.get('street_address',{}))
        address_locality = str(profile_payload.get('locality','').get('name',''))
        address_region = str(profile_payload.get('landmark',{}))
        postal_code = ''
        opening_timings = profile_payload.get('has_24x7_timings','')
        if opening_timings == True : opening_timings = 'Open 24 x 7'
        if opening_timings ==False : opening_timings = opening_timings1
        pho = profile_payload.get('photos','')
        hospital_images =  '<>'.join([qua.get('url', {}) for qua in pho])
        amentities_list = []
        hospital_amenities = []
        hosp_amenities = profile_payload.get('amenities',{})
        for i,j in hosp_amenities.iteritems():
            hosp_amenitie = j.get('value','')
            if hosp_amenitie==True:
                hospital_amenitie = j.get('name','')
                hospital_amenities.append(hospital_amenitie)
        amenities = "<>".join(hospital_amenities)
        emergency_contact_number = str(profile_payload.get('emergency_phone_number',''))
        esta = str(profile_payload.get('group_establishment_year',''))
        services = profile_payload.get('facilities')
        services =  '<>'.join([qua.get('facility', {}).get('name', '') for qua in services]) 
        awards= profile_payload.get('awards',[])
        awards = '<>'.join([awa.get('title', '') for awa in awards])
        latitude = str(profile_payload.get('latitude',''))
        longitude =  str(profile_payload.get('longitude',''))
        hosp_pf_link=normalize(response.url)
        rating_values=str(profile_payload.get('clinic_score',{}).get('clinic_score',''))
        y =''
        hospital_meta = HospitalMeta()
        hospital_meta['hospital_id']  = normalize(hosp_id)
        hospital_meta['hospital_name']  = normalize(hosp_name)
        hospital_meta['hospital_profile_link']  = normalize(hosp_pf_link)
        hospital_meta['rating_count']  = normalize(rating_count)
        hospital_meta['rating_value']  = normalize(rating_values)
        hospital_meta['location']  = normalize(clinic_location)
        hospital_meta['medical_specialities']  = normalize(medical_spec)
        hospital_meta['number_of_doctors']  = normalize(number_of_doctors)
        hospital_meta['description']  = normalize(hospt_description)
        hospital_meta['no_of_beds']  = normalize(no_of_beds)
        hospital_meta['no_of_ambulances']  = normalize(no_of_ambulances)
        hospital_meta['method_of_payment']  = normalize(method_of_payment)
        hospital_meta['address']  = normalize(hospital_address)
        hospital_meta['street_address']  = normalize(street_address)
        hospital_meta['locality']  = normalize(address_locality)
        hospital_meta['region']  = normalize(address_region)
        hospital_meta['postal_code']  = normalize(postal_code)
        hospital_meta['opening_timings']  = opening_timings
        hospital_meta['clinic_images']  = normalize(hospital_images)
        hospital_meta['amenities']  = normalize(amenities)
        hospital_meta['emergency_contact_number']  = normalize(emergency_contact_number)
        hospital_meta['services']  = normalize(services)
        hospital_meta['longitude']  = normalize(latitude)
        hospital_meta['latitude']  = normalize(longitude)
        hospital_meta['establishment_data']  = normalize(esta)
        hospital_meta['feedback_count']  = normalize(feedback_count)
        hospital_meta['awards']  = normalize(awards)
        hospital_meta['other_centers']  = normalize(y)
        hospital_meta['reference_url']  = normalize(response.url)
        yield hospital_meta
        grp_id = profile_payload.get('group_data',{}).get('id','')
        if grp_id:
            other_center='https://www.practo.com/client-api/v1/practicegroups/'+str(grp_id)+'?offset=0&city=chennai&type=clinic&group_id='+str(grp_id)
            yield Request(other_center, callback=self.other_center, meta = {"hospital_meta": hospital_meta,"doc_ref":normalize(doc_ref)})
        else:
            yield hospital_meta
        if number_of_doctors and hosp_id:
	        doctors_link = 'https://www.practo.com/client-api/v1/practices/'+str(hosp_id)+'/relations?total_count='+str(number_of_doctors)+'&limit='+str(number_of_doctors)+'&profile_id='+str(hosp_id)+'&profile_type=hospital'
	        yield Request(doctors_link, callback=self.dct_hsp_meta_info, meta={"hsp_id":hosp_id, "doc_ref":normalize(doc_ref)})

    def other_center(self,response):
        hospital_meta = response.meta['hospital_meta']
        jscsv_data = {}
        json21 =json.loads(response.body)
        other_cen = json21.get('clinics',[])
        y='<>'.join([i.get('name','') for i in other_cen])
        hospital_meta.update({'other_centers':normalize(y)})
        yield hospital_meta

    def dct_hsp_meta_info(self,response):
        hct_id = response.meta['hsp_id']
        doc_ref = response.meta['doc_ref']
        jscsv_data = {}
        json12=json.loads(response.body)
        doctor_nodes = json12.get('relations', [])
        final_set = {}
        for hnd in doctor_nodes:
            doc_id = str(hnd.get('id', ''))
            doc_link = str(hnd.get('public_profile_url', ''))
            doc_name = ''.join(hnd.get('doctor','').get('name','')).encode('ascii', 'ignore').decode('ascii')
            dct_qualifications = hnd.get('doctor','').get('qualifications', [])
            doc_qualifications = '<>'.join([qua.get('qualification', {}).get('name', '') for qua in dct_qualifications])
            doc_years_experience = str(hnd.get('doctor','').get('experience_years', ''))
            if not doc_years_experience:
                doc_years_experience = str(hnd.get('experience_year', ''))
            #dct_photo = hnd.get('profile_photo', {}).get('photo_url', '')
            dct_specialization = hnd.get('doctor','').get('specializations',[])
            doc_specialities = '<>'.join([spe.get('subspecialization',{}).get('subspecialization','') for spe in dct_specialization])
            doc_rating = str(hnd.get('doctor','').get('recommendation',{}).get('patient_experience_score',''))
            doc_votes=''
            if doc_rating:
                doc_rating= doc_rating+ ' '+ "%"
                doc_votes = str(hnd.get('doctor','').get('recommendation',{}).get('response_count',''))
                if doc_votes:
                    doc_votes= doc_votes+' '+'votes'
                else :
                    doc_votes =''
            #dct_services = '<>'.join([ser.get('service', {}).get('name', '') for ser in hnd.get('services', [])])
            pics = ''
            pics = hnd.get('doctor','').get('photos', [])
            pics= '<>'.join([i.get('photo_url', '') for i in pics])
            doc_fee_amount = str(hnd.get('consultation_fee',''))
            slug_id = hnd.get('doctor','').get('new_slug','')
            ref_url ='https://www.practo.com/chennai/doctor/'+str(slug_id)+'?specialization='+doc_specialities
            dct_booking_type = hnd.get('on_call', '')
            if dct_booking_type == True or dct_booking_type == 'True' or dct_booking_type == 'true':
                doc_booking_type = "Call Now"
            else:
                doc_booking_type = "Book Appointment"
            doc_on_calls = hnd.get('on_call','')
            if doc_on_calls ==True:
                doc_on_call = 'ON-CALL'
            else:
                doc_on_call =''
            visit_times = hnd.get('visit_timings', [])
            hsp_timesch1,hsp_timesch = [],[]
            if not visit_times:
                visit_times = []
            for vit in visit_times:
                vit_days = vit.get('days', [])
                vit_timisng = vit.get('timings', [])
                vit_day_list, vit_timisng_list = [], []
                for vdi in vit_days:
                    from_vdi = vdi.get('from', '').strip()
                    to_vdi = vdi.get('to', '').strip()
                    fromto = ''
                    if from_vdi == to_vdi:
                        fromto = from_vdi
                    else:
                        fromto = ("%s%s%s" % (from_vdi, '-', to_vdi)).strip()
                    vit_day_list.append(fromto)
                for dft in vit_timisng:
                    from_time = dft.get('from', '').strip()
                    to_time = dft.get('to', '').strip()
                    toa_time = ('%s%s%s'% (from_time, '-', to_time)).strip()
                    vit_timisng_list.append(toa_time)
                for toalid in vit_timisng_list:
                    for toada in vit_day_list:
                        hsp_timesch1.append("%s%s%s" % (toada, ' ', toalid))
	        hsp_timesch = '<>'.join(hsp_timesch1)
	        final_set = {'MON':[], 'TUE':[], 'WED':[], 'THU':[], 'FRI':[], 'SAT':[], 'SUN':[]}
            if hsp_timesch:
                hso_timesc_list = hsp_timesch.split('<>')
                for sc in hso_timesc_list:
                    if sc:
                        if self.pattern2.search(sc):
                            weeks, slots = self.pattern2.findall(sc)[0]
                            scslots = []
                            if ',' in weeks:
                                weeksf_list = []
                                try:
                                    weeks1f, weeks2f = weeks.split(',')
                                    weeksf_list = [weeks1f, weeks2f]
                                except:
                                    try:
                                        weeks1f, weeks2f, weeks3f = weeks.split(',')
                                        weeksf_list = [weeks1f, weeks2f, weeks3f]
                                    except:
                                        weeks1f, weeks2f, weeks3f, weeks4f = weeks.split(',')
                                        weeksf_list = [weeks1f, weeks2f, weeks3f, weeks4f]
                                scs_lots = []
                                for weekf_ in weeksf_list:
                                    scslotsi = []
                                    if weekf_ and '-' in weekf_:
                                        a1 = self.week_list.index(weekf_.split('-')[0].strip())
                                        b1 = self.week_list.index(weekf_.split('-')[1].strip())
                                        if a1<b1:
                                            scslotsi = self.week_list[a1:b1+1]
                                        else:
                                            scsl1 = self.week_list[a1:]
                                            scsl2 = self.week_list[:b1+1]
                                    else:
                                        scslots1 = [weekf_.strip()]
                                    if scslotsi: scs_lots.extend(scslotsi)
                                if scs_lots: scslots = scs_lots
                            elif '-' in weeks:
                                a1 = self.week_list.index(weeks.split('-')[0])
                                b1 = self.week_list.index(weeks.split('-')[1])
                                if a1<b1:
                                    scslots = self.week_list[a1:b1+1]
                                else:
                                    scsl1 = self.week_list[a1:]
                                    scsl2 = self.week_list[:b1+1]
                                    scslots = scsl1+scsl2
                            else:
                                scslots = [weeks]
                            if scslots:
                                for inns in scslots:
                                    final_set[inns].extend([slots])
            final_dict = dict((k, v) for k, v in final_set.iteritems() if v)
            doc_hosp_ = HospitalDoctor()
            doc_hosp_['sk'] = md5("%s%s%s" % (hct_id, doc_id, doc_name))
            doc_hosp_['hospital_id'] = normalize(hct_id)
            doc_hosp_['doctor_id'] = normalize(doc_id)
            doc_hosp_['doctor_name'] = normalize(doc_name)
            #doc_hosp_['doctor_profile_link'] = normalize(ref_url)
            doc_hosp_['qualification'] = normalize(doc_qualifications)
            doc_hosp_['years_of_experience'] = normalize(doc_years_experience)
            doc_hosp_['specialization'] = normalize(doc_specialities)
            doc_hosp_['rating'] = normalize(doc_rating)
            doc_hosp_['vote_count'] = normalize(doc_votes.replace('(','').replace(')',''))
            #doc_hosp_['feedback_count'] = normalize(doc_feedback_count.replace('(','').replace(')',''))
            doc_hosp_['consultation_fee'] = normalize(doc_fee_amount)
            doc_hosp_['doctor_image'] = normalize(pics)
            #doc_hosp_['doctor_practo_gurantee'] = normalize(doc_practo_gua)
            doc_hosp_['booking_type'] = normalize(doc_booking_type)
            doc_hosp_['doctor_monday_timing'] = normalize('<>'.join(final_dict.get('MON',[])))
            doc_hosp_['doctor_tuesday_timing'] = normalize('<>'.join(final_dict.get('TUE',[])))
            doc_hosp_['doctor_wednesday_timing'] = normalize('<>'.join(final_dict.get('WED',[])))
            doc_hosp_['doctor_thursday_timing'] = normalize('<>'.join(final_dict.get('THU',[])))
            doc_hosp_['doctor_friday_timing'] = normalize('<>'.join(final_dict.get('FRI',[])))
            doc_hosp_['doctor_saturday_timing'] = normalize('<>'.join(final_dict.get('SAT',[])))
            doc_hosp_['doctor_sunday_timing'] = normalize('<>'.join(final_dict.get('SUN',[])))
            doc_hosp_['doctor_on_call'] = normalize(doc_on_call)
            doc_hosp_['reference_url'] = normalize(doc_ref)
            yield Request(ref_url, self.parse_feedback,meta={"doc_hosp_":doc_hosp_,'hct_id':normalize(hct_id)})

    def parse_feedback(self, response):
        sel = Selector(response)
        hct_id =response.meta['hct_id']
        doc_hosp_ = response.meta['doc_hosp_']
        fedback = extract_data(sel, '//li[@data-qa-id="feedback-tab"]/span[contains(text(),"Feedback")]/../text()').strip('(').strip(')').strip()
        gurre = normalize(extract_data(sel , '//div[@class="u-spacer--top"]/a/@href'))
        if gurre:guree = 'This appointment is guaranteed by Practo'
        else : guree=''
        doc_hosp_.update({'doctor_practo_gurantee':guree,'feedback_count':normalize(fedback),'doctor_profile_link':normalize(response.url)})
        yield doc_hosp_
        self.got_page(hct_id, 1)


