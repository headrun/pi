import json
import MySQLdb
from juicer.utils import *
api_key = "u4mAABUu6yKKGGyGorl0Oh0A0aGGEKGZ"


class Accuweather(JuicerSpider):
                name        = 'accuweather_crawler_browse'
                start_urls  =  ['https://www.justdial.com/Trichy/Ophthalmologists/nct-10343851']
                handle_httpstatus_list = [404, 302, 303, 403, 500]

                def parse(self,response):
                    with open('lat_long_20181224.csv', 'r') as f:
                    	rows = f.readlines()
            		for row in rows[0:20]:
                	    #import pdb;pdb.set_trace()
                            data = row.split(',')
                            cust_no, lat, lon = data
                            lat = lat.replace('\r\n','')
                            lon = lon.replace('\r\n','')
                            if 'Number' in cust_no : continue
                            link = "http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey=%s&q=%s,%s"%(api_key,lat,lon)
                            yield Request(link,callback=self.parse_meta,dont_filter=True,meta={'lat':lat,'lon':lon,'cust_no':cust_no})	

                def parse_meta(self,response):
                    sel = Selector(response)
                    cust_no = response.meta.get('cust_no','')
                    import pdb;pdb.set_trace()
                    body = json.loads(response.body)
                    key = body.get('Key','')
                    city_name = body.get('LocalizedName','')
                    region_name = body.get('Region',{}).get('LocalizedName','')
                    country_name = body.get('Country',{}).get('LocalizedName','')
                    timezone_code =  body.get('TimeZone',{}).get('Code','')
                    timezone_name = body.get('TimeZone',{}).get('Name','')
                    timeoffset = body.get('TimeZone',{}).get('GmtOffset','')
                    day_light_saving = body.get('TimeZone',{}).get('IsDaylightSaving','')
                    lat = body.get('GeoPosition',{}).get('Latitude','')
                    lon =  body.get('GeoPosition',{}).get('Longitude','')
                    api_link = "http://dataservice.accuweather.com/forecasts/v1/daily/1day/%s?apikey=%s"%(key,api_key)
                    self.get_page("accuweather_crawler_terminal",api_link,cust_no,meta_data={'lat':lat,'lon':lon,'cust_no':cust_no,'city_name':city_name,'region_name':region_name,'country_name':country_name,'timezone_code':timezone_code,'timezone_name':timezone_name,'timeoffset':timeoffset,'day_light_saving':day_light_saving})

