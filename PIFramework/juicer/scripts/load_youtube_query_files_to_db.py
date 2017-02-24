#!/usr/bin/env python

import os
import re
import md5
import sys
import optparse
import traceback
from glob import glob
import logging, logging.handlers
from ConfigParser import SafeConfigParser
from vtv_db import get_mysql_connection
import MySQLdb

PAR_DIR = os.path.abspath(os.pardir)
OUTPUT_DIR = os.path.join(PAR_DIR, 'spiders/clips_out')
PROCESSING_QUERY_FILES_PATH = os.path.join(OUTPUT_DIR, 'processing')
PROCESSED_QUERY_FILES_PATH = os.path.join(OUTPUT_DIR, 'processed')

LOGS_DIR = os.path.join(os.getcwd(), 'logs')

def init_logger(filename, level=''):
   if not os.path.isdir(LOGS_DIR):
        os.mkdir(LOGS_DIR)

   file_name = os.path.join(LOGS_DIR, filename)
   log = logging.getLogger(file_name)
   handler = logging.handlers.RotatingFileHandler(file_name, maxBytes=524288000, backupCount=5)
   formatter = logging.Formatter('%(asctime)s.%(msecs)d: %(filename)s: %(lineno)d: %(funcName)s: %(levelname)s: %(message)s', "%Y%m%dT%H%M%S")
   handler.setFormatter(formatter)
   log.addHandler(handler)
   log.setLevel(logging.DEBUG)

   return log

log = init_logger('load_queries_to_db.log')

def move_file(source, dest=PROCESSED_QUERY_FILES_PATH):
    cmd = "mv %s %s" % (source, dest)
    os.system(cmd)
    log.info("Moved File From %s", cmd)

def queries_input_gen(queries_file):
    while 1:
        query = queries_file.readline()
        if not query:
            break

        query = query.strip()
        params = queries_file.readline().strip()

        yield query, params


def load_meta_data_files(queries_file, _setup):
    _host = "10.28.218.81"
    db_name = 'YOUTUBECLIPSDB'

    query_files = glob("%s/ytclipdetails_out*.queries" % (PROCESSING_QUERY_FILES_PATH))
    for query_file in query_files:
	load_data(query_file)


def load_data(queries_file):
    connection = MySQLdb.connect(host='10.28.218.81', user='root', db='YOUTUBECLIPSDB')
    connection.set_character_set('utf8')
    cursor = connection.cursor()

    data = queries_input_gen(open(queries_file))

    count=0

    for index, (query, params) in enumerate(data):
        count = count + 1
        params = eval(params)
        status = cursor.execute(query,params)

    connection.commit()
    cursor.close()
    connection.close()
    move_file(queries_file)


def main(options):
    load_meta_data_files(options.queries_file, options.setup)

if __name__ == '__main__':
    parser = optparse.OptionParser()

    parser.add_option('-q', '--queries-file', default=None, help='Query File Name' )
    parser.add_option('-s', '--setup', default='prod', help='Setup - prod / dev' )

    (options, args) = parser.parse_args()

    main(options)
