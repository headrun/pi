import os, sys, datetime, subprocess, MySQLdb, codecs, json
import optparse, logging, logging.handlers
import xlwt, csv
import smtplib,ssl
import string
import smtplib

class ExcelGenIOC():

    def __init__(self):
        self.load_dict = {}
        self.today_date = datetime.datetime.now().date()
        self.excel_file_name = 'doctorprofile.xls' 

    def xcode(self, text, encoding='utf8', mode='strict'):
        return text.encode(encoding, mode) if isinstance(text, unicode) else text

    def get_mysql_conn(self):
        self.conn = MySQLdb.connect(db = 'ASKAPOLLO', user='root', host = 'localhost', passwd='hdrn59!', charset   = "utf8", use_unicode=False)
        self.cur = self.conn.cursor()

    def excel_generation(self):
        header = ['doctor_id','doctor_name','doctor_profile_link','qualification','specialization','years_of_experience','research_and_publications','languages_spoken','special_interets','services','awards_recognitions','summary','clinic_names','time_schedule','memeberships','experience','medical_council_registration','recommendations','doctor_image','reference_url','aux_info','review_sk','feedback_filters','feedback_name','feedback_publish_date','feeback_text']

        query = "select doctor_id, doctor_name, doctor_profile_link,qualification,specialization,years_of_experience,research_and_publications,languages_spoken,special_interets,services,awards_recognitions,summary,clinic_names,time_schedule,memeberships,experience,medical_council_registration,recommendations,doctor_image,reference_url,aux_info from DoctorMeta where date(modified_at)>='2017-11-23'"

        self.cur.execute(query)
        rows = self.cur.fetchall()
        todays_excel_file = xlwt.Workbook(encoding="utf-8")
        todays_excel_sheet1 = todays_excel_file.add_sheet("sheet1")
        row_count = 1

        for i, row in enumerate(header):
            todays_excel_sheet1.write(0, i, row)

        for _row in rows:

            doctor_id,doctor_name, doctor_profile_link,qualification,specialization,years_of_experience,research_and_publications,languages_spoken,special_interets,services,awards_recognitions,summary,clinic_names,time_schedule,memeberships,experience,medical_council_registration,recommendations,doctor_image,reference_url,aux_info = _row
            qry = 'select sk,feedback_filters,feedback_name,feedback_publish_date,feeback_text from DoctorFeedback where doctor_id ="%s" and date(modified_at)>="2017-11-23"'%str(doctor_id)
            self.cur.execute(qry)
            data = self.cur.fetchall()
            sk,feedback_filters,feedback_name,feedback_publish_date,feeback_text=['']*5
            if data:
                for data_ in data :
                    sk,feedback_filters,feedback_name,feedback_publish_date,feeback_text = data_

                    values = [doctor_id, doctor_name, doctor_profile_link,qualification,specialization,years_of_experience,research_and_publications,languages_spoken,special_interets,services,awards_recognitions,summary,clinic_names,time_schedule,memeberships,experience,medical_council_registration,recommendations,doctor_image,reference_url,aux_info,sk,feedback_filters,feedback_name,feedback_publish_date,feeback_text]
                    for col_count, value in enumerate(values):
                        todays_excel_sheet1.write(row_count, col_count, value)
                    row_count = row_count+1
            else:
                values = [doctor_id, doctor_name, doctor_profile_link,qualification,specialization,years_of_experience,research_and_publications,languages_spoken,special_interets,services,awards_recognitions,summary,clinic_names,time_schedule,memeberships,experience,medical_council_registration,recommendations,doctor_image,reference_url,aux_info,sk,feedback_filters,feedback_name,feedback_publish_date,feeback_text]

                for col_count, value in enumerate(values):
                    todays_excel_sheet1.write(row_count, col_count, value)
                row_count = row_count+1

        todays_excel_file.save(self.excel_file_name)

    def main(self):
        self.get_mysql_conn()
        self.excel_generation()


if __name__ == '__main__':
    OBJ = ExcelGenIOC()
    OBJ.main()


