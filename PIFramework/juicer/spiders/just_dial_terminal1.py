from scrapy.http import  Request,FormRequest
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
import json
import re
from ast import *
import MySQLdb
from generic_functions import *
import md5
import requests
con = MySQLdb.connect(host='localhost', user= 'root',passwd='root',db="AGENTS1",charset="utf8",use_unicode=True)
cur = con.cursor()

class Justdial1(BaseSpider):
    name = 'justdail_agent1_crawl'
    handle_httpstatus_list = [401, 404, 302, 303, 403, 500, 100]
    url_dict = {'https://www.justdial.com/Chennai/Sathyam-Cinemas-Royapettah/044P7300885_BZDET':'Sathyam Cinemas, Royapettah','https://www.justdial.com/Chennai/S2-Theyagaraja-Cinemas-Thiruvanmiyur/044PXX44-XX44-120830123655-D3H9_BZDET':'S2 Cinemas: Theyagaraja','https://www.justdial.com/Chennai/S2-Perambur-Perambur/044PXX44-XX44-180518114303-P9C1_BZDET':'S2 Perambur','https://www.justdial.com/Chennai/Escape-Cinemas-express-Avenue-Mall-Royapettah/044PXX44-XX44-100824102143-C9K7_BZDET':'Escape Cinemas, Royapettah','https://www.justdial.com/Chennai/SPI-Cinemas-(Customer-Care)/044PXX44-XX44-170425114552-V8K2_BZDET?xid=Q2hlbm5haSBTUEkgQ2luZW1hcyBQcml2YXRlIEx0ZA==':'SPI Palazzo','https://www.justdial.com/Chennai/PVR-Cinemas-Ampa-Skywalk-Aminjikarai/044PXX44-XX44-100408152006-R2H3_BZDET?xid=Q2hlbm5haSBQVlIgQ2luZW1hcyBBbXBhIFNreXdhbGs=':'PVR, Ampa Mall','https://www.justdial.com/Chennai/PVR-Cinemas-Grand-Galada-Pallavaram/044PXX44-XX44-170621102720-T9Q7_BZDET':'PVR Grand Galada','https://www.justdial.com/Chennai/Velco-Cinema-Hall-Anakaputhur/044PXX44-XX44-100421151330-M2Z5_BZDET':'Velco Cinemas','https://www.justdial.com/Mumbai/Woodland-Cinema-Virar-West/022PXX22-XX22-110224171128-Q3C9_BZDET?xid=TXVtYmFpIFdvb2RsYW5kIFRoZWF0cmUgUHZ0IEx0ZA==':'Woodlands Theatre','https://www.justdial.com/Davangere/Nataraja-Theater-M-G-Road/9999P8192-8192-170922132049-C1L7_BZDET':'Nataraja','https://www.justdial.com/Sangli/Ambika-Theatre-Sangli-Ho/9999PX233-X233-140719122819-L2R9_BZDET':'Ambika Theatre','https://www.justdial.com/Chennai/VVM-Cinemas-Ponneri/044PXX44-XX44-121126175638-K1B5_BZDET':'VVM Cinemas','https://www.justdial.com/Chennai/Sangam-Cinemas-Kilpauk/044PXX44-XX44-110120173122-L4K7_BZDET':'Sangam Cinemas','https://www.justdial.com/villupuram/Kasi-Amman-Theatre-Near-Bus-Stand-Vikravandi/9999P4146-4146-170906064645-B6P3_BZDET?xid=VmlsbHVwdXJhbSBLYXNpIEFtbWFuIFRoZWF0cmU=':'Kasi Theatre','https://www.justdial.com/Chennai/Albert-Cinemas-Egmore/044P3007668_BZDET':'Albert Complex','https://www.justdial.com/Chennai/Murugan-Cinemas-Near-Railway-Station-O-V-Alagesan-Nagar-Ambattur/044P7018762_BZDET?xid=Q2hlbm5haSBNdXJ1Z2FuIENpbmVtYXM=':'Murugan Cinemas','https://www.justdial.com/Chennai/Ganesh-Cinemas-Anakaputhur/044PXX44-XX44-160220132629-E5Z3_BZDET':'Ganesh Cinemas','https://www.justdial.com/Chennai/Arvind-Cinema-Hall-Karapakkam/044PXX44-XX44-101006100436-S9T4_BZDET?xid=Q2hlbm5haSBBcnZpbmQgU2hyaXJhbQ==':'Arvind Theatre','https://www.justdial.com/Chennai/VVM-Cinemas-Ponneri/044PXX44-XX44-121126175638-K1B5_BZDET':'VVM Cinemas','https://www.justdial.com/Chennai/Lakshmi-Bala-Movie-Park-Cinemas-Near-Maruthi-Cinema-Hall-Dr-Moorthy-Nagar-Padi/044PXX44-XX44-110802173411-W2I6_BZDET?xid=Q2hlbm5haSBMYWtzaG1pIEJhbGEgTW92aWUgUGFyayBDaW5lbWFz':'Lakshmi Cinemas','https://www.justdial.com/arani/Rajeswari-Cinema-Hall-Near-Bharat-Petroleum-Dr-Ambedkar-Nagar/9999P4173-4173-170503134424-X5K5_BZDET?xid=YXJhbmkgUmFqZXN3YXJpIENpbmVtYSBIYWxs':'AVM Rajeswari','https://www.justdial.com/Chennai/M-R-Cinema-Hall-Opposite-Tambaram-Railway-Station-Tambaram/044P3009900_BZDET?xid=Q2hlbm5haSBNIFIgQ2luZW1hIEhhbGw=':'M.R Theatre','https://www.justdial.com/Chennai/Vidya-Cinema-Hall-Tambaram/044P3009902_BZDET':'Vidya Theatre','https://www.justdial.com/Chennai/Vela-Cinemas-Thirunindravur/044P7018649_BZDET':'Vela Cinemas','https://www.justdial.com/Chennai/Devi-Karumari-Theatre-Vadapalani/044PXX44-XX44-170913143024-G6P2_BZDET':'Devi Karumari Theatre','https://www.justdial.com/Bangalore/Sri-Lakshmi-Theatre-Opposite-Vinayaka-Store-Ramamurthy-Nagar/080P5126643_BZDET?xid=QmFuZ2Fsb3JlIFNyaSBMYWtzaG1pIFRoZWF0cmU=':'Sri Lakshmi Theatre','https://www.justdial.com/Chennai/Sri-Shanmuga-Cinema-Hall-Near-Moolakadai-Junction-Flyover-Erukkancheri/044P9018882_BZDET?xid=Q2hlbm5haSBTcmkgU2hhbm11Z2EgQ2luZW1hIEhhbGw=':'Sri Shanmuga Theatre','https://www.justdial.com/Raichur/Bharath-Theatre-Deodurga/9999P8532-8532-141103104201-L2D3_BZDET':'Bharath Theatre','https://www.justdial.com/Chengalpattu/Lathaa-Cinemas-Chengalpattu-Ho/9999PXX44-XX44-111031152937-U8R6_BZDET':'Lathaa Cinemas','https://www.justdial.com/Chennai/Meera-Theatre/044PXX44-XX44-120613104604-J5H2_BZDET':'Meera Theatre','https://www.justdial.com/Chennai/Rakki-Cinemas-Ambattur/044P7300883_BZDET':'Rakki Cinemas','https://www.justdial.com/Chennai/Anna-Cinema-Hall-Mount-Road/044P3007671_BZDET':'Anna Theatre','https://www.justdial.com/Aligarh/Meenakshi-Cinema-Ramghat-Road/9999PX571-X571-140228182607-Y4X4_BZDET':'Meenakshi Cinemas','https://www.justdial.com/Chennai/Varadharaja-Cinema-Hall-Chitlapakkam/044P1232451856M7F5E9_BZDET':'Varadharaja Theatre','https://www.justdial.com/Chengalpattu/C3-Cinemas-Laurel-Mall-Mamandur/9999PXX44-XX44-140109182620-E2Q7_BZDET':'C3 Laurel','https://www.justdial.com/chittoor/Sri-Venkateswara-Cinema-Hall-Punganur/9999P8572-8572-140216170240-S6U8_BZDET':'Sri Venkateswara Talkies','https://www.justdial.com/Chennai/Lakshmi-Bala-Movie-Park-Cinemas-Padi/044PXX44-XX44-110802173411-W2I6_BZDET':'Lakshmi Bala','https://www.justdial.com/Kottayam/Maharani-Theatre-Palai/9999PX481-X481-091123170132-Z7F4DC_BZDET':'Maharani Theatre','https://www.justdial.com/Chennai/Vetrrivel-Cinemas-Nanganallur/044P7006375_BZDET?xid=Q2hlbm5haSBWZXRycml2ZWwgQ2luZW1hcw==':'Vetrrivel Theatre','https://www.justdial.com/Chennai/Velco-Cinema-Hall-Anakaputhur/044PXX44-XX44-100421151330-M2Z5_BZDET':'Velco Cinemas','https://www.justdial.com/Chennai/Sri-Gopalakrishna-Theatre-Opposite-Vinayagar-Temple-Karanodia/044PXX44-XX44-180508130459-S2C1_BZDET?xid=Q2hlbm5haSBTcmkgR29wYWxha3Jpc2huYSBUaGVhdHJl':'Gopalakrishna Theatre','https://www.justdial.com/Chennai/INOX-Cinemas-(chennai-Citi-Centre)-Near-CSI-Kalyani-Hospital-Mylapore/044P1230636486U7Z4F1_BZDET?xid=Q2hlbm5haSBJTk9YIENpbmVtYXM=':'INOX, Citi Center','https://www.justdial.com/Chennai/INOX-Cinemas-Chandra-Metro-Mall-Virugambakkam/044P3009916_BZDET':'INOX national, Virgumbakkam'}

    def get_cookies(self, headers):
        res_headers = json.dumps(str(headers))
        res_headers = json.loads(res_headers)
        my_dict = literal_eval(res_headers)
        cookies = {}
        for i in my_dict.get('Set-Cookie', []):
            key_ = i
            data = i.split(';')[0]
            if data:
                try : key, val = data.split('=', 1)
                except : continue
                cookies.update({key.strip():val.strip()})
	return cookies

    def start_requests(self):
    	for url, keyword in self.url_dict.iteritems():
		yield Request(url,self.parse, meta={'keyword':keyword})

    def parse(self, response):
        sel = Selector(response)
	url = response.url
	keyword = response.meta['keyword']
	city = response.url.split('/')[3]
	distance = ''
	program_sk = hashlib.md5(response.url.split('/')[4]+city).hexdigest()
	sk = hashlib.md5(normalize(url)).hexdigest()
        ref_url_city = response.url.split('/')[3]
        name = extract_data(sel, '//div[@class="tleorlp"]/h1/span[@class="item"]/span/text()')
	place = extract_list_data(sel, '//span[@class="lng_add"]//text()')
	if place:
	    place = place[0].replace('\t','').replace('\n','')
	else:
	    place = ''
        rat_value = extract_data(sel, '//span[@class="rating"]/span[@class="total-rate"]/span/text()')
        rat_votes = extract_data(sel, '//span[@class="rtngsval"]/span[@class="votes"]//text()').strip(' ')
        address = extract_data(sel, '//span[@class="comp-text"]/span[@id="fulladdress"]/span/span//text()')
        services = '<>'.join(extract_list_data(sel, '//ul[@class="alstdul"]/li/span[@class="sritxt"]/span/text()'))
        payment_mode = '<>'.join(extract_list_data(sel, '//ul[@class="alstdul"]/li/span[@class="lng_mdpay"]/text()'))
        images = '<>'.join(extract_list_data(sel, '//div[@id="gal_img"]/ul[@class="catyimgul"]/li/a[@class="e_prop "]/@data-original'))
        photo = extract_data(sel, '//div[@class="col-sm-12 padding0 col-xs-12"]/div[@class="detail-banner"]/img/@data-src')
        category = normalize("<>".join(extract_list_data(sel, '//span[@class="comp-text also-list showmore "]//a//text()')))
        tel = "<>".join(extract_list_data(sel, '//div//ul[@id="comp-contact"]//div[@class="telCntct cmawht"]/a[@class="tel"]/text()')).strip('<>')
	days = extract_list_data(sel, '//div[@class="mreinfwpr"]//ul[@class="alstdul dn"]/li/span[@class="mreinflispn1 lng_commn"]/text()')
	timings = extract_list_data(sel, '//div[@class="mreinfwpr"]//ul[@class="alstdul dn"]/li/span[contains(@class, "mreinflispn2")]//text()')
        open_hours = '<>'.join(map(lambda a,b: normalize(a)+':-'+normalize(b), days,timings))
	website_link = extract_data(sel, '//span[@class="mreinfp comp-text"]/a/@href')
        year = ''
        year = extract_data(sel, '//p[text()="Year Established"]/parent::div/ul/li/text()')
        buisness_info = normalize(extract_data(sel, '//div[@class="col-sm-12 businfo seoshow "]//text()'))
	book_appointment = '<>'.join(extract_list_data(sel, '//section[@id="alldtlbtn"]/a//text()')).replace('\n','').replace('\t','')
	number_of_ratings = extract_data(sel, '//ul[@class="tabsCustom"]/li[contains(text(),"All Ratings")]/text()').replace('All Ratings','').replace('\n','').replace('\t','').replace('(','').replace(')','')
        patt_match = re.findall('\d{4}',year)
        if patt_match : year = "".join(year)
	aux_info = {'keyword':keyword}
	meta_query = 'insert into justdail_meta(sk, name, city, ref_url_city, photos, image, address ,medicalspecialty, payment_mode, rating_val, rating_count, telephone, time, year, available_services, buisness_info, aux_info,reference_url, main_url, place, website_link, book_appointment, distance,number_of_ratings,program_sk,created_at, modified_at) values ( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),now()) on duplicate key update modified_at = now(),place=%s,website_link=%s,book_appointment=%s,distance=%s,time=%s,image=%s,number_of_ratings=%s,program_sk=%s'
	vals = (str(sk),normalize(name),normalize(city),str(ref_url_city),normalize(photo),normalize(images),normalize(address),normalize(category),normalize(payment_mode),str(rat_value),str(rat_votes),str(tel),str(open_hours),str(year),normalize(services),normalize(buisness_info),json.dumps(aux_info),normalize(response.url),normalize(response.url),normalize(place),normalize(website_link),normalize(book_appointment),normalize(distance),normalize(number_of_ratings),str(program_sk),normalize(place),normalize(website_link),normalize(book_appointment),normalize(distance),normalize(open_hours),normalize(images),normalize(number_of_ratings),str(program_sk))
        cur.execute(meta_query,vals)
        con.commit()
        cookies = self.get_cookies(response.headers)
	headers = {
    		'cookie': 'ppc=; _ctk=d09ebf5dd9b141ca762d7627bdbee48050a8d2b95ebc4cb2d112e02a434b421d; _ga=GA1.2.1180172423.1515076095; _gid=GA1.2.823631544.1530596680; vfdisp=%7B%22011PXX11.XX11.110927215823.V8A7%22%3A%222097152%22%7D; docidarray=%7B%22044P7300885%22%3A%222018-07-03%22%2C%22011PXX11.XX11.110927215823.V8A7%22%3A%222018-07-03%22%2C%22011PXX11.XX11.150527081421.Z7V4%22%3A%222018-07-03%22%2C%22044PXX44.XX44.170621102720.T9Q7%22%3A%222018-07-03%22%2C%22011PXX11.XX11.171228103956.C3L3%22%3A%222018-07-03%22%7D; detailmodule=044P7300885; TKY=d216e1cffb992f9ab255cbeca7531e53270240b677a979f20c3e675b1a4ba990; main_city=Chennai; PHPSESSID=hl7qe1a1mmuoebd74qovvnb3u0; attn_user=logout; inweb_city=Chennai; ak_bmsc=E5A40B6684EECA6F01C521B6BC10C16417CDDF04E5590000DC483C5BA32BC144~plpfTV4VBKLjdcWko1wudy3bKQUhn/8RbKc/whdeQoUaYLHa8NHDdXKLoXDI7fW9DAWkc4Wsove6TvYNURwN/H1JOqkwPPOIZ3ygQzMQQF9bYsREVUgBq3tSpZPIIF9ixUaWHS1MrY+Tcx6U7YH6zyJKTuqoUjlYOjk0kwiDSJtc5wL20hEhyFp+uOCvCTDukTdiIKmCWROgMJ7UhuD2d0NkfzJhoounjHNMlkBFROuP3MWq+07lr3w2roQfvLydU13HpD0QXn8bVxK70pqNiwkg==',
    		'origin': 'https://www.justdial.com',
    		'accept-encoding': 'gzip, deflate, br',
    		'x-frsc-token': 'd216e1cffb992f9ab255cbeca7531e53270240b677a979f20c3e675b1a4ba990',
    		'accept-language': 'en-US,en;q=0.9',
    		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    		'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    		'accept': '*/*',
    		'referer': response.url,
    		'authority': 'www.justdial.com',
    		'x-requested-with': 'XMLHttpRequest',
		}

        cid = ''.join(set(sel.xpath('//input[@name="docid"][@id="mpdocid"]/@value').extract()))
	main_page = 'https://www.justdial.com/functions/subrat.php'
	body_txt = extract_list_data(sel, '//span[@class="jpag"]//a[@href="#rvw"]/@onclick')
	if body_txt:
		body_txt = body_txt[0] 
	else:
		body_txt = ''
	if body_txt:
		cs_txt,rev,ct,emo,np_txt,gdoc_txt,txt,tc = re.findall('\((.*)\)', ''.join(body_txt))[0].split("',")
		ct_txt = city
		data = [
			('dc', cid),
			('cs', cs_txt.replace("'", '')),
			('rev', ''),
			('ct', city),
			('emo', ''),
			('np', '1'),
			('gdoc', gdoc_txt.replace("'", '')),
			('txt', ''),
			('tc', ''),
			]
		resp = requests.post(main_page, headers=headers, data=data)	
		sel1 = Selector(text=(resp.text).replace('\t', '').replace('\n', ''))
		last_page = extract_list_data(sel1, '//a[@href="#rvw"][not(contains(text(), "Next"))]/text()')
		if not last_page:
			last_page = extract_list_data(sel1, '//span[@class="jpag"]//a[@href="#rvw"]/text()')[-1]
		else:
			last_page = last_page[-1]
		review_nodes = get_nodes(sel1, '//div[@class="col-sm-12 allratingM"]/div[@class="allratR"]')
		for node in review_nodes:
		    rev_name = extract_data(node, './span[@class="fr"]/span[@class="rName lng_commn"]//text()')
		    rev_rat = extract_data(node, './span[@class="fr"]/span[@class="star_m"]/@aria-label').replace('Rated','').strip()
		    rev_on = extract_data(node, './span[@class="dtyr ratx pull-right"]/text()')
		    rev_text = extract_data(node, './/div/p[@class="thr lng_commn"]/text()')
		    rev_query = 'insert into Reviews(sk, program_sk, reviewed_by, reviewed_on, review,rating_value,created_at, modified_at) values ( %s,%s, %s, %s, %s, %s, now(), now()) on duplicate key update modified_at = now(),rating_value=%s'
		    rev_sk = hashlib.md5(rev_name+'1'+sk+rev_on+rev_text+rev_rat).hexdigest()
		    vals1 = (rev_sk,sk,rev_name,rev_on,rev_text,rev_rat,rev_rat)
		    cur.execute(rev_query,vals1)
		for page_no in range(2, int(last_page)+1):
		    cs_txt,rev,ct,emo,np_txt,gdoc_txt,txt,tc = re.findall('\((.*)\)', ''.join(body_txt))[0].split("',")
		    data1 = [
			('dc', cid),
			('cs', cs_txt.replace("'", '')),
			('rev', ''),
			('ct', city),
			('emo', ''),
			('np', str(page_no)),
			('gdoc', gdoc_txt.replace("'", '')),
			('txt', ''),
			('tc', ''),
			]
		    resp1 = requests.post(main_page, headers=headers, data=data1)
		    sel2 = Selector(text=(resp1.text).replace('\t', '').replace('\n', ''))
		    self.get_data(sel2, sk, str(page_no))
	else:
	    review_nodes = get_nodes(sel, '//div[@class="col-sm-12 allratingM"]/div[@class="allratR"]')
            for node in review_nodes:
                rev_name = extract_data(node, './span[@class="fr"]/span[@class="rName lng_commn"]//text()')
                rev_rat = extract_data(node, './span[@class="fr"]/span[@class="star_m"]/@aria-label').replace('Rated','').strip()
                rev_on = extract_data(node, './span[@class="dtyr ratx pull-right"]/text()')
                rev_text = extract_data(node, './/div/p[@class="thr lng_commn"]/text()')
                rev_query = 'insert into Reviews(sk, program_sk, reviewed_by, reviewed_on, review,rating_value,created_at, modified_at) values ( %s,%s, %s, %s, %s, %s, now(), now()) on duplicate key update modified_at = now(),rating_value=%s'
                rev_sk = hashlib.md5(rev_name+'1'+sk+rev_on+rev_text+rev_rat).hexdigest()
                vals1 = (rev_sk,sk,rev_name,rev_on,rev_text,rev_rat,rev_rat)
                cur.execute(rev_query,vals1)

    def get_data(self, sel2, sk, num):
	review_nodes = get_nodes(sel2, '//div[@class="col-sm-12 allratingM"]/div[@class="allratR"]')
        for node in review_nodes:
            rev_name = extract_data(node, './span[@class="fr"]/span[@class="rName lng_commn"]//text()')
            rev_rat = extract_data(node, './span[@class="fr"]/span[@class="star_m"]/@aria-label').replace('Rated','').strip()
            rev_on = extract_data(node, './span[@class="dtyr ratx pull-right"]/text()')
            rev_text = extract_data(node, './/div/p[@class="thr lng_commn"]/text()')
            rev_query = 'insert into Reviews(sk, program_sk, reviewed_by, reviewed_on, review,rating_value,created_at, modified_at) values ( %s,%s, %s, %s, %s, %s, now(), now()) on duplicate key update modified_at = now(),rating_value=%s'
            rev_sk = hashlib.md5(rev_name+num+sk+rev_on+rev_text+rev_rat).hexdigest()
            vals1 = (rev_sk,sk,rev_name,rev_on,rev_text,rev_rat,rev_rat)
            cur.execute(rev_query,vals1)

