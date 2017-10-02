#!/usr/bin/env python

import sys
from glob import glob
import MySQLdb
import os
import optparse
import sys
import json
import traceback
from ConfigParser import SafeConfigParser
from insert_qry import *
_cfg = SafeConfigParser()
_cfg.read('linkedin_voyager.cfg')

OUTPUT_DIR = '/root/crawl_automation/Linkedin/Linkedin/spiders/'
PROCESSING_QUERY_FILES_PATH = os.path.join(OUTPUT_DIR, 'OUTPUT/processing')
PROCESSED_QUERY_FILES_PATH = os.path.join(OUTPUT_DIR, 'OUTPUT/processed')

def queries_input_gen(queries_file):
    while 1:
        query = queries_file.readline()
        if not query:
            break
        query = query.strip()
        params = queries_file.readline().strip()

        yield query, params

def move_file(source, dest=PROCESSED_QUERY_FILES_PATH):
    cmd = "mv %s %s" % (source, dest)
    os.system(cmd)

def load_data_files(queries_file):
    connection = MySQLdb.connect(host='localhost', user='root', passwd = 'root',  db='CRAWL_AUTOMATION')
    connection.set_character_set('utf8')
    cursor = connection.cursor()
    con1 = MySQLdb.connect(user=_cfg.get('aws', 'user'),host=_cfg.get('aws', 'host'), db=_cfg.get('aws', 'db_name'), passwd=_cfg.get('aws', 'awspasswd'))
    con1.set_character_set('utf8')
    cur1 = con1.cursor()
    #query = "INSERT INTO test_lnkd(created_dt,lnkd_url)values('2017-09-28','https://www.linkedin.com/in/aravindrajanm/')"
    #query2 = "INSERT INTO test_lnkd(created_dt,lnkd_url)values('2017-09-27','https://www.linkedin.com/in/kiranmayi-cheedella-b87699a3/')"
    #query3 = "INSERT INTO test_lnkd(created_dt,lnkd_url)values('2017-09-27','https://www.linkedin.com/in/anusha-boyina-349812140/')"
    #cur1.execute(query)
    #cur1.execute(query3)
    #cur1.execute(query2)
    import pdb;pdb.set_trace()
    query_files = [queries_file] if queries_file else glob("%s/*.queries" % (PROCESSING_QUERY_FILES_PATH))
  
    """for query_file in query_files:
        data = queries_input_gen(open(query_file))                                                                              
        count=0                                                                                                                 
        for index, (query, params) in enumerate(data):                                                                          
            count = count + 1
            params = eval(params)
            try : 
                if 'linkedin_aws_csv1' in query_file :                                                                                                          	cur1.execute(query, params)
                elif 'linkedin_pi_csv1' in query_file :                                                                                                                cursor.execute(query, params)                                                                               
                else : print query

            except: print params[0] 
                                                                                                                                
        move_file(query_file)"""                                                                                                   
    cursor.close()                                                                                                              
    connection.close()                                                                                                          
                                                                                                                                
def main(queries_file):                                                                                                         
    load_data_files(options.queries_file)                                                                                       
                                                                                                                                
if __name__ == '__main__':                                                                                                      
    parser = optparse.OptionParser()                                                                                            
    parser.add_option('-q', '--queries-file', default=None, help='Query File Name' )                                            
    (options, args) = parser.parse_args()                                                                                       
    main(options)  
