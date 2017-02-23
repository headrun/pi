import MySQLdb
import re
from juicer.utils import*
from juicer.items import*
import json


def get_current_ts_with_ms():
    dt = datetime.datetime.now().strftime("%Y%m%dT%H%M%S%f")
    return dt

name = 'clipids'
file_dirs = os.path.join('/home/headrun/GenFramework/juicer/spiders', 'clips_out')
QUERY_FILES_DIR = os.path.join(file_dirs, 'crawl_out')
out_file = os.path.join(QUERY_FILES_DIR, "%s_out_file_%s.queries" %(name, get_current_ts_with_ms()))
out_file = open(out_file, 'a+')



class youtube_browse(JuicerSpider):
    name='youtube_browse'
    start_urls = []
    #lis = ['PewDiePie','smosh','TheFineBros','lindseystomp','RhettandLink','KSIOlajidebt','MichellePhan','IISuperwomanII','RomanAtwood','RosannaPansino']
    lis = ['IGNentertainment', 'PopSugarTV', 'TimeMagazine', 'comedycentral', 'ClevverNews', 'Refinery29TV', 'EEntertainment', \
            'mashable', 'BuzzFeedVideo', 'VEVO']

    for i in lis:
	link = 'https://www.googleapis.com/youtube/v3/channels?part=contentDetails&forUsername='+i+'&key=AIzaSyCvYjNKnU9VFaV-kldX89qQ6jHu0uW10FM&maxResults=20'
    	start_urls.append(link)
    def parse(self,response):
	sel = Selector(response)
	temp = json.loads(response.body)
	te = temp['items']
	for i in te:
		 idd = i['id']
		 if idd:
			#link = 'https://www.googleapis.com/youtube/v3/search?key=AIzaSyCvYjNKnU9VFaV-kldX89qQ6jHu0uW10FM&channelId='+idd+'&part=snippet,id&order=date&maxResults=20'
			link = 'https://www.googleapis.com/youtube/v3/search?part=snippet%2Cid&channelId='+idd+'&maxResults=20&key=AIzaSyCvYjNKnU9VFaV-kldX89qQ6jHu0uW10FM'
				
			yield Request(link,self.details,meta = {'idd':idd})
	
    def details(self,response):
    	sel = Selector(response)
	idd = response.meta['idd']
	body   = json.loads(response.body)
	try:
		nex = body['nextPageToken']
	except:
		nex = ''
	tem = body['items']
	for i in tem:
		try:
			videoid = i['id']['videoId']
		except:		
			videoid = ''
		kind_of_video = i['id']['kind']
		channelId =  i['snippet']['channelId']
		published_at = i['snippet']['publishedAt']
		title = i['snippet']['title']
		description = i['snippet']['description']
		channel_title = i['snippet']['channelTitle']
		now = datetime.datetime.now()
		if videoid:
			#conn = MySQLdb.connect("localhost", db="YOUTUBE")
			conn = MySQLdb.connect(user="root", host = "localhost", db="YOUTUBEOBDB")
			cur = conn.cursor()
			#query  = 'insert into video(video_id,channel_id)values("%s","%s")'
			query  = 'insert into ChannelClip(clip_sk,channel_sk, created_at, modified_at) values(%s,%s, now(), now())'
			values = (videoid,channelId)
			if values:
				out_file.write('%s\n%s\n' %(query, values))
			cur.execute(query,values)
			conn.commit()
	if nex:
		next_link = 'https://www.googleapis.com/youtube/v3/search?part=snippet%2Cid&channelId='+idd+'&maxResults=20&pageToken='+nex+'&key=AIzaSyCvYjNKnU9VFaV-kldX89qQ6jHu0uW10FM'
		yield Request(next_link,self.details,meta = {'idd':idd})
