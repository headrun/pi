#!/usr/bin/env python
import sys
from glob import glob
import MySQLdb
import os
import optparse
import sys
import json
import traceback

OUTPUT_DIR = '/root/pi_crawling/Practo/juicer/spiders'
PROCESSING_QUERY_FILES_PATH = os.path.join(OUTPUT_DIR, 'OUTPUT/load_script/processing')
PROCESSED_QUERY_FILES_PATH = os.path.join(OUTPUT_DIR, 'OUTPUT/load_script/processed')
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
    connection = MySQLdb.connect(host='localhost', user='root', passwd = 'hdrn59!',  db='PRACTO')
    connection.set_character_set('utf8')
    cursor = connection.cursor()
    #query_files = [queries_file] if queries_file else glob("%s/*_out_*.queries" % (PROCESSING_QUERY_FILES_PATH))
    query_files = [queries_file] if queries_file else glob("%s/*.queries" % (PROCESSING_QUERY_FILES_PATH))
    for query_file in query_files:
        data = queries_input_gen(open(query_file))
        count=0
        for index, (query, params) in enumerate(data):
            count = count + 1
            params = eval(params)
            try:
                    cursor.execute(query, params)
            except: import pdb;pdb.set_trace()
        move_file(query_file)
    cursor.close()
    connection.close()
def main(queries_file):
    load_data_files(options.queries_file)
if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-q', '--queries-file', default=None, help='Query File Name' )
    (options, args) = parser.parse_args()
    main(options)
