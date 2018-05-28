"""from juicer.utils import *
from juicer.items import HospitalInfo
from practo_hospitals_xpaths import *
import requests

class Practohospitals(JuicerSpider):
    name = 'practo_hospitals_browse'
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
        else:
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
        import pdb;pdb.set_trace()
        url = response.meta.get('url','')
        city_url = response.url
        if '/ie/unsupported' not in city_url:
            nodes = get_nodes(sel, doc_nodes)
            for nd in nodes:
                hosp_link = extract_data(nd, hosp_link_xpb)
                hosp_id = extract_data(nd, hosp_id_xpb)
                if hosp_id:
                    hosp_id = textify(self.pattern1.findall(hosp_id))

                aux_infos = {}
                if hosp_id:
                    phone_numer, extension = self.phoneno(response.url, hosp_id, response.meta.get('proxy'))
                    if phone_numer:
                        aux_infos.update({"phone_number":phone_numer})
                    if extension:
                        aux_infos.update({"extension": extension})
                hosp_name = extract_data(nd, hosp_name_xpb)
                hosp_location = extract_data(nd, hosp_location_xpb,', ')
                hosp_medical_speciality = extract_data(nd, hosp_medical_speciality_xpb)
                hosp_no_of_doctor = extract_data(nd, hosp_no_of_doctor_xpb)#67 Doctors
                hospital_images = extract_data(nd, hospital_images_xpb, '<>')
                hsp_star_rat = extract_list_data(nd, hsp_star_rat_xpath)
                hsp_star_rat1 = extract_list_data(nd, hsp_star_rat1_xpath)
                if hsp_star_rat and hsp_star_rat1:
                    hsp_star_rat = len(hsp_star_rat)
                    hsp_star_rat = hsp_star_rat+len(hsp_star_rat1)*0.5
                elif hsp_star_rat and not hsp_star_rat1:
                    hsp_star_rat = len(hsp_star_rat)
                elif hsp_star_rat1 and not hsp_star_rat:
                    hsp_star_rat = len(hsp_star_rat1)*0.5
                else:
                    hsp_star_rat = ''
                hosp_feedback_count = extract_data(nd, hosp_feedback_count_xpb)
                hosp_open_h = extract_data(nd, hosp_open_h_xpb)#Open 24 x 7
                hosp_practo_guarentee = extract_data(nd, hosp_practo_guarentee_xpb)
                if hosp_practo_guarentee and 'http' not in hosp_practo_guarentee:
                    hosp_practo_guarentee = "%s%s" % (self.domain, hosp_practo_guarentee)
                doc_booking_type = extract_data(nd, doc_booking_type_xpb)
                sch_list = []
                doc_schedule_nodes = nd.xpath(doc_schedule_nodes_xpb)
                for sch in doc_schedule_nodes:
                    sch_days = extract_data(sch, sch_days_xpb, ', ')
                    sch_timings = extract_data(sch, sch_timings_xpb,', ')
                    sch_slot = ("%s%s%s"%(sch_days,':-',sch_timings)).strip('<>')
                    if sch_slot:
                        sch_list.append(sch_slot)
                sch_list = '<>'.join(sch_list).strip('<>:-')
                hosp_iso_accr = extract_data(nd, hosp_iso_accr_xpb)#ISO Accredited
                if hosp_link and hosp_id:
                    hostp_item = self.parse_hospitalinfo(hosp_id, hosp_name, hosp_link, hospital_images,  hosp_location, hosp_medical_speciality, hosp_no_of_doctor, hsp_star_rat, hosp_feedback_count, hosp_practo_guarentee, doc_booking_type, hosp_open_h, sch_list, hosp_iso_accr, response.url, aux_infos)
                    self.get_page('practo_hospitals_terminal', hosp_link, hosp_id)
                    if hostp_item:
                        yield hostp_item

            next_page = extract_data(sel, next_path_xpb)
            #if 'page=%s'%self.pageend in response.url: next_page = ''
            if next_page and  self.crawl_type=="catchup":
                yield Request(next_page, callback=self.parse_cities, meta={'url':response.url})


    def parse_hospitalinfo(self, hosp_id, hosp_name, hosp_link, hospital_images,  hosp_location, hosp_medical_speciality, hosp_no_of_doctor, hsp_star_rat, hosp_feedback_count, hosp_practo_guarentee, doc_booking_type, hosp_open_h, sch_list, hosp_iso_accr, response_url, aux_infos):
        hospital_item = HospitalInfo()
        hospital_item['hospital_id']                 = normalize(hosp_id)
        hospital_item['hospital_name']               = normalize(hosp_name)
        hospital_item['hospital_link']               = normalize(hosp_link)
        hospital_item['hospital_images']             = normalize(hospital_images)
        hospital_item['hospital_location']           = normalize(hosp_location)
        hospital_item['hospital_speciality']         = normalize(hosp_medical_speciality)
        hospital_item['no_of_doctors_in_hospital']   = normalize(hosp_no_of_doctor)
        hospital_item['hospital_star_rating']        = normalize(str(hsp_star_rat))
        hospital_item['hospital_feedback_count']     = normalize(hosp_feedback_count)
        hospital_item['hospital_practo_gurantee']    = normalize(hosp_practo_guarentee)
        hospital_item['hospital_booking_type']       = normalize(doc_booking_type)
        hospital_item['hospital_open_timings']       = normalize(hosp_open_h)
        hospital_item['hospital_schedule_timeslot']  = normalize(sch_list)
        hospital_item['hospital_accredited']         = normalize(hosp_iso_accr)
        hospital_item['reference_url']               = normalize(response_url)
        if aux_infos:
            hospital_item['aux_info']                    = normalize(json.dumps(aux_infos))
        return hospital_item"""

