from juicer.utils import *
from practo_xpaths import *
from juicer.items import *

class Practodoctor(JuicerSpider):
    name = 'practo_doctor_terminal'
    handle_http_status_list = ['302', '504']

    def __init__(self, *args, **kwargs):
        super(Practodoctor, self).__init__(*args, **kwargs)
        self.domain = "https://www.practo.com"
        self.pattern1 = re.compile(r'\((.*?)\)')
        self.pattern2 = re.compile('(.*) (.*)')
        self.week_list = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
        self.feedjson1 = "https://www.practo.com/wave/reviewmoderations/doctorreviews.json?show_recommended_reviews&doctor_id="
        self.feedjson2 = "&with_practice=true&mr=true&page="
        self.feedjson3 = "&show_feedback_summary_tags=true"

    def parse(self, response):
        sel = Selector(response)
        dct_id = response.meta['sk']
        dct_profile = extract_data(sel, dct_profile_xpath)
        dct_name = extract_data(sel, dct_name_xpath)
        dct_qualifications = extract_data(sel, dct_qualifications_xpath)
        dct_experience = extract_data(sel, dct_experience_xpath).strip().strip(',')
        dct_photo = extract_data(sel, dct_photo_xpath)
        if '/bundles/practopractoapp/images/profile.png' in dct_photo: dct_photo = ''
        dct_specialization = extract_data(sel, dct_specialization_xpath,'<>').replace('<><>','').strip('<>')
        dct_verification = extract_data(sel, dct_verification_xpath)
        if 'Medical Registration Verified' in dct_verification:
            dct_verification = dct_verification
        dct_rating =  extract_data(sel, dct_rating_xpath)
        dct_votes = extract_data(sel, dct_votes_xpath)
        if self.pattern1.search(dct_votes):
            dct_votes = textify(self.pattern1.findall(dct_votes))
        dct_summary = extract_data(sel, dct_summary_xpath)
        dct_services = extract_data(sel, dct_services_xpath1,'<>')+extract_data(sel, dct_services_xpath2,'<>').replace('<><>','').strip('<>')
        dct_specializations = extract_data(sel, dct_specializations_xpath1,'<>')+extract_data(sel, dct_specializations_xpath2,'<>').replace('<><>','').strip('<>')

        dct_education = extract_data(sel, dct_education_xpath, '<>').replace('<>-',' -')
        dct_awards = extract_data(sel, dct_awards_xpath, '<>')
        dct_memberships = extract_data(sel, dct_memberships_xpath, '<>')
        dct_organizations = get_nodes(sel, dct_organizations_xpath)
        final_orga = []
        if dct_organizations:
            for dctn in dct_organizations:
                exp_year = extract_data(dctn, exp_year_xpath)
                exp_details = extract_data(dctn, exp_details_xpath)
                exp_total = ("%s%s%s"%(exp_year,' ',exp_details)).strip()
                if exp_total:
                    final_orga.append(exp_total)
        final_orga = '<>'.join(final_orga)
        dct_registrations = get_nodes(sel, dct_registrations_xpath)
        final_regin = []
        if dct_registrations:
            for dctr in dct_registrations:
                registr_tenure = extract_data(dctr, registr_tenure_xpath)
                registr_details = extract_data(dctr, registr_details_xpath)
                regsitr_total = ("%s%s%s"%(registr_tenure,' ',registr_details)).strip()
                if regsitr_total: final_regin.append(regsitr_total)
        final_regin = '<>'.join(final_regin)
        feedback_count = extract_data(sel, feedback_count_xpath)
        if not feedback_count:
            feedback_count = extract_data(sel, feedback_count_xpath1)
        if feedback_count and self.pattern1.search(feedback_count):
            feedback_count = textify(self.pattern1.findall(feedback_count))
        doc_id_feedback = extract_data(sel, doc_id_feedback_xpath)
        if feedback_count and doc_id_feedback and feedback_count != '0':
            feedback_url = "%s%s%s%s%s"%(self.feedjson1, str(doc_id_feedback), self.feedjson2, '1', self.feedjson3)
            if feedback_url:
                yield Request(feedback_url,callback=self.parse_feedback, meta={"dct_id":dct_id,"dct_url":response.url, "feedback_id":str(doc_id_feedback), 'feedback_count':feedback_count})
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
            doctor_meta['rating'] = normalize(dct_rating)
            doctor_meta['vote_count'] =  normalize(str(dct_votes))
            doctor_meta['summary'] = normalize(dct_summary)
            doctor_meta['services'] =  normalize(dct_services)
            doctor_meta['specializations'] = normalize(dct_specializations)
            doctor_meta['education'] = normalize(dct_education)
            doctor_meta['memeberships'] = normalize(dct_memberships)
            doctor_meta['experience'] = normalize(final_orga)
            doctor_meta['registrations'] = normalize(final_regin)
            doctor_meta['feedback_count'] = normalize(str(feedback_count))
            doctor_meta['doctor_image'] = normalize(dct_photo)
            doctor_meta['reference_url'] = normalize(response.url)
            yield doctor_meta
        hospital_nodes = get_nodes(sel, hospital_nodes_xpath)
        for hnd in hospital_nodes:
            hsp_location = extract_data(hnd, hsp_location_xpath)
            hsp_link = extract_data(hnd, hsp_link_xpath)
            if not hsp_link:
                hsp_link = extract_data(hnd, hsp_link_xpath1)
            hsp_name = extract_data(hnd, hsp_name_xpath)
            hsp_star_rat = extract_list_data(hnd, hsp_star_rat_xpath)
            hsp_star_rat1 = extract_list_data(hnd, hsp_star_rat1_xpath)
            if hsp_star_rat and hsp_star_rat1:
                hsp_star_rat = len(hsp_star_rat)
                hsp_star_rat = hsp_star_rat+len(hsp_star_rat1)*0.5
            elif hsp_star_rat and not hsp_star_rat1:
                hsp_star_rat = len(hsp_star_rat)
            elif hsp_star_rat1 and not hsp_star_rat:
                hsp_star_rat = len(hsp_star_rat1)*0.5
            else:
                hsp_star_rat = ''
            hsp_address = extract_data(hnd, hsp_address_xpath).strip('#')
            hsp_addr_locality = extract_data(hnd, hsp_addr_locality_xpath)
            hsp_add_region = extract_data(hnd, hsp_add_region_xpath)
            hsp_photos = extract_data(hnd, hsp_photos_xpath,'<>')
            hsp_booking_type = extract_data(hnd, hsp_booking_type_xpath)
            hsp_map_latitude = extract_data(hnd, hsp_map_latitude_xpath)
            hsp_map_longitude = extract_data(hnd, hsp_map_longitude_xpath)
            hsp_schedule = extract_data(hnd, hsp_schedule_xpath)
            hsp_timesch = extract_data(hnd, hsp_timesch_xpath, '<>')
            hsp_consultation_fee = extract_data(hnd, hsp_consultation_fee_xpath)
            hsp_fee_indicator = extract_data(hnd, hsp_fee_indicator_xpath, ' ')
            hsp_currencies_accpe = extract_data(hnd, hsp_currencies_accpe_xpath)
            hsp_practo_gura = extract_data(hnd, hsp_practo_gura_xpath)
            if hsp_practo_gura:
                hsp_practo_gura = 'yes'
            else: hsp_practo_gura = 'no'
            final_set = {'Mo':[], 'Tu':[], 'We':[], 'Th':[], 'Fr':[], 'Sa':[], 'Su':[]}
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
            doctor_hospital['hospital_monday_timing'] = normalize('<>'.join(final_dict.get('Mo',[])))
            doctor_hospital['hospital_tuesday_timing'] = normalize('<>'.join(final_dict.get('Tu',[])))
            doctor_hospital['hospital_wednesday_timing'] =  normalize('<>'.join(final_dict.get('We',[])))
            doctor_hospital['hospital_thursday_timing'] = normalize('<>'.join(final_dict.get('Th',[])))
            doctor_hospital['hospital_friday_timing'] = normalize('<>'.join(final_dict.get('Fr',[])))
            doctor_hospital['hospital_saturday_timing'] = normalize('<>'.join(final_dict.get('Sa',[])))
            doctor_hospital['hospital_sunday_timing'] = normalize('<>'.join(final_dict.get('Su',[])))
            doctor_hospital['hospital_consultation_fee'] = normalize(hsp_consultation_fee)
            doctor_hospital['hospital_practo_gurantee'] = normalize(hsp_practo_gura)
            doctor_hospital['hospital_photos'] = normalize(hsp_photos)
            doctor_hospital['hospital_booking_type'] = normalize(hsp_booking_type)
            doctor_hospital['hospital_latitude'] = normalize(hsp_map_latitude)
            doctor_hospital['hospital_longitude'] = normalize(hsp_map_longitude)
            doctor_hospital['reference_url'] = normalize(response.url)
            yield doctor_hospital
        self.got_page(sk_d, 1)

    def parse_feedback(self, response):
        if 'https://www.practo.com/ie/unsupported' not in response.url:
            tmp = json.loads(response.body)
            feedback_count = response.meta.get('feedback_count','')
            dct_id = response.meta.get('dct_id','')
            dct_url = response.meta.get('dct_url','')
            feedback_id = response.meta.get('feedback_id','')
            total_pages = tmp.get('page_count','')
            current_page = tmp.get('page','')
            reviews_count = tmp.get('reviews_count','')
            total_count = tmp.get('total_count','')
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
                    review_item['reference_url']= normalize(dct_url)
                    yield review_item
            if total_pages != current_page and total_pages >= current_page:
                feedback_url = "%s%s%s%s%s"%(self.feedjson1, str(feedback_id), self.feedjson2, str(int(current_page)+1), self.feedjson3)
                yield Request(feedback_url,callback=self.parse_feedback, meta={"dct_id":dct_id,"dct_url":dct_url, "feedback_id":str(feedback_id), 'feedback_count':feedback_count})

