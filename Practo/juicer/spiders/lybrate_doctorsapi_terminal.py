from juicer.utils import *
from juicer.items import *
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class LybratedoctorsTerminal(JuicerSpider):
    name = 'lybrate_doctorsapi_terminal'
    #start_urls = ['https://www.lybrate.com/hyderabad/doctor/dr-shaivalini-obstetrician']

    def __init__(self, *args, **kwargs):
        super(LybratedoctorsTerminal, self).__init__(*args, **kwargs)
        self.domain = "https://www.lybrate.com/"
        self.pattern2 = re.compile('(.*):-(.*)')
        self.week_list = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']

    def parse(self, response):
        sel = Selector(response)
        aux_infos = {}
        print response.url
        #doc_id = 'dr-shaivalini-obstetrician'
        #feedback_count = '14'
        doc_id = response.meta['sk']
        rating = response.meta['data']['rating']
        specialization = response.meta['data']['specialization']
        city = response.meta['data']['city']
        if city:
            aux_infos.update({"city":city})
        feedback_count = response.meta['data']['feedback_count']
        name = response.meta['data']['name']
        vote_count = response.meta['data']['vote_count']
        clinic_address = response.meta['data']['clinic_address']
        qualification = response.meta['data']['qualification']
        doctor_image = response.meta['data']['doctor_image']
        years_of_experience = response.meta['data']['years_of_experience']
        cli_images = response.meta['data']['cli_images']
        sub_spe = '<>'.join(set(sel.xpath('//div[contains(@id, "speciality")]//a//text()').extract()))
        education = '<>'.join(set(sel.xpath('//div[contains(@id, "education")]//text()').extract())).replace('\t','').replace('\n','')
        past_exp = '<>'.join(set(sel.xpath('//div[contains(@id, "experience")]//text()').extract())).replace('\t','').replace('\n','')
        desc = normalize('.'.join(response.xpath('//div[@itemprop="description"]//text()').extract()))
        language = '<>'.join(set(sel.xpath('//div[contains(@id, "language")]//text()').extract())).replace('\t','').replace('\n','')
        prof_mem = '<>'.join(set(sel.xpath('//div[contains(@id, "professional")]//text()').extract())).replace('\t','').replace('\n','')
        award = '<>'.join(set(sel.xpath('//div[contains(@id, "award")]//text()').extract())).replace('\t','').replace('\n','')
        services = extract_data(sel, '//div[@itemprop="makesOffer"]/div//h3[@itemprop="name"]/text()','<>')
        if doc_id:
            doctor_meta  = DoctorMeta()
            doctor_meta['sk'] = normalize(doc_id)
            doctor_meta['doctor_id'] = normalize(doc_id)
            doctor_meta['doctor_name'] = normalize(name)
            doctor_meta['doctor_profile_link'] = normalize(response.url)
            doctor_meta['qualification'] = normalize(qualification)
            doctor_meta['specialization'] = normalize(specialization)
            doctor_meta['years_of_experience'] = str(years_of_experience)
            doctor_meta['languages_spoken'] = normalize(language)
            doctor_meta['rating'] = str(rating)
            doctor_meta['vote_count'] =  normalize(str(vote_count))
            doctor_meta['summary'] = normalize(desc)
            doctor_meta['services'] =  normalize(services)
            doctor_meta['specializations'] = normalize(sub_spe)
            doctor_meta['education'] = normalize(education)
            doctor_meta['memeberships'] = normalize(prof_mem)
            doctor_meta['experience'] = normalize(past_exp)
            doctor_meta['registrations'] = ''
            doctor_meta['feedback_count'] = normalize(str(feedback_count))
            doctor_meta['doctor_image'] = normalize(doctor_image)
            doctor_meta['reference_url'] = normalize(response.url)
            if aux_infos:
                doctor_meta['aux_info'] = json.dumps(aux_infos)
            yield doctor_meta
            print "1"
        main_nodes = response.xpath('//div[@itemprop="memberOf"]')
        for main_node in main_nodes:
            hsp_timesch = []
            hsp_timesch1 = ''
            link = ''.join(main_node.xpath('.//div[@class="grid__col-15 lybPad-top"]/h2[@itemprop="name"]/a/@href').extract())
            hsp_name = ''.join(main_node.xpath('.//div[@class="grid__col-15 lybPad-top"]/h2[@itemprop="name"]/a/text()').extract()).replace('\n', '').replace('\t', '').strip(  )
            st_add = ''.join(main_node.xpath('.//div[@class="grid__col-15 lybPad-top"]//span[@class="lybGrey"]/span[@itemprop="streetAddress"]/text()').extract())
            cli_re = ''.join(main_node.xpath('.//div[@class="grid__col-15 lybPad-top"]//span[@class="lybGrey"]/span[@itemprop="addressRegion"]/text()').extract())
            cli_locality = ''.join(main_node.xpath('.//div[@class="grid__col-15 lybPad-top"]//span[@class="lybGrey"]/meta[@itemprop="addressLocality"]/@content').extract())
            cli_cou = ''.join(main_node.xpath('.//div[@class="grid__col-15 lybPad-top"]//span[@class="lybGrey"]/meta[@itemprop="addressCountry"]/@content').extract())
            cli_pos = ''.join(main_node.xpath('.//div[@class="grid__col-15 lybPad-top"]//span[@class="lybGrey"]/meta[@itemprop="postalCode"]/@content').extract())
            clic_location = st_add+' '+cli_re+' '+cli_locality+' '+cli_cou+' '+cli_pos
            images_cli = main_node.xpath('.//div[@class="grid__col-15 lybPad-top"]//div[@class="ly-doctor__clinic-photos grid--direction-row lybMar-top--half"]/span/img/@src').extract()
            if images_cli:
                images_cli1 = '<>'.join(set(images_cli))
            else: images_cli1 = ''
            lat = ''.join(main_node.xpath('.//div[@class="grid__col-15 lybPad-top"]/span[@itemprop="geo"]/meta[@itemprop="latitude"]/@content').extract())
            lon = ''.join(main_node.xpath('.//div[@class="grid__col-15 lybPad-top"]/span[@itemprop="geo"]/meta[@itemprop="longitude"]/@content').extract())
            fee = ''.join(main_node.xpath('.//div[@class="padding left top grid--direction-row grid__col-7 grid__col-xs-20"]//div[@class="grid--direction-row grid--wrap grid__col-20 clinic-list hack"]//span[@itemprop="priceRange"]/text()').extract())
            rat = ''.join(main_node.xpath('./div[@class="padding left top grid--direction-row grid__col-7 grid__col-xs-20"]//span[@class="grid--direction-row grid__col-20 grid--align-center"]/span[@itemprop="ratingValue"]/text()').extract())
            day = main_node.xpath('.//div[@class="padding left top grid--direction-row grid__col-7 grid__col-xs-20"]//div[@class="grid--direction-row grid--wrap grid__col-20 clinic-list hack"]//time[@itemprop="openingHours"]//div[contains(@class, "clinic-time")]/ly-svg-icon[contains(@class, "ly-svg--md light")]//following-sibling::text()').extract()
            timee = main_node.xpath('.//div[@class="padding left top grid--direction-row grid__col-7 grid__col-xs-20"]//div[@class="grid--direction-row grid--wrap grid__col-20 clinic-list hack"]//time[@itemprop="openingHours"]//div[contains(@class, "lybGrey clinic-time")]//text()').extract()
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
            final_set = {'MON':[], 'TUE':[], 'WED':[], 'THU':[], 'FRI':[], 'SAT':[], 'SUN':[]}
            if hsp_timesch1:
                    hso_timesc_list = hsp_timesch1.split('<>')
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
                                                scslots1 = [weekf_.strip()]
                                                csl2 = self.week_list[:b1+1]
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
            doc_hsp_sk = md5(normalize(link)+normalize(hsp_name)+normalize(doc_id))
            doctor_hospital = DoctorHospital()
            doctor_hospital['sk'] = normalize(doc_hsp_sk)
            doctor_hospital['doctor_id'] = normalize(doc_id)
            doctor_hospital['hospital_location'] = normalize(clic_location)
            doctor_hospital['hospital_link'] = normalize(link)
            doctor_hospital['hospital_name'] =  normalize(hsp_name)
            doctor_hospital['hospital_rating'] = normalize(str(rat))
            doctor_hospital['hospital_address'] = normalize(cli_re)
            doctor_hospital['hospital_monday_timing'] = normalize('<>'.join(final_dict.get('MON',[])))
            doctor_hospital['hospital_tuesday_timing'] = normalize('<>'.join(final_dict.get('TUE',[])))
            doctor_hospital['hospital_wednesday_timing'] =  normalize('<>'.join(final_dict.get('WED',[])))
            doctor_hospital['hospital_thursday_timing'] = normalize('<>'.join(final_dict.get('THU',[])))
            doctor_hospital['hospital_friday_timing'] = normalize('<>'.join(final_dict.get('FRI',[])))
            doctor_hospital['hospital_saturday_timing'] = normalize('<>'.join(final_dict.get('SAT',[])))
            doctor_hospital['hospital_sunday_timing'] = normalize('<>'.join(final_dict.get('SUN',[])))
            doctor_hospital['hospital_consultation_fee'] = normalize(fee)
            doctor_hospital['hospital_photos'] = normalize(images_cli1)
            doctor_hospital['hospital_latitude'] = normalize(lat)
            doctor_hospital['hospital_longitude'] = normalize(lon)
            doctor_hospital['reference_url'] = normalize(response.url)
            yield doctor_hospital
            print '2'
            self.got_page(doc_id, 1)

        nodes = response.xpath('//div[@itemprop="review"]')
        for node in nodes:
            rev_name = normalize(extract_data(node, './/span[@itemprop="author"]/h4/text()'))
            rev_date = normalize(extract_data(node, './/div[@class="lybText--tiny lybText--light lybMar-btm--half"]/text()'))
            review_desc = normalize(extract_data(node, './/p[@itemprop="reviewBody"]//text()'))
            review_sk = md5(rev_name+rev_date+review_desc)
            aux_info1 = {}
            if doc_id and review_sk:
                review_item = DoctorFeedback()
                review_item['sk'] = normalize(review_sk)
                review_item['feedback_count'] = normalize(str(feedback_count))
                review_item['doctor_id'] = normalize(doc_id)
                review_item['feedback_name'] = normalize(rev_name)
                review_item['feedback_publish_date'] = normalize(rev_date)
                review_item['feeback_text'] = normalize(review_desc)
                review_item['reference_url']= normalize(response.url)
                if aux_info1:
                    review_item['aux_info'] = json.dumps(aux_info1)
                yield review_item
                print '3'









