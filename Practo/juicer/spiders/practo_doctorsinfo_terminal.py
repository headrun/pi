from juicer.utils import *
from practo_doctorsinfo_xpaths import *
from juicer.items import *

class Practodoctorsinfote(JuicerSpider):
    name = 'practo_doctorsinfo_terminal'
    handle_http_status_list = ['500','302', '504','403','404','410']
    def __init__(self, *args, **kwargs):
        super(Practodoctorsinfote, self).__init__(*args, **kwargs)
        self.domain = "https://www.practo.com"
        self.pattern1 = re.compile(r'\((.*?)\)')
        self.pattern2 = re.compile('(.*) (.*)')
        self.week_list = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        self.feedjson1 = "https://www.practo.com/client-api/v1/feedback/doctorreviews?profile_id=%s"
        self.feedjson2 = "&profile_type=doctor&page="
        self.feedjson3 = "&mr='true'&show_recommended_reviews='true'&doctor_id=%s"

    def parse(self, response):
        sel = Selector(response)
        city_browse = json.loads(response.meta.get('data')).get('city', '')
        jscsv_data = {}
        try:
            cvss = sel.xpath('//script[contains(text(), "window.__REDUX_STATE__")]/text()').extract()[0].split('window.__REDUX_STATE__=')[1]
            jscsv_data = json.loads(cvss)
        except:
            jscsv_data = {}
        if jscsv_data:
            profile_payload = jscsv_data.get('analyticsData', {}).get('profilePayload', {})
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
            dct_specialization = extract_data(sel, '//div[@class="c-profile__details"][@data-qa-id="doctor-specializations"]/span[@data-reactid]/h2/text()', '<>')
            dct_verification = extract_data(sel, '//div[@class="c-profile--verification"]//span[@data-qa-id="doctor-verification-label"]/span/text()')
            if 'Medical Registration Verified' in dct_verification:
                dct_verification = dct_verification
            dct_rating =  extract_data(sel, '//p[@data-qa-id="doctor-patient-experience-score"]/span[contains(text(),"%")]/text()')
            dct_votes = extract_data(sel, '//p[@data-qa-id="doctor-patient-experience-score"]/span[@class="u-smallest-font u-grey_3-text"]/text()')
            if self.pattern1.search(dct_votes):
                dct_votes = textify(self.pattern1.findall(dct_votes))
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
                #'>>>>>>>>>>>>>>>>>>>>>'
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
            feedback_count = str(jscsv_data.get('feedback_reducer', {}).get('reviews_count', ''))
            doc_id_feedback = dct_id
            if feedback_count and doc_id_feedback and feedback_count != '0':
                #feedback_url = "%s%s%s%s"%((self.feedjson1 % str(doc_id_feedback)), self.feedjson2, '1', (self.feedjson3 % str(doc_id_feedback)))
                feedback_url=''
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
                doctor_meta['aux_info'] = json.dumps({"city": (city_browse)})
                yield doctor_meta
            hos_parit_link = response.url.split('/doctor')[0]
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
                #final_set = {'Mo':[], 'Tu':[], 'We':[], 'Th':[], 'Fr':[], 'Sa':[], 'Su':[]}
                final_set = {'Mon':[], 'Tue':[], 'Wed':[], 'Thu':[], 'Fri':[], 'Sat':[], 'Sun':[]}
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
                doctor_hospital['hospital_monday_timing'] = normalize('<>'.join(final_dict.get('Mon',[])))
                doctor_hospital['hospital_tuesday_timing'] = normalize('<>'.join(final_dict.get('Tue',[])))
                doctor_hospital['hospital_wednesday_timing'] =  normalize('<>'.join(final_dict.get('Wed',[])))
                doctor_hospital['hospital_thursday_timing'] = normalize('<>'.join(final_dict.get('Thu',[])))
                doctor_hospital['hospital_friday_timing'] = normalize('<>'.join(final_dict.get('Fri',[])))
                doctor_hospital['hospital_saturday_timing'] = normalize('<>'.join(final_dict.get('Sat',[])))
                doctor_hospital['hospital_sunday_timing'] = normalize('<>'.join(final_dict.get('Sun',[])))
                doctor_hospital['hospital_consultation_fee'] = normalize(hsp_consultation_fee)
                doctor_hospital['hospital_practo_gurantee'] = normalize(hsp_practo_gura)
                doctor_hospital['hospital_photos'] = normalize(hsp_photos)
                doctor_hospital['hospital_booking_type'] = normalize(hsp_booking_type)
                doctor_hospital['hospital_latitude'] = normalize(hsp_map_latitude)
                doctor_hospital['hospital_longitude'] = normalize(hsp_map_longitude)
                doctor_hospital['reference_url'] = normalize(response.url)
                yield doctor_hospital
        self.got_page(sk_d, 1)


