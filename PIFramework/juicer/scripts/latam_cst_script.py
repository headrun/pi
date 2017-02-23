country_ids = {1:"ARGENTINA",2:"AUSTRALIA",3:"AUSTRIA",4:"BELGIUM",5:"BRAZIL",6:"CANADA",7:"CENTRAL AMERICA",8:"CHILE",9:"CHINA",10:"COLUMBIA",11:"COSTA RICA",12:"DENMARK",13:"DOMINICAN REPUBLIC",14:"ECUADOR",15:"EL SALVADOR",16:"ENGLAND",17:"FINLAND",18:"FRANCE",19:"GAUTEMALA",20:"GERMANY",21:"GLOBAL",22:"HONDURAS",23:"HONGKONG",24:"INDIA",25:"IRELAND",26:"ITALY",27:"JAPAN",28:"MAINLAND",29:"MALAYSIA",30:"MEXICO",31:"NETHERLANDS",32:"NEW ZEALAND",33:"NICARAGUA",34:"NORWAY",35:"PANAMA",36:"PARAGUAY",37:"PERU",38:"PHILIPPINES",39:"POLAND",40:"PORTUGAL",41:"PUERTO RICO",42:"RUSSIA",43:"SCOTLAND",44:"SINGAPORE",45:"SPAIN",46:"SWEDEN",47:"SWITZERLAND",48:"TAIWAN",49:"TURKEY",50:"UAE",51:"UK",52:"URUGUAY",53:"USA",54:"VENEZUELA"}

status_ids = {1:"Done",2:"On Going",3:"Q",4:"Hold",5:"Not Taken"}

project_id = 6
db_ip = '10.28.218.81'
machine_ip = '10.28.216.44'

import MySQLdb
import commands

cur = MySQLdb.connect(host=db_ip, user = "veveo",passwd = 'veveo123', db = "LATAM_COMMONDB", charset="utf8", use_unicode=True).cursor()
insert_query = 'insert ignore into Crawler(source_id, project_id, country_id, status_id, rights_id, dri_id, \
name, reference_url, db_ip, db_name, machine_ip, is_robots, priority,created_at) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s","%s", "%s", "%s", "%s")'

f1 = open('details1.txt', 'r+')
for line in f1:
	source_name , country, source_id, status, url, project, crawlers, db_name, dri_id = line.split('#<>#')
        spiders_list = []
	try:
		country_id = [key for key, value in country_ids.items() if value == country][0]
	except:
		country_id =0
	status_id  = [key for key, value in status_ids.items() if value.lower() in status.lower()][0]
	if len(crawlers.split('<>')) >= 1 and status_id == 1:
		for crawler in crawlers.split('<>'):
			cmd = 'cd /home/veveo/LATAM_PROD/LATAM/GenFramework/juicer/spiders; grep "(JuicerSpider)" %s -a1 | grep "name"' % crawler 
			status, spider_name = commands.getstatusoutput(cmd)
			'''
			if status != 0:
				cmd = 'cd /home/veveo/LATAM_PROD/OUTBOUND_V2/juicer/spiders; grep "(JuicerSpider)" %s -a1 | grep "name"' % crawler

				print cmd
				status, spider_name = commands.getstatusoutput(cmd)
				spider_name = spider_name.replace('name', '').replace('=', '').strip().strip('"').strip("'")
				spiders_list.append(spider_name)	
			'''
			spider_name = spider_name.replace('name', '').replace('=', '').strip().strip('"').strip("'")
			spiders_list.append(spider_name)
		if spiders_list:
			for spider in spiders_list:
				if not spider: continue
				from datetime import datetime, timedelta
				import datetime

				now = datetime.datetime.now()
				values = (source_id, project_id, country_id, status_id, 0, dri_id, spider, url, db_ip, db_name, machine_ip, 0 , 0,str(now))
				cur.execute(insert_query % values)

		else:
			values = (source_id, project_id, country_id, status_id, 0, dri_id, source_name, url, db_ip, db_name, machine_ip, 0 , 0)
			cur.execute(insert_query % values)
		
		
