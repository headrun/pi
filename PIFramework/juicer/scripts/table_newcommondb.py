import MySQLdb
import json
import commands

source_file = 'new_schema/sources'
status_file = 'new_schema/status'
rights_file = 'new_schema/rights'
projects_file = 'new_schema/projects'
dris = 'new_schema/dri'
countries_file = 'new_schema/countries'
#f = 'all_sources_crawler_list.txt'

conn = MySQLdb.connect(host="10.28.218.81", user = "root", db = "OUTBOUND_COMMONDB", charset="utf8", use_unicode=True)
cur = conn.cursor()

query =  "select * from latam_source_stats where crawl_status ='Done'"
cur.execute(query)

rows = cur.fetchall()

#f = open('all_sources_crawler_list.txt', 'r')
grep_cmd = "grep '%s' %s"
for row in rows:
    _id, source_name, country, project_name, reference_url, crawl_status, priority, db_ip, db_name, \
    machine_ip, meta_language, is_inactive, is_robots, is_relevance, is_sanity, is_parser, is_merge, \
    is_crew_merge, merge_type, overall_merge, rovi_merge, is_keepup, is_catchup, crawl_frequency, \
    movies_count, tvshows_count, episodes_count, othermedia_count, DRI, inactive_reason, analysis, \
    exception, created_at, modified_at = row 
    if 'OUTBOUND' in db_name:
	movie_table = source_name + '_movies'
        tvshow_table =source_name + '_tvshows'
        episode_table = source_name + '_episodes'
        crew_table = source_name + '_crew'
        image_table = source_name + '_rich_media'
	o_table = source_name + '_ots'

    else:
	movie_table = 'Movie'
        tvshow_table = 'Tvshow'
        episode_table = 'Episode'
        crew_table = 'Crew'
        image_table = 'RichMedia'
        o_table = 'OtherMedia'
       
    if source_name == 'interfilmes': continue
    query1 = 'select count(*) from %s.%s' % (db_name, movie_table)
    cur.execute(query1)
    m_count = cur.fetchall()[0][0]

    query1 = 'select count(*) from %s.%s' % (db_name, tvshow_table)
    cur.execute(query1)
    t_count = cur.fetchall()[0][0]

    query1 = 'select count(*) from %s.%s' % (db_name,episode_table)
    cur.execute(query1)
    e_count = cur.fetchall()[0][0]

    query1 = 'select count(*) from %s.%s' % (db_name,image_table)
    cur.execute(query1)
    i_count = cur.fetchall()[0][0]

    query1 = 'select count(*) from %s.%s' % (db_name, crew_table)
    cur.execute(query1)
    c_count = cur.fetchall()[0][0]

    query1 = 'select count(*) from %s.%s' % (db_name, o_table)
    cur.execute(query1)
    o_count = cur.fetchall()[0][0]

    status1, country_grep = commands.getstatusoutput(grep_cmd % (country, countries_file))
    country_id = country_grep.split(',')[0]

    status2, status_grep = commands.getstatusoutput(grep_cmd % (country, status_file))
    status_id = status_grep.split(',')[0]

    status3, crawler_grep = commands.getstatusoutput(grep_cmd % (source_name, source_file))
    crawler_id = crawler_grep.split(',')[0]

    status4, project_grep = commands.getstatusoutput(grep_cmd % (project_name, projects_file))
    project_id = project_grep.split(',')[0]

    rights_id = 0
    status4, rights_grep = commands.getstatusoutput(grep_cmd % (project_name, rights_file))
    rights_id = rights_grep.split(',')[0]

    dri_id = 0
    f = open('all_sources_crawler_list.txt', 'r')
    files_list = []
    for line in f:
	s_n = line.split('|')[0]
	if source_name == s_n.strip():
            dri_id = line.split('|')[3]
	    files_list.extend(line.split('|')[-1].split('<>'))
	    print files_list

    for _file in files_list:
	if 'movie' in _file and 'browse' not in _file  and 'terminal' in _file:	
		
		
	    insert_into_stats = "insert  ignore into Stats (crawler_id, movies, tvshows, episodes, crew, images, channels, \
				lineup, merge_type, overall_merge, rovi_merge, merge_stamp, max_modified_at) values \
				('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
	    Stats_values = (crawler_id, m_count, '0', '0', '0', i_count, '0', '0', 'gmrf', \
			    overall_merge, rovi_merge, 0, 0)
	    Stats_values
	    cur.execute(insert_into_stats % Stats_values)

	    insert_into_crawler =  "insert ignore into Crawler (source_id, project_id, country_id, status_id, rights_id, \
				    dri_id, name, reference_url, db_ip, db_name, machine_ip, is_robots, priority) \
				    values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
	    Crawler_values = (crawler_id, project_id, country_id, status_id, 0, dri_id, str(source_name), \
			     reference_url, db_ip, str(db_name), machine_ip, is_robots, priority)
	    cur.execute(insert_into_crawler % Crawler_values)

	    insert_into_InformationScore = "insert ignore into InformationScore (crawler_id, is_charts, is_site_rating) \
					    values ('%s', '%s', '%s')"
	    InformationScore_values = (crawler_id, 0, 0)
	    cur.execute(insert_into_InformationScore % InformationScore_values)

	    insert_into_IsData = "insert ignore into IsData (crawler_id, is_keepup, frequency) \
				  values ('%s', '%s', '%s')"
	    IsData_values = (crawler_id, is_keepup, str(crawl_frequency))
	    cur.execute(insert_into_IsData % IsData_values)
