from juicer.utils import *
from juicer.items import *
import requests

class Askapolloterminal(JuicerSpider):
    name = 'askapollo_doctors_terminal'
    handle_http_status_list = ['302', '500', '403']

    def parse(self, response):
        sel = Selector(response)
        doc_id = response.meta['sk']
        doc_name = response.meta['data']['doc_name']
        sch_slot = response.meta['data']['sch_slot']
        doc_spe = response.meta['data']['doc_spe']
        ref_url = response.meta['data']['ref_url']
        doc_booking_type = response.meta['data']['doc_booking_type']
        address = response.meta['data']['address']
        doc_exp = response.meta['data']['doc_exp']
        dct_hsp = response.meta['data']['dct_hsp']
        doc_feed = response.meta['data']['doc_feed']
        phone_number = response.meta['data']['doc_pne']
        aux_info1 = {}
        doc_photo = response.meta['data']['doc_photo']
        if '/defaultprofilepic' in doc_photo:
            doc_photo1 = ''
        else:
            doc_photo1 = 'https://www.askapollo.com/physical-appointment'+normalize(doc_photo).replace('..','')
        languages_spoken = extract_data(sel, '//div[@class="doc-profile-block"]/div[@class="col-sm-8 dr-info"]//ul[@class="quick-info"]/li/span[@id="MainContent_lblLang"]/text()').replace(',','<>')
        qualification = normalize(extract_data(sel, '//div[@class="qualification_details"]//div[@class="personal-list qualification"]/span[@id="MainContent_lblQualificationTab"]/text()')).replace(',','<>').replace('; ','<>').replace(', ','')
        summary = ''.join(response.xpath('//div[@class="curriculam-Vitae"]//div[@id="MainContent_pnlSummary"]/div[@class="personal-list"]/span/ul/li//text()').extract()).replace('\r','').replace('\t','').replace('\n','').encode('utf8')
        awards_ach = '<>'.join(sel.xpath('//div[@class="curriculam-Vitae"]//div[@class="personal-list"]//span[@id="MainContent_lblAwards"]/ul/li//text()').extract()).replace('\n','').replace('\t','').replace('\r','').encode('utf8')
        if not awards_ach:
            awards_ach = '<>'.join(sel.xpath( '//div[@class="curriculam-Vitae"]/div[@id="MainContent_pnlAwards"]/div[@class="personal-list"]//span[@id="MainContent_lblAwards"]/table//tr//p//text()').extract()).replace('\r','').replace('\t','').replace('\n','')
        research_pub = '<>'.join(sel.xpath('//div[@class="curriculam-Vitae"]//div[@class="personal-list"]//span[@id="MainContent_lblResearch"]/ul/li//text()').extract()).replace('\n','').replace('\t','').replace('\r','').encode('utf8')
        if not research_pub:
            research_pub = '<>'.join(sel.xpath('//div[@class="curriculam-Vitae"]//div[@id="MainContent_pnlResearch"]/div[@class="personal-list"]//span[@id="MainContent_lblResearch"]/table//tr//p//text()').extract()).replace('\t','').replace('\n','').replace('\r','').encode('utf8')
        work_exp = '<>'.join(sel.xpath('//div[@class="curriculam-Vitae"]//div[@class="personal-list"]//span[@id="MainContent_lblWorkExp"]/ul/li//text()').extract()).replace('\n','').replace('\t','').replace('\r','').encode('utf8')
        if not work_exp:
            work_exp = '<>'.join(sel.xpath('//div[@class="curriculam-Vitae"]/div[@id="MainContent_pnlWorkExperience"]/div[@class="personal-list"]/span[@id="MainContent_lblWorkExp"]/table//tr//p//text()').extract()).replace('\t','').replace('\n','').replace('\r','').encode('utf8')
        cer_profmem = '<>'.join(sel.xpath('//div[@class="curriculam-Vitae"]//div[@class="personal-list"]//span[@id="MainContent_lblMembership"]/ul/li//text()').extract()).replace('\n','').replace('\t','').replace('\r','').encode('utf8')
        if not cer_profmem:
            cer_profmem = '<>'.join(response.xpath('//div[@class="curriculam-Vitae"]/div[@id="MainContent_pnlMemberships"]/div[@class="personal-list"]/span[@id="MainContent_lblMembership"]/table//tr//p//text()').extract()).replace('\t','').replace('\n','').replace('\r','').encode('utf8')
        medical_con_reg = extract_data(sel, '//div[@class="curriculam-Vitae"]//div[@class="personal-list"]//span[@id="MainContent_lblRegistrations"]//text()')
        special_int = '<>'.join(sel.xpath('//div[@class="curriculam-Vitae"]//div[@class="personal-list"]//span[@id="MainContent_lblSpecialInterests"]/ul/li//text()').extract()).replace('\n','').replace('\t','').replace('\r','').replace(', ','<>').encode('utf8')
        doctor_lin = sel.xpath('//div[@class="col-md-6"]/div[@id="MainContent_pnlDoctorLinks"]/span/a/@href').extract()
        doctor_text = sel.xpath('//div[@class="col-md-6"]/div[@id="MainContent_pnlDoctorLinks"]/span/a/text()').extract()
        doctors_link = map(lambda a, b: a +', '+ b, doctor_text, doctor_lin)
        doctors_link1='<>'.join(list(set(doctors_link)))
        city_speciality_links = sel.xpath('//div[@class="col-md-6"]/div[@id="MainContent_pnlCitySpecialistLinks"]/span/a/@href').extract()
        city_speciality_text = sel.xpath('//div[@class="col-md-6"]/div[@id="MainContent_pnlCitySpecialistLinks"]/span/a/text()').extract()
        city_specialist_links = map(lambda x, y: x +', '+ y, city_speciality_text,city_speciality_links)
        city_specialist_links1 = '<>'.join(list(set(city_specialist_links)))

        services = '<>'.join(sel.xpath('//div[@class="col-md-6"]/div[@id="MainContent_pnlSpecialityServices"]//table[@id="dlSpecialityServices"]//tr/td/a/text()').extract())
        other_popular_hyper_locations_text = sel.xpath('//div[@class="col-md-6"]/div[@id="MainContent_pnlPopularHyperLocations"]//table[@id="MainContent_dlPopularHyperLocations"]//tr/td/a/text()').extract()
        other_popular_hyper_locations_link = sel.xpath('//div[@class="col-md-6"]/div[@id="MainContent_pnlPopularHyperLocations"]//table[@id="MainContent_dlPopularHyperLocations"]//tr/td/a/@href').extract()
        popular_hyper_locations = map(lambda a1, b1: a1 +', '+ b1, other_popular_hyper_locations_text,other_popular_hyper_locations_link)
        popular_hyper_locations1 = '<>'.join(list(set(popular_hyper_locations)))
        popular_treatments = '<>'.join(sel.xpath('//table[@id="MainContent_dlPopularTreatments"]//tr/td/a/text()').extract())
        searched_localities_text = sel.xpath('//table[@id="MainContent_dlHyperLocations"]//tr/td/a/text()').extract()
        searched_localities_links = sel.xpath('//table[@id="MainContent_dlHyperLocations"]//tr/td/a/@href').extract()
        most_searched_localities = map(lambda x1, y1: x1 +', '+ y1, searched_localities_text,searched_localities_links)
        most_searched_localities1 = '<>'.join(list(set(most_searched_localities)))
        special_treatments = '<>'.join(sel.xpath('//table[@id="MainContent_dlSpecialtyTreatments"]//tr/td/a/text()').extract())
        other_desc1 = '.'.join(sel.xpath('//div[@class="content-block dr-profile"]//span[@id="MainContent_lblSpecialityContent"]//text()').extract()).encode('utf8')
        other_desc2 = '.'.join(sel.xpath('//div[@class="content-block dr-profile"]//span[@id="MainContent_lblBoilerContent"]//text()').extract()).encode('utf8')
        other_desc = other_desc1+other_desc2
        aux_info2 = {}
        days = ''.join(response.xpath('//div[@class="col-sm-8 dr-info"]//ul[@class="quick-info"]//li/span[@id="MainContent_lblAvaliableDayNameShortForm"]/text()').extract())
        timings = ''.join(response.xpath('//div[@class="col-sm-8 dr-info"]//ul[@class="quick-info"]//li/span[@id="MainContent_lblAvailableTime"]/text()').extract())
        time_schedule = days +':-'+timings
        if doc_id and doc_name:
            doctor_listing = DoctorInfo()
            doctor_listing.update({"doctor_id":normalize(doc_id), "doctor_name":normalize(doc_name), "doctor_profile_link" : normalize(response.url),
                                    "years_of_experience":normalize(doc_exp), "recomandations":normalize(doc_feed),
                                    "specialization": normalize(doc_spe), "address": normalize(address),
                                    "schedule_timeslot":normalize(sch_slot),"doctor_image":normalize(doc_photo1),"clinic_names":normalize(dct_hsp),
                                    "booking_type":normalize(doc_booking_type),"reference_url":normalize(ref_url), "phone_number":normalize(phone_number)})
            if aux_info2:
                doctor_listing.update({"aux_info":json.dumps(aux_info2)})
            yield doctor_listing
            doctor_meta = DoctorMeta()
            doctor_meta.update({"sk":normalize(doc_id),"doctor_id":normalize(doc_id),"doctor_name":normalize(doc_name),
                        "doctor_profile_link":normalize(response.url),"qualification":normalize(qualification),"specialization":normalize(doc_spe),
                        "years_of_experience":normalize(doc_exp),"research_and_publications":normalize(research_pub),
                        "languages_spoken":normalize(languages_spoken),"special_interets":normalize(special_int),
                        "services":normalize(services),"awards_recognitions":normalize(awards_ach),"summary":normalize(summary),
                        "clinic_names": normalize(dct_hsp),"time_schedule":normalize(time_schedule),
                        "memeberships":normalize(cer_profmem),"experience":normalize(work_exp),"medical_council_registration":normalize(medical_con_reg),
                        "recommendations":normalize(doc_feed),"doctor_image":normalize(doc_photo1),"doctor_links":normalize(doctors_link1),
                        "city_specialist_links":normalize(city_specialist_links1),"popular_hyper_locations":normalize(popular_hyper_locations1),
                        "most_searched_localities":normalize(most_searched_localities1),"popular_treatments":normalize(popular_treatments),
                        "treatments":normalize(special_treatments),"other_description":normalize(other_desc),"reference_url":normalize(response.url)})
            if aux_info1:
                doctor_listing.update({"aux_info":json.dumps(aux_info1)})
            yield doctor_meta
        #self.got_page(doc_id, 1)
        nodes = response.xpath('//div[@id="pnlFeedabckDetail"]//td[@class="DataList"]')
        for node in nodes:
            feed_name = extract_data(node, './/td/span[@class="FeedbackTitle"]//text()')
            created_on = extract_data(node, './/td/span[@class="CreatedOn"]//text()')
            craeted_by = extract_data(node, './/td/span[@class="CreatedBy"]//text()')
            review_text = extract_data(node, './/span[@class="Feedback"]//text()')
            review_sk = md5(normalize(feed_name)+normalize(created_on)+normalize(craeted_by)+normalize(review_text))
            aux_info3 = {}
            if review_sk and doc_id:
                doctor_feedback = DoctorFeedback()
                doctor_feedback.update({"sk":normalize(review_sk),"doctor_id":normalize(doc_id),"feedback_name":normalize(craeted_by),
                                        "feedback_filters":normalize(feed_name),"feedback_publish_date":normalize(created_on),
                                        "feeback_text":normalize(review_text),"reference_url":normalize(response.url)})
                if aux_info3:
                    doctor_feedback.update({"aux_info":json.dumps(aux_info3)})
                yield doctor_feedback
        self.got_page(doc_id, 1)



