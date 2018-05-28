import MySQLdb
import datetime
import csv
import cPickle as pickle
import json

class MahaJson(object):
    def __init__(self, *args, **kwargs):
        self.con = MySQLdb.connect(host = 'localhost', user = 'root', passwd = '', db = 'MAHARERA', charset = 'utf8', use_unicode = True)
        self.cur = self.con.cursor()
        self.columns_query = 'SELECT COLUMN_NAME FROM information_schema.columns where table_schema= "MAHARERA" and table_name = "%s"'
        self.main()

    def main(self):
        tables_list = ['MahaRera_Meta','MahaRera_ProjectMeta','building_details_apartment_type','building_details_tasks','compliant_details','development_work','litigation_details','member_information','past_experience_details','project_details','project_prof_information','promoter_details']
        main_dict = {}
        self.cur.execute(self.columns_query%'Maharera_mainpage')
        main_headers = self.cur.fetchall()
        main_headers =  [x[0] for x in main_headers]
        sel_qry = 'select * from Maharera_mainpage'
        self.cur.execute(sel_qry)
        main_details = self.cur.fetchall()
        for index,row in enumerate(main_details) :
            inner_dict = {}
            inner_dict = {str(key):str(value) for key,value in zip(main_headers[2:-3],row[2:-3])}
            sel_qry2 = 'select * from %s where program_sk="%s"'
            for dx, table_name in enumerate(tables_list):
                self.cur.execute(self.columns_query%table_name)
                colum_names = self.cur.fetchall()
                colum_names =  [x[0] for x in colum_names]
                if dx != 0:
                     self.cur.execute(sel_qry2%(table_name,row[0]))
                elif dx ==0 : 
                    sel_qry3 = 'select * from %s where sk="%s"'
                    self.cur.execute(sel_qry3%(table_name,row[0]))
                data = self.cur.fetchall()
                list_ = []
                for data_row in data:
                    _dict = {str(key):str(value) for key,value in zip(colum_names[2:-3],data_row[2:-3])}
                    list_.append(_dict)
                inner_dict.update({table_name:list_})
		if not list_: print inner_dict[table_name]
            main_dict.update({index:inner_dict})         
        file_name = 'Mahaonline.json' 
        with open(file_name, 'wb+') as f :
            json.dump(main_dict,f)
        

if __name__ == '__main__':
    MahaJson()

