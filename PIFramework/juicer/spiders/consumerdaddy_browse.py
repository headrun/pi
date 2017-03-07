from juicer.utils import *
from juicer.items import *
from scrapy.http import FormRequest

class Consumerdaddyb(JuicerSpider):
    name = "consumerdaddy_browse"
    start_urls = []
    def __init__(self, *args, **kwargs):
        super(Consumerdaddyb, self).__init__(*args, **kwargs)
        self.search_url = 'http://www.consumerdaddy.com/search-result-%s-t2-l1g26g133.htm'
        self.domain = "http://www.consumerdaddy.com/"
        #self.browse_list = 'Apollo hospitals'#comma seperated values
        self.browse_list = 'Apollo hospitals'
        self.browse_list =  kwargs.get('search', self.browse_list)
        self.browse_list = self.browse_list.split(',')
        for br in self.browse_list:
            br = br.replace(' ','-')
            self.start_urls.append(self.search_url%br)

    def parse(self, response):
        sel = Selector(response)
        if not response.meta.get('browse',''):
            browse = textify(re.findall('result-(.*)-t2-', response.url))
        else:
            browse = response.meta['browse']
        aux_info = {}
        aux_info.update({"browse":browse})
        nodes = get_nodes(sel, '//table[contains(@id,"MasterPanel_gvList")]/tr[td]/td/table/tr')
        for nd in nodes:
            image = extract_data(nd, './/input[@type="image"]/@src')
            if 'http' not in image: image = "{}{}".format(self.domain, image)
            review_ur = extract_data(nd, './/a[contains(@id, "lnkProductName")]/@href')
            location = extract_data(nd, './/span[contains(@id, "State")]/text()')
            score = extract_data(nd, './/span[contains(@id, "Score")]//text()')
            score_interpr = extract_data(nd, './/span[contains(@id, "Interpretation")]//text()')
            if score_interpr: score_interpr = textify(re.findall('\((.*?)\)',score_interpr))
            aux_info = {}
            aux_info.update({"browse":browse})
            if image: aux_info.update({"image":image})
            if location: aux_info.update({"location":location})
            if score:aux_info.update({"score":score})
            if score_interpr: aux_info.update({"score_interpretaion":score_interpr})
            if 'http' not in review_ur: review_ur = "{}{}".format(self.domain,review_ur)
            sk = md5(review_ur)
            self.get_page('consumerdaddy_review_terminal',review_ur, sk, aux_info)
        next_page = sel.xpath('//a[@class="gridPaginghighlight"][contains(text(),"Next")]')
        view_state = extract_data(sel, '//input[@id="__VIEWSTATE"]/@value')
        c_tab = extract_data(sel, '//input[@name="ctab"]/@value')
        user_active = extract_data(sel, '//input[@name="ctl00$cphMasterPanel$hfUserActive"]/@value')
        hf_url = extract_data(sel, '//input[@name="ctl00$cphMasterPanel$hfUrl"]/@value')
        calling_page = extract_data(sel, '//input[@name="ctl00$Footer$hdnCallingPage"]/@value')
        hdn_url = extract_data(sel, '//input[@name="ctl00$Footer$hdnUrl"]/@value')
        user_status = extract_data(sel, '//input[@name= "ctl00$Footer$hdnUserStatus"]/@value')
        event_validation = extract_data(sel, '//input[@name="__EVENTVALIDATION"]/@value')
        user_login = extract_data(sel, '//input[@name="ctl00$searchControl$hdnUserLogIn"]/@value')
        local_id = extract_data(sel, '//input[@name="ctl00$searchControl$hdnLocID"]/@value')
        hdn_check = extract_data(sel,'//input[@name="ctl00$searchControl$hdnCheck"]/@value')
        if next_page:
            next_headers = {
            'Origin': 'http://www.consumerdaddy.com',
            'Host':"www.consumerdaddy.com",
            'Accept-Encoding': 'gzip, deflate',
            'Upgrade-Insecure-Requests': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Cache-Control': 'max-age=0',
            'Referer': response.url,
            'Connection': 'keep-alive',
            }
            form_data = {
            "__EVENTTARGET":"ctl00$cphMasterPanel$pcSelectList",
            "__EVENTARGUMENT": "NextPage",
            "ctl00$searchControl$hdnLocID":local_id,
            "__VIEWSTATE": view_state,
            "ctl00$searchControl$txtSearch$ctl00":self.browse_list,
            "PageLoadedHiddenTxtBox":"Set",
            "ctl00$Footer$hdnCallingPage":calling_page,
            "ctl00$Footer$hdnUrl":hdn_url,
            "ctl00$Footer$hdnUserStatus":user_status,
            "__EVENTVALIDATION":event_validation,
            "ctl00$Footer$hdnUserName":"",
            "ctl00$SleepCount":'1',
            "ctl00$searchControl$hdnCheck":hdn_check,
            "ctl00$searchControl$hdnUserLogIn":user_login,
            "ctab":c_tab,
            "ctl00$searchControl$hdnTab":'',
            "ctl00$searchControl$hdnUser":'',
            "ctl00$searchControl$txtSearch$_SelectedValue":''}
            yield FormRequest(response.url, formdata=form_data, callback=self.parse, headers=next_headers,  dont_filter=True, meta={"browse":browse})
