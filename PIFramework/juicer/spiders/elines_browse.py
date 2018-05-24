import scrapy
import hashlib
import md5
import re
import csv
import datetime
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest
#from crowdanalytix_generic_functions import *

class Elines(scrapy.Spider):
    name = 'elines_browse'
    start_urls = ('http://elines.coscoshipping.com/NewEBWeb/public/cargoTracking/cargoTracking.xhtml#',)
    
    def __init__(self, *args, **kwargs):
        super(Elines, self).__init__(*args, **kwargs)
        self.header_params = ['Container Number', 'Size/Type', 'Location', 'Status Message', 'Event Date/Time']
        self.excel_file_name = 'shipment_status_data_for_elines_%s.csv'%str(datetime.datetime.now().date())
        oupf = open(self.excel_file_name, 'ab+')
        self.todays_excel_file  = csv.writer(oupf)
        self.todays_excel_file.writerow(self.header_params)
        self.list_of = ['CBHU5592835', 'MAGU2489750','FCIU5209349', 'CDDU9005920', 'CSLU1199501', 'GVCU5226322','GVCU2079887', 'CBHU5845337', 'CBHU3948927', 'DFSU2250785', 'CSLU2431890', 'BSIU2777810', 'SEGU3164481', 'GESU1289232', 'CBHU5845337', 'GVCU2079887', 'CBHU3948927', 'TEMU3994968', 'CBHU3703478', 'CBHU3703478']
        self.headers = {
        'Pragma': 'no-cache',
        'Origin': 'http://elines.coscoshipping.com',
        'Accept-Encoding': 'gzip, deflate',
        'Faces-Request': 'partial/ajax',
        'Accept-Language': 'en-GB,en-US;q=0.8,en;q=0.6',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/xml, text/xml, */*; q=0.01',
        'Cache-Control': 'no-cache',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Referer': 'http://elines.coscoshipping.com/NewEBWeb/public/cargoTracking/cargoTracking.xhtml',
        }
        self.partial_render = 'bookingNumbers billToBookingGrop billofLading_Table3 release_Information_bill release_Information_booking cargoTrackingOrderBillInformation cargoTrackingBookingOfLadingInformation cargoTrackingContainerHistory cargoTrackingContainerInfoStatus cargoTrackingContainerBillOfLadingNumber1 cargoTrackingContainerInfoByContainerNumber release_Information_booking_version release_Information_bill_version actualLoadingInfo containerInfoByBlNum containerInfoByBkgNumTable actualLoadingInfo5 documentStatus cargoTrackingAcivePictures containerNumberAll containerInfo_table3 containerInfo_table4 cargoTrackingPrintByContainer containerNumberAllByBookingNumber registerUserValidate validateCargoTracking isbillOfLadingExist isbookingNumberExist cargoTrackingContainerPictureByContainer cargoTrackingContainerHistory1 cargoTrackingOrderBillMyFocus cargoTrackingBookingMyFocus userId contaienrNoExist billChange4 bookingChange4 bookingChange3 cargoTrackingContainerHistory6 numberType containerSize containerMessage containerTab isLogin cargoTrackingBillContainer cargoTrackingBillContainer1 BillMessage BookingMessage searchSuccess searchError containerTransportationMode'
 
    def parse(self, response):
        sel = Selector(response)
        view_state = ''.join(sel.xpath('//input[@id="javax.faces.ViewState"]/@value').extract())
        for list_ in self.list_of:
            data = {'mainForm': 'mainForm',
              'cargoTrackSearchId': 'CONTAINER',
              'cargoTrackingPara': list_,
              'numberType': 'CONTAINER',
              'containerSize': '1',
              'containerTransportationMode': '',
              'bookingNumbers': '0',
              'javax.faces.partial.ajax': 'true',
              'javax.faces.source':'cargoTrckingFindButton',
              'javax.faces.partial.execute': '@all',
              'javax.faces.partial.render': self.partial_render,
              'cargoTrckingFindButton': 'cargoTrckingFindButton',
              'javax.faces.ViewState':view_state}
            yield FormRequest('http://elines.coscoshipping.com/NewEBWeb/public/cargoTracking/cargoTracking.xhtml', headers=self.headers,  formdata=data, dont_filter = True, callback = self.parse_next, meta = {'data':data})
    
    def parse_next(self, response):
        sel = Selector(response)
        import pdb;pdb.set_trace()
        search = sel.xpath('//update[@id="searchSuccess"]/text()').extract()
        values = ['', '', '', '', '']
        if search:
            sel = Selector(text = search[0])
            display_text = sel.xpath('//div[@class="CargoTracking_bar2"][strong[contains(text(), "Latest Container Status")]]//..//table[1]//td//text()').extract()
            nodes = sel.xpath('//div[@class="CargoTracking_bar2"][strong[contains(text(), "Latest Container Status")]]//../table[2]//tr')
            for node in nodes : 
                import pdb;pdb.set_trace()
                status = node.xpath('.//td[0]//text()').extract()
 
            if display_text:
                try:
                    conta_num, siz_type, seal_no, location, status, time = display_text
                    values = [conta_num, siz_type, location, status, time]
                except:
                    print '1'
        self.todays_excel_file.writerow(values)
                
