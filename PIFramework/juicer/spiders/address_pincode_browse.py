"""from juicer.utils import *
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
import os
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


    def read(self):
        with open('chennai_pincodes.txt', 'r') as f: rows = f.readlines()
        for row in rows:
            pincode = row.replace('\r\n','')
            sk = 0
            if pincode :
                url =  "https://maps.googleapis.com/maps/api/geocode/json?sensor=true&address=%s&key=AIzaSyDb1d7ic0UAmQxcXvD3Bs75NQJ24OuIEVM"%int(pincode)
                #import pdb;pdb.set_trace()
                self.get_page("address_latlong_terminal",url,sk,meta_data={'pincode':int(pincode)})
                sk = sk + 1

        files_list = glob.glob(address_processing_path+'/*.xlsx')
        for _file in files_list:
                if 'address_cleaned' in _file :continue
                W = px.load_workbook(_file, use_iterators = True)
                sheet_list = W.get_sheet_names()
                for xl in sheet_list:                      
                    sheet_ = W.get_sheet_by_name(name = xl)
                    if  'Permanent' in xl or 'Sheet3' in xl:continue
                    address_list = []
                    sk = 1
                    for row in sheet_.iter_rows():
                        pincode = row[0].value
                        if pincode :
                            url =  "http://maps.googleapis.com/maps/api/geocode/json?sensor=true&address=%s" %int(pincode)
                            self.get_page("address_latlong_terminal",url,sk,meta_data={'pincode':int(pincode)})
                            sk = sk + 1

                        else :break"""
                        
                   





