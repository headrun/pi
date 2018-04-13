import re
import hashlib
import traceback
import os
import json
import scrapy
import hashlib
import requests
import sys
import time
import timeit
import random
import codecs
import logging.handlers
import optparse
import datetime
import csv
import collections
import calendar
import string
import logging
import pymysql
from operator import itemgetter
from itertools import chain
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

DB_PASSWD = 'root'
DB_HOST = 'localhost'
DB_NAME_REQ = 'FACEBOOK'#'PI_AUTOMATION'
REQ_DB_NAME = 'FACEBOOK'#'PI_AUTOMATION'
LINKEDIN_DB = 'FACEBOOK'#'PI_AUTOMATION'
DB_USERNAME = 'root'
MYSQL_CONNECT_TIMEOUT_VALUE = 30
BATCH_SIZE = 2000

def get_mysql_connection(server, db_name, cursorclass=""):
    try:
        """from MySQLdb.cursors import Cursor, DictCursor, SSCursor, SSDictCursor
        cursor_dict = {'dict': DictCursor, 'ssdict': SSDictCursor, 'ss': SSCursor}
        cursor_class = cursor_dict.get(cursorclass, Cursor)

        conn = MySQLdb.connect(
                    host=server, user=DB_USERNAME, passwd=DB_PASSWD, db=db_name,
                    connect_timeout=MYSQL_CONNECT_TIMEOUT_VALUE, cursorclass=cursor_class,
                    charset="utf8", use_unicode=True
        )
        if db_name: conn.autocommit(True)
        cursor = conn.cursor()"""
        conn = pymysql.connect(db = DB_NAME_REQ, host = server,
                charset="utf8mb4", user=DB_USERNAME, password=DB_PASSWD)
        cursor = conn.cursor()

    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception:
        conn, cursor = None, None

    return conn, cursor


def get_request_url(response):
    if response.meta.get('redirect_urls', []):
        resp_url = response.meta.get('redirect_urls')[0]
    else:
        resp_url = response.url

    return resp_url


def make_dir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def close_mysql_connection(conn, cursor):
    if cursor: cursor.close()
    if conn: conn.close()



def init_logger(filename, level=''):
        log_dir = os.path.join(os.getcwd(), 'logs')
        if not os.path.isdir(log_dir):
            os.mkdir(log_dir)
        file_name = os.path.join(log_dir, filename)
        log = logging.getLogger(file_name)
        handler = logging.handlers.RotatingFileHandler(
        file_name, maxBytes=524288000, backupCount=5)
        formatter = logging.Formatter(
        '%(asctime)s.%(msecs)d: %(filename)s: %(lineno)d: \
        %(funcName)s: %(levelname)s: %(message)s', "%Y%m%dT%H%M%S")
        handler.setFormatter(formatter)
        log.addHandler(handler)
        log.setLevel(logging.DEBUG)
        return log


def execute_query(cursor, query, values=''):
    try:
        if values:
            cursor.execute(query, values)

        try: cursor.execute(query)
        except Exception as e: print(e)
    except Exception as e:
        print(e)

def fetchone(cursor, query):
    execute_query(cursor, query)
    recs = cursor.fetchone()

    return recs[0]

def fetchmany(cursor,query):
    execute_query(cursor, query)
    recs = cursor.fetchmany(BATCH_SIZE)
    return recs


def fetchall(cursor, query):
    execute_query(cursor, query)
    recs = cursor.fetchall()

    return recs


def textify(nodes, sep=' '):
    if not isinstance(nodes, (list, tuple)):
        nodes = [nodes]

    def _t(x):
        if isinstance(x, (str, unicode)):
        #if isinstance(x, (bytes, str)):
            return [x]

        if hasattr(x, 'xmlNode'):
            if not x.xmlNode.get_type() == 'element':
                return [x.extract()]
        else:
            if isinstance(x.root, (str, unicode)):
            #if isinstance(x.root, (bytes, str)):
                return [x.root]

        return (n.extract() for n in x.select('.//text()'))

    nodes = chain(*(_t(node) for node in nodes))
    nodes = (node.strip() for node in nodes if node.strip())

    return sep.join(nodes)


def xcode(text, encoding='utf8', mode='strict'):
    return text.encode(encoding, mode) if isinstance(text, unicode) else text 
    #return text.encode(encoding, mode) if isinstance(text, str) else text

def compact(text, level=0):
    text = text.decode('utf-8')
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
    value = re.sub("<br>",'',value)

    return value

def normalize(text):
    return clean(compact(xcode(text)))

def extract(sel, xpath, sep=' '):
    return clean(compact(textify(sel.xpath(xpath).extract(), sep)))

def extract_data(data, path, delem=''):
   return delem.join(i.strip() for i in data.xpath(path).extract() if i).strip()

def extract_list_data(data, path):
   return data.xpath(path).extract()

def get_nodes(data, path):
   return data.xpath(path)

def md5(x):
    return hashlib.md5(xcode(x)).hexdigest()

