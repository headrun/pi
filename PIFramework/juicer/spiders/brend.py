from scrapy.http import Request
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
import json
import MySQLdb

"""
conn = MySQLdb.connect(host="10.4.18.108", user = "root", db = "CLUP2_DEV", charset="utf8", use_unicode=True)
cur = conn.cursor()
"""

def get_cursor():
      conn = MySQLdb.connect(db = 'BROADBANDOBDB', host = 'localhost', user = 'root', passwd='', charset ='utf8', use_unicode = True)
      cursor = conn.cursor()
      return conn, cursor

class Brend(BaseSpider):
    name = 'brend_clu'
    start_urls = ['https://bendbroadband.com/residential/tv/channel-lineup.asp']

    def __init__(self, *args, **kwargs):
        super(Brend, self).__init__(*args, **kwargs)
        db_name = kwargs.get('db_name')
        host = kwargs.get('host')
        #self.conn, self.cursor = get_cursor()

    def parse(self,response):
        import pdb;pdb.set_trace()
        sel = Selector(response)
        url = 'https://bendbroadband.com/residential/tv/channel-lineup.asp'
        yield Request(url, callback=self.parse_next, meta={'dont_redirect': True, 'handle_httpstatus_list': [301]}, dont_filter = True)

    def parse_next(self,response):
        import pdb;pdb.set_trace()
        rovi_service_id = '70769'
        query = 'insert into %s_locations(country, state, region, sub_region, zipcode, \
                     other_id, reference_url, rovi_service_id, created_at, modified_at)' % ('bendbroadband')
        query += 'values(%s, %s, %s, %s, %s, %s, %s, %s, now(), now())\
               on duplicate key update modified_at = now()'
        values = ('USA', 'OR', 'Bend', '', '', '', response.url, '70769')
        self.cursor.execute(query, values)
        ref_url = response.url
        query = 'select id from %s_locations where reference_url = "%s"' % ('bendbroadband', ref_url)
        self.cursor.execute(query)
        location_id = self.cursor.fetchone()[0]
        program_nodes = sel.xpath('//div[@class="table-responsive channel-lineup"]//table//tr')
        import pdb;pdb.set_trace()
        for prog in program_nodes:
            sd_num = ''.join(prog.xpath('./td[1]/text()').extract()).replace('\t','').replace('\n','').strip()
            hd_num = ''.join(prog.xpath('./td[2]/text()').extract()).replace('\t','').replace('\n','').strip()
            channel_name = ''.join(prog.xpath('./td[4]//a[contains(@id, "CH-")]/text()').extract()).strip() or \
            ''.join(prog.xpath('./td[4]//span/text()').extract()).strip()
            if channel_name == '':
                continue
            channel_reference_url = ''.join(prog.xpath('./td[4]/span/a/@href').extract()).strip()
            twogo = ''.join(prog.xpath('./td[3]/a/@href').extract()).replace('\t','').replace('\n','').strip()
            aux_data = {}
            if twogo:
                aux_data.update({'2go':twogo})
                aux_info = json.dumps(aux_data)
            else:
                aux_info = ''
            pacakages = '<>'.join(prog.xpath('.//span[contains(@class, "label label-ch-")]/@title').extract())
            qry = 'insert into bendbroadband_channels (title,reference_url,aux_info, created_at, modified_at) values (%s, %s,%s,now(), now()) on duplicate key update modified_at = now()'
            vals = (channel_name,channel_reference_url,aux_info)
            self.cursor.execute(qry, vals)
            print pacakages

            c_qry = 'select id from bendbroadband_channels where title = %s'
            vls = (channel_name)
            self.cursor.execute(c_qry, vls)

            ch_id = self.cursor.fetchall()[0][0]
            aux = {}
            if pacakages:
                aux.update({'pakages': pacakages})
                aux = json.dumps(aux)
            else:
                aux = ''


            sd_qry = 'insert into bendbroadband_lineup (stream_quality, tuner_number, channel_id,location_id,rovi_service_id, aux_info, created_at, modified_at) values (%s, %s, %s, %s, %s, %s,now(), now()) on duplicate key update modified_at = now()'
            sd_vals = ('SD', sd_num, ch_id, location_id,rovi_service_id,aux)
            hd_vals = ('HD', hd_num, ch_id, location_id,rovi_service_id,aux)


            if sd_num:
                self.cursor.execute(sd_qry, sd_vals)
            if hd_num:
                self.cursor.execute(sd_qry, hd_vals)

            #conn.commit()

