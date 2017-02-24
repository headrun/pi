#!/usr/bin/env python
import MySQLdb
import datetime
import time
from datetime import timedelta
from vtv_utils import initialize_timed_rotating_logger, vtv_send_html_mail_2

BASIC_LIST = ['niranjansagar@headrun.com', 'aruna@buzzinga.com', 'sowjanya@headrun.com', 'sports@headrun.com', 'delivery@headrun.com']
ADV_LIST  = ['sports@headrun.com', 'delivery@headrun.com', 'aruna@headrun.com', 'sowjanya@headrun.com', 'niranjan@headrun.com']

class TrendsMonitoring:

    def __init__(self):
        self.db_ip           = '10.28.218.81'
        self.db_name         = 'TRENDSDB'
        self.status_dict     = {}
        self.text            = ''
        self.boolean         = False
        self.conn = MySQLdb.connect(host=self.db_ip, user="veveo", db=self.db_name, passwd="veveo123")
        self.cursor = self.conn.cursor()

    def send_mail(self, text):
        subject = 'Trends Status'
        server  = 'localhost'
        sender  = 'noreply@rovicorp.com'
        if self.boolean == True:
            receivers = ADV_LIST
        else:
            receivers = BASIC_LIST
        vtv_send_html_mail_2('', server, sender, receivers, subject, '', text, '')

    def get_html_table(self, title, headers, table_body):
        table_data = '<br /><br /><b>%s</b><br /><table border="1" \
                        style="border-collapse:collapse;" cellpadding="3px" cellspacing="3px"><tr>' % title
        for header in headers:
            table_data += '<th>%s</th>' % header
        table_data += '</tr>'

        for data in table_body:
            table_data += '<tr>'
            for index, row in enumerate(data):
                table_data += '<td>%s</td>' % (str(row))

            table_data += '</tr>'
        table_data += '</table>'

        return table_data


    def news_trends(self, one_hour_minus):
        query = "select count(*) from news_trends_related where last_seen < %s and date(pub_date) > %s"
        self.cursor.execute(query, (one_hour_minus, datetime.datetime.utcnow()))
        records = self.cursor.fetchall()

        if records:
            return records[0][0]
        else:
            return 0

    def main(self):
        one_hour_minus = datetime.datetime.utcnow() - timedelta(hours=1)
        time    = datetime.datetime.now() - datetime.timedelta(minutes=40)
        trends  = {}

        query = 'select count(*) from hourly_trends where source="google" and modified_at > "%s"' %time
        self.cursor.execute(query)
        count = self.cursor.fetchone()
        if count and str(count[0]) == '20':
            self.status_dict['Google'] = count[0]
        else:
            self.boolean = True
            self.status_dict['Google'] = 'Trends Broken'

        query = 'select count(*) from hourly_trends where source="yahoo" and time > "%s"' %time
        self.cursor.execute(query)
        count = self.cursor.fetchall()

        if count:
            trends['Yahoo'] = count[0]
        else:
            trends['Yahoo'] = 0

        query = 'select count(*) from hourly_trends where source="twitter" and modified_at > "%s"' %time
        self.cursor.execute(query)
        count = self.cursor.fetchone()

        if count and str(count[0]) >= '10':
            self.status_dict['Twitter'] = count[0]
        else:
            self.boolean = True
            self.status_dict['Twitter'] = 'Trends Broken'

        query = 'select count(*) from hourly_trends where source="youtube" and modified_at > "%s"' %time
        self.cursor.execute(query)
        count = self.cursor.fetchone()

        if count and str(count[0]) == '20':
            self.status_dict['Youtube']  = count[0]
        else:
            self.boolean = True
            self.status_dict['Youtube']  = 'Trends Broken'

        query = 'select count(*) from hourly_trends_related where last_seen < "%s"' %one_hour_minus
        self.cursor.execute(query)
        count = self.cursor.fetchone()

        if not count:
            self.boolean = True
            self.status_dict['hourly_trends_related'] = 'Hourly Trends Related Table not updated'

        query = 'select count(*) from  hourly_trends_urls where modified_at < "%s"' %one_hour_minus
        self.cursor.execute(query)
        count = self.cursor.fetchone()

        if not count:
            self.boolean = True
            self.status_dict['hourly_trends_urls'] = 'Hourly Trends urls not updatenot updated'

        query = 'select count(*) from news_trends  where modified_at > "%s"' % one_hour_minus
        self.cursor.execute(query)
        count = self.cursor.fetchone()

        if count and count[0] < 7:
            self.status_dict['News Trends'] = 'Trends Broken'
        else:
            self.status_dict['News Trends'] = count[0]

        #self.status_dict['News Count'] = self.news_trends(one_hour_minus)
        table_count = ''
        for source in ['twitter', 'google', 'youtube']:
            query = "select count(*) from trends where last_time > curdate() - 1 and source='%s'" %source
            self.cursor.execute(query)
            count = self.cursor.fetchone()

            if not count:
                if table_count:
                    table_count += '<>%s' % source
                else:
                    table_count = source
        if table_count:
            self.boolean = True
            self.status_dict["Trends Table not updated for"] = table_count

        query = 'select count(*) from hourly_trends_locations where modified_at > curdate() - 1'
        self.cursor.execute(query)
        count = self.cursor.fetchone()
        if not count:
            self.boolean = True
            self.status_dict['hourly_trends_locations'] = "Hourly trends location table not update"
        stats_list = []
        for key, value in self.status_dict.iteritems():
            stats_list.append([key, value])
        self.text += self.get_html_table('Trends Stats', ['Title', 'Stats'], stats_list)

        if self.text:
            self.send_mail(self.text)


if __name__ == "__main__":
    OBJ = TrendsMonitoring()
    OBJ.main()
