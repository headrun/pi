import MySQLdb
from juicer.utils import *
from juicer.items import *
handle_httpstatus_list = [404, 302, 303]
class Linkedin30crawl(JuicerSpider):
        name = 'linkedin_flag_browse'

        def __init__(self, *args, **kwargs):
                super(Linkedin30crawl, self).__init__(*args, **kwargs)
                self.con = MySQLdb.connect(db   = 'FACEBOOK', \
                host = 'localhost', charset="utf8", use_unicode=True, \
                user = 'root', passwd = 'hdrn59!')
                self.cur = self.con.cursor()
                self.field =  kwargs.get('field', 'clean_url')
                get_query_param = ""
                if self.field == 'url':
                    get_query_param = "select sk, url, meta_data from linkedin_crawl30 where crawl_status=0 limit 500"
                else: get_query_param = "select sk, url, meta_data from linkedin_crawl30 where flag = 'True' and crawl_type = '' limit 10000"
                #get_query_param = "select sk, url, meta_data from linkedin_crawl30 where sk = '11930ca31e4678bdd4e3710c3b455fc9'"
                self.cur.execute(get_query_param)
                self.profiles_list = [i for i in self.cur.fetchall()]

        def start_requests(self):
                requests = []
                for i in self.profiles_list:
                        url = i[1]
                        query1 = ""
                        if self.field == 'url':
                            query1 = "update linkedin_crawl30 set crawl_status=1 where sk ='%s'"%(i[0])
                        else: query1 = "update linkedin_crawl30 set crawl_type ='crawled' where sk ='%s'"%(i[0])
                        self.cur.execute(query1)
                        request = Request(url, self.parse, meta={'sk':i[0], 'meta_data':i[2]}, dont_filter=True)
                        requests.extend(request)
                return requests

        def parse(self, response):
                sk = response.meta['sk']
                sel = Selector(response)
                if self.field == 'url':
                    valid = 'False'
                    if response.status== 200 and not 'your request could not be completed' in response.body.lower():
                        valid = 'True'
                    query = "update linkedin_crawl30 set flag= '%s' where sk ='%s'"%(valid,sk)
                    self.cur.execute(query)
                else:
                    first_name = extract_data(sel,'//div[@class="member-info"]/h1//span[@class="given-name"]/text()')
                    last_name = extract_data(sel, '//div[@class="member-info"]/h1//span[@class="family-name"]/text()')
                    name = ("%s%s%s"%(first_name,' ', last_name)).strip()
                    locality = extract_data(sel, '//div[@class="member-info"]/p//span[@class="locality"]/text()')
                    image = extract_data(sel, '//div[@class="member-photo"]/img/@src')
                    if 'icon_no_photo' in image: image = ''
                    mark = extract_data(sel, '//div[@class="member-photo"]/span[@class="mark"]/@class')
                    member_url = extract_data(sel, '//div[@class="member-info"]/h1/a[@class="url"]/@href')
                    linke_m = Linkedin()
                    if first_name:
                        linke_m['sk'] = normalize(sk)
                        linke_m['name'] = normalize(name)
                        linke_m['first_name'] = normalize(first_name)
                        linke_m['last_name'] = normalize(last_name)
                        linke_m['locality'] = normalize(locality)
                        linke_m['image'] = normalize(image)
                        linke_m['mark'] = normalize(mark)
                        linke_m['member_url'] = normalize(member_url)
                        linke_m['url'] = normalize(response.url)
                        yield linke_m
                        position_nodes = get_nodes(sel, '//div[@class="member-info"]/p//span[@class="title"]')
                        if position_nodes:
                            for posn in position_nodes:
                                title = extract_data(posn, './b[not(@*)]/text()')
                                organization = extract_data(posn, './/b[@class="org"]/text()')
                                if title:
                                    linke_p = Linkedinpostions()
                                    linke_p['sk'] = md5("%s%s%s"%(sk, title, organization))
                                    linke_p['profile_sk'] = normalize(sk)
                                    linke_p['title'] = normalize(title)
                                    linke_p['organization'] = normalize(organization)
                                    yield linke_p
                        viewer_nodes = get_nodes(sel, '//ul[@class="has-names"]/li[@class="vcard"]')
                        if viewer_nodes:
                            for node in viewer_nodes:
                                ndoe_url = extract_data(node,'./span[a]/a/@href')
                                node_txt = extract_data(node, './span[a]/a/text()')
                                node_headline = extract_data(node,'./span[@class="headline"]//text()').strip().strip(',').strip()
                                if node_txt:
                                    linke_v = Linkedinviewers()
                                    linke_v['sk'] = md5("%s%s%s"%(sk, ndoe_url, node_headline))
                                    linke_v['profile_sk'] = normalize(sk)
                                    linke_v['viewer_url'] = normalize(ndoe_url)
                                    linke_v['viewer_name'] = normalize(node_txt)
                                    linke_v['viewer_headline'] = normalize(node_headline)
                                    yield linke_v



