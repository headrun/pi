from generic_functions import *
import glob
import openpyxl as px

class Piparsing(object):

	def parameters(self):
		con, cur = get_mysql_connection(DB_HOST, DB_NAME_REQ, '')
                current_path = os.path.dirname(os.path.abspath(__file__))
                social_processing_path = os.path.join(
		current_path, 'excelfiles')
		return con, cur, current_path, social_processing_path

	def main(self):
		con, cur, current_path, social_processing_path = self.parameters()
		files_list = glob.glob(social_processing_path+'/*.xlsx')
	        if files_list:
			for _file in files_list:
				ws_ = px.load_workbook(_file, use_iterators=True)
				sheet_list = ws_.get_sheet_names()
				for xl_ in sheet_list:
					sheet_ = ws_.get_sheet_by_name(name=xl_)
					row_check = 0
					email_address, linkedin_profile, ida,\
					firstname, lastname, key_,\
					twitter_profile, facebook_profile = ['']*8
					for row in sheet_.iter_rows():
						if row_check > 0:
							row_check += 1
							continue
						counter = 0
						for i in row:
							if not i.value: continue
							lower_head = i.value.lower()
							if 'key' in lower_head:
								key_ = counter
							elif 'linkedin'  in lower_head:
								linkedin_profile = counter
							elif 'email' in lower_head:
								email_address = counter
							elif 'id' in lower_head and 'linkedin' not in lower_head:
								ida = counter
							elif 'first name' in lower_head:
								firstname = counter
							elif 'last name' in lower_head:
								lastname = counter
							elif 'twitter' in lower_head:
								twitter_profile = counter
							elif 'facebook' in lower_head:
								facebook_profile = counter
							counter += 1
						break
					m = 0
					final_indents = []
					_indents = {}
					for row in sheet_.iter_rows():
						temp_rows = []
						for i in row:
							temp_rows.append(i.value)
						final_indents.append(temp_rows)
					empty_dic = {}
					for row in final_indents:
						row_check = range(len(row))
						meta_date_from_browse, sk = {}, ''
						if email_address != '' and \
						email_address in row_check:
							email_addressf = normalize(
							str(row[email_address].encode('utf-8')))
							meta_date_from_browse.update(
						{"email_address": email_addressf.strip('"')})
						if ida != '' and ida in row_check:
							idaf = normalize(str(row[ida]))
							meta_date_from_browse.update({"id":idaf})
						if firstname != '' and firstname in row_check:
							firstnamef = normalize(str(row[firstname].encode('utf-8')))
							meta_date_from_browse.update({"firstname":firstnamef})
						if lastname != '' and lastname in row_check:
							lastnamef = normalize(str(row[lastnamef].encode('utf-8')))
							meta_date_from_browse.update({"lastname":lastnamef})
						if key_ != '' and key_ in row_check:
							key_f = normalize(str(row[key_].encode('utf-8')))
							meta_date_from_browse.update({"keys":key_f})
						#print row
						#print meta_date_from_browse
						#print '>>>>>>>>'
                                                if linkedin_profile != '' and linkedin_profile in row_check:
                                                        linkedin_profilef = normalize(str(row[linkedin_profile].encode('utf-8')))
                                                        meta_date_from_browse.update({"linkedin_url":linkedin_profilef})
                                                        sk = md5(normalize(linkedin_profilef))
                                                        linkedin_profilef = self.linkedin_pub_url(linkedin_profilef)
							if linkedin_profilef and 'linkedin.com' in linkedin_profilef:
								linkedin_profilef = MySQLdb.escape_string(linkedin_profilef)
								values = ('linkedin_crawl', sk, linkedin_profilef, 'linkedin', 0,MySQLdb.escape_string(json.dumps(meta_date_from_browse)), MySQLdb.escape_string(json.dumps(meta_date_from_browse)))
								execute_query(cur, insert_script_query%values)
						if twitter_profile != '' and twitter_profile in row_check:
							twitter_profilef = MySQLdb.escape_string(twitter_profilef)
							twitter_profilef = normalize(str(row[twitter_profile].encode('utf-8')))
							sk = twitter_profilef.split('/')[-1].strip()
							met_browse = meta_date_from_browse.get('email_address', '')
							if twitter_profilef and 'twitter.com' in twitter_profilef:
								values = ('twitter_crawl', sk, twitter_profilef, 'twitter', 0, MySQLdb.escape_string(json.dumps(met_browse)), MySQLdb.escape_string(json.dumps(met_browse)))
								execute_query(cur, insert_script_query%values)
						if facebook_profile != '' and facebook_profile in row_check:
							facebook_profilef = normalize(str(row[facebook_profile].encode('utf-8')))
							meta_date_from_browse.update({"mbasic_url":facebook_profilef.replace('www', 'mbasic')})
							sk = md5(normalize(facebook_profilef))
							if facebook_profilef and 'facebook.com' in facebook_profilef:
								facebook_profilef = MySQLdb.escape_string(facebook_profilef)
								values = ('facebook_crawl', sk, facebook_profilef, 'facebook', 0, MySQLdb.escape_string(json.dumps(meta_date_from_browse)), MySQLdb.escape_string(json.dumps(meta_date_from_browse)))
								execute_query(cur, insert_script_query%values)
				#cmd = ('"' + _file + '"')
				os.remove(_file)
		close_mysql_connection(con, cur)



	def linkedin_pub_url(self, linkedin_profilef):
		if 'http:' in linkedin_profilef:
			linkedin_profilef = linkedin_profilef.replace('http:', 'https:')
	        if 'id.www' in linkedin_profilef:
        		linkedin_profilef = linkedin_profilef.replace('id.www', 'https://www')
	        if 'www.linkedin.com' and 'https:' not in linkedin_profilef:
        		linkedin_profilef = linkedin_profilef.replace('www.', 'https://www')
        	if linkedin_profilef.startswith('linkedin.com'):
            		linkedin_profilef = linkedin_profilef.replace('linkedin.com', 'https://www.linkedin.com')
	        if 'https:' not in linkedin_profilef:
        		linkedin_profilef = re.sub('(\D+)\.linkedin.com', 'https://www.linkedin.com', linkedin_profilef) 
	        linkedin_profilef = re.sub('https://(.*?).linkedin.com/', 'https://www.linkedin.com/', linkedin_profilef)
        	if linkedin_profilef.endswith('/en') or linkedin_profilef.endswith('/fr'):
            		linkedin_profilef = linkedin_profilef[:-3]
        	linkedin_profilef = linkedin_profilef.strip('"').strip().strip("'").strip().strip('/').strip()
        	if not linkedin_profilef.startswith('https://www.linkedin.com'):
            		linkedin_profilef = ''.join(re.findall('.*(https://.*)', linkedin_profilef))
        	if '/pub/' in linkedin_profilef:
            		cv = ''.join(filter(None, re.split('https://www.linkedin.com/pub/.*?/(.*)', linkedin_profilef))).split('/')[::-1]
            		cv[0] = cv[0].zfill(3)
            		cv[1] = cv[1].zfill(3)
            		if cv[-1] == '0': del cv[-1]
            		linkedin_profilef = ('%s%s%s%s' % ('https://www.linkedin.com/in/', ''.join(re.findall('https://www.linkedin.com/pub/(.*?)/.*', linkedin_profilef)), '-', ''.join(cv)))
        	return linkedin_profilef

						
if __name__ == '__main__':
    Piparsing().main()
