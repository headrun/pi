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
            mobile_no,address_new = i[0],i[1]
            sk = md5.md5(normalize(address_new)+str(mobile_no)).hexdigest()
            url =  "https://maps.googleapis.com/maps/api/geocode/json?sensor=true&address=<%s>" %address_new+'&key=AIzaSyBiPi45gy9rNbZL-Jtfbk47s-TwZ7j1NkA'
            self.get_page("address_latlong_terminal",url,sk,meta_data={'full_address':address_new,'s_no': mobile_no})

    def read(self):
        files_list = glob.glob(address_processing_path+'/*.xlsx')
        for _file in files_list:
                if 'address_cleaned' in _file :continue
                W = px.load_workbook(_file, use_iterators = True)
                sheet_list = W.get_sheet_names()
                for xl in sheet_list:                      
                    sheet_ = W.get_sheet_by_name(name = xl)
                    if  'Permanent' in xl :continue
                    x = 1
                    address_list = []
                    for row in sheet_.iter_rows():
                        Address = row
                        mobile_no = Address[0].value
                        try : 
                            full_address = Address[1].value
                        except : print  "Addresses is empty"
                        if 'Address' in full_address : continue
                        address_list.append((mobile_no,full_address))
                        x = x+1
                    return address_list
                   





