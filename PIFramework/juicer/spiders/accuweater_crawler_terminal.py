import scrapy
import hashlib
import csv
import datetime
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest
import datetime
from juicer.utils import *
from juicer.items import *
import MySQLdb
import time
import scrapy
import json

class AccuweatherTerminal(JuicerSpider):
    name = "accuweather_crawler_terminal"
    #start_urls = ['http://dataservice.accuweather.com/forecasts/v1/daily/1day/2854563?apikey=KhGBThwa3dCnHkxYfa0oFFU6PJhA6Mqk']
    handle_httpstatus_list = [404, 302, 303, 403, 500, 999, 503]

    def __init__(self, *args, **kwargs):
        super(AccuweatherTerminal, self).__init__(*args, **kwargs)
        self.con = MySQLdb.connect(db='accuweather',
        user='root', passwd='root',
        charset="utf8", host='localhost', use_unicode=True)
        self.cur = self.con.cursor()
        self.cur = self.con.cursor()
        #self.excel_file_name = 'accuweather_data_on_%s.csv'%str(datetime.datetime.now().date())
        #oupf = open(self.excel_file_name, 'ab+')
        #self.todays_excel_file  = csv.writer(oupf)
        #todays_excel_file.writerow(header)
        self.insert_query = 'insert into Accuweather_data(sk,customer_no,latitude,longitude,city,country,timeoffset,timezone_name,region_name,timezone_code,day_light_saving,effective_date,severity,daily_forecast_date,weather_text,daily_forecast_epochdate,temp_min_value,temp_min_unit,temp_min_unittype,temp_max_value,temp_max_unit,temp_max_unittype,day_icon,dayiconphrase,night_icon,night_iconphrase,link,mobile_link,reference_url,created_at,modified_at)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),now()) on duplicate key update modified_at = now()' 
	#self.update_qry = 'update urlqueue_dev.openweather_crawl set crawl_status=1 where sk="%s"'        

    def parse(self, response):
        sel = Selector(response)
        body = json.loads(response.body)
        cust_no = response.meta.get('data','').get('cust_no','')
        city = response.meta.get('data','').get('city_name')
        timeoffset = response.meta.get('data','').get('timeoffset','')
        region_name = response.meta.get('data','').get('region_name','')
        country_name = response.meta.get('data','').get('country_name','')
        day_light_saving = response.meta.get('data','').get('day_light_saving','')
        timezone_name = response.meta.get('data','').get('timezone_name','')
        timezone_code = response.meta.get('data','').get('timezone_code','')
        lat = response.meta.get('data','').get('lat','')
        lon = response.meta.get('data','').get('lon','')
        effective_date = body.get('Headline',{}).get('EffectiveDate','')
        severity = body.get('Headline',{}).get('Severity','')
        text = body.get('Headline',{}).get('Text','')
        daily_forecast = body.get('DailyForecasts',{})[0].get('Date','')
        epochdate = body.get('DailyForecasts',{})[0].get('EpochDate','')
        temp = body.get('DailyForecasts',{})[0].get('Temperature',{}).get('Minimum','')
        min_val = temp.get('Value','')
        min_unit = temp.get('Unit','')
        minunit_type = temp.get('UnitType','')
        temp_max = body.get('DailyForecasts',{})[0].get('Temperature',{}).get('Maximum','')
        max_val = temp_max.get('Value','')
        max_unit = temp_max.get('Unit','')
        maxunit_type = temp_max.get('UnitType','')
        day_forecast = body.get('DailyForecasts',{})[0].get('Day',{})
        day_icon = day_forecast.get('Icon','')
        day_iconphrase = day_forecast.get('IconPhrase','')
        night_forecast = body.get('DailyForecasts',{})[0].get('Night',{})
        night_icon = night_forecast.get('Icon','')
        night_phrase = night_forecast.get('IconPhrase','')
        link =  body.get('DailyForecasts',{})[0].get('Link','')
        mobile_link =  body.get('DailyForecasts',{})[0].get('MobileLink','')
        sk = response.url.split('?')[0].split('/')[-1]
        values = (sk,cust_no,lat,lon,city,country_name,timeoffset,timezone_name,region_name,timezone_code,day_light_saving,effective_date,severity,daily_forecast,text,epochdate,min_val,min_unit,minunit_type,max_val,max_unit,maxunit_type,day_icon,day_iconphrase,night_icon,night_phrase,link,mobile_link,response.url)
        values = [str(i) for i in values]
        self.cur.execute(self.insert_query,values)
            
                    
        


        








