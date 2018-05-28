from juicer.utils import *
from juicer.items import DoctorInfo
from lybrate_doctors_xpaths import *
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class LybrateDoctors(JuicerSpider):
    name = 'lybrate_doctorsapi_browse'
    handle_http_status_list = ['302', '500', '403']
    #start_urls = ['https://www.lybrate.com/get/ba/doctors/facet/v2?ampPage=false&cityName=warangal&currentLocation=false&ffR=false&find=&isClinicSearch=false&isHospitalSearch=false&near=&page=2&seoRequest=false&sortBy=BMS&source=FNB&totalPages=&zipSearch=false']
    def __init__(self, *args, **kwargs):
        super(LybrateDoctors, self).__init__(*args, **kwargs)
        self.domain = "https://www.lybrate.com/"
        self.doctors = '/doctors'
        self.pattern2 = re.compile('(.*) (.*)')
        self.week_list = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        self.pagenumber =  kwargs.get('page', '')
        self.pagenumber = '%s%s'%('?page=',self.pagenumber)
        self.pageend = kwargs.get('end', '')
        self.particular_city = kwargs.get('city','')
        if self.particular_city:
            self.start_urls = ['https://www.lybrate.com/get/ba/doctors/facet/v2?ampPage=false&cityName=%s&currentLocation=false&ffR=false&find=&isClinicSearch=false&isHospitalSearch=false&near=&page=1&seoRequest=false&sortBy=BMS&source=FNB&totalPages=&zipSearch=false'%self.particular_city]

    def parse(self,response):
        reg = self.particular_city
        for i in range(1,7):
            next_page = 'https://www.lybrate.com/get/ba/doctors/facet/v2?ampPage=false&cityName=warangal&currentLocation=false&ffR=false&find=&isClinicSearch=false&    isHospitalSearch=false&near=&page=%s&seoRequest=false&sortBy=BMS&source=FNB&totalPages=&zipSearch=false'%(i)
            city_url = self.domain+reg+'/doctors?page=%s'%(i)
            yield Request(next_page, callback=self.parse_next,meta={"city_url":city_url})

    def parse_next(self,response):
        print response.url
        import pdb;pdb.set_trace()
        city_url = response.meta['city_url']
        main_data = json.loads(response.body)
        doc_meta = main_data.get('profileDTOs', [])
        for doc_info in doc_meta:
            aux_infos = {}
            cli_loc = doc_info.get('clinicLocation',{})
            cli_id = cli_loc.get('id', '')
            if cli_id:
                aux_infos.update({"clinic_location_id":cli_id})
            cli_name = cli_loc.get('name', '').replace(', ','<>')
            cli_add = cli_loc.get('line1', '')
            if cli_add: cli_add = cli_add
            else: cli_add = ''
            cli_loca = cli_loc.get('localityName', '')
            if cli_loca: cli_loca = cli_loca
            else: cli_loca = ''
            cli_locurl = cli_loc.get('localityUrl', '')
            cli_locid = cli_loc.get('localityId', '')
            cli_sta = cli_loc.get('state', '')
            if cli_sta: cli_sta = cli_sta
            else : cli_sta= cli_sta
            cli_pin = cli_loc.get('pincode', '')
            if cli_pin: cli_pin= cli_pin
            else: cli_pin = ''
            clinic_address =cli_add+' '+cli_loca+' '+cli_sta+' '+cli_pin
            cli_cou = cli_loc.get('country', '')
            cli_cityid = cli_loc.get('cityId', '')
            cli_cityna = cli_loc.get('cityName', '')
            cli_lat = str(cli_loc.get('latitude', ''))
            if 'None' in cli_lat:
                cli_lat = ''
            else: cli_lat = cli_lat
            cli_lon = str(cli_loc.get('longitude', ''))
            if 'None' in cli_lon:
                cli_lon = ''
            else: cli_lon = cli_lon
            cli_slug = cli_loc.get('slug', '')
            cli_preslug = cli_loc.get('preSlugUrl', '')
            cli_cha = str(cli_loc.get('consultationCharges', ''))
            if 'None' in cli_cha:
                cli_cha = ''
            else: cli_cha = cli_cha
            cli_nearlocid = cli_loc.get('nearestLocalityId', '')
            cli_type = cli_loc.get('clinicType', '')
            if cli_type:
                aux_infos.update({"clinic_type":normalize(cli_type)})
            username = doc_info.get('username','')
            qua = doc_info.get('degrees','')
            if qua: qua = qua.replace(', ','<>')
            else: qua= ''
            spe = doc_info.get('specialityName','')
            if spe: spe= spe.replace(', ','<>')
            else: spe=''
            name1 = str(doc_info.get('name',''))
            prefix = str(doc_info.get('namePrefix', ''))
            name = prefix+' '+name1
            sub_spe = '<>'.join(doc_info.get('subSpecialities',[]))
            exp = doc_info.get('experience','')
            image = doc_info.get('profilePicUrl','')
            if image: image= image.replace(',','<>')
            else : image = ''
            cli_image = doc_info.get('clPhotoDTOs',[])
            if cli_image:
                cli_images = '<>'.join([i.get('original','') for i in cli_image])
            else: cli_images = ''
            rat = str(doc_info.get('userRatings',''))
            if 'None' in rat: 
                rat = ''
            else: rat = rat
            popu = str(doc_info.get('userPopularityScore',''))
            if 'None' in popu:
                popu = ''
            else: popu=popu
            rec_vis = doc_info.get('freqUsedKeywords','')
            if rec_vis: rec_vis = rec_vis.replace(', ','<>')
            else: rec_vis = ''
            feed_co = doc_info.get('feedbackCount','')
            feed_li = doc_info.get('feedbackLink','')
            sch_slot,values1 = '',''
            if feed_li:
                main_link = feed_li.split('#')[-2]
            day = doc_info.get('openingHours',{}).keys()
            values1 = doc_info.get('openingHours',{}).values()
            hsp_timesch=[]
            hsp_timesch1 = ''
            if values1:
                timee = [''.join(item) for item in values1]
                for days,timess in zip(day,timee):
                    day_list=[]
                    days1 = ''.join(days)
                    if ',' in days1:
                        day1 = days1.split(',')
                        for da in day1:
                            da1= da.strip(' ')
                            day_list.append(da1)
                        for da2 in day_list:
                            if not ', ' in da2:
                                hsp_timesch.append(("%s%s%s") % (da2,':-',timess ))
                    else:
                        hsp_timesch.append(("%s%s%s") % (days1, ':-',timess ))
                hsp_timesch1 = '<>'.join(hsp_timesch)
            reg = self.particular_city
            #city_url = self.domain+reg+'/doctors?page=2'
            currency = normalize(u'\u20b9')
            doc_avai = str(doc_info.get('callAvailable',''))
            doc_appointavai = str(doc_info.get('appointmentAvailable',''))
            doc_booking_type = ''
            if doc_avai=='True' and doc_appointavai=='True':
                doc_booking_type = 'Available On Call/Book Appointment'
            if doc_avai=='False' and doc_appointavai=='True':
                doc_booking_type = 'Appointment Available'
            if doc_avai=='True' and doc_appointavai=='False':
                doc_booking_type = 'Call Available'
            if doc_avai=='False' and doc_appointavai=='False':
                doc_booking_type = 'Not Available'
            doc_id = md5(normalize(username))
            if username and main_link:
                print main_link
                self.get_page('lybrate_doctorsapi_terminal', main_link, doc_id,meta_data={"name":name,"qualification":qua,
                                "specialization":spe,"years_of_experience":exp,"rating":rat,"vote_count":popu,"feedback_count":feed_co,
                                "doctor_image":image,"city":reg, "cli_lat":cli_lat,"cli_lon":cli_lon,
                                "clinic_address":clinic_address,"clic_location":cli_cityna, "cli_images":cli_images})
            #doc_id = md5(normalize(username))
            doctor_listing = DoctorInfo()
            doctor_listing['doctor_id'] = normalize(doc_id)
            doctor_listing['doctor_name'] = str(name)
            doctor_listing['doctor_profile_link'] = str(main_link)
            doctor_listing['qualification'] = str(qua)
            doctor_listing['years_of_experience'] = str(exp)
            doctor_listing['specialization'] = str(spe)
            doctor_listing['recently_visited_for'] = normalize(rec_vis)
            doctor_listing['rating'] = str(rat)
            doctor_listing['vote_count'] = str(popu)
            doctor_listing['feedback_count'] = str(feed_co)
            doctor_listing['location'] = normalize(reg)
            doctor_listing['address'] = str(clinic_address)
            doctor_listing['consultation_fee'] = str(cli_cha)
            doctor_listing['schedule_timeslot'] = normalize(hsp_timesch1)
            doctor_listing['doctor_image'] = str(image)
            doctor_listing['clinic_names'] = str(cli_name)
            doctor_listing['clinic_images'] = str(cli_images)
            doctor_listing['location_latitude'] = str(cli_lat)
            doctor_listing['location_longitude'] = str(cli_lon)
            doctor_listing['region'] = str(reg)
            doctor_listing['fee_currency'] = str(currency)
            doctor_listing['booking_type'] = str(doc_booking_type)
            doctor_listing['reference_url'] = str(city_url)
            if aux_infos:
                doctor_listing['aux_info'] = json.dumps(aux_infos)
            yield doctor_listing
