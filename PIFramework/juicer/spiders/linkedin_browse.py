from juicer.utils import *
from juicer.items import *

class Linkedinbrowse(JuicerSpider):
    name = "linkedin_profile_browse"
    start_urls = ['https://www.linkedin.com/']
    handle_httpstatus_list = [404, 302, 303, 403, 500, 999, 503]
    def __init__(self, *args, **kwargs):
        super(Linkedinbrowse, self).__init__(*args, **kwargs)
        self.original_url_list = {"https://www.linkedin.com/pub/hanafiah-hasni/5b/590/a75":"https://www.linkedin.com/in/hanafiah-hasni-a755905b","https://www.linkedin.com/pub/aaron-chong/3a/7a2/12":"https://www.linkedin.com/in/aaron-chong-0127a23a","https://www.linkedin.com/pub/alex-arroza-cpa-cisa-crisc/3/451/75b":"https://www.linkedin.com/in/alex-arroza-75b4513","https://www.linkedin.com/pub/japrin-thomas/3a/952/79a":"https://www.linkedin.com/in/japrin-thomas-79a9523a","https://www.linkedin.com/pub/ilyani-zahari/16/293/276":"https://www.linkedin.com/in/ilyanizahari","https://www.linkedin.com/pub/anwar-pazikadin/44/889/941":"https://www.linkedin.com/in/anwar-pazikadin-94188944","https://www.linkedin.com/pub/karthikeyan-vasudevan/23/39/5a0":"https://www.linkedin.com/in/karthikeyan-vasudevan-5a003923","https://www.linkedin.com/in/aajay-girit-b858154b":"https://www.linkedin.com/in/dr-aajay-girit-b858154b"}
    def parse(self, response):
        listprofiles = []
        for profiless_url in open('linke_screennames'):
            if profiless_url != '\n':
                if '/pub' in profiless_url or "https://www.linkedin.com/in/aajay-girit-b858154b" in profiless_url:
                    profiless_url = self.original_url_list.get(profiless_url.strip('\n'),'')
                listprofiles.append(profiless_url.strip('\n'))

