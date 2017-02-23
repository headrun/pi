import MySQLdb


class FBFeedsStats:
    def __init__(self):
        self.fb_db_name = "FACEBOOK_FEEDS"
        self.db_ip      = "10.28.218.81"
        self.cst_db_name= "WEBSOURCEDB"
        self.create_cursor()

    def create_cursor(self):
        self.conn = MySQLdb.connect(host=self.db_ip, user="veveo", passwd="veveo123")
        self.cursor = self.conn.cursor()

    def get_max_min(self):
        self.min_dict = {}
        query = "select channel_id, max(uploaded_at), min(uploaded_at) from %s.Posts group by channel_id;" %self.fb_db_name
        self.cursor.execute(query)
        records = self.cursor.fetchall()

        for record in records:
            channel_id, max_date, min_date = record
            self.min_dict[str(channel_id)] = (min_date, max_date)

    def get_channel_details(self):
        self.channels_details = {}
        query = 'select channel_id, channel_name, reference_url from FACEBOOK_FEEDS.Channels'
        self.cursor.execute(query)
        records = self.cursor.fetchall()

        for record in records:
            channel_id, channel_name, reference_url = record
            self.channels_details[str(channel_id)] = (channel_name, reference_url)
    
    def get_source_id(self):
        self.source_id = {}
        query = 'select id, name from WEBSOURCEDB.OVPCrawler where source_id = 936'
        self.cursor.execute(query)
        records = self.cursor.fetchall()

        for record in records:
            _id, channel_name = record
            self.source_id[channel_name] = _id

    def get_crawler_id(self, channel):
        db_ip       = "10.28.218.81"
        db_name     = "FACEBOOK_FEEDS"
        machine_ip  = "10.28.216.41"
        channel_name, reference_url = self.channels_details[str(channel)]
        source_id, country_id, status_id, rights_id, dri_id, project_id = 936, 53, 1, 0, 19, 18

        query = 'insert into WEBSOURCEDB.OVPCrawler(source_id, project_id, country_id, status_id, rights_id, dri_id,name, reference_url, db_ip, db_name, machine_ip,is_robots, priority, created_at, modified_at) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), now()) on duplicate key update modified_at =now()'
        values = (source_id, project_id, country_id, status_id, rights_id, dri_id, channel_name, reference_url, db_ip, db_name, machine_ip, '', '')
        self.cursor.execute(query, values)

    def run_main(self):
        self.get_max_min()
        self.get_channel_details()
        self.get_source_id()

        query   = 'select count(*) from FACEBOOK_FEEDS.Posts where channel_id = %s'
        query_1 = 'select distinct uploaded_at from FACEBOOK_FEEDS.Posts where channel_id = %s'
        for channel, dates in self.min_dict.iteritems():
            if channel == "315957273077": continue
            min_date, max_date = dates
            self.cursor.execute(query, (channel))
            total_clips = self.cursor.fetchall()[0][0]

            self.cursor.execute(query_1, (channel))
            total_days_w_min_1_clip  = self.cursor.fetchall()[0][0]

            num_months          = ((max_date - min_date).days) / 30
            num_weeks           = ((max_date - min_date).days) / 7
            clips_per_day       = total_clips / (max_date - min_date).days 
            num_clips_per_month = int(total_clips) / int(num_months)
            num_clips_per_week  = int(total_clips) / int(num_weeks) 
            channel_name, reference_url   = self.channels_details.get(channel) 
            c_id    = self.source_id.get(channel_name, '')
            if not c_id:
                c_id            = self.get_crawler_id(channel)            

            print "*"*30
            print num_months
            print num_weeks
            print num_clips_per_month
            print num_clips_per_week
            print clips_per_day
                   
            query_3 = "insert into WEBSOURCEDB.OVPStats(crawler_id,total_clips, total_days_w_min_1_clip, clips_per_day, clips_per_month, clips_per_week, latest_clip_date, oldest_clip_date, created_at, modified_at) values (%s, %s, %s, %s, %s, %s, %s, %s, now(), now()) on duplicate key update modified_at = now()"
            values = (c_id, total_clips, total_days_w_min_1_clip, clips_per_day, num_clips_per_month, num_clips_per_week, max_date, min_date)
            print query_3 % values
            self.cursor.execute(query_3, values)

	    update_query_stats = "update WEBSOURCEDB.OVPStats set total_clips ='%s', total_days_w_min_1_clip='%s', clips_per_day='%s', clips_per_month='%s', clips_per_week='%s', latest_clip_date='%s', oldest_clip_date='%s' where crawler_id = '%s'"
	    values = (total_clips, total_days_w_min_1_clip, clips_per_day, num_clips_per_month, num_clips_per_week, max_date, min_date, c_id)
	    self.cursor.execute(update_query_stats % values)

if __name__ == "__main__":
    FBFeedsStats().run_main()
