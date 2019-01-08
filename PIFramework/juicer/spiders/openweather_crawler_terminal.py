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

class OpenweatherTerminal(JuicerSpider):
    name = "openweather_crawler_terminal"
    #start_urls = ['https://www.flipkart.com/search?q=bestsellers&otracker=start&as-show=off&as=off']
    handle_httpstatus_list = [404, 302, 303, 403, 500, 999, 503]

    def __init__(self, *args, **kwargs):
        super(OpenweatherTerminal, self).__init__(*args, **kwargs)
        self.con = MySQLdb.connect(db='accuweather',
        user='root', passwd='root',
        charset="utf8", host='localhost', use_unicode=True)
        self.cur = self.con.cursor()
        self.cur = self.con.cursor()
	self.update_qry = 'update urlqueue_dev.openweather_crawl set crawl_status=1 where sk="%s"'        


    def parse(self, response):
        sel = Selector(response)
        body = json.loads(response.body)
        cust_no = response.meta.get('data','').get('cust_no','')
        cloud_data = body.get('clouds',{}).get('all','')
        city_name  = body.get('name','')
        visibility = body.get('visibility','')
        sys = body.get('sys','')
        weather = body.get('weather')
        coord  = body.get('coord','')
        base = body.get('base','')
        dt = body.get('dt','')
        main = body.get('main','')
        id_ = body.get('id','')
        wind = body.get('wind','')
        wind_speed = wind.get('speed','')
        wind_deg = wind.get('deg','')
        cod = body.get('cod','')
        pressure = main.get('pressure','')
        temp_min = main.get('temp_min','')
        temp_max = main.get('temp_max','')
        temp = main.get('temp','')
        humidity = main.get('humidity','')
        weather_dict = weather[0]
        weather_main = weather_dict.get('main','')
        weather_id = weather_dict.get('id','')
        icon = weather_dict.get('icon','')
        desc = weather_dict.get('description','')
        lat = response.meta.get('data','').get('lat','')
        lon = response.meta.get('data','').get('lon','')
        country = sys.get('country','')
        sunset = sys.get('sunset','')
        message = sys.get('message','')
        type_ = sys.get('type','')
        sys_id = sys.get('id','')
        sunrise = sys.get('sunrise','')
        openweatheritem = Openweather()
        openweatheritem.update({'sk':id_,
                                 'cust_no': cust_no,
                                 'latitude' : lat,
                                 'longitude' : lon,
                                 'city': city_name,
                                 'country' : country,
                                 'visibility': visibility,
                                 'dt' : dt,
                                 'base':base,
                                 'wind_speed': wind_speed,
                                 'wind_deg': wind_deg,
                                 'cod': cod,
                                 'pressure' : pressure,
                                 'temp_min': temp_min,
                                 'temp_max' : temp_max,
                                 'temp': temp,
                                 'humidity': humidity,
                                 'clouds' : cloud_data ,
                                  'weather_id': weather_id,
                                  'weather_main' : weather_main,
                                  'icon' : icon,
                                  'description' : desc,
                                   'sunrise' :sunrise,
                                   'sunset': sunset,
                                  'message': message,
                                   'sys_id' : sys_id,
                                    'type_': type_,
                                    'reference_url': response.url})
        print openweatheritem
        yield openweatheritem
        if weather :
            try :self.got_page(cust_no,1)
            except : print "second query"
                
                    
        


        








