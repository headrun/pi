import hashlib
import csv
import datetime
import datetime
import MySQLdb
import time
import scrapy
import json
import os
from datetime import timedelta

class Openweatherscript(object):

    def __init__(self, *args, **kwargs):
        super(Openweatherscript, self).__init__(*args, **kwargs)
        self.con = MySQLdb.connect(db='urlqueue_dev',
        user='root', passwd='root',
        charset="utf8", host='localhost', use_unicode=True)
        self.cur = self.con.cursor()
        self.cur = self.con.cursor()
        self.update_qry = 'update openweather_crawl set crawl_status=0'

    def run_main(self):
        self.cur.execute(self.update_qry)
        self.con.commit()
        

 
        
if __name__ == '__main__':
     Openweatherscript().run_main()

        








