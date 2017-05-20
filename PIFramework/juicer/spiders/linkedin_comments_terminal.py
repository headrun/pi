import time
from juicer.utils import *

class Linkedincomments(JuicerSpider):
    name = 'comments_comments_terminal'

    def __init__(self, *args, **kwargs):
        super(Linkedincomments, self).__init__(*args, **kwargs)
        self.con, self.cur = get_mysql_connection('localhost', 'LINKEDIN_COMMENTS_NEW', '')
        self.query1 = 'insert into Linkedin_comments(comment_sk, comment_main_sk, keyword_sk, comment_by, comment_datetime, commenter_by_image, commenter_by_public_url, comment_description, commenter_headline, commenter_member_token, comment_total_likes, comment_count, reference_url,  keyword_url, aux_info, created_at,modified_at) values (%s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,now(),now()) on duplicate key update modified_at = now(), comment_sk=%s'
        self.query2 = 'insert into Linkedin_replies(sk, comment_sk, comment_main_sk, keyword_sk, reply_by, reply_datetime, replier_by_image, replier_by_public_url, reply_text, replier_headline, replier_member_token, reply_total_likes, reply_count, reference_url, keyword_url, aux_info, created_at,modified_at) values (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, now(),now()) on duplicate key update modified_at = now(), sk=%s'


    def __del__(self):
        self.conn.close()
        self.cur.close()

    def parse(self, response):
        sel = json.loads(response.body)
        main_url = response.meta.get('data',{}).get('main_url','')
        pulse_url = response.meta.get('data',{}).get('pulse_url','')
        refer_url = pulse_url
        if not refer_url: refer_url = main_url
        total_comments_count = response.meta.get('data',{}).get('comments_count','')
        post_highlight_name = response.meta.get('data',{}).get('name','')
        main_sk = response.meta.get('sk','')
        main_keyword_sk = md5(main_url)
        keyword_url = main_url
        elements = sel.get('elements')
        for element in elements:
            created_date = str(element.get('createdDate',''))
            if created_date:
                created_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(created_date)/1000))
            urn = element.get('urn','')
            all_likes = element.get('viewAllLikesUrl','')
            total_likes = str(element.get('totalLikes',''))
            message = element.get('message','')
            commenter = element.get('commenter',{})
            commenter_member_urn = commenter.get('urn','')
            commenter_image = commenter.get('image',{}).get('url','')
            commenter_public_profile_url = commenter.get('publicProfileUrl','')
            commenter_name = commenter.get('name','')
            commenter_headline = commenter.get('headline','')
            commenter_member_token = commenter.get('memberToken','')
            nested_comment_count = str(element.get('nestedCommentCount',''))
            nested_nodes = element.get('nestedComments',{}).get('elements',[])
            commented_sk = md5("%s%s%s%s"%(commenter_public_profile_url, commenter_name, message, commenter_member_urn))
            vals  = (commented_sk, main_sk, main_keyword_sk, commenter_name, created_date, commenter_image, commenter_public_profile_url, message,  commenter_headline, commenter_member_token, total_likes, total_comments_count, refer_url, keyword_url,response.url, commented_sk)
            self.cur.execute(self.query1, vals)
            for nest in nested_nodes:
                reply_urn = nest.get('urn','')
                reply_all_likes = nest.get('viewAllLikesUrl','')
                reply_created_date = str(nest.get('createdDate',''))
                if reply_created_date:
                    reply_created_date = created_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(reply_created_date)/1000))
                reply_message = nest.get('message','')
                rcn = nest.get('commenter',{})
                reply_commenter_urn = rcn.get('urn','')
                reply_commnter_image = rcn.get('image',{}).get('url','')
                reply_public_profile = rcn.get('publicProfileUrl','')
                reply_name = rcn.get('name','')
                reply_headline = rcn.get('headline','')
                reply_member_token = rcn.get('memberToken','')
                reply_like_count = str(nest.get('totalLikes',''))
                reply_totla_comment = str(nest.get('nestedCommentCount',''))
                replye_sk = md5("%s%s%s%s%s"%(reply_urn, reply_message, reply_public_profile, reply_member_token, reply_created_date))
                values1 = (replye_sk, commented_sk, main_sk, main_keyword_sk, reply_name, reply_created_date, reply_commnter_image, reply_public_profile, reply_message,reply_headline, reply_member_token, reply_like_count, reply_totla_comment, refer_url, keyword_url, response.url, replye_sk)
                self.cur.execute(self.query2, values1)
        self.got_page(main_sk,1)
           
