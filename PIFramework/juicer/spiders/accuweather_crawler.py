import scrapy
import hashlib
import csv
import datetime
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest
import datetime
import MySQLdb
import time
import scrapy
import json


class Accuweatherbrowse(scrapy.Spider):
    name = "Accuweather_browse"
    handle_httpstatus_list = [404, 302, 303, 403, 500, 999, 503]

    def __init__(self, *args, **kwargs):
        super(Openweatherbrowse, self).__init__(*args, **kwargs)
        self.con = MySQLdb.connect(db='accuweather',
        user='root', passwd='root',
        charset="utf8", host='localhost', use_unicode=True)
        self.cur = self.con.cursor()
        self.cur = self.con.cursor()
        self.insert_query = 'insert into openweather(sk,latitude,longitude,city,country,visibility,dt,base,wind_speed,wind_deg,cod,pressure,temp_min,temp_max,temp,humidity,clouds,weather_id,weather_main,icon,description,sunrise,sunset,message,sys_id,type,reference_url,created_at,modified_at)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),now()) on duplicate key update modified_at = now()' 
        
    def start_requests(self):
        #import pdb;pdb.set_trace()
    	api_key = "0cbc3c0cab66a5d4381544824b8eaaf4"
        lat = '13.0827'
        lon = '80.2707'
        link = 'http://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&appid=%s'%(lat,lon,api_key)
        yield Request(link,callback=self.parse,dont_filter=True)

    def parse(self, response):
        sel = Selector(response)
        body = json.loads(response.body)
        cloud_data = body.get('clouds','').get('all','')
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
        import pdb;pdb.set_trace()
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
        lat = coord.get('lat','')
        lon = coord.get('lon','')
        country = sys.get('country','')
        sunset = sys.get('sunset','')
        message = sys.get('message','')
        type_ = sys.get('type','')
        sys_id = sys.get('id','')
        sunrise = sys.get('sunrise','')
        values = (id_,lat,lon,city_name,country,visibility,dt,base,wind_speed,wind_deg,cod,pressure,temp_min,temp_max,temp,humidity,cloud_data,weather_id,weather_main,icon,desc,sunrise,sunset,message,sys_id,type_,response.url)
        import pdb;pdb.set_trace()
        self.cur.execute(self.insert_query,values)
        


        








