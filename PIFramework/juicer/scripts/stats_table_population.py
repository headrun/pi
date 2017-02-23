import os
import codecs
import MySQLdb
import commands


conn = MySQLdb.connect(host="10.28.218.81", user = "veveo", passwd='veveo123',charset="utf8", use_unicode=True)
cur = conn.cursor()


query = 'select id,crawler_id,movies,tvshows,episodes,othermedia from MVP_COMMONDB.Stats;'
cur.execute(query)
lines = cur.fetchall()

for line in lines:
    id = line[0]
    crawler_id = line[1]
    movies_count  = line[2]
    tvshows_count = line[3]
    episodes_count = line[4]
    othermedia_count = line[-1]
    crawler_table_query = 'select name,db_name from  MVP_COMMONDB.Crawler where id=%s'%(crawler_id)
    cur.execute(crawler_table_query)
    lines = cur.fetchall()
    import pdb;pdb.set_trace()
    crawler_name = lines[0][0]
    db_name = lines[0][1]

 
    movies_count = 'select count(*) from %s.Movie'%(db_name)
    tvshows_count = 'select count(*) from %s.Tvshow'%(db_name)
    episodes_count = 'select count(*) from %s.Episode'%(db_name)
    othermedia_count = 'select count(*) from %s.OtherMedia'%(db_name)

    





   
    crawler_files = '<>'.join(crawler_files)
    if len(crawler_files)=='1' and 'browse' in name:
	movies_count  = movies_count
	tvshows_count = tvshows_count
	episodes_count = episodes_count
	images_count = images_count
	crew_count = crew_count
	othermedia_count = othermedia_count

    if len(crawler_files)!='1' and 'browse' in name and 'terminal' in crawler_files:
	movies_count = 0
	tvshows_count = 0
	episodes_count =0
	othermedia_count =0
	
    if len(crawler_files)!='1' and 'tvshow' in name and 'terminal' in name and 'movie' not in crawler_files:
	tvshows_count = tvshows_count
	if 'episode' not in crawler_files:
	    episodes_count = episodes_count
	else:
	    episodes_count = 0

	if 'othermedia' not in crawler_files and 'movie_terminal' not in crawler_files:
	    othermedia_count = othermedia_count
	else:
	    othermedia_count =0


	if 'movie' not in crawler_files:
	    movies_count = movies_count
	else:
	    movies_count = 0

    if len(crawler_files)!=1 and 'movie' in name and 'terminal' in name:
	movies_count = movies_count
	tvshows_count = 0
	othermedia_count = 0
	if 'tvshow' not in crawler_files:
	    tvshows_count = tvshows_count
	else:
	    tvshows_count= 0
	
	if 'othermedia' not in crawler_files and 'tvshow_terminal' not in crawler_files:
	    othermedia_count = othermedia_count
	else:
	    othermedia_count =0
	
    if len(crawler_files)!=1 and 'episode' in name and 'terminal' in name:
	movies_count =0
	episodes_count = episodes_count
	othermedia_count =0
	if 'tvshow' not in crawler_files:
	    tvshows_count=tvshows_count
	else:
	    tvshows_count =0
	

    if len(crawler_files)!=1 and 'othermedia' in name and 'terminal' in name:
	movies_count =0
	tvshows_count = 0
	episodes_count =0
	othermedia_count = othermedia_count


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
