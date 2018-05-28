from juicer.utils import *
from juicer.items import *
import requests
import json
import MySQLdb
import csv
city = 'chennai'

 
class ImaBrowse(JuicerSpider):
    name = 'ima_browse'
    start_urls = ["http://www.ima-india.org/demomembership/ima-member-sys-encr/server_processing.php?draw=20&columns[0][data]=0&columns[0][name]=&columns[0][searchable]=true&columns[0][orderable]=true&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=1&columns[1][name]=&columns[1][searchable]=true&columns[1][orderable]=true&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=2&columns[2][name]=&columns[2][searchable]=true&columns[2][orderable]=true&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=3&columns[3][name]=&columns[3][searchable]=true&columns[3][orderable]=true&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=4&columns[4][name]=&columns[4][searchable]=true&columns[4][orderable]=true&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=5&columns[5][name]=&columns[5][searchable]=true&columns[5][orderable]=true&columns[5][search][value]=&columns[5][search][regex]=false&columns[6][data]=6&columns[6][name]=&columns[6][searchable]=true&columns[6][orderable]=true&columns[6][search][value]=&columns[6][search][regex]=false&columns[7][data]=7&columns[7][name]=&columns[7][searchable]=true&columns[7][orderable]=true&columns[7][search][value]=&columns[7][search][regex]=false&order[0][column]=6&order[0][dir]=asc&start=0&length=10&search[regex]=false&_=1512385551483"]
     

    def __init__(self, *args, **kwargs):
        super(ImaBrowse, self).__init__(*args, **kwargs)
        self.header_params = ['State','Branch','La','first_name','Last_name','District','City','Pin']
        self.excel_file_name = 'Ima_dataon__%s.csv'%str(datetime.datetime.now().date())
        oupf = open(self.excel_file_name, 'wb+')
        self.todays_excel_file  = csv.writer(oupf)
        self.todays_excel_file.writerow(self.header_params)

    def parse(self, response):
        sel = Selector(response)
        json_data = json.loads(response.body)
        length = json_data['recordsFiltered']
        if length <= 25000 :  
            link = "http://www.ima-india.org/demomembership/ima-member-sys-encr/server_processing.php?draw=20&columns[0][data]=0&columns[0][name]=&columns[0][searchable]=true&columns[0][orderable]=true&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=1&columns[1][name]=&columns[1][searchable]=true&columns[1][orderable]=true&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=2&columns[2][name]=&columns[2][searchable]=true&columns[2][orderable]=true&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=3&columns[3][name]=&columns[3][searchable]=true&columns[3][orderable]=true&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=4&columns[4][name]=&columns[4][searchable]=true&columns[4][orderable]=true&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=5&columns[5][name]=&columns[5][searchable]=true&columns[5][orderable]=true&columns[5][search][value]=&columns[5][search][regex]=false&columns[6][data]=6&columns[6][name]=&columns[6][searchable]=true&columns[6][orderable]=true&columns[6][search][value]=&columns[6][search][regex]=false&columns[7][data]=7&columns[7][name]=&columns[7][searchable]=true&columns[7][orderable]=true&columns[7][search][value]=&columns[7][search][regex]=false&order[0][column]=6&order[0][dir]=asc&start=0&length=%s&search[regex]=false&_=1512385551483"%length
            yield Request(link,callback=self.parse_meta)
        else :
             length = length
             start_value = 25000
             link = "http://www.ima-india.org/demomembership/ima-member-sys-encr/server_processing.php?draw=20&columns[0][data]=0&columns[0][name]=&columns[0][searchable]=true&columns[0][orderable]=true&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=1&columns[1][name]=&columns[1][searchable]=true&columns[1][orderable]=true&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=2&columns[2][name]=&columns[2][searchable]=true&columns[2][orderable]=true&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=3&columns[3][name]=&columns[3][searchable]=true&columns[3][orderable]=true&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=4&columns[4][name]=&columns[4][searchable]=true&columns[4][orderable]=true&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=5&columns[5][name]=&columns[5][searchable]=true&columns[5][orderable]=true&columns[5][search][value]=&columns[5][search][regex]=false&columns[6][data]=6&columns[6][name]=&columns[6][searchable]=true&columns[6][orderable]=true&columns[6][search][value]=&columns[6][search][regex]=false&columns[7][data]=7&columns[7][name]=&columns[7][searchable]=true&columns[7][orderable]=true&columns[7][search][value]=&columns[7][search][regex]=false&order[0][column]=6&order[0][dir]=asc&start=%s&length=%s&search[regex]=false&_=1512385551483"%(start_value,length)
                 
             yield Request(link,callback=self.parse_meta,meta={'start_value':start_value,'length':length})
        

    def parse_meta(self,response):
        sel = Selector(response)
        start_value = response.meta.get('start_value','')
        json_data = json.loads(response.body)
        if json_data : 
            data = json_data.get('data',[])
            for data_ in data : 
                state,branch,la,first_name,last_name,district,city,pin = data_
                values = [state,branch,la,first_name,last_name,district,city,pin]
                self.todays_excel_file.writerow(values)

        range_value = length/25000
        for i in range(0,range_value):
            link = "http://www.ima-india.org/demomembership/ima-member-sys-encr/server_processing.php?draw=20&columns[0][data]=0&columns[0][name]=&columns[0][searchable]=true&columns[0][orderable]=true&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=1&columns[1][name]=&columns[1][searchable]=true&columns[1][orderable]=true&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=2&columns[2][name]=&columns[2][searchable]=true&columns[2][orderable]=true&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=3&columns[3][name]=&columns[3][searchable]=true&columns[3][orderable]=true&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=4&columns[4][name]=&columns[4][searchable]=true&columns[4][orderable]=true&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=5&columns[5][name]=&columns[5][searchable]=true&columns[5][orderable]=true&columns[5][search][value]=&columns[5][search][regex]=false&columns[6][data]=6&columns[6][name]=&columns[6][searchable]=true&columns[6][orderable]=true&columns[6][search][value]=&columns[6][search][regex]=false&columns[7][data]=7&columns[7][name]=&columns[7][searchable]=true&columns[7][orderable]=true&columns[7][search][value]=&columns[7][search][regex]=false&order[0][column]=6&order[0][dir]=asc&start=%s&length=%s&search[value]=%s&search[regex]=false&_=1512385551483"%(start_value,length,city)
            start_value = int(start_value) + 25000
            yield Request(link,callback=self.parse_nav,meta={'start_value':start_value,'length':length}) 

    def parse_nav(self,response):
        sel = Selector(response)
        json_data = json.loads(response.body)
        if json_data : 
            data = json_data.get('data',[])
            for data_ in data : 
                state,branch,la,first_name,last_name,district,city,pin = data_
                values = [state,branch,la,first_name,last_name,district,city,pin]
                self.todays_excel_file.writerow(values)

     
                
                
                   





