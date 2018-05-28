from juicer.utils import *
from juicer.items import HospitalInfo
from practo_hospitals_xpaths import *
import requests

class LybrateHospitalsInfo(JuicerSpider):
    name = 'lybrate_hospitals_browse'
    handle_http_status_list = ['302', '500', '403']

    def __init__(self, *args, **kwargs):
        super(LybrateHospitalsInfo, self).__init__(*args, **kwargs)
        self.domain = "https://www.lybrate.com/"
        self.hospitals = '/hospitals'
        self.particular_city = kwargs.get('city','')
        if self.particular_city:
            self.start_urls = ['https://www.lybrate.com/get/ba/hospitals/facet/v2?ampPage=false&cityName=%s&currentLocation=false&ffR=false&find=&isClinicSearch=false&isHospitalSearch=true'%self.particular_city]
        else:
            self.start_urls = ['https://www.practo.com/india']
           

    def parse(self, response):
        sel = Selector(response)
        if not self.particular_city:
            city_links = sel.xpath(city_lks).extract()
            city_links1 = sel.xpath(city_lks1).extract()
            city_links.extend(city_links1)
            for city in city_links:
                city_url = "{}{}{}".format(self.domain, city, self.hospitals)
                yield Request(city_url, callback=self.parse_cities, meta={'url':city_url})
        yield Request(response.url, callback=self.parse_cities, meta={'url': str(self.domain) + str(self.particular_city) +str(self.hospitals)}, dont_filter=True)


    def parse_cities(self, response):
        url = response.meta.get('url','')
        data = response.body
        actual_data = self.get_hospitaldata(data,url,1)
        for item in actual_data :
            yield item
            self.get_page('lybrate_hospitals_terminal', item.get('hospital_link',''), item.get('hospital_id',''), meta_data={'url':item.get('reference_url',''),'city':self.particular_city,'aux_info':item.get('aux_info'),'availability':item.get('hospital_booking_type',''),'feedback_count':item.get('hospital_feedback_count',''),'star_rating':item.get('hospital_star_rating','')})
        responsedata = json.loads(response.body)
        total_pages = responsedata.get('totalPages','')
        for page in range(1,7):
            url = self.domain + self.particular_city + '/hospitals' + '?page=' + str(page)   
            link = 'https://www.lybrate.com/get/ba/hospitals/facet/v2?ampPage=false&cityName=%s&currentLocation=false&ffR=false&find=&isClinicSearch=false&isHospitalSearch=false&near=&page=%s&seoRequest=false&sortBy=BMS&source=FNB&totalPages=&zipSearch=false'%(self.particular_city,str(page))
            yield Request(link,callback=self.parse_nav, meta={'url': str(url), 'page': str(page) },dont_filter=True)

    def parse_nav(self,response):
         page = response.meta.get('page','')
         data = self.get_hospitaldata(response.body, response.meta.get('url',''), page)
         for item in data :
             yield item
             self.get_page('lybrate_hospitals_terminal', item.get('hospital_link',''), item.get('hospital_id',''), meta_data={'url':item.get('reference_url',''),'city':self.particular_city,'aux_info':item.get('aux_info'),'availability':item.get('hospital_booking_type',''),'feedback_count':item.get('hospital_feedback_count',''),'star_rating':item.get('hospital_star_rating','')})
        

    def get_hospitaldata(self, data, url, page):
        data = json.loads(data)
        hosp_data = data.get('profileDTOs','')
        hosp_list = []
        for data in hosp_data : 
            hosp_link = self.domain + self.particular_city + '/hospital/'+ data.get('slug','')
            votes = data.get('clinicPopularityScore','')
            rating = data.get('clinicRatings',{})
            doctors_count = data.get('doctorCountDTO',{}).get('totalCount','')
            hosp_name = data.get('name','')
            consult_charge = data.get('consultationChargeString','')
            hosp_id = data.get('clinicLocation',{}).get('id','')
            hosp_location = data.get('clinicLocation',{}).get('line1','')
            sche_list = []
            availability = data.get('appointmentAvailable','')
            if availability == True : book_type = 'Book Appointment'
            else : book_type  = ''
            call_avail = str(data.get('callAvailable',''))
            today_availability = str(data.get('availableToday',''))
            hosp_image =  str(data.get('profilePicUrl',''))
            hosp_timings = data.get('clinicOpeningHours',{})
            if hosp_timings : keys = hosp_timings.keys()
            for key in keys :
                sch_list = key +' : '+ "".join(hosp_timings.get(key,[]))
                sche_list.append(sch_list)
            if sche_list : sche_list = ",".join(sche_list)
            aux_infos = {}
            aux_infos.update({'call_avail':call_avail,'today_availability':today_availability})
            hospital_item = HospitalInfo()
	    hospital_item['hospital_id']                 = str(hosp_id)
	    hospital_item['hospital_name']               = normalize(hosp_name)
	    hospital_item['hospital_link']               = normalize(hosp_link)
	    hospital_item['hospital_images']             = normalize(hosp_image)
	    hospital_item['hospital_location']           = normalize(hosp_location)
	    hospital_item['hospital_speciality']         = ''
	    hospital_item['no_of_doctors_in_hospital']   = str(doctors_count)
	    hospital_item['hospital_star_rating']        = str(votes)
	    hospital_item['hospital_feedback_count']     = str(rating)
	    hospital_item['hospital_practo_gurantee']    = ''
            hospital_item['hospital_booking_type']       = normalize(book_type)
	    hospital_item['hospital_open_timings']       = ''
	    hospital_item['hospital_schedule_timeslot']  = str(sche_list)
	    hospital_item['hospital_accredited']         = ''
	    hospital_item['reference_url']               = normalize(url)
	    hospital_item['aux_info']                    = normalize(json.dumps(aux_infos))
            hosp_list.append(hospital_item)
        return hosp_list
            
          





