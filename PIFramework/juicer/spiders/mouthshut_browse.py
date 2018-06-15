from juicer.utils import *
from juicer.items import *
from scrapy.http import FormRequest

class Mouthshutbrowse(JuicerSpider):
    name = "mouthshut_browse"
    start_urls = []

    def __init__(self, *args, **kwargs):
        super(Mouthshutbrowse, self).__init__(*args, **kwargs)
	self.browse_list = ['Sathyam Cinemas, Royapettah','S2 Cinemas: Theyagaraja','S2 Perambur','Escape Cinemas, Royapettah','Vijaya Mall','PVR, Ampa Mall','PVR, Grand Mall, Velachery','PVR Grand','Udhayam Complex','Velco Cinemas','Woodlands Theatre','Nataraja','Ambika Theatre','VVM','Meera Theatre','Sangam Cinemas','Kamala Cinemas','Kasi','Albert','Murugan Cinemas','Vettri Theatres','Ganesh Cinemas','IDREAMS','Arvind Theatre','INOX Chandra Metro Mall, Virugambakkam','Nadhamuni','VVM','Srinivasa Theatre','Lakshmi Cinemas','Sri Bhuvaneshwari Theatre','Sri Kumari','Devicineplex','AVM Rajeswari','Udhayam Complex','Rakki Cinemas - Ambattur','M.R','Vidya Theatre','Vela Cinemas','Sri Brinda','Devi Karumari','Sri Lakshmi Theatre','Sri Shanmuga','Bharath Theatre','Lathaa Cinemas','Meera Theatre','Rakki Cinemas','Ega Cinemas','Prarthana Complex','Anna Theatre','Meenakshi Cinemas','Varadharaja Theatre','INOX Chennai Citi Centre','C3','Sri Venkateswara Talkies','Gokulam Cinemas','Lakshmi Bala','Maharani Theatre','Vetrrivel Theatre','Angamuthuu Theatre','Velco Cinemas','Gopalakrishna Theatre']
	self.search_url = "https://www.mouthshut.com/search/prodsrch_loadmore_ajax.aspx?currentpage=0&data=%s&gsearch=0&p=0&id=0&parent2=&type="
	self.fp1 = open('links1.txt', 'ab+')
        self.domain = "https://www.mouthshut.com"
        for br in self.browse_list:
            self.start_urls.append(self.search_url%br)

    def parse(self, response):
	sel = Selector(response)
	reviews_urls = extract_list_data(sel, '//div[@class="box product"]//div[@class="rtitle"]/a/@href')
	browse = textify(re.findall('data=(.*?)&', response.url))
	if  reviews_urls:
		self.fp1.write(response.url+'\n')
	for review in reviews_urls:
		revi_url = "{}{}".format(self.domain, review)
		sk = md5(revi_url)
		aux_meta = {}
		aux_meta.update({"browse":browse})
		self.get_page('mouthshut_review_terminal', revi_url, sk, aux_meta)
	data_fromlk = textify(re.findall('data=(.*?)&type',response.url))
	next_link_number = extract_data(sel,'//ul[@class="pages"]/li/span[@class="btn btn-link active"]/../following-sibling::li[1]/a/text()')
	if next_link_number:
		next_link = 'https://www.mouthshut.com/search/prodsrch_loadmore_ajax.aspx?currentpage=%s&data=%s&gsearch=0&p=0&id=0&parent2=&type='%(next_link_number, browse)
		yield Request(next_link, callback=self.parse)
	
