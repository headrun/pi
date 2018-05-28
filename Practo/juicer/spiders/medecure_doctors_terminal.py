from juicer.utils import *
from juicer.items import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class MedecureTerminal(JuicerSpider):
    name='medecure_doctors_terminal'
    #name = 'medecure_doctors_crawl'
    #start_urls =['http://www.medecure.com/profiles/25489/dr-p-kosala-raman.html']
    handle_http_status_list = ['500', '302', '403']

    def __init__(self, *args, **kwargs):
        super(MedecureTerminal, self).__init__(*args, **kwargs)
        self.pattern2 = re.compile('(.*):-(.*)')
        self.week_list = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    def parse(self, response):
        sel= Selector(response)
        doctor_sk = response.meta['sk']
        doctor_name = response.meta['data']['doctor_name']
        doctor_id = response.meta['data']['doctor_id']
        edu_qu = response.meta['data']['edu_qu']
        speciality = response.meta['data']['speciality']
        condition_treated = response.meta['data']['condition_treated']
        clinic_name = response.meta['data']['clinic_name']
        clinic_link = response.meta['data']['clinic_link']
        address = response.meta['data']['address']
        region = response.meta['data']['region']
        fee = response.meta['data']['fee']
        schedule_slot = response.meta['data']['schedule_slot']
        doc_booking_type = response.meta['data']['doc_booking_type']
        doctor_img = response.meta['data']['doctor_img']
        if 'common/no_image.jpg' in doctor_img: doctor_img = ''
        else: doctor_img = doctor_img
        if 'N/A'in fee: fee = ''
        else: fee = fee
        doctor_rev = response.meta['data']['doctor_rev']
        city = response.meta['data']['city']
        ref_url = response.meta['data']['ref_url']
        rating = response.meta['data']['rating']
        if doctor_sk:
            doctor_info = DoctorInfo()
            doctor_info.update({"doctor_sk":normalize(doctor_sk),"doctor_id":normalize(doctor_id),
                            "doctor_name":normalize(doctor_name),"doctor_profile_link":normalize(response.url),
                            "doctor_rating":normalize(normalize),
                            "qualification":normalize(edu_qu).replace(', ','<>'),"speciality":normalize(speciality),
                            "conditions_treated":normalize(condition_treated),"clinic_name":normalize(clinic_name),
                            "clinic_link":normalize(clinic_link),"address":normalize(address),
                            "region":normalize(region),"fee":normalize(fee),"schedule_slot":normalize(schedule_slot),
                            "booking_type":normalize(doc_booking_type),"doctor_image":normalize(doctor_img),
                            "no_of_doctor_reviews":normalize(doctor_rev),"reference_url":normalize(ref_url),
                            "city":normalize(city)})
            yield doctor_info
        doc_pr_type = extract_data(sel, '//div[@class="specialist_in open_sans left"]//text()')
        doc_pr_sp = extract_data(sel, '//div[@class="profile_info right"]/table/tr/td[contains(text(),"Speciality")]//following-sibling::td[@class="profile-table-spacing-content open_sans"]/text()')
        doc_pr_area = extract_data(sel, '//div[@class="profile_info right"]/table/tr/td[contains(text(),"Area of Practice")]//following-sibling::td[@class="profile-table-spacing-content open_sans"]/text()')
        doc_pr_qu = extract_data(sel, '//div[@class="profile_info right"]/table/tr/td[contains(text(),"Qualification")]//following-sibling::td[@class="profile-table-spacing-content open_sans"]/text()').replace(', ','<>')
        doc_pr_ls = extract_data(sel, '//div[@class="profile_info right"]/table/tr/td[contains(text(),"Language Spoken")]//following-sibling::td[@class="profile-table-spacing-content open_sans"]/text()').replace(', ', '<>')
        doc_pr_ps = extract_data(sel,'//div[@class="profile_info right"]/table/tr/td[contains(text(),"Practicing Since")]//following-sibling::td[@class="profile-table-spacing-content open_sans"]/text()')
        doc_pr_ct = extract_data(sel, '//div[@class="profile_info right"]/table/tr/td[contains(text(),"Conditions Treated")]//following-sibling::td[@class="profile-table-spacing-content open_sans"]//a/text()', '<>')
        doc_pr_book = extract_data(sel, '//div[@class="doctor_profile-details-rightdiv right"]/a[@class="book_appt_bt box_shadow clear right"]/text()')
        doc_cli_names = extract_data(sel, '//div[@class="profile_details_bar left open_sans"]/div[@class="open_sans hosp_name left"]//text()','<>')
        desc_1 = extract_data(sel, '//td[@style="margin: 0px; padding: 0px;"]/p//span[@class="txtcont"]/text()')
        desc_2 = extract_data(sel, '//div[@class="TabbedPanelsContent"]/p//text()')
        de1 = extract_data(sel, '//div[@class="TabbedPanelsContent"]//td[@valign="top"]/text()')
        de2 = ''.join(sel.xpath('//div[@class="TabbedPanelsContent"]//p/text()').extract()[0])
        if de1 and de2:
            desc_3 = normalize(de1)+normalize(de2)
        else: desc_3 = ''
        desc = desc_1 or desc_2 or desc_3
        awards_1 = extract_data(sel, '//div[@class="TabbedPanelsContent"]//div[@class="tab-contebt-affiliation"]/p/text()','<>')
        awards_2 = extract_data(sel, '//div[@class="TabbedPanelsContent"]//div[@class="tab-contebt-affiliation"]/ul/li/text()','<>')
        awards = normalize(awards_1) or normalize(awards_2)
        affli = extract_data(sel, '//div[@class="TabbedPanelsContent"]/table/tr/td/text()','<>')
        recomm_count = extract_data(sel, '//div[@id="recommended_cnt"]//text()')
        if recomm_count=='0': recomm_count=''
        else: recomm_count=recomm_count
        recomm_text = extract_data(sel, '//div[@class="recommendations_text_div left"]//text()')
        recomm_te = extract_data(sel, '//div[@class="recommend_by left small-font"]//text()').replace('|','<>')
        doc_article_title = extract_data(sel, '//div[@class="TabbedPanelsContent"]/ul/li[@class="open_sans"]/a/text()')
        doc_article_desc = extract_data(sel, '//div[@class="TabbedPanelsContent"]/ul//li/div[@class="clear"]//text()')
        doc_article_author = extract_data(sel, '//div[@class="TabbedPanelsContent"]/ul/li/div[@class="small-font clear"]/a/text()')
        if doctor_sk and doctor_id:
            doctor_meta = DoctorMeta()
            doctor_meta.update({"sk":normalize(doctor_sk),"doctor_id":normalize(doctor_id),
                                "doctor_name":normalize(doctor_name),"doctor_profile_link":normalize(response.url),
                                "doctor_rating":normalize(rating),
                                "qualification":normalize(doc_pr_qu),"speciality":normalize(doc_pr_sp),
                                "doctor_type":normalize(doc_pr_type).replace(', ','<>'),"languages_spoken":normalize(doc_pr_ls),
                                "area_of_practice":normalize(doc_pr_area),"practicing_since":normalize(doc_pr_ps),
                                "condition_treated":normalize(doc_pr_ct),"doctor_book_type":normalize(doc_pr_book),
                                "doctor_image":normalize(doctor_img),
                                "clinic_names":normalize(doc_cli_names),"about_doctor":normalize(desc),
                                "awards":normalize(awards),"affliations":normalize(affli),
                                "recommendations_count":normalize(recomm_count),
                                "recommendations_text":normalize(recomm_text),
                                "recommendations_name_date":normalize(recomm_te),
                                "doctor_article_title":normalize(doc_article_title),
                                "doctor_article_description":normalize(doc_article_desc),
                                "doctor_article_author":normalize(doc_article_author),
                                "reference_url":normalize(response.url)})
            yield doctor_meta
        self.got_page(doctor_sk,1)
        final_set = {'Mon':[], 'Tue':[], 'Wed':[], 'Thu':[], 'Fri':[], 'Sat':[], 'Sun':[]}
        if schedule_slot:
            hso_timesc_list = schedule_slot.split('<>')
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
                                    weeksf_list = [weeks1f, weeks2f,weeks3f]
                                except:
                                    try:
                                        weeks1f, weeks2f, weeks3f, weeks4f = weeks.split(',')
                                        weeksf_list = [weeks1f, weeks2f, weeks3f, weeks4f]
                                    except:
                                        try:
                                            weeks1f, weeks2f, weeks3f, weeks4f,weeks5f = weeks.split(',')
                                            weeksf_list = [weeks1f, weeks2f, weeks3f, weeks4f,weeks5f]
                                        except:
                                            weeks1f, weeks2f, weeks3f, weeks4f,weeks5f,weeks6f = weeks.split(',')
                                            weeksf_list = [weeks1f, weeks2f, weeks3f, weeks4f,weeks5f,weeks6f]
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
                                    scslotsi = [weekf_.strip()]
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
        hospital_sk = md5(normalize(doctor_sk)+normalize(clinic_name)+normalize(clinic_link)+normalize(schedule_slot))
        clinic_id = clinic_link.split('/')[-3]
        if hospital_sk and clinic_name:
            doctor_hospital = DoctorHospital()
            doctor_hospital.update({"sk":normalize(hospital_sk),
                                    "doctor_id":normalize(doctor_id),
                                    "hospital_link":normalize(clinic_link),
                                    "hospital_name":normalize(clinic_name),
                                    "hospital_address":normalize(address),
                                    "hospital_region":normalize(region),
                                    "hospital_monday_timing":normalize('<>'.join(final_dict.get('Mon',[]))),
                                    "hospital_tuesday_timing":normalize('<>'.join(final_dict.get('Tue',[]))),
                                    "hospital_wednesday_timing":normalize('<>'.join(final_dict.get('Wed',[]))),
                                    "hospital_thursday_timing":normalize('<>'.join(final_dict.get('Thu',[]))),
                                    "hospital_friday_timing" :normalize('<>'.join(final_dict.get('Fri',[]))),
                                    "hospital_saturday_timing":normalize('<>'.join(final_dict.get('Sat',[]))),
                                    "hospital_sunday_timing" :normalize('<>'.join(final_dict.get('Sun',[]))),
                                    "hospital_consultation_fee" :normalize(fee),
                                    "hospital_booking_type":normalize(doc_pr_book),
                                    "reference_url" :normalize(ref_url)})
            yield doctor_hospital
        review_dec = extract_data(sel, '//div[@class="TabbedPanelsContent"]/div[@class="left review_div"]/p/text()')
        if 'No reviews' in review_dec: review_dec=''
        else: review_dec = review_dec
        review_by = extract_data(sel, '//div[@class="left review_div"]/div[@class="left clear margin-top"]/text()').replace('-','')
        review_on = extract_data(sel, '//div[@class="left review_div"]/div[@class="left clear margin-top"]/span[@class="small-font"]/text()').replace('(','').replace(')','')
        review_sk = md5(normalize(doctor_sk)+normalize(review_dec)+normalize(review_by)+normalize(review_on))
        if review_sk and review_by:
            review_item = DoctorFeedback()
            review_item.update({"sk":normalize(review_sk),
                                "doctor_id":normalize(doctor_id),
                                "feedback_name":normalize(review_by),
                                "feedback_publish_date":normalize(review_on),
                                "feeback_text":normalize(review_dec),
                                "reference_url":normalize(response.url)})
            yield review_item

