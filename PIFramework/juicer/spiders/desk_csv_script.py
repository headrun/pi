import os, sys, datetime, subprocess, MySQLdb, codecs, json
import optparse, logging, logging.handlers
import xlwt, csv
import re

def xcode(text, encoding='utf8', mode='strict'):
    return text.encode(encoding, mode) if isinstance(text, unicode) else text

def compact(text, level=0):
    if text is None: return ''

    if level == 0:
        text = text.replace("\n", " ")
        text = text.replace("\r", " ")
    compacted = re.sub("\s\s(?m)", " ", text)
    if compacted != text:
        compacted = compact(compacted, level+1)

    return compacted.strip()

def clean(text):
    if not text: return text

    value = text
    value = re.sub("&amp;", "&", value)
    value = re.sub("&lt;", "<", value)
    value = re.sub("&gt;", ">", value)
    value = re.sub("&quot;", '"', value)
    value = re.sub("&apos;", "'", value)

    return value

def normalize(text):
    return clean(compact(xcode(text)))



class Deskcsv(object):

	def is_path_file_name(self, excel_file_name):
		if os.path.isfile(excel_file_name):
			os.system('rm %s' % excel_file_name)
		oupf = open(excel_file_name, 'ab+')
		todays_excel_file = csv.writer(oupf)
		return todays_excel_file

	def __init__(self, *args, **kwargs):
		self.conn = MySQLdb.connect(user="root", host = "localhost", db="DESKCASES", passwd='root', use_unicode=True)
		self.cur  = self.conn.cursor()
		self.conn.set_character_set('utf8')
		self.cur.execute('SET NAMES utf8;')
		self.cur.execute('SET CHARACTER SET utf8;')
		self.cur.execute('SET character_set_connection=utf8;')
		self.excel_file_name = 'desk_cases_data_on_%s.csv' % (str(datetime.datetime.now().date()))
		todays_excel_file = self.is_path_file_name(self.excel_file_name)
		self.todays_excel_file = todays_excel_file
		self.header_params = ['id', 'filter_id', 'filter_name', 'assigned_group', 'active_at', 'active_attachments_count', 'active_notes_count', 'blurb', 'changed_at', 'label_ids', 'labels', 'language', 'locked_until', 'priority', 'opened_at', 'received_at', 'resolved_at', 'route_status', 'status', 'subject', 'type', 'updated_at', 'created_at', 'custom_fields', 'description', 'external_id', 'first_opened_at', 'first_resolved_at', 'has_failed_interactions', 'has_pending_interactions', 'customer_url', 'customer_id', 'customer_company_link', 'customer_twitter_user', 'customer_access_company_cases', 'customer_access_private_portal', 'customer_addresses', 'customer_avatar', 'customer_background', 'customer_company', 'customer_company_name', 'customer_created_at', 'customer_custom_fields', 'customer_display_name', 'customer_emails', 'customer_external_id', 'customer_first_name', 'customer_label_ids', 'customer_language', 'customer_last_name', 'customer_locked_until', 'customer_phone_numbers', 'customer_title', 'customer_uid', 'customer_updated_at', 'reply_updated_at', 'reply_from', 'reply']
		self.todays_excel_file.writerow(self.header_params)
		self.query1 = 'select * from desk_cases  where date(modified_at)>="2018-08-22"'
		self.query2 = 'select * from desk_customer where customer_link = "%s" and date(modified_at)>="2018-08-22"'
		self.query3 = 'select * from desk_replies where case_sk="%s" and date(modified_at)>="2018-08-22"'


	def main(self):
		self.cur.execute(self.query1)
		records = self.cur.fetchall()
		for rec in records:
			values_final = list(rec[1:-7])
			if values_final[-1]:
				self.cur.execute(self.query2 % values_final[-1])
				inner_records = self.cur.fetchmany()
				if inner_records:
					inner_records = list(inner_records[0][1:-3])
					try:
						spammer = json.loads(inner_records[11]).get('spammer')
						if spammer:
							inner_records[11] = "%s%s" % ('spammer:-', spammer)
					except:
						pass
				else:
					inner_records = ['' for i in range(24)]
			else:
				inner_records = ['' for i in range(24)]
			values_final.extend(inner_records)
			self.cur.execute(self.query3 % rec[0])
			reply_records = self.cur.fetchall()
			if reply_records:
				for r_record in reply_records:
					r_record = list(r_record[4:-2])
					values_dup = list(values_final)
					values_dup.extend(r_record)
					values_final_ = []
 	                       		for i in values_dup :
                            			if i==None :
                                			i = ''
                                			values_final_.append(i)
						elif not i:
							i = ''
                                                        values_final_.append(i)
                            			else :
                                 			values_final_.append(normalize(i))
					try : self.todays_excel_file.writerow(values_final_)
                                	except : print "Found error while writing into sheet"

			else:
				r_record = ['' for i in range(4)]
				values_final.extend(r_record)
                        	values_final_ = []
				for i in values_final :
                            		if i==None :
                                		i = ''
                                		values_final_.append(i)
                            		else :
                                 		values_final_.append(normalize(i))
			
				try : self.todays_excel_file.writerow(values_final_)
                        	except : print "Found error while writing into sheet"

if __name__ == '__main__':
    Deskcsv().main()
