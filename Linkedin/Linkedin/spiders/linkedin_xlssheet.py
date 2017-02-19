import xlwt
import MySQLdb
import json
from linkedin_queries import *
import datetime

class Lixlsfile(object):

    def __init__(self, *args, **kwargs):
        self.con = MySQLdb.connect(db   = 'FACEBOOK', \
        host = 'localhost', charset="utf8", use_unicode=True, \
        user = 'root', passwd ='root')
        self.cur = self.con.cursor()
        self.row_count = 1
        self.excel_file_name = 'linkedin_profiles_%s.xls'%str(datetime.datetime.now().date())
        self.todays_excel_file = xlwt.Workbook(encoding="utf-8")
        self.todays_excel_sheet1 = self.todays_excel_file.add_sheet("sheet1")
	header_params = header2_params+header1_params
        for i, row in enumerate(header_params):
            self.todays_excel_sheet1.write(0, i, row)

    def restore(self, text):
        text = text.replace('<>#<>','"').replace("<>##<>","'").replace('###',',').replace('\\','')
        if '<>' in text:
            text = set(text.split('<>'))
            text = '<>'.join(text)
        return text

    def replacefun(self, text):
        text = text.replace('"','<>#<>').replace("'","<>##<>").replace(',','###')
        return text

    def send_xls(self):
        self.cur.execute(selectall_params)
        records = self.cur.fetchall()
        records = self.cur.fetchall()
        for record in records:
            sk2 , name2,  aux_info2, profile_url2 , connections = record
	    self.cur.execute(update_getc_params%('updatedrecord',sk1))
            original_url = ''
            if profile_url2 in original_url_list_params.values():
                original_url = (list(original_url_list_params.keys())[list(original_url_list_params.values()).index(profile_url2)])
            else: original_url = profile_url2
            email_address_dic = (list(dic_email_address.keys())[list(dic_email_address.values()).index(original_url)])
            try:
                aux_info_connections = json.loads(connections.replace('\\',''))
                aux_infof = json.loads(aux_info2.replace('\r','').replace('\n','').replace('\t','').replace('\\','').strip())
                response_flag = ''
                if name2:
                    response_flag = 'Response Available'
                if not name2: response_flag = 'Response Not Available'
                values = []
                for kil in header2_params:
                    values.append(self.restore(aux_infof.get(kil,'')))
                values1 = [self.restore(aux_infof.get('phone','')), self.restore(aux_infof.get('email','')),self.restore(aux_infof.get('skill','')), self.restore(aux_infof.get('group','')),self.restore(aux_infof.get('recom','')), self.restore(aux_infof.get('news','')), self.restore(aux_infof.get('companies','')),self.restore(aux_infof.get('influencers','')),self.restore(aux_infof.get('schools','')), self.restore(aux_info_connections.get('connections','')) ,response_flag, original_url, self.restore(aux_infof.get('email_address',''))]
                values.extend(values1)
                for col_count, value in enumerate(values):
                    self.todays_excel_sheet1.write(self.row_count, col_count, value)
                self.row_count = self.row_count+1
            except: self.log.error("Error: %s", traceback.format_exc())
        self.todays_excel_file.save(self.excel_file_name)


def main():
        obj = Lixlsfile()
        obj.send_xls()
if __name__ == '__main__':
        main()

