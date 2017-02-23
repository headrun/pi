import datetime
import os
import glob
#files = glob.glob('/home/hadrun/GenFramework/juicer/spiders/OUTPUT/crawl_out/*.queries') or glob.glob('/home/headrun/GenFramework/juicer/spiders/OUTPUT/crawl_out/*.txt')
'''for i in [datetime.datetime.now().date() -  datetime.timedelta(days=i) for i in range(4)]:
    #files = glob.glob('/home/hadrun/GenFramework/juicer/spiders/OUTPUT/crawl_out/*"%s"*')% (str(i).replace('-',''))
    print i'''
#os.system('find /home/veveo/LATAM_PROD/LATAM/GenFramework/juicer/spiders/OUTPUT/crawl_out/* -mtime +2 -exec rm {} \;')
#import pdb;pdb.set_trace()
os.chdir('/home/veveo/LATAM_PROD/LATAM/GenFramework/juicer/spiders/OUTPUT/crawl_out/')
os.system('find `pwd` -mtime +4 -exec rm -f {} \;')

