from juicer.utils import *
from juicer.items import *
import MySQLdb
import time
from channel_input import *

class YoutubeCommentsTerminal(JuicerSpider):
    name = 'youtube_comments_terminal'

    def __init__(self, *args, **kwargs):
        super(YoutubeCommentsTerminal, self).__init__(*args, **kwargs)

        self.con = MySQLdb.connect(db='youtube_comments',
        user='root', passwd='root',
        charset="utf8", host='localhost', use_unicode=True)
        self.cur = self.con.cursor()
        self.cur = self.con.cursor()
        self.channel_qry = channel_insert_query
        self.video_qry = video_insert_qry
        self.richmedia_qry = richmedia_insert_qry
        self.comments_qry = comments_insert_qry
        self.del_qry = del_qry
        self.comments_qry = comments_insert_qry

    def parse(self, response):
        sel = Selector(response)
        program_sk = response.meta['data']['channelid']
        channel_desc = response.meta['data']['channel_desc']
        channel_country = response.meta['data']['channel_country']
        channel_url = response.meta['data']['channel_url']
        channel_logo = response.meta['data']['channel_logo']
        img_sk = md5(channel_logo)
        video_img_url = response.meta['data'][' video_img_url']
        sk = response.meta['sk']
        chan_vals = (str(program_sk), response.meta['data']['channel_title'], \
        normalize(channel_desc), normalize(channel_country), normalize(channel_logo), str(channel_url))
        try : self.cur.execute(self.del_qry % ("Channel", program_sk))
        except : print sk
        try : self.cur.execute(self.del_qry % ("RichMedia", md5(img_sk)))
        except : print "error found"
        media_vals = (md5(channel_logo), program_sk, 'Channel_logo', channel_logo, channel_url)
        self.cur.execute(self.channel_qry, chan_vals)
        video_title = response.meta['data']['video_title']
        video_link = response.meta['data']['video_link']
        video_desc = response.meta['data']['video_desc']
        self.cur.execute(self.del_qry % ("Video_Info", sk))
        video_values = (str(sk), str(program_sk), normalize(video_title), \
        normalize(video_desc), normalize(video_link), normalize(response.url))
	media_vals = (md5(video_img_url), sk, 'video', video_img_url, video_link)
	self.cur.execute(self.video_qry, video_values)
	self.cur.execute(self.del_qry % ("RichMedia", md5(video_img_url)))               
	self.cur.execute(self.richmedia_qry , media_vals)
        ref_link = response.url
        yield Request(ref_link, callback=self.comment_details, dont_filter=True, meta={'sk':sk,'program_sk':program_sk})

    def comment_details(self, response):
        sk = response.meta['sk']
        program_sk = response.meta['program_sk']
        response_ = json.loads(response.body)
        page_info = response_.get('pageInfo',{})
        tot_results = page_info.get('totalResults','')
        data = response_['items']
        next_page = response_.get('nextPageToken','')
        count = 0
        for data_ in data :
            snippet = data_.get('snippet',{}).get('topLevelComment',{}).get('snippet',{})
            auth_cha_url = snippet.get('authorChannelUrl','')
            auth_name = snippet.get('authorDisplayName','')
            updated_at = snippet.get('updatedAt','').split('T')[0]
            video_id = snippet.get('videoId','')
            published_at = snippet.get('publishedAt','').split('T')[0]
            rating = snippet.get('viewerRating','')
            auth_chan_id = snippet.get('authorChannelId',{}).get('value','')
            comment = normalize(snippet.get('textOriginal',''))
            no_of_likes = snippet.get('likeCount','')
            author_image = snippet.get('authorProfileImageUrl','')
            text = snippet.get('textDisplay','')
            count += 1
            comment_sk = md5(str(count)+normalize(comment)+normalize(auth_name))
            vals = (comment_sk,\
            str(sk),  str(program_sk), normalize(comment),str(tot_results),\
            str(no_of_likes),str(rating),normalize(auth_name),normalize(response.url),\
            str(published_at),str(updated_at),str(auth_cha_url),str(auth_chan_id),str(author_image))
            self.cur.execute(self.del_qry % ("comments", comment_sk))
            self.cur.execute(self.comments_qry, vals)
            self.cur.execute(self.del_qry % ("RichMedia", md5(author_image)))
            media_vals = (md5(author_image), comment_sk, 'author_image', normalize(author_image), str(auth_cha_url))
            self.cur.execute(self.richmedia_qry , media_vals)
        print tot_results
        if next_page :
                next_page = 'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet%2Creplies&videoId='+str(video_id)+'&key=AIzaSyBgUp3y8lmbuyCShJvnbuZT9HwX-EH8E8E&maxResults=100&pageToken='+ str(next_page)
                yield Request(next_page, callback=self.comment_details, meta = {'sk':sk, 'program_sk':program_sk})
           
                

                
            
            
 
            

