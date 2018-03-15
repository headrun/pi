import sys
sys.path.append('/root/pi_automation/table_schemas')
from pi_db_operations import constants_dict_fb, scrapy_run_cmd_fb
#Users names and passwords

#constants_dict = {'praneeth':['praneeth@headrun.com','praneeth@123'],'bala':['balakumaridevara@gmail.com','bala123123'],'pos':['positiveintegersproject@gmail.com','integersproject'], 'venu':['venu.kallakunta', 'venu@123'],'email':['yagnasree@headrun.com','yagna^123'],'kolla':['kollaprasanthi1997@gmail.com','515515515'],'email1':['9100214671','anantha*']}
#accound_disabled = 'chakri':['aalaa.chakrapani@gmail.com','@sdfghjkL']
#'bala':['balakumaridevara@gmail.com','bala123123'],'pos':['positiveintegersproject@gmail.com','integersproject']
constants_dict = constants_dict_fb
scrapy_run_cmd = scrapy_run_cmd_fb
#scrapy_run_cmd = 'scrapy crawl facebook_crawler -a login="%s" --set  ROBOTSTXT_OBEY=0 -a mpi="%s" --set HTTPCACHE_ENABLED=0'
