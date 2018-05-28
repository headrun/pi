from juicer.utils import *
from juicer.items import *
from scrapy.http import FormRequest

class Consumerdaddybkup(JuicerSpider):
    name = "consumerdaddybkup_browse"
    start_urls = ["http://www.consumerdaddy.com/home.htm"]
    def __init__(self, *args, **kwargs):
        super(Consumerdaddybkup, self).__init__(*args, **kwargs)
        self.headers = {
        'Origin': 'http://www.consumerdaddy.com',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Cache-Control': 'max-age=0',
        'Referer': 'http://www.consumerdaddy.com/home.htm',
        'Connection': 'keep-alive',
        }
        self.browse_list = 'apollo hospitals'
        self.browse_list =  kwargs.get('search', self.browse_list)

    def parse(self, response):
        sel = Selector(response)
        event_target = extract_data(sel,'//input[@id="__EVENTTARGET"]/@value')
        event_argument = extract_data(sel, '//input[@id="__EVENTARGUMENT"]/@value')
        view_state = extract_data(sel, '//input[@id="__VIEWSTATE"]/@value')
        c_tab = extract_data(sel, '//input[@name="ctab"]/@value')
        user_active = extract_data(sel, '//input[@name="ctl00$cphMasterPanel$hfUserActive"]/@value')
        hf_url = extract_data(sel, '//input[@name="ctl00$cphMasterPanel$hfUrl"]/@value')
        calling_page = extract_data(sel, '//input[@name="ctl00$Footer$hdnCallingPage"]/@value')
        hdn_url = extract_data(sel, '//input[@name="ctl00$Footer$hdnUrl"]/@value')
        user_status = extract_data(sel, '//input[@name= "ctl00$Footer$hdnUserStatus"]/@value')
        event_validation = extract_data(sel, '//input[@name="__EVENTVALIDATION"]/@value')
        user_name = extract_data(sel, '//input[@name="ctl00$Footer$hdnUserName"]/@value')
        user_login = extract_data(sel, '//input[@name="ctl00$searchControl$hdnUserLogIn"]/@value')
        local_id = extract_data(sel, '//input[@name="ctl00$searchControl$hdnLocID"]/@value')
        hdn_check = extract_data(sel,'//input[@name="ctl00$searchControl$hdnCheck"]/@value')
        form_data = {"__EVENTTARGET":event_target,
        "__EVENTARGUMENT": event_argument,
        "ctl00$searchControl$hdnLocID":local_id,
        "__VIEWSTATE": view_state,
        "ctl00$searchControl$txtSearch$ctl00":self.browse_list,
        "PageLoadedHiddenTxtBox":"Set",
        "ctl00$cphMasterPanel$hfUserActive":user_active,
        "ctl00$cphMasterPanel$hfUrl":hf_url,
        "ctl00$Footer$hdnCallingPage":calling_page,
        "ctl00$Footer$hdnUrl":hdn_url,
        "ctl00$Footer$hdnUserStatus":user_status,
        "__EVENTVALIDATION":event_validation,
        "ctl00$Footer$hdnUserName":user_name,
        "ctl00$SleepCount":'1',
        "ctl00$searchControl$hdnCheck":hdn_check,
        "ctl00$searchControl$hdnUserLogIn":user_login,
        "ctl00$searchControl$ImageButton1.x":"67",
        "ctl00$searchControl$ImageButton1.y":"22",
        "ctab":c_tab,
        "ctl00$searchControl$hdnTab":'',
        "ctl00$searchControl$hdnUser":'',
        "ctl00$searchControl$txtSearch$_SelectedValue":''}
        yield FormRequest(response.url, formdata=form_data, callback=self.parse_login, headers=self.headers,  dont_filter=True)
    def parse_login(self, response):
        sel = Selector(response)
        url = extract_data(sel, '//input[@name="ctl00$Footer$hdnCallingPage"]/@value')
        if '?SearchText' in url:
            url = url.split('?SearchText')[0]
        if url:
            print url

