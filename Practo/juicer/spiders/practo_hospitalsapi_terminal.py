from juicer.utils import *
from juicer.items import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Practohospitalsapi(JuicerSpider):
    name = 'practo_hospitalsapi_terminal'

    def __init__(self, *args, **kwargs):
        super(Practohospitalsapi, self).__init__(*args, **kwargs)
        self.week_list = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
        self.pattern2 = re.compile('(.*) (.*)')

    def parse(self, response):
        api_data = json.loads(response.body)
        response_url = response.meta.get('data').get('main_link','')
        doc_booking_type = response.meta.get('data').get('book_type','')
        hosp_feedback_count = api_data.get('feedback','').get('reviews_count','')
        hospital_details = api_data.get('profile',{})
        hospital_id = str(hospital_details.get('id',''))
        hospital_name = hospital_details.get('name','')
        hospital_slug = hospital_details.get('new_slug','')
        hospital_link = "https://www.practo.com/chennai/hospital/"+str(hospital_slug)
        hospital_images = hospital_details.get('photos',[])
        hospital_images ='<>'.join([i.get('url','') for i in hospital_images])
        hospital_address = str(hospital_details.get('street_address',{})).encode('ascii', 'ignore').decode('ascii') + str(hospital_details.get('landmark',{})).encode('ascii', 'ignore').decode('ascii')
        street_address = hospital_details.get('street_address','')
        hosp_landmark = hospital_details.get('landmark','')
        hosp_locality = hospital_details.get('locality',{}).get('name','')
       
        latitude = hospital_details.get('latitude','')
        longitude = hospital_details.get('longitude','')
        no_of_doctors_in_hospital = hospital_details.get('doctors_count','')
        no_of_ambulances = str(hospital_details.get('ambulance_count',''))
        hosp_rating = hospital_details.get('clinic_score',{})
        hosp_avg_rating = hosp_rating.get('avg_clinic_rating','')
        hosp_instant_rating = hosp_rating.get('instant_score','')
        star_rating = hosp_rating.get('clinic_score','')
        rating_responses = hosp_rating.get('number_of_rating_responses','')
        number_of_wait_time_responses_rating = hosp_rating.get('number_of_wait_time_responses','')
        hospital_beds = hospital_details.get('bed_count','')
        hospital_book_type = str(hospital_details.get('status',''))
        if hospital_book_type == 'VN' : hospital_booking_type='Call Now'
        if hospital_book_type == 'ABS' : hospital_booking_type='Book Appointment'
        hospital_pay_mode = '<>'.join(hospital_details.get('payment_mode',''))
        hospital_summary = hospital_details.get('summary','')
        hosp_accred = hospital_details.get('accreditations',[])
        hospital_accreditations = '<>'.join([h_ac.get('accreditation_body',{}).get('title','') for h_ac in hosp_accred])
        hosp_award = hospital_details.get('awards',[])
        if hosp_award:
            hosp_year = [str(h_a.get('awarded_year','')) for h_a in hosp_award]
            hosp_title = [h_t.get('title','') for h_t in hosp_award]
            hospital_awards = '<>'.join(map(lambda a, b: a +', '+ b, hosp_title, hosp_year))
        else:
            hospital_awards=''
        hospital_timings = hospital_details.get('has_24x7_timings','')
        if hospital_timings == True :
            opening_timings = 'Open 24 x 7'
        else : opening_timings = ''
        hsp_times = []
        hosp_times = hospital_details.get('timings', [])
        for vit in hosp_times:
                vit_days1 = vit.get('days', [])
                vit_timisng1 = vit.get('timings', [])
                vit_day_list1, vit_timisng_list1 = [], []
                for vdi in vit_days1:
                    from_vdi = vdi.get('from', '').strip()
                    to_vdi = vdi.get('to', '').strip()
                    fromto = ''
                    if from_vdi == to_vdi:
                        fromto = from_vdi
                    else:
                        fromto = ("%s%s%s" % (from_vdi, '-', to_vdi)).strip()
                    vit_day_list1.append(fromto)
                for dft in vit_timisng1:
                    from_time = dft.get('from', '').strip()
                    to_time = dft.get('to', '').strip()
                    toa_time = ('%s%s%s'% (from_time, '-', to_time)).strip()
                    vit_timisng_list1.append(toa_time)
                for toalid in vit_timisng_list1:
                    for toada in vit_day_list1:
                        hsp_times.append("%s%s%s" % (toada, ':-', toalid))
        sch_timings='<>'.join(hsp_times)
        if not opening_timings : opening_times = sch_timings
        esta = str(hospital_details.get('group_establishment_year',''))
        hosp_services = hospital_details.get('facilities',{})
        hospital_services = '<>'.join([h_s.get('facility',{}).get('name','') for h_s in hosp_services])
        emergency_contact_number = hospital_details.get('emergency_phone_number','')
        hosp_amenities = hospital_details.get('amenities',{})
        hospital_amenities = []
        for i,j in hosp_amenities.iteritems():
            hosp_amenitie = j.get('value','')
            if hosp_amenitie==True:
                hospital_amenitie = j.get('name','')
                hospital_amenities.append(hospital_amenitie)
        amenities = "<>".join(hospital_amenities)
        aux_infos = {}
        hosp_speciality = hospital_details.get('seo_data',{})
        hospital_speciality = hosp_speciality.get('clinicKeyword','')
        hospital_item = HospitalInfo()
        hospital_item['hospital_id']                 = str(hospital_id)
        hospital_item['hospital_name']               = normalize(hospital_name)
        hospital_item['hospital_link']               = normalize(hospital_link)
        hospital_item['hospital_images']             = str(hospital_images)
        hospital_item['hospital_location']           = normalize(hosp_locality)
        hospital_item['hospital_speciality']         = normalize(hospital_speciality)
        hospital_item['no_of_doctors_in_hospital']   = str(no_of_doctors_in_hospital)
        hospital_item['hospital_star_rating']        = str(star_rating)
        hospital_item['hospital_feedback_count']     = str(hosp_feedback_count)
        hospital_item['hospital_practo_gurantee']    = ''
        hospital_item['hospital_booking_type']       = normalize(doc_booking_type)
        hospital_item['hospital_open_timings']       = str(opening_timings)
        hospital_item['hospital_schedule_timeslot']  = normalize(opening_times)
        hospital_item['hospital_accredited']         = normalize(hospital_accreditations)
        hospital_item['reference_url']               = normalize(response_url)
        if aux_infos:
            hospital_item['aux_info']                    = normalize(json.dumps(aux_infos))

        hospital_meta = HospitalMeta()
        hospital_meta['hospital_id']  = normalize(hospital_id)
        hospital_meta['hospital_name']  = normalize(hospital_name)
        hospital_meta['hospital_profile_link']  = normalize(hospital_link)
        hospital_meta['rating_count']  = str(rating_responses)
        hospital_meta['rating_value']  = str(star_rating)
        hospital_meta['location']  = normalize(hosp_locality)
        hospital_meta['medical_specialities']  = normalize(hospital_speciality)
        hospital_meta['number_of_doctors']  = str(no_of_doctors_in_hospital)
        hospital_meta['description']  = normalize(hospital_summary)
        hospital_meta['no_of_beds']  = str(hospital_beds)
        hospital_meta['no_of_ambulances']  = str(no_of_ambulances)
        hospital_meta['method_of_payment']  = normalize(hospital_pay_mode)
        hospital_meta['address']  = normalize(hospital_address)
        hospital_meta['street_address']  = normalize(street_address)
        hospital_meta['locality']  = normalize(hosp_locality)
        hospital_meta['region']  = normalize(hosp_landmark)
        hospital_meta['postal_code']  = ''
        hospital_meta['opening_timings']  = opening_timings
        hospital_meta['clinic_images']  = normalize(hospital_images)
        hospital_meta['amenities']  = normalize(amenities)
        hospital_meta['emergency_contact_number']  = normalize(emergency_contact_number)
        hospital_meta['services']  = normalize(hospital_services)
        hospital_meta['longitude']  = str(latitude)
        hospital_meta['latitude']  = str(longitude)
        hospital_meta['establishment_data']  = normalize(esta)
        hospital_meta['feedback_count']  = normalize(hosp_feedback_count)
        hospital_meta['awards']  = normalize(hospital_awards)
        hospital_meta['other_centers']  = ''
        hospital_meta['reference_url']  = normalize(response_url) 
        centers_data = hospital_details.get('group_data',{}).get('id','')
        hsp_doc_nodes = hospital_details.get('relations', [])
        for hsp_doc_node in hsp_doc_nodes:
            doc_id = str(hsp_doc_node.get('doctor','').get('id', ''))
            doc_link = str(hsp_doc_node.get('doctor','').get('public_profile_url', ''))
            if doc_link : doc_link = 'https://www.practo.com'+doc_link
            else : doc_link = ''
            doc_name = ''.join(hsp_doc_node.get('doctor','').get('name',''))
            dct_qualifications = hsp_doc_node.get('doctor','').get('qualifications', [])
            doc_qualifications = '<>'.join([qua.get('qualification', {}).get('name', '') for qua in dct_qualifications])
            doc_years_experience = str(hsp_doc_node.get('doctor','').get('experience_years', ''))
            dct_specialization = hsp_doc_node.get('doctor','').get('specializations',[])
            doc_specialities = '<>'.join([spe.get('subspecialization',{}).get('subspecialization','') for spe in dct_specialization])
            doct_rat_vote = hsp_doc_node.get('doctor','').get('recommendation',{})
            doc_rat = str(doct_rat_vote.get('patient_experience_score',''))
            if doc_rat:
                doc_vote = str(doct_rat_vote.get('response_count',''))
            else:
                doc_vote = ''
            doc_consultation_fee = str(hsp_doc_node.get('consultation_fee',''))
            doc_image = hsp_doc_node.get('doctor','').get('photos',[])
            doc_do=[do_im.get('photo_url','') for do_im in doc_image][-1]
            doc_images = ''.join(doc_do)
            doc_book_type = str(hsp_doc_node.get('status',''))
            if doc_book_type == 'VN' :
                doc_booking_type='Call Now'
                doctor_practo_gurantee = ''
            if doc_book_type == 'ABS':
                doc_booking_type='Book Appointment'
                doctor_practo_gurantee   = 'This appointment is guaranteed by Practo'
            doc_on_calls = hsp_doc_node.get('on_call','')
            if doc_on_calls ==True:
                doc_on_call = 'ON-CALL'
            else:
                doc_on_call = ''
            hsp_timesch1 = []
            visit_times = hsp_doc_node.get('visit_timings', [])
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
                                        weeksf_list = [weeks1f, weeks2f]
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
                                            scslotsi = scsl1+scsl2
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
            hsp_doc_sk = md5("%s%s%s" % (hospital_id,doc_id,doc_name))
            doctor_ref_url = hospital_link+'/doctors'
            feedback_count=''
            if hospital_id and doc_id:
                doctor_hospital = HospitalDoctor()
                doctor_hospital.update({"sk":normalize(hsp_doc_sk),"hospital_id":normalize(hospital_id),"doctor_id":normalize(doc_id),
                                        "doctor_name":normalize(doc_name),"doctor_profile_link":normalize(doc_link),
                                        "qualification":normalize(doc_qualifications),"years_of_experience":normalize(doc_years_experience),
                                        "specialization":normalize(doc_specialities),"rating":normalize(doc_rat),
                                        "vote_count":normalize(doc_vote),"feedback_count":normalize(feedback_count),
                                        "consultation_fee":normalize(doc_consultation_fee),"doctor_image":normalize(doc_images),
                                        "doctor_practo_gurantee":normalize(doctor_practo_gurantee),"booking_type":normalize(doc_booking_type),
                                        "doctor_monday_timing":normalize('<>'.join(final_dict.get('MON',[]))),
                                        "doctor_tuesday_timing":normalize('<>'.join(final_dict.get('TUE',[]))),
                                        "doctor_wednesday_timing":normalize('<>'.join(final_dict.get('WED',[]))),
                                        "doctor_thursday_timing":normalize('<>'.join(final_dict.get('THU',[]))),
                                        "doctor_friday_timing":normalize('<>'.join(final_dict.get('FRI',[]))),
                                        "doctor_saturday_timing":normalize('<>'.join(final_dict.get('SAT',[]))),
                                        "doctor_sunday_timing":normalize('<>'.join(final_dict.get('SUN',[]))),
                                        "doctor_on_call":normalize(doc_on_call),"reference_url":normalize(doctor_ref_url)})
                yield doctor_hospital

            hosp_feedback_details = api_data.get('feedback',{})
            hospital_feedback_count = hosp_feedback_details.get('reviews_count','')
            hospital_page_count = hosp_feedback_details.get('page_count','')
            for p_c in range(1,hospital_page_count):
                hospital_rev_link = 'https://www.practo.com/client-api/v1/feedback/clinicreviews?slug=%s&profile_type=hospital&page=%s&mr=true&show_feedback_summary_tags=true'%(hospital_slug,h_c)
                yield Request(hospital_rev_link, callback=self.feedback,meta={'feedback_count':hospital_feedback_count,'dct_id':doc_id,'dct_url':doc_link})
            if centers_data:
                centers_url = 'https://www.practo.com/client-api/v1/practicegroups/'+str(centers_data)+'?offset=0&city=chennai&type=clinic&group_id='+str(centers_data)
                yield Request(centers_url, callback=self.center_data, meta = {"hospital_meta": hospital_meta})
            else :
                yield hospital_meta
                #self.got_page(sk_d, 1)
                


 

    def feedback(self,response):
            tmp = json.loads(response.body)
            feedback_count = response.meta.get('feedback_count','')
            dct_id = response.meta.get('dct_id','')
            dct_url = response.meta.get('dct_url','')
            total_pages = tmp.get('page_count','')
            current_page = tmp.get('page','')
            reviews_count = tmp.get('reviews_count','')
            total_count = tmp.get('total_count','')
            if not total_count:
                total_count = feedback_count
            review_nodes = tmp.get('reviews',{})
            if review_nodes:
                for nod in review_nodes:
                    review_inner = nod.get('review',{})
                    rev_sur = review_inner.get('survey_response',{})
                    status = review_inner.get('status','')
                    revi_id = str(review_inner.get('id',''))
                    review_text = rev_sur.get('review_text','')
                    revia_id = str(rev_sur.get('id',''))
                    reviewd_on = rev_sur.get('reviewed_on','')
                    rev_channe = rev_sur.get('channel','')
                    review_source = rev_sur.get('source','')
                    review_anony = rev_sur.get('anonymous','')
                    review_unread = str(review_inner.get('unread',''))
                    review_for = review_inner.get('review_for','')
                    review_doc_id = str(review_inner.get('doctor_id',''))
                    review_practice_id = str(review_inner.get('practice_id',''))
                    review_practice_name = review_inner.get('practice_name','')
                    review_like = review_inner.get('recommendation','').lower()
                    review_view_count = review_inner.get('view_count','')
                    review_publ_dur = review_inner.get('publish_time_duration','')
                    revewi_status_mod = review_inner.get('status_modified_at','')
                    review_cronfre = review_inner.get('cron_frequency','')
                    review_reply_text = review_inner.get('review_reply',{}).get('reply_text','')
                    patient_innter = nod.get('patient',{})
                    review_name = patient_innter.get('name','')
                    contexts_inner = nod.get('contexts',{})
                    review_filter_type, review_filter_text = ['']*2
                    if contexts_inner:
                        review_filter_type = contexts_inner[0].get('type','')
                        review_filter_text = contexts_inner[0].get('text','')
                    helpful_inner = nod.get('found_helpful_data',{})
                    helpful_overallcount = helpful_inner.get('review_total_count','')
                    helpful_count = helpful_inner.get('review_yes_count','')
                    practice_inner = nod.get('practice',{})
                    practice_name = practice_inner.get('name','')
                    practice_id = str(practice_inner.get('id',''))
                    practice_locality = practice_inner.get('locality','')
                    practice_city = practice_inner.get('city','')
                    review_item = HospitalFeedback()
                    review_item['sk'] = md5("%s%s%s%s%s%s"%(revi_id, revia_id, reviewd_on, review_doc_id, review_name, dct_id))
                    review_item['feedback_count'] = normalize(str(feedback_count))
                    review_item['hospital_id'] = normalize(dct_id)
                    review_item['feedback_text'] = normalize(review_text)
                    review_item['feedback_publish_date'] = normalize(reviewd_on)
                    review_item['feedback_for'] = normalize(review_for)
                    review_item['feedback_practice_name'] = normalize(review_practice_name)
                    review_item['feedback_practice_locality'] = normalize(practice_locality)
                    review_item['feedback_practice_city'] = normalize(practice_city)
                    review_item['feedback_like'] = normalize(review_like)
                    review_item['feedback_name'] = normalize(review_name)
                    review_item['feedback_filters'] = normalize(review_filter_text)
                    review_item['feedback_helpful_count'] = normalize(helpful_count)
                    review_item['feedback_helpful_overallcount'] = normalize(helpful_overallcount)
                    review_item['feedback_reply'] = normalize(review_reply_text)
                    review_item['reference_url']= normalize(dct_url)
                    yield review_item

    def center_data(self, response):
        jscsv_data = {}
        json21 =json.loads(response.body)
        other_cen = json21.get('clinics',[])
        y='<>'.join([i.get('name','') for i in other_cen])
        hospital_meta.update({'other_centers':normalize(y)})
        yield hospital_meta

