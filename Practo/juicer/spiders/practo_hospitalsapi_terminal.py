from juicer.utils import *
from juicer.items import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Practohospitalsapi(JuicerSpider):
    name = 'practo_hospitalinfoapi_crawl'
    start_urls = ['https://www.practo.com/client-api/v1/profile/pallavaram-children-medical-centre-pcmc-hospital-pallavaram-1?slug=pallavaram-children-medical-centre-pcmc-hospital-pallavaram-1&profile_type=practices&with_relations=true&is_slug=true&platform=desktop_web&doctors_limit=10&is_hospital=true&is_profile=true&city=chennai&label=hospital&with_seo_data=true&all_amenities=true&mr=true']

    def __init__(self, *args, **kwargs):
        super(Practohospitalsapi, self).__init__(*args, **kwargs)
        self.week_list = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
        self.pattern2 = re.compile('(.*) (.*)')

    def parse(self, response):
        api_data=json.loads(response.body)
        hospital_details = api_data.get('profile',{})
        hospital_id = str(hospital_details.get('id',''))
        hospital_name = hospital_details.get('name','')
        hospital_slug = hospital_details.get('new_slug','')
        hospital_link = "https://www.practo.com/chennai/hospital/"+str(hospital_slug)
        hospital_images = hospital_details.get('photos',[])
        hospital_images = [i.get('url','') for i in hospital_images]
        hosp_street_address = hospital_details.get('street_address','')
        hosp_landmark = hospital_details.get('landmark','')
        hosp_locality = hospital_details.get('locality',{}).get('name','')
        hospital_latitude = hospital_details.get('latitude','')
        hospital_longitude = hospital_details.get('longitude','')
        no_of_doctors_in_hospital = hospital_details.get('doctors_count','')
        hosp_rating = hospital_details.get('clinic_score',{})
        hosp_avg_rating = hosp_rating.get('avg_clinic_rating','')
        hosp_instant_rating = hosp_rating.get('instant_score','')
        number_of_rating_responses = hosp_rating.get('number_of_rating_responses','')
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
        else:
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
            opening_timings='<>'.join(hsp_times)
        hosp_services = hospital_details.get('facilities',{})
        hospital_services = '<>'.join([h_s.get('facility',{}).get('name','') for h_s in hosp_services])
        hospital_emergency_number = hospital_details.get('emergency_phone_number','')
        hosp_amenities = hospital_details.get('amenities',{})
        hospital_amenities = []
        for i,j in hosp_amenities.iteritems():
            hosp_amenitie = j.get('value','')
            if hosp_amenitie==True:
                hospital_amenitie = j.get('name','')
                hospital_amenities.append(hospital_amenitie)
 
        centers_data = hospital_details.get('group_data',{}).get('id','')
        if centers_data:
            centers_url = 'https://www.practo.com/client-api/v1/practicegroups/'+str(centers_data)+'?offset=0&city=chennai&type=clinic&group_id='+str(centers_data)
            yield Request(centers_url, callback=self.center_data)
        hosp_speciality = hospital_details.get('seo_data',{})
        hospital_speciality = hosp_speciality.get('clinicKeyword','')
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
        hospital_feedback_review_details = hosp_feedback_details.get('reviews',[])
        for hospital_feedback_review_detail in hospital_feedback_review_details:
            feedback_sk = hospital_feedback_review_detail.get('review',{}).get('id','')
            feedback_text = hospital_feedback_review_detail.get('review',{}).get('survey_response',{}).get('review_text','')
            feedback_reviewd_on = hospital_feedback_review_detail.get('review',{}).get('survey_response',{}).get('reviewed_on','')
            feedback_for = hospital_feedback_review_detail.get('review',{}).get('review_for','')
            feedback_name = hospital_feedback_review_detail.get('patient',{}).get('name','')
            feeddback_practice_name = hospital_feedback_review_detail.get('review',{}).get('practice_name','')

    def center_data(self, response):
        jscsv_data = {}
        json21 =json.loads(response.body)
        other_cen = json21.get('clinics',[])
        y='<>'.join([i.get('name','') for i in other_cen])

