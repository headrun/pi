from stats_gen_functions import *
import json
import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from scrapy import Selector

class TwitterScript(object):

    def __init__(self, *args, **kwargs):
        self.con, self.cur = get_mysql_connection(DB_HOST, DB_NAME_REQ, '')
        self.main()

    def __del__(self):
        self.con.close()
        self.cur.close()

    def send_xls(self):
        file_ = codecs.open("20180515_twitter_sourceCode.txt",'r', encoding = 'utf-8', errors='ignore')
        data = json.loads(file_.read())
        data_ = data.get('page','')
        data = Selector(text=data_)
        urls = data.xpath('//span[@class="username u-dir u-textTruncate"]//b//text()').extract()
        for url in urls :
            url = normalize(url)
            pro_url = "https://www.twitter.com/"+str(url)
            qry = 'insert into twitter_crawl(sk,url,crawl_type,content_type,related_type,crawl_status,meta_data,created_at,modified_at) values (%s, %s, %s, %s, %s, %s ,%s, now(), now())  on duplicate key update modified_at = now()'
            values = (url,str(pro_url),'','twitter','',0,'')
            self.cur.execute(qry,values)

    def main(self):
        self.send_xls()

if __name__ == '__main__':
        TwitterScript().main()

