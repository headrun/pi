from linkedin_voyager_functions import *
import ast

class Linkedincsc(object):
	def __init__(self, *args, **kwargs):
		self.con, self.cur = get_mysql_connection('localhost', 'FACEBOOK', '')
		self.excel_file_name = 'linkedin_company_data_%s.csv' % str(datetime.datetime.now().date())
		if os.path.isfile(self.excel_file_name):
			os.system('rm %s'%self.excel_file_name)
		oupf = open(self.excel_file_name, 'ab+')
		self.todays_excel_file  = csv.writer(oupf)
		self.query1 = 'select * from %s'
		self.query2 = 'select * from %s where %s = "%s"'
		self.headers1 = ['company_given_url', 'company_given_sno', 'company_given_name', 'company_name', 'company_page_url', 'number_of_employees', 'no_of_followers', 'industry', 'city', 'geographic_area', 'line1', 'line2', 'postal_code', 'company_type', 'company_description', 'status']
		self.todays_excel_file.writerow(self.headers1)


	def main(self):
		records = fetchall(self.cur, self.query1%('linkedin_company_check'))
		for rec in records:
			recmain = fetchmany(self.cur, self.query2 % ('linkedin_company_meta', 'sk', rec[1]))
			jso_data = ast.literal_eval(rec[3])
			her_va3 = []
			if recmain:
				cvs = list(recmain[0])[1:-3]
				her_va3 = cvs + ['Avaialble']
			else:
				her_va3 = ['' for i in self.headers1]
				her_va3[-1] = 'Not Available'
			her_va3[0] = jso_data.get('company_url', '')
			her_va3[1] = str(jso_data.get('sno', ''))
			her_va3[2] = jso_data.get('company_given_name', '')
			her_va3 = [normalize(i) for i in her_va3]
			print her_va3[0:4]
			self.todays_excel_file.writerow(her_va3)

if __name__ == '__main__':
	Linkedincsc().main()
	
