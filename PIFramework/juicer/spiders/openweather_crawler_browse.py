import json
import MySQLdb
from juicer.utils import *

con = MySQLdb.connect(host='localhost', user= 'root',  passwd='root', db="AGENTS",charset="utf8",use_unicode=True)
cur = con.cursor()


class OPENWEATHER(JuicerSpider):
                name        = 'openweather_crawler_browse'
                start_urls  =  ['https://www.justdial.com/Trichy/Ophthalmologists/nct-10343851']
                handle_httpstatus_list = [404, 302, 303, 403, 500]


                def parse(self,response):
                    big_list , small_list , final_list= [],[],[]
		    api_key = "0cbc3c0cab66a5d4381544824b8eaaf4"
                    with open('lat_long_20181224.csv', 'r') as f:
                    	rows = f.readlines()
            		for row in rows:
                	    #import pdb;pdb.set_trace()
                            data = row.split(',')
                            cust_no, lat, lon = data
                            lat = lat.replace('\r\n','')
                            lon = lon.replace('\r\n','')
                            if 'Number' in cust_no : continue
                            big_list.append(cust_no)
                            link = 'http://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&appid=%s'%(lat,lon,api_key)
                            self.get_page("openweather_crawler_terminal",link,cust_no,meta_data={'lat':lat,'lon':lon,'cust_no':cust_no})
                        #import pdb;pdb.set_trace()
                        """sel_qry = 'select customer_no from accuweather.openweather'
                        cur.execute(sel_qry)
                        data = cur.fetchall()
                        for row in data :
                            cust_no = row[0]
                            small_list.append(cust_no)
                    for cust_no in big_list : 
                        if cust_no not in small_list : 
                            final_list.append(cust_no)
                            print final_list
                    open('data.txt','wb+').write('%s\n'%final_list)
                    with open('lat_long_20181224.csv', 'r') as f:
                        rows = f.readlines()
                        for row in rows:
                            #import pdb;pdb.set_trace()
                            data = row.split(',')
                            cust_no, lat, lon = data
                            lat = lat.replace('\r\n','')
                            lon = lon.replace('\r\n','')
                            if 'Number' in cust_no : continue
                            if cust_no in final_list : #big_list.append(cust_no)
                                #import pdb;pdb.set_trace()
                                print cust_no
                                link = 'http://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&appid=%s'%(lat,lon,api_key)"""
                            #yield Request(link,callback=self.parse,dont_filter=True,meta={'lat':lat,'lon':lon,'cust_no':cust_no})	
                        
