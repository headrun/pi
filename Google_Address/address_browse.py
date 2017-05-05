from juicer.utils import *
from juicer.items import *
import requests
import json
import MySQLdb
import optparse
import smtplib
import datetime
import time
from datetime import timedelta
import email
import getpass
import imaplib
import datetime
import os
import MySQLdb
import re
from auto_input import *
import glob
import openpyxl as px
import md5

 
class AddressBrowse(JuicerSpider):
    name = 'address_browse'
    start_urls = ['https://docs.google.com/spreadsheets/d/104iijFYtMvApZFK5qafLr4hQJQxkJrgr2zeTq6qjPaw/edit']
     

    def __init__(self, *args, **kwargs):
        super(AddressBrowse, self).__init__(*args, **kwargs)

    def parse(self, response):
        sel = Selector(response)
        address_list = self.read()
        for i in address_list :
            s_no,sk,old_address,address_new = i[0],i[1],i[2],i[3]
            #id_ = md5.md5(str(sk)+normalize(address_original)+normalize(address_new)).hexdigest()
            url =  "http://maps.googleapis.com/maps/api/geocode/json?sensor=true&address=<%s>" %address_new
            self.get_page("address_latlong_terminal",url,s_no,meta_data={'addess_new':address_new,'old_address':old_address,'sk':sk})

    def read(self):
        files_list = glob.glob(address_processing_path+'/*.xlsx')
        for _file in files_list:
                if 'address_cleaned' in _file :continue
                W = px.load_workbook(_file, use_iterators = True)
                sheet_list = W.get_sheet_names()
                for xl in sheet_list:                      
                    sheet_ = W.get_sheet_by_name(name = xl)
                    if  'Permanent' in xl or 'Sheet3' in xl:continue
                    address_list = []
                    for row in sheet_.iter_rows():
                        Address = row
                        s_no = Address[0].value
                        try : 
                            old_address = Address[2].value
                            sk = Address[1].value
                            address_new = Address[3].value
                        except : print  "Addresses is empty"
                        if 'address_old' in old_address : continue
                        address_list.append((s_no,sk,old_address,address_new))
                    return address_list
                   





