from juicer.spiders import *
from juicer.utils import *
from practo_xpaths import *
from juicer.items import *

class Practodoctor(JuicerSpider):
    name = 'practo_doctor_terminal'

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
        dct_id = extract_list_data(sel, '//input[@data-doctorid]/@data-doctorid')
        if dct_id:
            dct_id = dct_id[0]
        else:
            dct_id = ''
        dct_profile = extract_data(sel, '//div[@class="doctor-details-wrapper"]/meta[@itemprop="url"]/@content')
        dct_name = extract_data(sel, '//div[@class="doctor-details-wrapper"]/h1[@class="doctor-name"]/text()')
        dct_qualifications = extract_data(sel,'//div[@class="doctor-details-wrapper"]/p[@class="doctor-qualifications"]/text()')
        dct_experience = extract_data(sel, '//div[@class="doctor-details-wrapper"]/h2[@class="doctor-specialties"]/text()').strip().strip(',')
        dct_photo = extract_data(sel, '//div[@class="doc_photo"]//link[@itemprop="photo"]/@href')
        dct_specialization = extract_data(sel, '//div[@class="doctor-details-wrapper"]/h2[@class="doctor-specialties"]/meta[@itemprop="medicalSpecialty"]/@content','<>').replace('<><>','').strip('<>')
        dct_verification = extract_data(sel,'//div[@class="verifications-block"]/span[@class="verification-label"]/text()')
        if 'Medical Registration Verified' in dct_verification:
            dct_verification = dct_verification
        else:
            print dct_verification
        dct_rating =  extract_data(sel, '//div[@class="doctor-details-wrapper"]//div[contains(@class,"patient_experience_score")]/text()')
        dct_votes = extract_data(sel, '//div[@class="doctor-details-wrapper"]//span[@class="doctor-votes"]/text()')
        if self.pattern1.search(dct_votes):
            dct_votes = textify(self.pattern1.findall(dct_votes))
        dct_summary = extract_data(sel, '//div[@class="doctor-summary"]//span[@id="summaryTextFull"]/text()')
        dct_services = extract_data(sel, '//div[@class="services-block"]//div[@class="doc-info-item service-cell "][@itemprop="name"]/a/text()','<>')+extract_data(sel, '//div[@class="services-block"]//div[@class="doc-info-item service-cell "][@itemprop="name"]/text()','<>').replace('<><>','').strip('<>')
        dct_specializations = extract_data(sel, '//div[@class="doc-info-section specialties-block"]//h2[contains(@class,"doc-info-item specialty")]//a[@itemprop="name"]/text()','<>')+extract_data(sel, '//div[@class="doc-info-section specialties-block"]//h2[contains(@class,"doc-info-item specialty")]/text()','<>').replace('<><>','').strip('<>')

        dct_education = extract_data(sel, '//div[@class="doc-info-section qualifications-block"]//span[contains(@class,"qualification-degree") or contains(@class,"qualification-details")]/text()','<>').replace('<>-',' -')
        dct_awards = extract_data(sel, '//div[@class="doc-info-section awards-block"]//p[contains(@class,"doc-info-item award")]/text()','<>')
        dct_memberships = extract_data(sel, '//div[@class="doc-info-section memberships-block"]//p[contains(@class,"doc-info-item membership")]/text()','<>')
        dct_organizations = get_nodes(sel, '//div[@class="doc-info-section organizations-block"]/div[contains(@class,"doc-info-item organization")]')
        final_orga = []
        if dct_organizations:
            for dctn in dct_organizations:
                exp_year = extract_data(dctn, './span[@class="exp-tenure"]/text()')
                exp_details = extract_data(dctn, './span[@class="exp-details"]/text()')
                exp_total = ("%s%s%s"%(exp_year,' ',exp_details)).strip()
                if exp_total:
                    final_orga.append(exp_total)
        final_orga = '<>'.join(final_orga)
        dct_registrations = get_nodes(sel, '//div[@class="doc-info-section registrations-block"]//div[contains(@class, "doc-info-item registration")]')
        final_regin = []
        if dct_registrations:
            for dctr in dct_registrations:
                registr_tenure = extract_data(dctr, './span[@class="exp-tenure"]/text()')
                registr_details = extract_data(dctr, './span[@class="exp-details"]/text()')
                regsitr_total = ("%s%s%s"%(registr_tenure,' ',registr_details)).strip()
                if regsitr_total: final_regin.append(regsitr_total)
        final_regin = '<>'.join(final_regin)
        feedback_count = extract_data(sel,'//a[@id="reviewsNavLink"]/text()')
        if not feedback_count:
            feedback_count = extract_data(sel,'//a[@id="all-reviews"]/text()')
        if feedback_count and self.pattern1.search(feedback_count):
            feedback_count = textify(self.pattern1.findall(feedback_count))

        doc_id_feedback = extract_data(sel, '//input[@type="hidden"][@name="id"][@data-type="doc"]/@value')
        """if feedback_count and doc_id_feedback:
            feedback_url = "%s%s%s%s%s"%(self.feedjson1, str(doc_id_feedback), self.feedjson2, '1', self.feedjson3)
            if feedback_url:
                yield Request(feedback_url,callback=self.parse_feedback, meta={"dct_id":dct_id,"dct_url":response.url, "feedback_id":str(doc_id_feedback), 'feedback_count':feedback_count})"""
        #feedback_nodes = get_nodes(sel,'' )
        feedback_script = ''.join(sel.xpath('//script[@type="text/javascript"]/text()[contains(.,"window.practo.fabric.cacheFeedback")]').extract()).replace('\n','').replace('\t','')
        if feedback_script:
            try:
                feed_json = re.findall('fabric.cacheFeedback = (.*);window.practo.fabric.currentRole', feedback_script)[0]
                if feed_json:
                    itemhere = self.parse_feedback(feed_json, dct_id, response.url, str(doc_id_feedback),feedback_count)
                    if itemhere:
                        for ith in itemhere:
                            yield ith
            except: feed_json = {}
        import pdb;pdb.set_trace()
        if dct_id:
            doctor_meta  = DoctorMeta()
            doctor_meta['sk'] = normalize(response.meta.get('sk',''))
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


        hospital_nodes = get_nodes(sel, '//div[@id="infoTab"]//div[contains(@class,"clinic-block")]')
        for hnd in hospital_nodes:
            hsp_location = extract_data(hnd, './div[@class="clinic-locality"]//text()')
            hsp_link = extract_data(hnd, './/p[@class="map-link-container"]/meta[@itemprop="url"]/@content')
            if not hsp_link:
                hsp_link = extract_data(hnd, './/div[@class="clinic-address"]/h2/a[@itemprop="name"]/@href')
            hsp_name = extract_data(hnd, './/div[@class="clinic-address"]/h2/a[@itemprop="name"]/text()')
            hsp_star_rat = extract_list_data(hnd, './/div[@class="practice-star-rating aes-star-rating"]/span[@class="font-star icon-ic_star_solid filled-star"]/@class')
            hsp_star_rat1 = extract_list_data(hnd, './/div[@class="practice-star-rating aes-star-rating"]/span[@class="font-star icon-ic_star_half filled-star"]/@class')
            if hsp_star_rat and hsp_star_rat1:
                hsp_star_rat = len(hsp_star_rat)
                hsp_star_rat = hsp_star_rat+len(hsp_star_rat1)*0.5
            elif hsp_star_rat and not hsp_star_rat1:
                hsp_star_rat = len(hsp_star_rat)
            elif hsp_star_rat1 and not hsp_star_rat:
                hsp_star_rat = len(hsp_star_rat1)*0.5
            else:
                hsp_star_rat = ''
            hsp_address = extract_data(hnd, './/span[@itemprop="streetAddress"]/text()').strip('#')
            hsp_addr_locality = extract_data(hnd, './/meta[@itemprop="addressLocality"]/@content')
            hsp_add_region = extract_data(hnd, './/meta[@itemprop="addressRegion"]/@content')
            hsp_photos = extract_data(hnd, './/p[@class="clinic-photos-container"]/a[@data-clinicid]/@href','<>')
            hsp_booking_type = extract_data(hnd, './/span[@class="button-text vn-call-button"]/text()')
            hsp_map_latitude = extract_data(hnd, './/p[@class="map-link-container"]/span[@itemprop="geo"]/meta[@itemprop="latitude"]/@content')
            hsp_map_longitude = extract_data(hnd, './/p[@class="map-link-container"]/span[@itemprop="geo"]/meta[@itemprop="longitude"]/@content')
            hsp_schedule = extract_data(hnd, './/div[@class="clinic-timings"]//p[@class="clinic-timings-day"]/text()')
            hsp_timesch = extract_data(hnd, './/div[@class="clinic-timings"]//meta[@itemprop="openingHours"]/@content','<>')
            hsp_consultation_fee = extract_data(hnd, './div[@class="clinic-fees"]/span[@itemprop="priceRange"]/text()')
            hsp_fee_indicator = extract_data(hnd, './div[@class="clinic-fees"]//span[@id="feesindicator"]//div[@class="fees-indicator-tooltip"]//text()', ' ')
            hsp_currencies_accpe = extract_data(hnd, './meta[@itemprop="currenciesAccepted"]/@content')
            hsp_practo_gura = extract_data(hnd, './div[@class="clinic-fees"]//div[@class="gc-mini-message"]/a/@href')
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
                                    weeks1f, weeks2f, weeks3f = weeks.split(',')
                                    weeksf_list = [weeks1f, weeks2f, weeks3f]
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

    def parse_feedback(self, body, dct_id, dct_url, feedback_id,feedback_count):
        #if 'https://www.practo.com/ie/unsupported' not in response.url:
        final_items = []
        if body:
            tmp = json.loads(body)
            """feedback_count = response.meta.get('feedback_count','')
            dct_id = response.meta.get('dct_id','')
            dct_url = response.meta.get('dct_url','')
            feedback_id = response.meta.get('feedback_id','')
            total_pages = tmp.get('page_count','')
            current_page = tmp.get('page','')
            reviews_count = tmp.get('reviews_count','')
            total_count = tmp.get('total_count','')
            #review_nodes = tmp.get('reviews',{})"""
            review_nodes = tmp.get('recommended',{}).get('reviews','')+tmp.get('recent',{}).get('reviews','')
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
                    #yield review_item
                    final_items.append(review_item)

            """if total_pages != current_page:
                feedback_url = "%s%s%s%s%s"%(self.feedjson1, str(feedback_id), self.feedjson2, str(int(current_page)+1), self.feedjson3)
                yield Request(feedback_url,callback=self.parse_feedback, meta={"dct_id":dct_id,"dct_url":dct_url, "feedback_id":str(feedback_id), 'feedback_count':feedback_count})"""

        return final_items

