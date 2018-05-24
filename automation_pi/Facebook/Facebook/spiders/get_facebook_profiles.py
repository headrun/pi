import json
import collections
import re
from fb_constants import *
from fb_browse_queries import *
import sys
sys.path.append('/root/automation_pi/table_schemas')
from generic_functions import *

class Facebookbrowseprofiles(BaseSpider):
    name = "facebook_browse"
    start_urls = ['https://www.facebook.com/login']
    handle_httpstatus_list = [404, 302, 303, 403, 500]

    def __init__(self, *args, **kwargs):
        super(Facebookbrowseprofiles, self).__init__(*args, **kwargs)
        self.login = kwargs.get('login','yagnasree@headrun.com')
        self.modified_at_crawl  = kwargs.get('mpi', '')
        self.domain = "https://mbasic.facebook.com"
        self.con, self.cur = get_mysql_connection(DB_HOST, REQ_DB_NAME, '')
        self.profiles = []
        self.cur_date = str(datetime.datetime.now().date())
        self.dup_list = []


    def __del__(self):
        self.con.close()
        self.cur.close()


    def parse(self,response):
        dup_list = []
        files = ['html fb 1.txt','html fb 2.txt','html fb 4.txt','html fb 6.txt','html fb 8.txt','html fb 10.txt','html fb 3.txt','html fb 5.txt','html fb 9.txt','html fb 7.txt']
        for file_ in files :
            file_ = open(file_,'r')
            data = file_.read()
            if data : sel = Selector(text=data)
            img_urls = sel.xpath('//i//@style').extract()
            for i in img_urls : 
                post_id = "".join(re.findall('(\d+)_\d+_n.jpg',i))
                if post_id : 
                    link = "https://mbasic.facebook.com/photo.php?fbid="+str(post_id)
                    self.profiles.append(link)
                else : continue
        if self.profiles :
                login  = constants_dict[self.login]
                lsd = ''.join(sel.xpath('//input[@name="lsd"]/@value').extract())
                lgnrnd = ''.join(sel.xpath('//input[@name="lgnrnd"]/@value').extract())

                return [FormRequest.from_response(response, formname = 'login_form',\
                                formdata={'email': login[0],'pass':login[1],'lsd':lsd, 'lgnrnd':lgnrnd},callback=self.parse_next)]

    def parse_next(self,response):         
        sel = Selector(response)
        if self.profiles :
            for profile in self.profiles :
                yield Request(profile,callback=self.parse_data)
 
    def parse_data(self,response):
        sel = Selector(response)
        dup_list = []
        profile_link = "".join(sel.xpath('''//div[@id="MPhotoContent"]//div[@data-ft='{"tn":",g"}']/div/a[contains(@href,"refid")]/@href''').extract())
        if 'profile.php?' in profile_link : 
            url = profile_link.split('&')[0]
            pro_url = "https://www.facebook.com"+str(url)
            mbasic = "https://mbasic.facebook.com"+str(url)
        else :
            url = profile_link.split('?')[0]
            pro_url = "https://www.facebook.com"+str(url)
            mbasic = "https://mbasic.facebook.com"+str(url)
        qry = 'insert into facebook_crawl(sk,url,crawl_type,content_type,related_type,crawl_status,meta_data,created_at,modified_at) values (%s, %s, %s, %s, %s, %s ,%s, now(), now())  on duplicate key update modified_at = now()'
        meta_data = {'mbasic_url':str(mbasic)}
        values = (md5(pro_url),str(pro_url),'','facebook','',0,json.dumps(meta_data))
        self.dup_list.append(pro_url)
        self.cur.execute(qry,values)

        print([item for item, count in collections.Counter(self.dup_list).items() if count > 1])


