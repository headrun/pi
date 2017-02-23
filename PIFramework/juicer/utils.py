# Stdlib imports
import os
import re
import sys
import json
import time
import timeit
import codecs
import random
import string
import hashlib
import logging
import inspect
import MySQLdb
import datetime
import asyncore
import urlparse
import traceback
import logging.handlers
import tornado.httpclient as HT
from itertools import chain
from urlparse import urljoin
from dateutil.parser import *
from collections import defaultdict
from dateutil.relativedelta import *
from ConfigParser import SafeConfigParser

# Scrapy related imports
from scrapy import signals
from scrapy.conf import settings
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.xlib.pydispatch import dispatcher
from scrapy.http import Request as ScrapyHTTPRequest, TextResponse

from scripts.robots_txt_checker import get_crawl_access
from scripts.crawl_table_queries import CRAWL_TABLE_SELECT_QUERY, CRAWL_TABLE_CREATE_QUERY
from scripts.crawl_table_queries import SECTIONS_TABLE_CREATE_QUERY

BATCH_SIZE = 100
YIELD_SIZE = 500
MYSQL_CONNECT_TIMEOUT_VALUE = 30
DB_HOST = settings['DB_HOST']
DB_UNAME = settings['DB_USERNAME']
DB_PASSWD = settings['DB_PASSWORD']
URLQ_DB_NAME = settings['URLQ_DATABASE_NAME']
LOGS_DIR = settings['LOGS_DIR']
PROXY_PATTERN = 'http://%s:%s'

OUTPUT_DIR = os.path.join(os.getcwd(), 'OUTPUT')
JSON_FILES_DIR = os.path.join(OUTPUT_DIR, 'ott')
QUERY_FILES_DIR = os.path.join(OUTPUT_DIR, 'crawl_out')
QUERY_FILES_PROCESSING_DIR = os.path.join(OUTPUT_DIR, 'processing')
JSON_FILES_PROCESSED_DIR = os.path.join(OUTPUT_DIR, 'ott_processed')

class JuicerSpider(Spider):

        def __init__(self, name=None, **kwargs):
            self.crawl_type = kwargs.get('crawl_type', 'keepup')
            self.related_type = kwargs.get('related_type', '')
            self.content_type = kwargs.get('content_type', '')
            self.request_headers = {}
            self.allow_duplicate_urls = False
            self.is_ott = False
            self.limit = kwargs.get('limit', 0) or getattr(self.__class__, 'limit', 1000)

            self.create_logger_obj()
            self.create_default_dirs()
            self.initialize_default_variables()
            self.crawl_table_name, self.sections_table_name = self.ensure_tables()
            self.robots, self.proxy_ip, self.proxy_port = self.get_source_details()

            self.proxy = None
            if self.proxy_ip:
                self.proxy = PROXY_PATTERN % (self.proxy_ip, self.proxy_port)
            #settings.overrides['PROXIES_LIST'] = [self.proxy]

            ROBOTSTXT_DISALLOW_SOURCES_LIST = parse_genframework_config_file(section='ROBOTSTXT_DISABLED_SOURCES', sub_section='sources')
            if self.name.split('_')[0] in ROBOTSTXT_DISALLOW_SOURCES_LIST:
                settings.overrides['ROBOTSTXT_OBEY'] = False

            self._start_urls = None
            if hasattr(self.__class__, 'start_urls'):
                self._start_urls = getattr(self.__class__, 'start_urls')
                try:
                    delattr(self.__class__, 'start_urls')
                except AttributeError:
                    pass

            dispatcher.connect(self._spider_closed, signals.spider_closed)
            super(JuicerSpider, self).__init__(name, **kwargs)

        def create_logger_obj(self):
            cur_dt = str(datetime.datetime.now().date())
            make_dir(LOGS_DIR)
            self.log_file_name = "spider_%s.log" % (cur_dt)
            self.log = initialize_logger(os.path.join(LOGS_DIR, self.log_file_name))

        def get_urlQ_cursor(self):
            if self.urlQ_cursor: return self.urlQ_cursor

            self.urlQ_conn, self.urlQ_cursor = get_mysql_connection(db_name=URLQ_DB_NAME)

            return self.urlQ_cursor

        def close_conn(self):
            self.log.info("Close MySQL Cursor Function Called")
            close_mysql_connection(self.urlQ_conn, self.urlQ_cursor)
            self.log.info("Successfully Closed MySQL Connection")

        def create_default_dirs(self):
            DEFAULT_DIRS = [
                'crawl_out', 'processing', 'processed', 'un-processed', 'invalid_jsons', 'ott_processed', 'ott'
            ]
            make_dir_list(DEFAULT_DIRS)

        def initialize_default_variables(self):
            self._close_called = False
            self._sks = defaultdict(set)
            self.location_file = self.lineup_file = self.richmedia_file = self.relatedsellers_file= None
            self.source = self.json_file = self.bestsellers_file = self.products_file = self.customerreviews_file=  None
            self.custom_query_file  = self.created_file= None

            self.urlQ_cursor = None
            self.got_page_sks_len = 0
            self.crawl_vals_set = set()
            self.section_vals_set = set()

        def get_source_details(self):
            query = 'select is_robots, proxy_ip, proxy_port from source \
                    where source_id = %s'
            self.get_urlQ_cursor().execute(query, (self.name.split('_')[0], ))
            entry = self.get_urlQ_cursor().fetchone()
            if not entry:
                return None, None, None
            return entry[0], entry[1], entry[2]

        def ensure_tables(self):
            source = self.name.split('_')[0]
            crawl_table_name = "%s_crawl" % (source)
            sections_table_name = "%s_sections" % (source)

            SHOW_QUERY = 'SHOW TABLES LIKE "%s_%%";' % (source)
            self.get_urlQ_cursor().execute(SHOW_QUERY)
            if self.get_urlQ_cursor().rowcount > 0:
                self.log.info("Tables: %s - %s Already Exist.", crawl_table_name, sections_table_name)
                return crawl_table_name, sections_table_name

            self.get_urlQ_cursor().execute(CRAWL_TABLE_CREATE_QUERY.replace('#CRAWL-TABLE#', crawl_table_name))
            self.get_urlQ_cursor().execute(SECTIONS_TABLE_CREATE_QUERY.replace('#SECTION-TABLE#', sections_table_name))
            self.log.info("Tables: %s - %s Newly Created.", crawl_table_name, sections_table_name)

            return crawl_table_name, sections_table_name

        def get_recs_by_batch_wise(self, batch_size=BATCH_SIZE):
            while True:
                recs = self.get_urlQ_cursor().fetchmany(batch_size)
                if not recs: break
                for rec in recs:
                    yield rec

        def check_is_url_crawlable(self, url):
            if not settings['ROBOTSTXT_OBEY'] or not self.robots:
                return True
            crawl_status, robotsurl = get_crawl_access(url)
            self.log.info("Checked Url: %s - Is Crawlable: %s", url, crawl_status)

            return crawl_status

        def get_terminal_requests(self, content_type, requests):
            sel_query = CRAWL_TABLE_SELECT_QUERY % (self.crawl_table_name, content_type, self.limit)
            execute_query(self.get_urlQ_cursor(), sel_query)

            selected_sks = set()
            for sk, url, meta_data in self.get_recs_by_batch_wise():
                if not self.check_is_url_crawlable(url): continue
                if not sk.strip(): continue
                try:
                    if meta_data: meta_data = eval(meta_data)
                    req_meta = {'data': meta_data, 'sk': sk}
                    req = Request(
                            url, self.parse, None, meta=req_meta,
                            headers=self.request_headers,
                            dont_filter=self.allow_duplicate_urls,
                    )
                    requests.extend(req)
                    selected_sks.add(sk)
                except:
                    traceback.print_exc()
                    self.log.error("Error: %s", traceback.format_exc())

            self.log.info("Total Sks Picked From Crawl Tables: %s", len(selected_sks))
            if len(selected_sks) > 0:
                self.update_selected_sks_with_nine_status(selected_sks, content_type)

            return requests

        def get_start_urls_requests(self, start_urls, requests):
            if not isinstance(start_urls, (tuple, list)) and not inspect.isgenerator(start_urls):
                start_urls = [start_urls]

            for start_url in start_urls:
                if not self.check_is_url_crawlable(start_url): continue

                if isinstance(start_url, ScrapyHTTPRequest):
                    requests.append(start_url)
                else:
                    req_meta = {'data': None}
                    req = Request(
                            start_url, self.parse, None, meta=req_meta,
                            headers=self.request_headers,
                            dont_filter=self.allow_duplicate_urls,
                    )
                    requests.extend(req)

            return requests

        def start_requests(self):
            start_urls = self._start_urls or getattr(self, 'start_urls', None)
            source, content_type, crawl_type = self.get_source_content_and_crawl_type(self.name)

            requests = []
            if crawl_type == "terminal":
                requests = self.get_terminal_requests(content_type, requests)
            elif start_urls:
                requests = self.get_start_urls_requests(start_urls, requests)

            return requests

        def get_source_content_and_crawl_type(self, spider_name):
            content_type = ''

            if "_browse" in spider_name:
                source, crawl_type = self.name.split('_')[0], 'browse'
            else:
                source, content_type, crawl_type = self.name.split('_')

            return source.strip(), content_type.strip(), crawl_type.strip()

        def update_selected_sks_with_nine_status(self, selected_sks, content_type):
            self.log.info("In Update Selected Sks With Nine Status Func Called")
            conn, cursor = get_mysql_connection()

            sks = ', '.join(['"%s"' % sk for sk in selected_sks])
            delete_query = 'DELETE FROM ' + self.crawl_table_name + ' WHERE crawl_status=9 AND content_type="%s" AND sk in (%s);'
            self.get_urlQ_cursor().execute(delete_query  % (content_type, sks))

            update_query = 'UPDATE ' + self.crawl_table_name + ' SET crawl_status=9, modified_at=NOW() WHERE content_type="%s"'
            update_query += ' AND crawl_status=0 AND sk="%s";'

            for selected_sk in selected_sks:
                try:
                    self.get_urlQ_cursor().execute(update_query % (content_type, selected_sk))
                except MySQLdb.IntegrityError:
                    self.log.info("IntegrityError: Unable to update the status for this Sk: %s", selected_sk)
                except Exception:
                    self.log.error("Error Query: %s - Error: %s", update_query, traceback.format_exc())

            del(selected_sks)

        def update_urlqueue_with_resp_status(self):
            self.log.info("In Update Url Queue With Respective Status")
            source, content_type, crawl_type = self.name.split('_')
            self.log.info("Source: %s - Content Type: %s - Type: %s", source, content_type, crawl_type)

            delete_query = 'DELETE FROM ' + self.crawl_table_name + ' WHERE crawl_status=%s AND content_type="%s" AND sk in (%s);'
            update_query = 'UPDATE ' + self.crawl_table_name + ' SET crawl_status=%s, modified_at=NOW() WHERE crawl_status=9 AND'
            update_query += ' content_type="%s" AND sk="%s";'

            for k, vals in self._sks.iteritems():
                self.log.info("Source: %s - Content Type: %s - Status: %s - Sks Length: %s", source, content_type, k, len(vals))
                sks = ", ".join(['"%s"' % val for val in vals])
                self.get_urlQ_cursor().execute(delete_query % (k, content_type, sks))

                for sk in vals:
                    try:
                        self.get_urlQ_cursor().execute(update_query % (k, content_type, sk))
                    except MySQLdb.IntegrityError:
                        self.log.error("IntegrityError: Unable to update Status=1 for given Sk: %s", sk)
                    except:
                        self.log.error("Error Query: %s - Error: %s", update_query, traceback.format_exc())

        def reset_cnt_and_crawl_sec_vals(self):
            self.crawl_vals_set = set()
            self.section_vals_set = set()

        def insert_crawl_tables_data(self):
            CRAWL_TABLE_QUERY = 'INSERT INTO %s_crawl' % self.source + ' (sk, url, meta_data, crawl_type, content_type, '
            CRAWL_TABLE_QUERY += 'crawl_status, created_at, modified_at) VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW())'
            CRAWL_TABLE_QUERY += ' ON DUPLICATE KEY UPDATE url=%s, meta_data=%s, crawl_type=%s, crawl_status=%s, modified_at=NOW();'

            SECTIONS_TABLE_QUERY = 'INSERT INTO %s_sections' % self.source + ' (sk, section, content_type, created_at) '
            SECTIONS_TABLE_QUERY += 'VALUES (%s, %s, %s, NOW()) ON DUPLICATE KEY UPDATE content_type=%s, modified_at=NOW();'

            self.log.info("Source: %s - Crawl Sks Length: %s - Section Sks Length: %s", self.source, len(self.crawl_vals_set), len(self.section_vals_set))
            if len(self.crawl_vals_set) > 0:
                for setc in self.crawl_vals_set:
                    self.get_urlQ_cursor().execute(CRAWL_TABLE_QUERY,setc)
                #self.get_urlQ_cursor().executemany(CRAWL_TABLE_QUERY, self.crawl_vals_set)
                #self.get_urlQ_cursor().executemany(SECTIONS_TABLE_QUERY, self.section_vals_set)

        def get_page(self, spider_name, url, sk, meta_data=None, section='', related_type=''):
            self.source, content_type, crawl_type = spider_name.split('_')
            if len(self.crawl_vals_set) == YIELD_SIZE:
                self.insert_crawl_tables_data()
                self.reset_cnt_and_crawl_sec_vals()

            meta_data = repr(meta_data) if meta_data else ''
            related_type = related_type if related_type else ''
            self.crawl_vals_set.add((
                sk, url, meta_data, self.crawl_type, content_type, 0,
                url, meta_data, self.crawl_type, 0
            ))
            self.section_vals_set.add((sk, section, content_type, content_type))

        def got_page(self, sk, got_pageval=1):
            if not sk: raise

            if self.got_page_sks_len == 100:
                self.update_urlqueue_with_resp_status()
                self._sks = defaultdict(set)
                self.got_page_sks_len = 0

            self._sks[got_pageval].add(sk)
            self.got_page_sks_len += 1

        def get_relatedsellers_file(self):
            if self.relatedsellers_file: return self.relatedsellers_file

            relatedsellers_queries_filename = os.path.join(QUERY_FILES_DIR, "%s_relatedsellers_%s.queries" % (self.name, get_current_ts_with_ms()))
            self.relatedsellers_file = open(relatedsellers_queries_filename, 'w')
            return self.relatedsellers_file



        def get_bestsellers_file(self):
            if self.bestsellers_file: return self.bestsellers_file

            bestsellers_queries_filename = os.path.join(QUERY_FILES_DIR, "%s_bestsellers_%s.queries" % (self.name, get_current_ts_with_ms()))
            self.bestsellers_file = open(bestsellers_queries_filename, 'w')
            return self.bestsellers_file

        def get_richmedia_file(self):
            if self.richmedia_file: return self.richmedia_file
            richmedia_queries_filename = os.path.join(QUERY_FILES_DIR, "%s_richmedia_%s.queries" % (self.name, get_current_ts_with_ms()))
            self.richmedia_file = open(richmedia_queries_filename, 'w')
            return self.richmedia_file


        def get_created_file(self):
            if self.created_file: return self.created_file

            created_queries_filename=os.path.join(QUERY_FILES_DIR, "%s_created_%s.created" % (self.name, get_current_ts_with_ms()))
            self.created_file = open(created_queries_filename, 'w')

            return self.created_file


        def get_products_file(self):
            if self.products_file: return self.products_file

            products_queries_filename = os.path.join(QUERY_FILES_DIR, "%s_products_%s.queries" % (self.name, get_current_ts_with_ms()))
            self.products_file = open(products_queries_filename, 'w')

            return self.products_file


        def get_json_file(self):
            if self.json_file: return self.json_file

            json_filename = os.path.join(JSON_FILES_DIR, "crawl_%s_%s.txt" % (self.name.split('_', 1)[0], get_current_ts_with_ms()))
            self.json_file = open(json_filename, 'w')

            return self.json_file


        def get_custom_query_file(self):
            if self.custom_query_file: return self.custom_query_file

            custom_query_filename = os.path.join(QUERY_FILES_DIR, "%s_queries_%s.custom" % (self.name.split('_', 1)[0], get_current_ts_with_ms()))
            self.custom_query_file = open(custom_query_filename, 'w')

            return self.custom_query_file


        def get_customerreviews_file(self):
            if self.customerreviews_file: return self.customerreviews_file

            customerreviews_queries_filename = os.path.join(QUERY_FILES_DIR, "%s_customerreviews_%s.queries" % (self.name, get_current_ts_with_ms()))
            self.customerreviews_file = open(customerreviews_queries_filename, 'w')

            return self.customerreviews_file

        def move_json_file_to_ott_processed_dir(self):
            if self.json_file:
                self.json_file.flush()
                self.json_file.close()
                move_file(self.json_file.name, JSON_FILES_PROCESSED_DIR)

        def close_all_opened_query_files(self):
            files_list = [
                self.bestsellers_file , self.products_file , self.customerreviews_file, self.created_file, self.richmedia_file, self.relatedsellers_file
            ]
            for f in files_list:
                if not isinstance(f, file): continue
                f.flush()
                f.close()
                move_file(f.name, QUERY_FILES_PROCESSING_DIR)

        def close_all_opened_files(self):
            if self.json_file:
                self.move_json_file_to_ott_processed_dir()
            # Call Close Open Files Function
            self.close_all_opened_query_files()

        def _spider_closed(self, spider, reason):
            if spider.name != self.name: return
            if self.crawl_vals_set: self.insert_crawl_tables_data()

            if '_browse' not in self.name and len(self._sks) > 0:
                self.update_urlqueue_with_resp_status()
            self.close_all_opened_files()

            self.close_conn()
            self.initialize_default_variables()
            remove_logger_handler(self.log, os.path.join(LOGS_DIR, self.log_file_name))

        def spider_closed(self, spider, reason):
            pass


class MyCounter:

    def __init__(self):
        self.counter = 0

    def increase_counter_by_1(self):
        self.counter += 1

    def reset_counter_value(self):
        self.counter = 0


class SpiderMiddleware(object):

    def process_spider_output(self, response, result, spider):
        if inspect.isgenerator(result):
            result = list(result)
            _result = []
            for r in result:
                if isinstance(r, (list, tuple)):
                    _result.extend(r)
                else:
                    _result.append(r)
            result = _result

        return result


class RandomUserAgentMiddleware(object):

    def process_request(self, request, spider):
        ua = random.choice(settings['USER_AGENT_LIST'])
        if ua:
            request.headers.setdefault('User-Agent', ua)


class _Selector:

    def select_urls(self, xpaths, response=None):
        if not isinstance(xpaths, (list, tuple)):
            xpaths = [xpaths]

        return self._get_urls(response, xpaths)

    def _get_urls(self, response, xpaths):
        urls = [self.select(xpath) for xpath in xpaths]
        urls = list(chain(*urls))
        urls = [textify(u) for u in urls]
        if response:
            urls = [urljoin(response.url, u) for u in urls]
        return urls


class HTML(Selector, _Selector):
    pass


class XML(Selector, _Selector):
    pass


def Request(url, callback=None, response=None, **kwargs):
    kwargs['callback'] = callback
    kwargs['meta'] = kwargs.get('meta', {})
    if kwargs.has_key('headers') and not kwargs['headers']:
        kwargs.pop('headers', None)

    if kwargs.has_key('dont_filter') and not kwargs['dont_filter']:
        kwargs.pop('dont_filter', None)

    if settings['PROXIES_LIST']:
        kwargs['meta']['proxy'] = random.choice(settings['PROXIES_LIST'])


    urls = url if isinstance(url, (tuple, list)) else [url]

    do_random_scheduling = settings.get('RANDOM_SCHEDULING', True)
    response_url = '' if response is None else response.url

    out = []
    for url in urls:
        if not isinstance(url, (str, unicode)):
            url = url.extract()

        out.append(urlparse.urljoin(response_url, url))

    if do_random_scheduling and 'priority' not in kwargs:
        kwargs['priority'] = 1


    return [ScrapyHTTPRequest(u, **kwargs) for u in out]

def get_ts_with_seconds():
    ts = datetime.datetime.utcnow()
    st = ts.strftime('%Y-%m-%d %H:%M:%S') + 'Z'
    return st


def get_request_url(response):
    if response.meta.get('redirect_urls', []):
        resp_url = response.meta.get('redirect_urls')[0]
    else:
        resp_url = response.url

    return resp_url

def get_mysql_connection(server=DB_HOST, db_name=URLQ_DB_NAME, cursorclass=""):
    try:
        from MySQLdb.cursors import Cursor, DictCursor, SSCursor, SSDictCursor
        cursor_dict = {'dict': DictCursor, 'ssdict': SSDictCursor, 'ss': SSCursor}
        cursor_class = cursor_dict.get(cursorclass, Cursor)

        conn = MySQLdb.connect(
                    host=server, user=DB_UNAME, passwd=DB_PASSWD, db=db_name,
                    connect_timeout=MYSQL_CONNECT_TIMEOUT_VALUE, cursorclass=cursor_class,
                    charset="utf8", use_unicode=True
        )
        if db_name: conn.autocommit(True)
        cursor = conn.cursor()

    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception:
        conn, cursor = None, None

    return conn, cursor

def execute_query(cursor, query, values=''):
    try:
        if values:
            cursor.execute(query, values)

        cursor.execute(query)
    except:
        traceback.print_exc()

def fetchone(cursor, query):
    execute_query(cursor, query)
    recs = cursor.fetchone()

    return recs[0]

def fetchall(cursor, query):
    execute_query(cursor, query)
    recs = cursor.fetchall()

    return recs

def close_mysql_connection(conn, cursor):
    if cursor: cursor.close()
    if conn: conn.close()

def get_current_ts_with_ms():
    dt = datetime.datetime.now().strftime("%Y%m%dT%H%M%S%f")

    return dt

def make_dir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

def make_dir_list(dir_list, par_dir=OUTPUT_DIR):
    make_dir(par_dir)

    for dir_name in dir_list:
        make_dir(os.path.join(par_dir, dir_name))

def copy_file(source, dest):
    cmd = "cp %s %s" % (source, dest)
    os.system(cmd)

def move_file(source, dest):
    cmd = "mv %s %s" % (source, dest)
    os.system(cmd)

def get_compact_traceback(e=''):
    except_list = [asyncore.compact_traceback()]
    return "Error: %s Traceback: %s" % (str(e), str(except_list))

def set_logger_log_level(logger, log_level_list):
    if not log_level_list:
        logger.setLevel(logging.INFO)

    log_str = string.join(log_level_list, ":")

    if log_str.find("DEBUG_") != -1:
        logger.setLevel(logging.DEBUG)
        return

    if "INFO" in log_level_list:
        logger.setLevel(logging.INFO)

    return

def add_logger_handler(logger, file_name, log_level_list=[]):
    success_cnt, handler = 3, None

    for i in xrange(success_cnt):
        try:
            handler = logging.FileHandler(file_name)
            break
        except (KeyboardInterrupt, SystemExit):
            raise
        except: pass

    if not handler: return

    formatter = logging.Formatter('%(asctime)s.%(msecs)d: %(filename)s: %(lineno)d: %(funcName)s: %(levelname)s: %(message)s', "%Y%m%d%H%M%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    set_logger_log_level(logger, log_level_list)

    if handler.stream:
        set_close_on_exec(handler.stream)

def remove_logger_handler(logger, file_name='', log_level_list=[]):
    for handler in logger.handlers:
        if handler.name == file_name:
            handler.close()
            logger.removeHandler(handler)

def initialize_logger(file_name, log_level_list=[]):
    logger = logging.getLogger()
    try:
        add_logger_handler(logger, file_name, log_level_list)
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception as e:
        e = sys.exc_info()[2]
        time_str = time.strftime("%Y%m%dT%H%M%S", time.localtime())
        exception_str = "%s: %s: Exception: %s" % (time_str, sys.argv, get_compact_traceback(e))
        #print exception_str

    return logger

def set_close_on_exec(fd):
    import fcntl
    st = fcntl.fcntl(fd, fcntl.F_GETFD)
    fcntl.fcntl(fd, fcntl.F_SETFD, st | fcntl.FD_CLOEXEC)

def textify(nodes, sep=' '):
    if not isinstance(nodes, (list, tuple)):
        nodes = [nodes]

    def _t(x):
        if isinstance(x, (str, unicode)):
            return [x]

        if hasattr(x, 'xmlNode'):
            if not x.xmlNode.get_type() == 'element':
                return [x.extract()]
        else:
            if isinstance(x.root, (str, unicode)):
                return [x.root]

        return (n.extract() for n in x.select('.//text()'))

    nodes = chain(*(_t(node) for node in nodes))
    nodes = (node.strip() for node in nodes if node.strip())

    return sep.join(nodes)

def xcode(text, encoding='utf8', mode='strict'):
    return text.encode(encoding, mode) if isinstance(text, unicode) else text

def compact(text, level=0):
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

    return value

def normalize(text):
    return clean(compact(xcode(text)))

def extract_data(data, path, delem=''):
   return delem.join(i.strip() for i in data.xpath(path).extract() if i).strip()

def extract_list_data(data, path):
   return data.xpath(path).extract()

def get_nodes(data, path):
   return data.xpath(path)

def md5(x):
    return hashlib.md5(xcode(x)).hexdigest()

def validate_year(self, year):
        is_valid = False
        if year and isinstance(year, int):
            if year >= 1900 and year <= 2020:
                is_valid = True
        return is_valid

def get_year_from_string(text):
    import re
    cleaned_text, year = '', ''
    re_match = re.search('\((\d{4})\)', text) or re.search('\s(\d{4})$', text) or re.search('\s(\d{4})\s', text) or re.search('\[(\d{4})\]', text)
    if re_match:
        year_info    = re_match.re.findall(text)
        if year_info:
            final_year = int(year_info[0])
            if validate_year(final_year):
                cleaned_text = re_match.re.sub('', text).strip()
                year         = final_year
    return cleaned_text, year

def get_rating_val(self, rating, mul=0):
        rating = get_digit(rating)
        if mul > 1:
            rating = rating * mul
        return rating

"""def get_response(reference_url, logger=''):
    start_time = timeit.default_timer()

    http_client = HT.HTTPClient()
    try:
        r =  http_client.fetch(reference_url, user_agent=USER_AGENT)
        res = TextResponse(url=reference_url, headers=r.headers, body=r.body)
        status = res.status
        end_time = timeit.default_timer()
        logger.info("URL Response Time: %s - Reference URL: %s", (end_time - start_time), reference_url)

        start_time = timeit.default_timer()
        sel = Selector(res)
        end_time = timeit.default_timer()
        logger.info("DOM Construction Time: %s  - Reference URL: %s", (end_time - start_time), reference_url)

    except Exception as e:
        status, sel = 404, ''
        logger.error(get_compact_traceback(e))

    return (status, sel)"""



def get_response_by_passing_headers(reference_url, logger, headers={}, conn_timeout=0, req_timeout=0):
    USER_AGENT = "Mozilla/5.0 (Linux; Pibot; + http://positiveintegers.com/) AppleWebKit/535.21 (KHTML, like Gecko) Chrome/19.0.1042.0"
    conn_timeout = conn_timeout or 1800.0
    req_timeout = req_timeout or 1800.0

    start_time = timeit.default_timer()
    http_client = HT.HTTPClient()

    if headers['User-Agent']:
        USER_AGENT = headers['User-Agent']
    headers['User-Agent'] = USER_AGENT

    try:
        request = HT.HTTPRequest(reference_url, headers=headers, connect_timeout=conn_timeout, request_timeout=req_timeout)
        response = http_client.fetch(request)
        status, body = response.code, response.body
        end_time = timeit.default_timer()
        logger.info("URL Response Time: %s - Reference URL: %s", (end_time - start_time), reference_url)

    except Exception as e:
        logger.error(get_compact_traceback(e))
        status, body = 404, ''
    return status, body


def get_xml_response(reference_url, logger=''):
    start_time = timeit.default_timer()

    http_client = HT.HTTPClient()

    try:
        r =  http_client.fetch(reference_url)
        res = XmlResponse(url=reference_url, headers=r.headers, body=r.body)
        status = res.status

        end_time = timeit.default_timer()
        logger.info("URL Response Time: %s - Reference URL: %s", (end_time - start_time), reference_url)

        start_time = timeit.default_timer()
        sel = Selector(res)
        end_time = timeit.default_timer()
        logger.info("DOM Construction Time: %s  - Reference URL: %s", (end_time - start_time), reference_url)

    except Exception as e:
        status, sel = 404, ''
        logger.error(get_compact_traceback(e))

    return (status, sel)

def get_response_body(reference_url, logger=''):
    start_time = timeit.default_timer()

    http_client = HT.HTTPClient()
    try:
        r   = http_client.fetch(reference_url)
        sel = r.body
        res = TextResponse(url=reference_url, headers=r.headers, body=r.body)
        status = res.status
        end_time = timeit.default_timer()
        logger.info("URL Response Time: %s - Reference URL: %s", (end_time - start_time), reference_url)
    except HT.HTTPError, e:
        status, sel = 404, ''
        logger.error(get_compact_traceback(e))

    return (status, sel)

def parse_date(data, dayfirst=False):
    if not 'ago' in data and 'Yesterday' not in data:
        return parse(data, dayfirst=dayfirst, fuzzy=True)
    elif 'Yesterday' in data:
        return parse(data, dayfirst=dayfirst, fuzzy=True)+relativedelta(days=-1)
    else:
        DEFAULT = datetime.datetime.utcnow()
        dat = re.findall('\d+', data)
        if len(dat)==1 : dat.append(0)
        if 'years' in data:
            return DEFAULT + relativedelta(years=-int(dat[0]), months=-int(dat[1]))
        elif 'months' in data:
            return DEFAULT + relativedelta(months=-int(dat[0]), weeks=-int(dat[1]))
        elif 'week' in data:
            return DEFAULT + relativedelta(weeks=-int(dat[0]))
        elif 'day' in data:
            return DEFAULT + relativedelta(days=-int(dat[0]), hours=-int(dat[1]))
        elif 'hour' in data or 'hrs' in data or 'hr' in data:
            return DEFAULT + relativedelta(hours=-int(dat[0]), minutes=-int(dat[1]))
        elif 'minute' in data or 'mins' in data:
            return DEFAULT + relativedelta(minutes=-int(dat[0]))

def get_digit(self, value):
    if value.isdigit():
        value = int(value)
    else:
        try:
            value = float(value)
        except ValueError:
            value = 0
    return value

def convert_str_to_dict_obj(text):
    conv_text = json.loads(text)

    return conv_text

def convert_dict_to_str_obj(text):
    conv_text = json.dumps(text)

    return conv_text

def get_datetime(epoch):
    t = time.gmtime(epoch)
    dt = datetime.datetime(*t[:6])

    return dt

def parse_genframework_config_file(section='', sub_section=''):
    cfg_file_path = os.path.join(os.path.abspath(os.path.pardir), 'genframework.cfg')
    parser = SafeConfigParser()
    parser.read(cfg_file_path)

    sections = parser.sections()
    if not sections: return {}

    cfg_data = {}
    for section in sections:
        for key, value in parser.items(section):
            cfg_data.setdefault(section, {}).update({key: json.loads(value)})

    if section and sub_section:
        return cfg_data[section][sub_section]
    elif section:
        return cfg_data[section]

    return cfg_data

