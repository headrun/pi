import MySQLdb
import json
import datetime
import re
import sys
import optparse
import csv
from itertools import chain
from collections import OrderedDict
from linkedin_functions import *

class magicbricks(object):

    def __init__(self):
        self.con = MySQLdb.connect(db='magicbricks', user='root', passwd='root',
                   charset="utf8", host='localhost', use_unicode=True).cursor()
        self.cur = self.con
        self.excel_file_name = 'magicbricks_data_%s.csv'%str(datetime.datetime.now().date())
        self.selectqry = 'select sk,data_dict,reference_url from magicbricks'
        self.header_params = ['title']
        oupf = open(self.excel_file_name, 'wb+')
	self.todays_excel_file  = csv.writer(oupf)

    def send_xlstwitter(self):
            main_dict = {}
            self.cur.execute(self.selectqry)
            records = self.cur.fetchall()
	    for inde,rec in enumerate(records):
                try : me_dict  = eval(rec[1])
                except : continue
                for key,value in me_dict.iteritems():
                    key = key.lower()
                    if key=='title' : continue
                    if 'lift' in key : key = 'lifts'
                    if 'balcon' in key : key = 'balconies'
                    if key not in self.header_params : self.header_params.append(key)
            self.header_params.append('reference_url')
            self.todays_excel_file.writerow(self.header_params)
            for data in records :
                    sk, meta_dict, ref_url =  data
                    try : meta_dict = eval(meta_dict)
                    except :
                        meta_dict = {}
                        continue
                    for key ,value  in meta_dict.iteritems():	
                        key = key.lower()
                        if 'lift' in key : key = 'lifts'
                        if 'balcon' in key : key = 'balconies'
                        main_dict.update({key:value})
                    data_val = []
                    for i in self.header_params :
                         i_val = main_dict.get(i,' ').replace('u20b9', u'\u20b9 ').encode('utf-8')
                         i_val = i_val.replace('xa0',' ').replace('xc2','')
                         if i=='reference_url' : data_val.append(ref_url)
                         else : data_val.append(i_val)
                    values_ = [normalize(i) for i in data_val]
                    self.todays_excel_file.writerow(values_)
              
    def main(self):
        self.send_xlstwitter()

if __name__ == '__main__':
        magicbricks().main()
