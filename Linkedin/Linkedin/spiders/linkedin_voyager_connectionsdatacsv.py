from linkedin_voyager_functions import *

class Liccsvfile(object):

    def __init__(self, options):
	self.dic = {"274896029surabhi-verma-42508b78": "surabhiverma1492@gmail.com", "181510280dhruv-aneja-80895450": "dhruv.aneja@positivemoves.com", "369657400anagh-sood-13496aa3" : "anaghsood@gmail.com", "210181193ifrah-matto-7754805a" : "ifrahmatto@gmail.com", "232893281neha-dutt-255bb465":"nehabdutt@gmail.com", "9219595pooja-a-mahindra-4b71073":"Pooja.mahindra@gmail.com", "76843848rahul-singh-rana-9a089921":"rahul.rana@iiml.org", "162657323satish-mudaliar-48b58246":"satishgunner@gmail.com"}
        self.modified_at       = options.modified_at
        self.excel_file_name = 'linkedinconnections_data_%s.csv'%str(datetime.datetime.now().date())
	if os.path.isfile(self.excel_file_name):
		os.system('rm %s'%self.excel_file_name)
	self.con, self.cur = get_mysql_connection(DB_HOST, 'FACEBOOK', '')
        self.selectqry = 'select profile_sk, connections_profile_url, member_id, headline, name, image_url, image_path, background_image_url from linkedin_connections where date(modified_at)>="%s"' % (self.modified_at)
        self.header_params = ['name', 'headline', 'member_id','profile_url', 'image_url', 'image_path', 'background_image', 'email_address']
        oupf = open(self.excel_file_name, 'ab+')
	self.todays_excel_file  = csv.writer(oupf)
        self.main()

    def __del__(self):
	close_mysql_connection(self.con, self.cur)

    def main(self):
            records = fetchall(self.cur, self.selectqry)
            for inde , record in enumerate(records):
            	sk, connections_profile_url, member_id, headline, name, image_url, image_path, background_image = record
		values = [name, headline, member_id, connections_profile_url, image_url, image_path, background_image, self.dic.get(sk, '')]
                values =  [normalize(i) for i in values]
		if inde == 0:
			self.todays_excel_file.writerow(self.header_params)
		self.todays_excel_file.writerow(values)
		print values

if __name__ == '__main__':
        parser = optparse.OptionParser()
        parser.add_option('-d', '--db-name', default='', help = 'db_name')
        parser.add_option('-m', '--modified_at', default = '', help = 'modified_at')
        (options, args) = parser.parse_args()
        Liccsvfile(options)
