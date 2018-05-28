from juicer.utils import *
from juicer.items import *
import requests

class Askapollobrowse(JuicerSpider):
    name = 'askapollo_doctors_browse'
    start_urls = ['https://www.askapollo.com/physical-appointment/doctorsearch/chennai?page=1']

    def parse(self,response):
        sel = Selector(response)
        ref_url = response.url
        nodes = response.xpath('//div[@class="DrProfile col-md-6 col-xs-6 padding-right-none"]/div[@class="DoctorProfile"]')
        for node in nodes:
            doc_photo = extract_data(node, './/div[@class="DoctorImage"]/img/@src')
            doc_name = extract_data(node, './/div[@class="DrProfileContent"]/div[@class="DrProfileContentInner dr-info"]/div/a/h2/span[@itemprop="name"]/text()')
            doc_link = extract_data(node, './/div[@class="DrProfileContent"]/div[@class="DrProfileContentInner dr-info"]/div/a/@href')
            doc_spe = extract_data(node, './/div[@class="DrProfileContent"]/div[@class="DrProfileContentInner dr-info"]/span[@class="desg"]/a/h3/span[@itemprop="medicalSpecialty"]/text()')
            doc_exp = extract_data(node, './/div[@class="DrProfileContent"]/div[@class="DrProfileContentInner dr-info"]/span[@class="exp"]/span[contains(@id, "MainContent_rptSearchResult_lblExp")]/text()').split(':')[-1]
            doc_feed = extract_data(node, './/div[@class="DrProfileContent"]/div[@class="DrProfileContentInner dr-info"]/span[@class="exp"]/span[contains(@id, "MainContent_rptSearchResult_lblRecomandations")]/text()')
            dct_hsp1 = extract_data(node, './/div[@class="DrProfileContent"]/div[@class="DrProfileContentInner dr-info"]//h4/span[contains(@id, "MainContent_rptSearchResult_lblHospitalName")]/text()').replace('&', '').strip()
            dct_hsp2 = extract_data(node, './/div[@class="DrProfileContent"]/div[@class="DrProfileContentInner dr-info"]//h4/div/span[contains(@id, "MainContent_rptSearchResult_lblMoreHospitals")]/text()', '<>').replace(', ','<>')
            if dct_hsp1 and dct_hsp2:
                dct_hsp = dct_hsp1+'<>'+dct_hsp2
            else:
                dct_hsp = dct_hsp1

            address = extract_data(node, './/div[@class="DrProfileContent"]/div[@class="DrProfileContentInner dr-info"]/h5/span[@itemprop="addressLocality"]/text()')
            doc_booking_type = extract_data(node, './/div[@class="DrProfileContent"]//div[@class="DoctorProfileBtn"]/div/a/text()')
            doc_id = extract_data(node, './/div[@class="DrProfileContent"]//div[@class="DoctorProfileBtn"]/div/a/@onclick')
            doctor_id = ''.join(re.findall('(\d+)',doc_id))
            doc_pne = extract_data(node, './/div[@class="DrProfileContent"]//div[@class="DoctorProfileBtn"]/div/span/a/strong/text()')
            time_slot1 = node.xpath('.//div[@class="DrProfileContent"]/div[@class="DrProfileContentInner dr-info"]//span[@class="date"]/span[contains(@id, "MainContent_rptSearchResult_lblDayWithTimeDetails")]/text()').extract()
            time_slot2 = node.xpath('.//div[@class="DrProfileContent"]/div[@class="DrProfileContentInner dr-info"]//span[@class="date"]/div/span[contains(@id, "MainContent_rptSearchResult_lblMoreDays")]/text()').extract()
            time_slot1.extend(time_slot2)
            time_slots = time_slot1
            sch_slot = '<>'.join(set(time_slots)).replace('|',':-')
            if doctor_id and doc_name:
                self.get_page('askapollo_doctors_terminal', doc_link, doctor_id, meta_data={'doc_photo':normalize(doc_photo),"doc_name":normalize(doc_name),
                                "doc_exp":normalize(doc_exp),"doc_feed":normalize(doc_feed),"dct_hsp":normalize(dct_hsp),
                                "address":normalize(address),"doc_spe":normalize(doc_spe),"doc_pne":normalize(doc_pne),
                                "doc_booking_type":normalize(doc_booking_type),"sch_slot":normalize(sch_slot),"ref_url":normalize(ref_url)})
            for i in range(1, 90):
                next_page = 'https://www.askapollo.com/physical-appointment/doctorsearch/chennai?page='+str(i)
                yield Request(next_page, callback=self.parse)
