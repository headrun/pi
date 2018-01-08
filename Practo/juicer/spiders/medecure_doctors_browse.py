from juicer.utils import *
from juicer.items import DoctorInfo
from lybrate_doctors_xpaths import *
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class MedecureDoctors(JuicerSpider):
    name = 'medecure_doctors_browse'
    handle_http_status_list = ['500', '302', '403']
    def __init__(self, *args, **kwargs):
        super(MedecureDoctors, self).__init__(*args, **kwargs)
        self.domain = "https://www.lybrate.com/"
        self.doctors = '/doctors'
        self.pattern2 = re.compile('(.*) (.*)')
        self.week_list = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        self.pagenumber =  kwargs.get('page', '')
        self.pagenumber = '%s%s'%('?page=',self.pagenumber)
        self.pageend = kwargs.get('end', '')
        self.particular_city = kwargs.get('city','')
        if self.particular_city:
            self.start_urls = ['http://www.medecure.com/doctor-in-%s.html'%self.particular_city]
        else:
            self.start_urls = ['https://www.medecure.com/india']

    def parse(self,response):
        reg = self.particular_city
        sel= Selector(response)
        nodes=response.xpath('//div[@class="left listing_maindiv"]')
        for node in nodes:
            doctor_name = extract_data(node, './div[@class="listing_new_info_div left"]//a[@class="left dark_blue title16 open_sans margin-right tips"]/text()')
            doctor_link = extract_data(node, './div[@class="listing_new_info_div left"]//a[@class="left dark_blue title16 open_sans margin-right tips"]/@href')
            doctor_id = doctor_link.split('/')[-2]
            edu_qu = extract_data(node, './/div[@class="listing_new_info_div left"]//div[@class="left small-font edu_info margin-top clear"]/text()')
            speciality = extract_data(node,'.//div[@class="info_left_new margin-bottom padding-top5 clear"]/div[contains(text(),"Speciality")]//following-sibling::div[@class="left info_details"]/text()')
            condition_treated = '<>'.join(sel.xpath('//div[@class="info_left_new margin-bottom padding-top5 clear"]//div[@class="info_title_new middle_title left"][contains(text(),"Conditions Treated")]//following-sibling::div[@class="left info_details"]/a/text()').extract())
            clinic_name = extract_data(node, './/div[@class="info_left_new margin-bottom padding-top clear"]/div[contains(text(),"Clinic Name")]/following-sibling::div[@class="left info_details"]/a/text()')
            clinic_link = extract_data(node, './/div[@class="info_left_new margin-bottom padding-top clear"]/div[contains(text(),"Clinic Name")]/following-sibling::div[@class="left info_details"]/a/@href')
            clinic_id = clinic_link.split('/')[-3]
            address = extract_data(node, './/div[@class="info_left_new margin-bottom padding-top5 clear"]/div[contains(text(),"Address")]/following-sibling::div[@class="left info_details"]/text()')
            region = extract_data(node, './/div[@class="listing_info_new_right right"]/div[@class="left margin-top5 clear"]/text()')
            fee = extract_list_data(node, './/div[@class="listing_info_new_right right"]/div[@class="clear margin-top"]//text()')[2]
            list1=[]
            sche_ti = ''
            days = extract_list_data(node, './/div[@class="clear margin-top"]//div[@style="padding-left:5px;width:155px;"]/b/text()')
            timings = extract_list_data(node, './/div[@class="clear margin-top"]//div[@style="padding-left:5px;width:155px;"]//b/following-sibling::text()')
            for day,timing in zip(days,timings):
                list1.append(''.join(day).replace('To','-')+':-'+''.join(timing).replace('To','-'))
            sche_ti='<>'.join(list1)
            doctor_sk = md5(normalize(doctor_name)+normalize(doctor_link)+normalize(fee)+normalize(clinic_name))
            doc_va = 'a_appointments_'+doctor_id+'_'+clinic_id
            doc_booking_type = extract_data(node, './..//div[@class="band_div right"]/ul/li/a[contains(@id,"%s")]/text()'%doc_va)
            doctor_img = extract_data(node,'./div[@class="left listing_photo_left"]/img/@src')
            doctor_rev = extract_data(node,'./div[@class="left small-font link_blue padding-top"]/a/text()')
            ref_url= response.url
            rat = len(sel.xpath('//div[@class="ratings"]/div[contains(@class,"ratings_stars_disable ratings_vote disable")]'))
            self.get_page('medecure_doctors_terminal', doctor_link, doctor_sk, meta_data={"doctor_name":normalize(doctor_name),"doctor_id":normalize(doctor_id),"edu_qu":normalize(edu_qu),"speciality":normalize(speciality),"condition_treated":normalize(condition_treated),"clinic_name":normalize(clinic_name),"clinic_link":normalize(clinic_link),"address":normalize(address),"region":normalize(region),"fee":normalize(''.join(fee)),"schedule_slot":normalize(sche_ti),"doc_booking_type":normalize(doc_booking_type),"doctor_img":normalize(doctor_img),"doctor_rev":normalize(doctor_rev),"city":normalize(reg),"ref_url":normalize(ref_url),"rating":normalize(rat)})
        page_nav=sel.xpath('//div[@class="pagination-maindiv"]//a/@href').extract()[-1]
        if page_nav:
            yield Request(page_nav,callback=self.parse)
