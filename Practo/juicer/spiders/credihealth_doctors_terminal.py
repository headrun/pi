from juicer.utils import *
from practo_doctorsinfo_xpaths import *
from juicer.items import *
import re

class CredicoctorsTerminal(JuicerSpider):
    name = 'credihealth_doctors_terminal'
    handle_http_status_list = ['302', '504','403','404']
    def __init__(self, *args, **kwargs):
        super(CredicoctorsTerminal, self).__init__(*args, **kwargs)

    def parse(self, response):
        sel = Selector(response)
        hosp_con_fee,sch_timings = '',''
	dct_id = sk_d = response.meta['sk']
        doc_desg = normalize("".join(sel.xpath('//div[@class="doctor-designation"]//text()').extract()))
        doctor_listing = response.meta.get('data','').get('doctor_listing','').replace('&nbsp;','')
        try : 
            data = json.loads(normalize(sel.xpath('//script[@type="application/ld+json"]//text()').extract()[1]))
            doc_desc = normalize(data.get('description',''))
        except : doc_desc = normalize("".join(sel.xpath('//div[@class="doctor-description"]//p//text()').extract())).replace('&nbsp;','')
        education,experience,awards = [],[],[]
        edu_nodes = sel.xpath('//h2//div[contains(text(), "Education")]/../following-sibling::div/table')
        for node in edu_nodes:
           tr_nodes = node.xpath('.//tbody//tr')
           for tr_node in tr_nodes:
               course = "".join(tr_node.xpath('./td[1]/text()').extract())
               institute = "".join(tr_node.xpath('./td[2]/text()').extract())
               year = "".join(tr_node.xpath('./td[3]/text()').extract())
               doc_edu = course+', Institute:'+institute+', Year:'+ year
               education.append(doc_edu)
        doctor_edu = "<>".join(education)
        if doctor_edu : doctor_edu = normalize(normalize(doctor_edu).replace('----',''))
        else : doctor_edu = ''
        exp_nodes = sel.xpath('//h2//div[contains(text(), "Experience")]/../following-sibling::div/table')     
        for node in exp_nodes:
           tr_nodes = node.xpath('.//tbody//tr')
           for tr_node in tr_nodes:
               desg = "".join(tr_node.xpath('./td[1]/text()').extract())
               hosp = "".join(tr_node.xpath('./td[2]/text()').extract())
               year = "".join(tr_node.xpath('./td[3]/text()').extract())
               doc_exp = desg+','+'Hospital:'+hosp+', year: '+year
               experience.append(doc_exp)
        doctor_exp = "<>".join(experience)
        if doctor_exp : doctor_exp = normalize(normalize(doctor_exp).replace('----',''))
        else : doctor_exp = ''
        award_nodes = sel.xpath('//h2//div[contains(text(), "Awards and Achievements")]/../following-sibling::div/table')
        for node in award_nodes:
           tr_nodes = node.xpath('.//tbody//tr')
           for tr_node in tr_nodes:
               title = "".join(tr_node.xpath('./td[1]/text()').extract())
               year = "".join(tr_node.xpath('./td[2]/text()').extract())
               doc_award = title+', year:'+year
               awards.append(doc_award)
        doctor_award = "<>".join(awards)
        if doctor_award : doctor_award = normalize(normalize(doctor_award).replace('----',''))
        else : doctor_award = ''
        fee_currency = ''
        no_of_awards = normalize("".join(sel.xpath('//div[@class="text-center"]//div[contains(text(),"Award")]//text()').extract()))
        doc_image = "".join(sel.xpath('//div[@class="fullwidth credi-box"]//img[@class="credi-image-box doctor-image-brdr"]/@src').extract())
        if hosp_con_fee : fee_currency = 'INR'
        doc_meta_exp = normalize("".join(sel.xpath('//div[@class="text-center"]//div[contains(text(),"Experience")]//text()').extract()))
        hospital_nodes = sel.xpath('//div[@class="fullwidth credi-box"]/div[@class="fullwidth"]')
        for node in hospital_nodes :
            hosp_link = "".join(node.xpath('.//a[contains(@href,"hospital")]//@href').extract())
            try : hosp_id = hosp_link.split('/')[-2]
            except : continue
            hosp_name = hosp_id.replace('-',' ')
            hosp_con_fee = ''
            fee = normalize("".join(node.xpath('.//span[contains(text(),"INR:")]//text()').extract()))
            hosp_book_type = normalize("".join(node.xpath('.//a[@class="btn credi-bclr"]//text()').extract()))
            if fee : 
                hosp_con_fee = "".join(re.findall('\d+',fee))
                fee_currency = "INR"
            hsp_address = normalize("".join(node.xpath('.//small//div//text()').extract()))
            sch_list = []
            timing_nodes = node.xpath('.//table//tr')
            for times in timing_nodes :
                times = normalize("<>".join(times.xpath('.//td//text()').extract())).replace('<> <> <>','<>').replace('<> <>',',').replace('<>','').strip()
                sch_list.append(times)

                if sch_list : sch_timings = "<>".join(sch_list)
            timings_data = self.parse_timings(sch_timings)
            if sch_timings : final_dict = self.parse_timings(sch_timings)    
            else : final_dict = {}
            if sk_d and hosp_link:
                doctor_hospital = DoctorHospital()
                doctor_hospital['sk'] = md5("%s%s"%(hosp_link, dct_id))
                doctor_hospital['doctor_id'] = normalize(dct_id)
                doctor_hospital['hospital_location'] = normalize(hsp_address)
                doctor_hospital['hospital_link'] = normalize(hosp_link)
                doctor_hospital['hospital_name'] =  normalize(hosp_name)
                doctor_hospital['hospital_rating'] = ''
                doctor_hospital['hospital_address'] = normalize(hsp_address)
                doctor_hospital['hospital_monday_timing'] = normalize('<>'.join(final_dict.get('Mon',[])))
                doctor_hospital['hospital_tuesday_timing'] = normalize('<>'.join(final_dict.get('Tue',[])))
                doctor_hospital['hospital_wednesday_timing'] =  normalize('<>'.join(final_dict.get('Wed',[])))
                doctor_hospital['hospital_thursday_timing'] = normalize('<>'.join(final_dict.get('Thu',[])))
                doctor_hospital['hospital_friday_timing'] = normalize('<>'.join(final_dict.get('Fri',[])))
                doctor_hospital['hospital_saturday_timing'] = normalize('<>'.join(final_dict.get('Sat',[])))
                doctor_hospital['hospital_sunday_timing'] = normalize('<>'.join(final_dict.get('Sun',[])))
                doctor_hospital['hospital_consultation_fee'] = normalize(hosp_con_fee)
                doctor_hospital['hospital_practo_gurantee'] = ''
                doctor_hospital['hospital_photos'] = ''
                doctor_hospital['hospital_booking_type'] = hosp_book_type
                doctor_hospital['hospital_latitude'] = ''
                doctor_hospital['hospital_longitude'] = ''
                doctor_hospital['reference_url'] = normalize(response.url)
                yield doctor_hospital

            doctor_data = DoctorInfo()
            doctor_data['doctor_id'] = str(dct_id)
            doctor_data['doctor_name'] =  normalize(doctor_listing.get('doctor_name',''))
            doctor_data['doctor_profile_link'] = normalize(doctor_listing.get('doctor_profile_link',''))
            doctor_data['qualification'] = normalize(doctor_listing.get('qualification',''))
            doctor_data['years_of_experience'] = normalize(doctor_listing.get('years_of_experience',''))
            doctor_data['specialization'] = normalize(doctor_listing.get('specialization',''))
            doctor_data['rating'] =  normalize(doctor_listing.get('rating',''))
            doctor_data['vote_count'] = ''
            doctor_data['feedback_count'] = str(no_of_awards)
            doctor_data['location'] = ''
            doctor_data['address'] = ''
            doctor_data['consultation_fee'] = doctor_listing.get('consultation_fee','')
            doctor_data['schedule_timeslot'] = str(sch_timings)
            doctor_data['doctor_image'] = str(doc_image)
            doctor_data['clinic_names'] = normalize(doctor_listing.get('clinic_names',''))
            doctor_data['clinic_images'] = ''
            doctor_data['location_latitude'] = ''
            doctor_data['location_longitude'] = ''
            doctor_data['region'] = doc_desg
            doctor_data['fee_currency'] = fee_currency
            doctor_data['booking_type'] = normalize(doctor_listing.get('booking_type',''))
            doctor_data['reference_url'] = normalize(doctor_listing.get('reference_url',''))
            yield doctor_data

        if dct_id:
                doctor_meta  = DoctorMeta()
                doctor_meta['sk'] = normalize(sk_d)
                doctor_meta['doctor_id'] = normalize(dct_id)
                doctor_meta['doctor_name'] = normalize(doctor_listing.get('doctor_name',''))
                doctor_meta['doctor_profile_link'] = normalize(doctor_listing.get('doctor_profile_link',''))
                doctor_meta['qualification'] = normalize(doctor_listing.get('qualification',''))
                doctor_meta['specialization'] = normalize(doctor_listing.get('specialization',''))
                doctor_meta['years_of_experience'] = doc_meta_exp
                doctor_meta['medical_registration_verified'] = ''
                doctor_meta['rating'] = normalize(doctor_listing.get('rating',''))
                doctor_meta['vote_count'] =  ''
                doctor_meta['summary'] = doc_desc
                doctor_meta['services'] = normalize(doctor_award)
                doctor_meta['specializations'] = normalize(doctor_listing.get('specialization',''))
                doctor_meta['education'] = normalize(doctor_edu)
                doctor_meta['memeberships'] = ''
                doctor_meta['experience'] = normalize(doctor_exp)
                doctor_meta['registrations'] = ''
                doctor_meta['feedback_count'] = no_of_awards
                doctor_meta['doctor_image'] = normalize(doc_image)
                doctor_meta['reference_url'] = normalize(response.url)
                doctor_meta['aux_info'] = json.dumps({"city": 'chennai'})
                yield doctor_meta
                self.got_page(sk_d, 1)

        
    def parse_timings(self,opening_hours):
        opening_hours = opening_hours.split('<>')
        week_list = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']
        week_days = {'Sun':[],'Mon':[],'Tue':[],'Wed':[],'Thu':[],'Fri':[],'Sat':[]}
        Sun,Mon,Tue,Wed,Thu,Fri,Sat = [],[],[],[],[],[],[]
        for times in opening_hours :
             for i in week_list : 
                 if i in times :
                     val = week_days[i]
                     times = times.replace(i,'').strip()
                     val.append(times)
                     week_days.update({i:val})
        return week_days
      
                    
                       
