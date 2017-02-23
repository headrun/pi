import os
import codecs
import MySQLdb
import commands


conn = MySQLdb.connect(host="10.28.218.81", user = "veveo", passwd='veveo123',charset="utf8", use_unicode=True)
cur = conn.cursor()

#query = "show databases like '%_COMMONDB%'"
#cur.execute(query)


input_file = os.path.join(os.getcwd(), "all_ger_crawlers.txt")
lines = codecs.open(input_file, "r+", "utf8").readlines()


for line in lines:
    line = line.encode("utf8")
    all_records = line.split('\t')
    if len(all_records)>3:
	source_id = all_records[2]
	project_id = all_records[5]
	country_id = all_records[1] 
	status_id = all_records[3]
	rights_id = ''
	dri_id = all_records[6]
	reference_url= all_records[4]
	db_ip = '10.28.218.81'
	machine_ip = '10.28.216.42'
	db_name = all_records[-1].replace('\n', '')
	is_robots = 'yes'
	priority ='' 
	crawler_files = all_records[7].split(',')
	for name in crawler_files:
	    name = name.strip()
	    common_db=''
	    if project_id=='9':
		common_db='MVP_COMMONDB'
	    if project_id=='6':
		common_db='LATAM_COMMONDB'
	    if project_id=='17':
	    	common_db = 'THEATRES_COMMONDB'
	    id =  "select max(id) from %s.Crawler"%(common_db)
	    cur.execute(id)
	    id = cur.fetchall()
	    id =id[0][0]
	    try:
            	id = id+1
	    except:
		id = 0
            stats_id = "select max(id) from %s.Stats"%(common_db)
	    cur.execute(stats_id)
	    stats_id = cur.fetchall()
	    stats_id = stats_id[0][0]
	    try:
            	stats_id =stats_id+1
	    except:
		stats_id = 0

	    isdata_id = "select max(id) from %s.IsData"%(common_db)
	    cur.execute(isdata_id)
	    isdata_id=cur.fetchall()
	    isdata_id = isdata_id[0][0]
	    try:
		isdata_id = isdata_id+1
	    except:
		isdata_id =0
	
	    insert_query_to_crawler = "insert ignore into %s.Crawler(id,source_id, project_id, country_id, status_id, rights_id,dri_id, name, reference_url, db_ip, db_name, machine_ip, is_robots, priority, created_at,modified_at) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s', now(),now())"%(common_db,id,source_id,project_id,country_id,status_id,rights_id,dri_id, name,reference_url, db_ip, db_name, machine_ip, is_robots, priority)


	    cur.execute(insert_query_to_crawler)

	    
	    crawler_id = id
	    
	    use_db_query =  "use %s"%db_name
            cur.execute(use_db_query)	   
	
	    movie_counts_query = "select count(*) from Movies"
	    cur.execute(movie_counts_query)
	    movies_count  = cur.fetchall()[0][0]

	    tvshows_counts_query = "select count(*) from Tvshows"
	    cur.execute(tvshows_counts_query)
	    tvshows_count = cur.fetchall()[0][0]

	    episodes_counts_query = "select count(*) from Episodes"
	    cur.execute(episodes_counts_query)
	    episodes_count = cur.fetchall()[0][0]

	
	    crew_counts_query = "select count(*) from Persons"
	    cur.execute(crew_counts_query)
            crew_count = cur.fetchall()[0][0]
    

	    channels_counts_query = "select count(*) from Channels"
	    cur.execute(channels_counts_query)
	    channels_count = cur.fetchall()[0][0]

	    othermedia_count=0

	    crawler_files = '<>'.join(crawler_files)
	    if len(crawler_files)=='1' and 'browse' in name:
		movies_count  = movies_count
		tvshows_count = tvshows_count
		episodes_count = episodes_count
		crew_count = crew_count

	    if len(crawler_files)!='1' and 'browse' in name and 'terminal' in crawler_files:
		movies_count = 0
		tvshows_count = 0
		episodes_count =0

	    if len(crawler_files)!='1' and 'xpath' in name:
		movies_count = 0
                tvshows_count = 0
                episodes_count =0
		
	    if len(crawler_files)!='1' and 'tvshow' in name and 'terminal' in name and 'movie' not in crawler_files:
		tvshows_count = tvshows_count
		if 'episode' not in crawler_files:
		    episodes_count = episodes_count
		else:
		    episodes_count = 0


		if 'movie' not in crawler_files:
		    movies_count = movies_count
		else:
		    movies_count = 0
	
	    if len(crawler_files)!=1 and 'movie' in name and 'terminal' in name:
		movies_count = movies_count
		tvshows_count = 0
		if 'tvshow' not in crawler_files:
		    tvshows_count = tvshows_count
		else:
		    tvshows_count= 0
	        
	    if len(crawler_files)!=1 and 'episode' in name and 'terminal' in name:
		movies_count =0
		episodes_count = episodes_count
		if 'tvshow' not in crawler_files:
		    tvshows_count=tvshows_count
		else:
		    tvshows_count =0
		

	    if len(crawler_files)!=1 and 'othermedia' in name and 'terminal' in name:
	 	movies_count =0
		tvshows_count = 0
	  	episodes_count =0

	
	    insert_query_to_stats = "insert ignore into %s.Stats(id,crawler_id,movies,tvshows,episodes,othermedia,crew,images,channels,lineup,merge_type,overall_merge,rovi_merge, merge_stamp,max_modified_at,created_at,modified_at) values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s', now(), now())"%(common_db,stats_id,id,movies_count, tvshows_count,episodes_count,othermedia_count, 0,0,0,0,'gmrf',0,0,'','')	

	   
	    try:
		cur.execute(insert_query_to_stats)
		#print 'done'
	    except:
		 print db_name


	    iskeep_up = 'yes'
	    frequency = 'FORTNIGHT'
	    insert_into_isdata = "insert ignore into %s.IsData(id,crawler_id,is_keepup,frequency,created_at,modified_at) values('%s', '%s', '%s', '%s', now(), now())"%(common_db,isdata_id,id,iskeep_up,frequency)
	    try:
		cur.execute(insert_into_isdata)
	    except:
		print db_name
