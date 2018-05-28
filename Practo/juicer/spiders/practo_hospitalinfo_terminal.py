from juicer.utils import *
from practo_hospitals_xpaths import *
from juicer.items import *

class Practohospitals(JuicerSpider):
    name = 'practo_hospitalinfo_terminal1111'
    #start_urls = ['https://www.practo.com/chennai/hospital/hindu-mission-hospital-tambaram-tambaram-west/doctors']
    handle_http_status_list = ['302', '504', '403', 403]

    def __init__(self, *args, **kwargs):
        super(Practohospitals, self).__init__(*args, **kwargs)
        self.domain = "https://www.practo.com"
        self.week_list = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
        self.pattern1 = re.compile(r'\((.*?)\)')
        self.pattern2 = re.compile('(.*) (.*)')
        #self.feedjson1 = "https://www.practo.com/wave/reviewmoderations/clinicreviews.json?show_recommended_reviews&practice_id="
        #self.feedjson2 = "&with_doctor=true&mr=true&page="
        #self.feedjson3 = "&show_feedback_summary_tags=true"

    def parse(self, response):
        sel = Selector(response)
        import pdb;pdb.set_trace()
        hosp_photo = extract_data(sel, hosp_photo_xpt)
        #hosp_id = response.meta['sk']
        hosp_name = extract_data(sel, hosp_name_xpt)
        hosp_pf_link = extract_data(sel, hosp_pf_link_xpt)
        rating_values = extract_data(sel, rating_values_xpt)
        rating_count = extract_data(sel, rating_count_xpt)
        clinic_location = extract_data(sel, clinic_location_xpt)
        medical_spec = extract_data(sel, medical_spec_xpt, ', ')
        number_of_doctors = extract_data(sel, number_of_doctors_xpt)
        hospt_description = extract_data(sel, hospt_description_xpt, ' ')
        no_of_beds = extract_data(sel, no_of_beds_xpt)
        no_of_ambulances = extract_data(sel, no_of_ambulances_xpt)
        method_of_payment = extract_data(sel, method_of_payment_xpt).replace('|','<>')
        hospital_address = extract_data(sel, hospital_address_xpt)
        street_address = extract_data(sel, street_address_xpt)
        address_locality = extract_data(sel, address_locality_xpt)
        address_region = extract_data(sel, address_region_xpt)
        postal_code = extract_data(sel, postal_code_xpt)
        opening_timings = extract_data(sel, opening_timings_xpt)
        if not opening_timings:
            opening_timings = []
            doc_schedule_nodes = sel.xpath(doc_schedule_nodes_xpt)
            for sch in doc_schedule_nodes:
                sch_days = extract_data(sch, sch_days_xpt, ', ')
                sch_timings = extract_data(sch, sch_timings_xpt,', ')
                sch_slot = ("%s%s%s"%(sch_days,':-',sch_timings)).strip('<>')
                if sch_slot:
                    opening_timings.append(sch_slot)
            opening_timings = '<>'.join(opening_timings).strip('<>:-')
        hospital_images = extract_data(sel, hospital_images_xpt, '<>')
        amenities = extract_data(sel, amenities_xpt,'<>')+extract_data(sel, amenities_xpt1,'<>').replace('<><>','<>').strip()
        emergency_contact_number = extract_data(sel, emergency_contact_number_xpt)
        services = extract_data(sel, services_xpt,'<>')+'<>'+extract_data(sel, services_xpt1,'<>').replace('<><>','<>').strip('<>').strip()
        latitude = extract_data(sel, latitude_xpt)
        longitude = extract_data(sel, longitude_xpt)
        branch_setup = extract_data(sel, branch_setup_xpt).replace('|','')
        if not branch_setup:
            branch_setup = extract_data(sel, branch_setup_xpt1).replace('|',' and ')
        doctor_nodes = sel.xpath(doctor_nodes_xpt)
        if doctor_nodes:
            for nd in doctor_nodes:
                doctor_info  = self.parse_doctor(nd, 'main', hosp_id, response.url)
                if doctor_info:
                    yield doctor_info
        nex_pge_doc = extract_data(sel, nex_pge_doc_xpt)
        if nex_pge_doc:
            new_ajax_url = "%s%s" % (response.url, '?page=2&ajax=true')
            yield Request(new_ajax_url, callback=self.parse_doctorajax, meta= {"main_dct_url":response.url, 'hct_id':hosp_id})
        feedback_count = extract_data(sel, feedback_count_xpath)
        if not feedback_count:
            feedback_count = extract_data(sel, feedback_count_xpath1)
        if feedback_count and self.pattern1.search(feedback_count):
            feedback_count = textify(self.pattern1.findall(feedback_count))
        doc_id_feedback = extract_data(sel, doc_id_feedback_xpath)
        if feedback_count and doc_id_feedback and feedback_count != '0':
            feedback_url = "%s%s%s%s%s"%(self.feedjson1, str(doc_id_feedback), self.feedjson2, '1', self.feedjson3)
            if feedback_url:
                yield Request(feedback_url,callback=self.parse_feedback, meta={"dct_id":hosp_id,"dct_url":response.url, "feedback_id":str(doc_id_feedback), 'feedback_count':feedback_count})
        awards = extract_data(sel, awards_xpt,' ')
        other_centers_title = sel.xpath(other_centers_title_xpt)
        other_centers_ = []
        for ocen in other_centers_title:
            ocen_id = extract_data(ocen, ocen_id_xpt)
            ocen_name = extract_data(ocen, ocen_name_xpt)
            if ocen_id and ocen_name:
                ocen_names = "%s%s%s" % (ocen_id, ':-', ocen_name)
                other_centers_.append(ocen_names)
        other_centers_ = '<>'.join(other_centers_)
        hosp_meta_item = self.parse_get_hospital_meta(hosp_id, hosp_name, hosp_pf_link, rating_count, rating_values, clinic_location, medical_spec, number_of_doctors, hospt_description, no_of_beds, no_of_ambulances, method_of_payment, hospital_address, street_address, address_locality, address_region, postal_code, opening_timings, hospital_images, amenities, emergency_contact_number, services, latitude, longitude, branch_setup, feedback_count, awards, other_centers_, response.url)
        if hosp_meta_item:
            yield hosp_meta_item
        self.got_page(hosp_id, 1)

    def parse_get_hospital_meta(self, hosp_id, hosp_name, hosp_pf_link, rating_count, rating_values, clinic_location, medical_spec, number_of_doctors, hospt_description, no_of_beds, no_of_ambulances, method_of_payment, hospital_address, street_address, address_locality, address_region, postal_code, opening_timings, hospital_images, amenities, emergency_contact_number, services, latitude, longitude, branch_setup, feedback_count, awards, other_centers_, response_url):
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
        hospital_meta['opening_timings']  = normalize(opening_timings)
        hospital_meta['clinic_images']  = normalize(hospital_images)
        hospital_meta['amenities']  = normalize(amenities)
        hospital_meta['emergency_contact_number']  = normalize(emergency_contact_number)
        hospital_meta['services']  = normalize(services)
        hospital_meta['longitude']  = normalize(latitude)
        hospital_meta['latitude']  = normalize(longitude)
        hospital_meta['establishment_data']  = normalize(branch_setup)
        hospital_meta['feedback_count']  = normalize(feedback_count)
        hospital_meta['awards']  = normalize(awards)
        hospital_meta['other_centers']  = normalize(other_centers_)
        hospital_meta['reference_url']  = normalize(response_url)
        return hospital_meta

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
            if total_pages != current_page and total_pages >= current_page:
                feedback_url = "%s%s%s%s%s"%(self.feedjson1, str(feedback_id), self.feedjson2, str(int(current_page)+1), self.feedjson3)
                yield Request(feedback_url,callback=self.parse_feedback, meta={"dct_id":dct_id,"dct_url":dct_url, "feedback_id":str(feedback_id), 'feedback_count':feedback_count})



    def parse_doctorajax(self, response):
        sel = Selector(response)
        main_dct_url = response.meta.get('main_dct_url', '')
        hct_id = response.meta.get('hct_id','')
        doctor_nodes = sel.xpath(doctor_nodes_xptd)
        if doctor_nodes:
            for nd in doctor_nodes:
                doctor_info  = self.parse_doctor(nd, 'sub', hct_id, response.url)
                if doctor_info:
                    yield doctor_info
        next_page_doc = extract_data(sel, next_page_doc_xptd)
        if next_page_doc:
            new_ajax_url = "%s%s" % (main_dct_url, '?page=%s&ajax=true' % next_page_doc)
            yield Request(new_ajax_url, callback=self.parse_doctorajax, meta= {"main_dct_url":main_dct_url, "hct_id":hct_id})


    def parse_doctor(self, nd, check_for_page, hct_id, response_url):
        details_nodes = nd.xpath(details_block)
        doctor_photos = extract_data(nd, doctor_photos_xpath)
        if '/bundles/practopractoapp/images/profile.png' in doctor_photos: doctor_photos = ''
        doc_name = extract_data(details_nodes, name_xpath)
        doc_link = extract_data(details_nodes, url_xpath)
        if doc_link and  ('https://' not in doc_link):
             doc_link = "%s%s" % ("https://www.practo.com", doc_link)
        doc_qualifications = extract_data(details_nodes, qual_, '<>')
        doc_years_experience = extract_data(details_nodes, exp_)
        doc_specialities = extract_data(details_nodes, specialities_, '<>')
        doc_availability = nd.xpath(doc_availability_xpath)
        doc_rating = extract_data(doc_availability, doc_rating_xpath)
        doc_votes = extract_data(doc_availability, doc_votes_xpath)
        doc_feedback_count = extract_data(doc_availability, doc_feedback_count_xpath)
        doc_fee_amount = extract_data(doc_availability, doc_fee_amount_xpath)
        doc_booking_type = extract_data(nd, doc_booking_type_xpath)
        doc_id = extract_data(nd, doc_id_xpts)
        #doc_price_currency = extract_data(doc_availability, doc_price_currency_xpath)
        doc_practo_gua = extract_data(nd,  doc_practo_gua_xpts)
        sched_timins = extract_data(nd, schedule_timings, '<>')
        doc_on_call = extract_data(nd, doc_on_call_xpts)
        dic_week = {}
        if sched_timins:
            dic_week = self.parse_get_week_sche(sched_timins)
        doc_hosp_ = self.parse_get_doctor_info(hct_id, doc_id, doc_name, doc_link, doc_qualifications, doc_years_experience, doc_specialities, doc_rating, doc_votes, doc_feedback_count, doc_fee_amount, doctor_photos,doc_practo_gua, doc_booking_type, dic_week, response_url, doc_on_call)
        return  doc_hosp_

    def parse_get_doctor_info(self, hct_id, doc_id, doc_name, doc_link, doc_qualifications, doc_years_experience, doc_specialities, doc_rating, doc_votes, doc_feedback_count, doc_fee_amount, doctor_photos,doc_practo_gua, doc_booking_type, final_dict, response_url, doc_on_call):
        doc_hosp_ = HospitalDoctor()
        doc_hosp_['sk'] = md5("%s%s%s" % (hct_id, doc_id, doc_name))
        doc_hosp_['hospital_id'] = normalize(hct_id)
        doc_hosp_['doctor_id'] = normalize(doc_id)
        doc_hosp_['doctor_name'] = normalize(doc_name)
        doc_hosp_['doctor_profile_link'] = normalize(doc_link)
        doc_hosp_['qualification'] = normalize(doc_qualifications)
        doc_hosp_['years_of_experience'] = normalize(doc_years_experience)
        doc_hosp_['specialization'] = normalize(doc_specialities)
        doc_hosp_['rating'] = normalize(doc_rating)
        doc_hosp_['vote_count'] = normalize(doc_votes.replace('(','').replace(')',''))
        doc_hosp_['feedback_count'] = normalize(doc_feedback_count.replace('(','').replace(')',''))
        doc_hosp_['consultation_fee'] = normalize(doc_fee_amount)
        doc_hosp_['doctor_image'] = normalize(doctor_photos)
        doc_hosp_['doctor_practo_gurantee'] = normalize(doc_practo_gua)
        doc_hosp_['booking_type'] = normalize(doc_booking_type)
        doc_hosp_['doctor_monday_timing'] = normalize('<>'.join(final_dict.get('Mo',[])))
        doc_hosp_['doctor_tuesday_timing'] = normalize('<>'.join(final_dict.get('Tu',[])))
        doc_hosp_['doctor_wednesday_timing'] = normalize('<>'.join(final_dict.get('We',[])))
        doc_hosp_['doctor_thursday_timing'] = normalize('<>'.join(final_dict.get('Th',[])))
        doc_hosp_['doctor_friday_timing'] = normalize('<>'.join(final_dict.get('Fr',[])))
        doc_hosp_['doctor_saturday_timing'] = normalize('<>'.join(final_dict.get('Sa',[])))
        doc_hosp_['doctor_sunday_timing'] = normalize('<>'.join(final_dict.get('Su',[])))
        doc_hosp_['doctor_on_call'] = normalize(doc_on_call)
        doc_hosp_['reference_url'] = normalize(response_url)
        return doc_hosp_

    def parse_get_week_sche(self, hsp_timesch):
        final_set = {'Mo':[], 'Tu':[], 'We':[], 'Th':[], 'Fr':[], 'Sa':[], 'Su':[]}
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
                                try:
                                     weeks1f, weeks2f, weeks3f, weeks4f = weeks.split(',')
                                     weeksf_list = [weeks1f, weeks2f, weeks3f, weeks4f]
                                except: pass
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
        return final_dict

