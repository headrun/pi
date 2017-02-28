from juicer.utils import *
from juicer.items import *
import dateparser

class Consumercourtbrowse(JuicerSpider):
    name = "consumercourt_browse"

    def __init__(self, *args, **kwargs):
        super(Consumercourtbrowse, self).__init__(*args, **kwargs)
        self.search_url = 'https://www.consumercourt.in/search.php?do=process/securitytoken=guest&do=process&query='
        self.domain = "https://www.consumercourt.in/"
        self.browse_list = 'apollo hospitals'#comma seperated values
        self.browse_list =  kwargs.get('search', self.browse_list)
        self.browse_list = self.browse_list.split(',')

    def start_requests(self):
        requests = []
        for br in self.browse_list:
            url = "{}{}".format(self.search_url,br)
            browse = textify(re.findall('&query=(.*)', url))
            request = Request(url, self.parse, meta={'browse':browse})
            requests.extend(request)
        return requests

    def name_clean(self, text):
        text = text.replace('\n','').replace('\t','').replace('\r','').strip()
        return text

    def parse(self, response):
        sel = Selector(response)
        browse = response.meta.get('browse','')
        complaint_list = get_nodes(sel,'//ol[@id="searchbits"]/li[@title]')
        for complist in complaint_list:
            main_link = extract_data(complist, './/h3[@class="searchtitle"]/a/@href')
            main_text = extract_data(complist, './/h3[@class="searchtitle"]/a/text()')
            main_replies = self.name_clean(extract_data(complist, './/ul[contains(@class,"threadstats")]/li/text()[contains(.,"Replie")]'))
            if main_replies: main_replies = textify(re.findall(':(.*)', main_replies))
            main_views = self.name_clean(extract_data(complist, './/ul[contains(@class,"threadstats")]/li/text()[contains(.,"Views")]'))
            if main_views: main_views = textify(re.findall(':(.*)', main_views))
            date1 = ''
            last_post = self.name_clean(extract_data(complist, './/dl[contains(@class,"threadlastpost")]/dd[span]//text()',' '))
            if last_post: last_post = textify(re.findall(': (.*)', last_post))
            if last_post:
                try: date1 =  str(dateparser.parse(last_post))
                except: pass
            last_post_author_url = extract_data(complist, './/dl[contains(@class,"threadlastpost")]/dd[contains(.,"by ")]/a[contains(@href,"member.php")]/@href')
            last_post_author_text = extract_data(complist, './/dl[contains(@class,"threadlastpost")]/dd[contains(.,"by ")]/a[contains(@href,"member.php")]/text()')
            if not last_post_author_url:
                last_post_author_text = extract_data(complist, './/dl[contains(@class,"threadlastpost")]/dd/text()[contains(.,"by ")]').replace('by ','').strip()
            forum_url = extract_data(complist, './/div[contains(@class,"threadpostedin")]/p/a/@href')
            forum_text = extract_data(complist, './/div[contains(@class,"threadpostedin")]/p/a/text()')

            aux_info = {}
            aux_info.update({"browse":browse})
            main_link_ = ''
            if 'http' not in main_link: main_link_ = "{}{}".format(self.domain, main_link.encode('utf8'))
            else: main_link_ = main_link
            if not main_link_: continue
            sk = md5(main_link_)
            if main_text: aux_info.update({"forum_title": main_text})
            if main_replies: aux_info.update({"forum_replies": main_replies})
            if main_views: aux_info.update({"forum_views": main_views})
            if date1: aux_info.update({"last_post_date": date1})
            if last_post_author_url:
                if 'http' not in last_post_author_url: last_post_author_url = "{}{}".format(self.domain, last_post_author_url)
                aux_info.update({"last_post_author_url": last_post_author_url})
            if last_post_author_text: aux_info.update({"last_post_author_name": last_post_author_text})
            if forum_url:
                if 'http' not in forum_url: forum_url = "{}{}".format(self.domain, forum_url)
                aux_info.update({"forum_url": forum_url})
            aux_info.update({"ref_url":response.url})
            if forum_text: aux_info.update({"forum_text": forum_text})
            self.get_page('consumercourt_review_terminal',main_link_, sk, aux_info)

        next_page = extract_data(sel,'//div[@id="below_searchresults"]//a[@rel="next"]/@href')
        if next_page:
            next_page_url = "{}{}".format(self.domain, next_page)
            if next_page_url: yield Request(next_page_url, callback=self.parse, meta={"browse":browse})

