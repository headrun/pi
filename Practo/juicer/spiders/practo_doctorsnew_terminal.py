from juicer.utils import *
from practo_doctorsinfo_xpaths import *
from juicer.items import *

class Practodoctorsinfot(JuicerSpider):
    name = 'practo_doctorsnew_terminal'
    handle_http_status_list = ['302', '504','403','404']
    def __init__(self, *args, **kwargs):
        super(Practodoctorsinfot, self).__init__(*args, **kwargs)
        self.domain = "https://www.practo.com"
        self.pattern1 = re.compile(r'\((.*?)\)')
        self.pattern2 = re.compile('(.*) (.*)')
        self.week_list = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']

    def parse(self, response):
        sel = Selector(response)
        city_browse = json.loads(response.meta.get('data')).get('city', '')
        json_data = json.loads(response.body)
        if json_data:
            profile_payload = json_data.get('profile',{})
            dct_id = str(profile_payload.get('id', ''))
            dct_profile = str(profile_payload.get('public_profile_url', ''))
            dct_name = str(profile_payload.get('name', ''))
            dct_qualifications = profile_payload.get('qualifications', [])
            dct_qualifications = '<>'.join([qua.get('qualification', {}).get('name', '') for qua in dct_qualifications])
            dct_experience = str(profile_payload.get('experience_years', ''))
            if not dct_experience:
                dct_experience = str(profile_payload.get('experience_year', ''))
            dct_photo = profile_payload.get('profile_photo', {}).get('photo_url', '')
            if '/bundles/practopractoapp/images/profile.png' in dct_photo: dct_photo = ''
            dct_specialization = profile_payload.get('specializations',[])[0].get('subspecialization','{}').get('speciality','{}').get('speciality','')
            dct_verification = json_data.get('profile',{}).get('verification','').get('verification_status','')
            if 'VERIFIED' in dct_verification:
                dct_verification = 'Medical Registration Verified'
            dct_rating = profile_payload.get('recommendation',{}).get('patient_experience_score','')  
            dct_votes = profile_payload.get('profile',{}).get('recommendation',{}).get('response_count','')
            dct_summary = profile_payload.get('summary', '')
            dct_services = '<>'.join([ser.get('service', {}).get('name', '') for ser in profile_payload.get('services', [])])
            dct_specializations = '<>'.join([speci.get('subspecialization', {}).get('subspecialization', '') for speci in profile_payload.get('specializations', [])])
            dec_edu_ls, dec_awa_ls = [], []
            for qudct in profile_payload.get('qualifications', []):
                collge_nmae = qudct.get('college', {}).get('name')
                qu_namect = qudct.get('qualification', {}).get('name')
                qu_com_year = qudct.get('completion_year', '')
                total_qua_string = "%s%s%s%s%s" % (qu_namect, ' - ', collge_nmae, ', ', qu_com_year)
                dec_edu_ls.append(total_qua_string.strip().strip(',').strip().strip('-'))
            dct_education = '<>'.join(dec_edu_ls)
            for qudaw in profile_payload.get('awards', []):
                qu_tit = qudaw.get('title', '')
                qu_year = str(qudaw.get('awarded_year', ''))
                qu_summ = qudaw.get('summary', '')
                if qu_summ:
                    file("date_practo_awards_summary","ab+").write("%s\n" %normalize(response.url))
                total_qa_string = "%s%s%s" % (qu_tit, ' - ', qu_year)
                dec_awa_ls.append(total_qa_string.strip().strip(',').strip().strip('-'))
            dct_awards = '<>'.join(dec_awa_ls)
            dct_memberships = '<>'.join([meser.get('membership_council', {}).get('name', '') for meser in profile_payload.get('memberships', [])])
            dct_organizations = profile_payload.get('organizations', [])
            final_orga = []
            for dctn in dct_organizations:
                exp_years1 = dctn.get('tenure_start', '').split('-')[0]
                exp_years2 = dctn.get('tenure_end', '').split('-')[0]
                exp_role = dctn.get('role', '')
                exp_org_name = dctn.get('organization_name', '')
                exp_years_both = ('%s%s%s' % (exp_years1,' - ', exp_years2)).strip().strip('-').strip()
                exp_at = ''
                if exp_org_name:
                    exp_at = '%s%s' % (' at ', exp_org_name)
                exp_total = ("%s%s%s%s"%(exp_years_both, ' ', exp_role, exp_at)).strip()
                if exp_total:
                    final_orga.append(exp_total)
            final_orga = '<>'.join(final_orga)
            dct_registrations = profile_payload.get('registrations',[])
            final_regin = []
            if dct_registrations:
                for dctr in dct_registrations:
                    registr_number = dctr.get('registration_number', '')
                    registr_name = dctr.get('registration_council', {}).get('name', '')
                    registr_year = str(dctr.get('registration_year', ''))
                    regsitr_total = ("%s%s%s%s%s"%(registr_number,' ',registr_name, ', ', registr_year)).strip().strip(',').strip()
                    if regsitr_total: final_regin.append(regsitr_total)
            final_regin = '<>'.join(final_regin)
            feedback_count = json_data.get('feedback',{}).get('reviews_count','')
            sk_d = response.meta.get('sk','')
            if dct_id:
                doctor_meta  = DoctorMeta()
                doctor_meta['sk'] = normalize(sk_d)
                doctor_meta['doctor_id'] = normalize(dct_id)
                doctor_meta['doctor_name'] = normalize(dct_name)
                doctor_meta['doctor_profile_link'] = normalize(dct_profile)
                doctor_meta['qualification'] = normalize(dct_qualifications)
                doctor_meta['specialization'] = normalize(dct_specialization)
                doctor_meta['years_of_experience'] = normalize(dct_experience)
                doctor_meta['specialization'] = normalize(dct_specialization)
                doctor_meta['medical_registration_verified'] = normalize(dct_verification)
                doctor_meta['rating'] = str(dct_rating)
                doctor_meta['vote_count'] =  str(dct_votes)
                doctor_meta['summary'] = normalize(dct_summary)
                doctor_meta['services'] =  normalize(dct_services)
                doctor_meta['specializations'] = normalize(dct_specializations)
                doctor_meta['education'] = normalize(dct_education)
                doctor_meta['memeberships'] = normalize(dct_memberships)
                doctor_meta['experience'] = normalize(final_orga)
                doctor_meta['registrations'] = normalize(final_regin)
                doctor_meta['feedback_count'] = str(feedback_count)
                doctor_meta['doctor_image'] = normalize(dct_photo)
                doctor_meta['reference_url'] = normalize(response.url)
                doctor_meta['aux_info'] = json.dumps({"city": (city_browse)})
                yield doctor_meta

            hos_parit_link = ''
            hospital_nodes = profile_payload.get('relations', [])
            for hnd in hospital_nodes:
                hsp_practice_data = hnd.get('practice', {})
                hsp_city_prc = hsp_practice_data.get('city', {}).get('name', '')
                hsp_loality = hsp_practice_data.get('locality', {}).get('name', '')
                hsp_location = ("%s%s%s" % (hsp_loality, ', ', hsp_city_prc)).strip().strip(',').strip()
                hsp_new_slug = hsp_practice_data.get('new_slug', '')
                hsp_link = "%s%s%s" % (hos_parit_link, '/clinic/', hsp_new_slug)
                hsp_name =  hsp_practice_data.get('name', '')
                hsp_star_rat =  hsp_practice_data.get('clinic_score', {}).get('clinic_score', '')
                hsp_stree_add = hsp_practice_data.get('street_address', '')
                hsp_landmark = hsp_practice_data.get('landmark', '')
                if hsp_landmark:
                    hsp_stree_add = ('%s%s%s%s%s' % (hsp_stree_add, ', Landmark: ', hsp_landmark, ',', hsp_city_prc)).strip().strip(',').strip()
                else:
                    hsp_stree_add = ('%s%s%s' % (hsp_stree_add,', ', hsp_city_prc)).strip().strip(',').strip()
                hsp_address = hsp_stree_add
                hsp_photos = '<>'.join([dfp.get('url', '') for dfp in hsp_practice_data.get('default_photos', [])]).strip()
                hsp_booking_type = hnd.get('on_call', '')
                if hsp_booking_type == True or hsp_booking_type == 'True' or hsp_booking_type == 'true':
                    hsp_booking_type = "Call Now"
                else:
                    hsp_booking_type = "Book Appointment"
                hsp_map_latitude = str(hsp_practice_data.get('latitude', ''))
                hsp_map_longitude = str(hsp_practice_data.get('longitude', ''))
                hsp_consultation_fee = hnd.get('consultation_fee', '')
                hsp_practo_gura = hnd.get('has_gc', '')
                if hsp_practo_gura == True or hsp_practo_gura == 'True' or hsp_practo_gura == 'true':
                    hsp_practo_gura = 'yes'
                else: hsp_practo_gura = 'no'
                visit_times = hnd.get('visit_timings', [])
                hsp_timesch = []
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
                            hsp_timesch.append("%s%s%s" % (toada, ' ', toalid))
                hsp_timesch = '<>'.join(hsp_timesch)
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
                doctor_hospital = DoctorHospital()
                doctor_hospital['sk'] = md5("%s%s%s%s%s%s"%(hsp_link, hsp_name, hsp_address, hsp_map_latitude, hsp_consultation_fee, dct_id))
                doctor_hospital['doctor_id'] = normalize(dct_id)
                doctor_hospital['hospital_location'] = normalize(hsp_location)
                doctor_hospital['hospital_link'] = normalize(hsp_link)
                doctor_hospital['hospital_name'] =  normalize(hsp_name)
                doctor_hospital['hospital_rating'] = normalize(str(hsp_star_rat))
                doctor_hospital['hospital_address'] = normalize(hsp_address)
                doctor_hospital['hospital_monday_timing'] = normalize('<>'.join(final_dict.get('MON',[])))
                doctor_hospital['hospital_tuesday_timing'] = normalize('<>'.join(final_dict.get('TUE',[])))
                doctor_hospital['hospital_wednesday_timing'] =  normalize('<>'.join(final_dict.get('WED',[])))
                doctor_hospital['hospital_thursday_timing'] = normalize('<>'.join(final_dict.get('THU',[])))
                doctor_hospital['hospital_friday_timing'] = normalize('<>'.join(final_dict.get('FRI',[])))
                doctor_hospital['hospital_saturday_timing'] = normalize('<>'.join(final_dict.get('SAT',[])))
                doctor_hospital['hospital_sunday_timing'] = normalize('<>'.join(final_dict.get('SUN',[])))
                doctor_hospital['hospital_consultation_fee'] = normalize(hsp_consultation_fee)
                doctor_hospital['hospital_practo_gurantee'] = normalize(hsp_practo_gura)
                doctor_hospital['hospital_photos'] = normalize(hsp_photos)
                doctor_hospital['hospital_booking_type'] = normalize(hsp_booking_type)
                doctor_hospital['hospital_latitude'] = normalize(hsp_map_latitude)
                doctor_hospital['hospital_longitude'] = normalize(hsp_map_longitude)
                doctor_hospital['reference_url'] = normalize(response.url)
                yield doctor_hospital
		print '2'
            slug = profile_payload.get('new_slug','')
            doc_feedback_details = json_data.get('feedback',{})
            doc_feedback_count = doc_feedback_details.get('feedback_count','')
            import pdb;pdb.set_trace()
            doc_page_count = int(doc_feedback_details.get('page_count',''))
            for p_c in range(1,doc_page_count):
                    #feed_api_link = "https://www.practo.com/client-api/v1/feedback/doctorreviews?slug=%s&profile_type=doctor&page=%s&mr=true&active_filter[id]=0&active_filter[text]=All&active_filter[type]=All&show_recommended_reviews=true&show_feedback_summary_tags=true"%(slug,p_c)
                    feed_api_link =  "https://www.practo.com/client-api/v1/feedback/doctorreviews?slug=dr-g-shanmugasundar-diabetologist&profile_type=doctor&page=2&mr=true&active_filter[id]=0&active_filter[text]=All&active_filter[type]=All&show_recommended_reviews=true&show_feedback_summary_tags=true"
                    yield Request(feed_api_link, callback=self.feedback_data,meta={'dct_id':dct_id})
            self.got_page(sk_d, 1)


    def feedback_data(self,response):
            sel = Selector(response)
            import pdb;pdb.set_trace() 
            json_data = json.loads(response.body)
            dct_id = response.meta.get('dct_id','')
            feedback_data = json_data.get('reviews',{})         
            feedback_count = json_data.get('reviews_count','')
            total_pages = json_data.get('page_count','')
            current_page = json_data.get('page','')
            reviews_count = json_data.get('reviews_count','')
            total_count = json_data.get('total_count','')
            review_nodes = json_data.get('reviews',{})
            happy_da = ''
            if review_nodes:
                for nod in review_nodes:
                    review_inner = nod.get('review',{})
                    happy_data = []
                    happy_with = nod.get('feedback_summary_tags')
                    for tag in happy_with : 
                        happy_text = tag.get('tag')
                        happy_data.append('happy_text')
                    happy_da = ",".join(happy_data)
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
                    aux_info = {}
                    if happy_da : 
                        aux_info.update({'happy_with':happy_da})
                    review_item = DoctorFeedback()
                    review_item['sk'] = md5("%s%s%s%s%s%s"%(revi_id, revia_id, reviewd_on, review_doc_id, review_name, dct_id))
                    review_item['feedback_count'] = normalize(str(feedback_count))
                    review_item['doctor_id'] = normalize(dct_id)
                    review_item['feeback_text'] = normalize(review_text)
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
                    review_item['reference_url']= normalize(dct_profile)
                    review_item['aux_info'] = json.dumps(aux_info)
                    yield review_item
		   

