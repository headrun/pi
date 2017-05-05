import MySQLdb
import optparse
import smtplib
import getpass
import datetime
import os
from auto_input import *
import glob
import openpyxl as px



class CleanBrowse():

    def __init__(self):
        self.con = MySQLdb.connect(db          = 'address_components',
                      user        = 'root',
                      passwd      = 'root',
                      charset     = "utf8",
                      host        = 'localhost',
                      use_unicode = True)
        self.cur = self.con.cursor()



        self.insert_qry = 'insert into Clean_address_permutations(sk,key_value,old_address,address_new,flat,localityname,location2,city,state,code,country) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)'


    def main(self) :

        files_list= glob.glob(address_processing_path+'/*.xlsx')
        for _file in files_list:
      
		W = px.load_workbook(_file, use_iterators = True)
		sheet_list = W.get_sheet_names()
		for xl in sheet_list:                      
		    sheet_ = W.get_sheet_by_name(name = xl)
		    if  'Permanent' in xl or 'Sheet3' in xl:continue
		    address_list = []
		    for row in sheet_.iter_rows():
			Address = row
			#import pdb;pdb.set_trace()
			s_no = Address[0].value
		    
			old_address = Address[2].value
			sk = Address[1].value
			address_new = Address[3].value
			flat_no = Address[4].value
			localityname = Address[5].value
			location2 = Address[6].value
		      
			location3 = Address[7].value
			city = Address[8].value
			state = Address[9].value
			code = Address[10].value
			country = Address[11].value
			if 'Old address' in old_address : continue
		     
			if location2==None : location2 = ''  
			if flat_no==None : flat_no = '' 
			if localityname==None :  localityname = '' 
			if location3==None: localityname = ''
			if  city==None :city = '' 
			if state==None :state = ''
			if  code==None :code = '' 
			if country==None :country = ''
		      
			vals = (s_no,sk,old_address,address_new,flat_no,localityname,location2,city,state,code,country)
		 
			self.cur.execute(self.insert_qry,vals)

	 

if __name__ == '__main__':
    CleanBrowse().main()
