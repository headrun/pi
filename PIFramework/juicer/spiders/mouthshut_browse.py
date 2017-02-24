from juicer.utils import *
from juicer.items import *
from scrapy.http import FormRequest

class Mouthshutbrowse(JuicerSpider):
    name = "mouthshut_browse"
    start_urls = []

    def __init__(self, *args, **kwargs):
        super(Mouthshutbrowse, self).__init__(*args, **kwargs)
        self.browse_list = 'Apollo hospitals'
        self.search_url = "https://www.mouthshut.com/search/prodsrch.aspx?data=%s&type=&p=0"
        self.browse_list =  kwargs.get('search', self.browse_list)
        self.browse_list = self.browse_list.split(',')
        self.domain = "https://www.mouthshut.com"
        for br in self.browse_list:
            self.start_urls.append(self.search_url%br)
        self.headers = {
        'Origin': 'https://www.mouthshut.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        }
        self.data = {
        'type': '',
        'gsearch': '0',
        'p': '0',
        'dat': '',
        'id': '0',
        'parent2': ''
        }
        self.post_url = 'https://www.mouthshut.com/search/prodsrch_loadmore_ajax.aspx'

    def parse(self, response):
        sel = Selector(response)
        if self.headers.get('Referer',''):
            del self.headers['Referer']
        if self.data.get('data',''):
            del self.data['data']
        if self.data.get('currentpage',''):
            del self.data['currentpage']
        browse = textify(re.findall('data=(.*?)&', response.url))
        reviews_urls = sel.xpath('//div[@class="box product"]//div[@class="rtitle"]/a/@href').extract()
        for review in reviews_urls:
            revi_url = "{}{}".format(self.domain, review)
            sk = md5(revi_url)
            aux_meta = {}
            aux_meta.update({"browse":browse})
            self.get_page('mouthshut_review_terminal', revi_url, sk, aux_meta)
        data_fromlk = textify(re.findall('data=(.*?)&type',response.url))
        next_link_numbers = extract_list_data(sel,'//ul[@class="pages"]/li/a/text()')
        for nextlk in next_link_numbers:
            self.headers.update({"Referer":response.url})
            self.data.update({'data':data_fromlk})
            self.data.update({'currentpage':nextlk})
            yield FormRequest(self.post_url, callback=self.parse_next, headers= self.headers, formdata=self.data, meta={"browse":browse})

    def parse_next(self, response):
        sel = Selector(response)
        browse =  response.meta['browse']
        reviews_urls =  sel.xpath('//div[@class="box product"]//div[@class="rtitle"]/a/@href').extract()
        for review in reviews_urls:
            revi_url = "{}{}".format(self.domain, review)
            sk = revi_url.split('-')[-1]
            meta_aux = {}
            meta_aux.update({"browse":browse})
            self.get_page('mouthshut_review_terminal', revi_url, sk, meta_aux)
