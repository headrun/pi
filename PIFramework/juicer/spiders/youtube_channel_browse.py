from juicer.utils import *
from channel_input import *

class YoutubeChannelBrowse(JuicerSpider):
    name='youtube_channel_browse' 
    start_urls = [start_link]

    def parse(self, response):
        sel = Selector(response)
        temp = json.loads(response.body)
        te = temp['items']
        for i in te:
            sk = i['id']
            if sk:
                channel_title = i['snippet']['title']
                channel_country =  i['snippet']['country']
                channel_desc = i['snippet']['description']
                url = i['snippet']['thumbnails']['high']['url']
                link = meta_link 
                yield Request(link, callback=self.details, \
                meta={'sk':sk, 'title':channel_title, 'country':channel_country, 'desc':channel_desc, 'channel_logo':url})

    def details(self, response):
        sel = Selector(response)
        idd = response.meta['sk']
        body = json.loads(response.body)
        channel_title = response.meta['title']
        country = response.meta['country']
        channel_desc =response.meta['desc']
        channel_logo = response.meta['channel_logo']
        next_page = body.get('nextPageToken', '')
        temp = body['items']
        for i in temp:
            video = i.get('id', '')
            if video:
                sk = video.get('videoId', '')
                video_title =  i['snippet']['title']
                video_desc = i['snippet']['description']
                video_img_url = i['snippet']['thumbnails']['high']['url']
                video_link = 'https://www.youtube.com/watch?v='+str(sk)
                if sk: 
                    comment_link = 'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet%2Creplies&videoId='+str(sk)+'&key=AIzaSyBgUp3y8lmbuyCShJvnbuZT9HwX-EH8E8E&maxResults=100'
                    self.get_page("youtube_comments_terminal", comment_link, sk, meta_data={'channelid':idd, 'video_desc':video_desc, 'video_link':video_link})

        if next_page :
             next_link = 'https://www.googleapis.com/youtube/v3/search?order=date&part=snippet&channelId=UCGBnz-FR3qaowYsyIEh2-zw&maxResults=50&pageToken='+next_page+'&key=AIzaSyBgUp3y8lmbuyCShJvnbuZT9HwX-EH8E8E'   
             yield Request(next_link, callback=self.details, \
                meta={'sk':idd, 'title':channel_title, 'country':country, 'desc':channel_desc, 'channel_logo':channel_logo})
