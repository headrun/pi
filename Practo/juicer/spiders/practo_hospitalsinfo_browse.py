from juicer.utils import *
from juicer.items import HospitalInfo
from practo_hospitals_xpaths import *
import requests

class Practohospitals(JuicerSpider):
    name = 'practo_hospitalsinfo_browse'
    handle_http_status_list = ['302', '500', '403']

    def __init__(self, *args, **kwargs):
        super(Practohospitals, self).__init__(*args, **kwargs)
        self.domain = "https://www.practo.com"
        self.hospitals = '/hospitals'
        self.pagenumber =  kwargs.get('page', '')
        self.pagenumber = '%s%s'%('?page=',self.pagenumber)
        self.pageend = kwargs.get('end', '')
        self.phone_post_url = "https://www.practo.com/health/api/vn/vnpractice"
        self.particular_city = kwargs.get('city','')
        if self.particular_city:
            self.start_urls = ['https://www.practo.com/%s/hospitals'%self.particular_city]
        else:
            self.start_urls = ['https://www.practo.com/india']
        self.pattern1 = re.compile(r'\d+')

    def parse(self, response):
        sel = Selector(response)
        if not self.particular_city:
            city_links = sel.xpath(city_lks).extract()
            city_links1 = sel.xpath(city_lks1).extract()
            city_links.extend(city_links1)
            for city in city_links:
                city_url = "{}{}{}".format(self.domain, city, self.hospitals)
                #city_url = "{}{}{}{}".format(self.domain, city, self.hospitals, self.pagenumber)
                yield Request(city_url, callback=self.parse_cities, meta={'url':city_url})
        yield Request(response.url, callback=self.parse_cities, meta={'url': response.url}, dont_filter=True)

    def phoneno(self, url, hosid, proxy):
        headers = {
            'referer': url,
                'authority': 'www.practo.com',
                }
        params = (
            ('practice_id', hosid),
                 ('type', 'hospital'),
                )
        proxies = {'https': normalize(proxy)}
        data = ''
        try:
            data = requests.get(self.phone_post_url,headers=headers, params=params, proxies=proxies).text
        except:
            data = ''
        extension, phone_numbe = ['']*2
        if data:
            jsdata = {}
            try:
                jsdata = json.loads(data)
            except:
                jsdata = {}
            if jsdata:
                extension = jsdata.get('extension','')
                phone_numbe = jsdata.get('vn_phone_number',{}).get('number','')
        return phone_numbe, extension

    def parse_cities(self, response):
        sel = Selector(response)
        url = response.meta.get('url','')
        city_url = response.url
        if '/ie/unsupported' not in city_url:
            cvss = sel.xpath('//script[contains(text(), "window.__REDUX_STATE__")]/text()').extract()[0].split('window.__REDUX_STATE__=')[1]
            other_info = response.xpath('//script[@type="application/ld+json"]//text()').extract()
            book_type = response.xpath('//button[@data-qa-id="call_button"]//span//text()').extract()
            if len(other_info) >10:
                other_info = other_info[1:]
            else:
                other_info=other_info
            json_data = json.loads(cvss)
            listing =  json_data['listing']['list']
            doc_booking_type = 'Call Now'
            for data,more_info in zip(listing,other_info) :
                more_info = json.loads(more_info)
                link = more_info.get('url','')
                hosp_link = str(link)
                hosp_id =  data.get('id','')
                aux_infos = {}
                if hosp_id:
                    phone_numer, extension = self.phoneno(response.url, hosp_id, response.meta.get('proxy'))
                    if phone_numer:
                        aux_infos.update({"phone_number":phone_numer})
                    if extension:
                        aux_infos.update({"extension": extension})
                hosp_name = data.get('name','')
                hosp_location = more_info.get('address',{}).get('addressLocality','')
                hosp_medical_speciality = data.get('specialization','')
                hosp_no_of_doctor = data.get('doctors_count','')
                image_list = []
                hospital_images =  data.get('clinic_photos',{})
                for image in hospital_images :
                    image = image.get('url','')
                    image_list.append(image)
                hospital_images = "<>".join(image_list)
                hosp_feedback_count = str(data.get('reviews_count','0')) + ' '+'Feedback'  
                hosp_open_h = data.get('has_24x7_timings','')
                if hosp_open_h == True : hosp_open_h = 'Open 24 x 7'
                else : hosp_open_h = ''
                hosp_practo_guarentee = ''
                hsp_star_rat = ''
                hos_iso_acc = []
                hosp_iso_accr = data.get('accreditations',{})
                for accr in hosp_iso_accr :
                    accr_ = accr.get('accreditation_body',{})
                    for i in accr_ : 
                        try : acc_ = i.get('title',{})
                        except : acc = ''
                        if acc : hos_iso_acc.append(acc)
                hosp_iso_accr  = "& ".join(hos_iso_acc)  
                visit_times = data.get('timings', [])
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
                sch_list = '<>'.join(hsp_timesch)
                if not aux_infos : aux_infos = '' 
                if hosp_link and hosp_id:
                    hostp_item = self.parse_hospitalinfo(hosp_id, hosp_name, hosp_link, hospital_images,  hosp_location, hosp_medical_speciality, hosp_no_of_doctor, hsp_star_rat, hosp_feedback_count, hosp_practo_guarentee, doc_booking_type, hosp_open_h, sch_list, hosp_iso_accr, response.url, aux_infos)
                    self.get_page('practo_hospitalinfo_terminal', hosp_link, hosp_id,meta_data={"hsp_feed_count":hosp_feedback_count,"sch_list":sch_list})
                    if hostp_item:
                        yield hostp_item
            next_page = extract_data(sel, '//div[@data-qa-id="pagination_container"]/ul/li[@class="active"]//following-sibling::li[1]/a/@href')
            if next_page :
                next_page = self.domain+'/'+'chennai'+'/hospitals'+str(next_page) 
                if next_page:
                    yield Request(next_page, callback=self.parse_cities, meta={'url':response.url})


    def parse_hospitalinfo(self, hosp_id, hosp_name, hosp_link, hospital_images,  hosp_location, hosp_medical_speciality, hosp_no_of_doctor, hsp_star_rat, hosp_feedback_count, hosp_practo_guarentee, doc_booking_type, hosp_open_h, sch_list, hosp_iso_accr, response_url, aux_infos):
        hospital_item = HospitalInfo()
        hospital_item['hospital_id']                 = str(hosp_id)
        hospital_item['hospital_name']               = normalize(hosp_name)
        hospital_item['hospital_link']               = normalize(hosp_link)
        hospital_item['hospital_images']             = normalize(hospital_images)
        hospital_item['hospital_location']           = normalize(hosp_location)
        hospital_item['hospital_speciality']         = normalize(hosp_medical_speciality)
        hospital_item['no_of_doctors_in_hospital']   = str(hosp_no_of_doctor)
        hospital_item['hospital_star_rating']        = normalize(str(hsp_star_rat))
        hospital_item['hospital_feedback_count']     = normalize(hosp_feedback_count)
        hospital_item['hospital_practo_gurantee']    = normalize(hosp_practo_guarentee)
        hospital_item['hospital_booking_type']       = normalize(doc_booking_type)
        hospital_item['hospital_open_timings']       = str(hosp_open_h)
        hospital_item['hospital_schedule_timeslot']  = normalize(sch_list)
        hospital_item['hospital_accredited']         = normalize(hosp_iso_accr)
        hospital_item['reference_url']               = normalize(response_url)
        if aux_infos:
            hospital_item['aux_info']                    = normalize(json.dumps(aux_infos))
        return hospital_item

