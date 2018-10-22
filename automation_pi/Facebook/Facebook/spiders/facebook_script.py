import datetime
import csv
import json
import ast

class FacebookSheetScript(object):
    def __init__(self):
	self.excel_file_name = 'facebook_pages_comments_%s.csv' %str(datetime.datetime.now()).split('.')[0].replace(' ','_')
        oupf = open(self.excel_file_name, 'ab+')
        self.todays_excel_file  = csv.writer(oupf)
        main_dict = {}
        headers1 = ['page_url', 'page_name', 'post_from_name', 'post_url', 'post_message', 'post_created_time', 'post_picture', 'post_shares_count', 'post_comments_total_count', 'post_reactions_total_count', 'post_like_count', 'post_love_count', 'post_wow_count', 'post_haha_count', 'post_sad_count', 'post_angry_count','comment_from_name', 'comment_message', 'comment_created_time', 'comment_reactions_total_count', 'comment_like_count', 'comment_love_count', 'comment_wow_count', 'comment_haha_count', 'comment_sad_count', 'comment_angry_count','inner_comments_total_count','inner_comment_from_name', 'inner_comment_message', 'inner_comment_created_time', 'innercomment_like_count', 'inner_comment_love_count', 'inner_comment_wow_count', 'inner_comment_haha_count', 'inner_comment_sad_count', 'inner_comment_angry_count', 'inner_comment_reactions_total_count']
        self.todays_excel_file.writerow(headers1)
    	self.main()

    def main(self):
	f1 = open('facebook_data.txt', 'r')
	body = f1.read()
	body = ast.literal_eval(body)
	for page_id,dict_ in body.iteritems():
            page_url = dict_.get('page_link','')
            page_name = dict_.get('page_name', '')
            page_id = dict_.get('page_id', '')
            posts = dict_.get('posts', {})
            if posts:
                for p_id, post_dict in posts.iteritems():
                    cmnt_dict = post_dict.get('post_comments', {})
		    try:
		    	post_message = post_dict.get('post_message', '').encode('ascii','ignore').decode()
		    except:
			post_dict.get('post_message', '').decode('utf8').encode('ascii','ignore').decode()
		    try:
			post_from = post_dict.get('post_from', '').encode('ascii','ignore').decode()
		    except:
			post_from = post_dict.get('post_from', '').decode('utf8').encode('ascii','ignore').decode()
                    if cmnt_dict:
                        cmns_count = str(len(cmnt_dict.keys()))
                        for c_id, c_dict in cmnt_dict.iteritems():
                            inner_dict = c_dict.get('inner_comments', {})
			    try: 
			    	comment_from_name = c_dict.get('comment_from_name', '').encode('ascii','ignore').decode()
			    except:
				comment_from_name = c_dict.get('comment_from_name', '').decode('utf8').encode('ascii','ignore').decode()
                            if inner_dict:
                                inner_cmnts_count = str(len(inner_dict.keys()))
                                for i_id, i_dict in inner_dict.iteritems():
				    try:
				    	inner_comment_from_name = i_dict.get('inner_comment_from_name', '').encode('ascii','ignore').decode()
				    except:
					inner_comment_from_name = i_dict.get('inner_comment_from_name', '').decode('utf8').encode('ascii','ignore').decode()
                                    values = (page_url, page_name,  post_from, post_dict.get('post_url', ''), post_message, post_dict.get('post_on', ''), post_dict.get('post_picture', ''), post_dict.get('post_shares_count', ''),cmns_count, post_dict.get('post_reactions_total_count', ''), post_dict.get('post_like_count', ''), post_dict.get('post_love_count', ''), post_dict.get('post_wow_count', ''), post_dict.get('post_haha_count', ''), post_dict.get('post_sad_count', ''), post_dict.get('post_angry_count', ''), comment_from_name, c_dict.get('comment_message', ''), c_dict.get('comment_created_time', ''), c_dict.get('comment_reactions_total_count', ''), c_dict.get('comment_like_count', ''), c_dict.get('comment_love_count', ''), c_dict.get('comment_wow_count', ''), c_dict.get('comment_haha_count', ''), c_dict.get('comment_sad_count', ''), c_dict.get('comment_angry_count', ''), inner_comment_from_name, i_dict.get('inner_comment_message', ''), i_dict.get('inner_comment_created_time', ''), i_dict.get('inner_comment_like_count', ''), i_dict.get('inner_comment_love_count', ''), i_dict.get('inner_comment_wow_count', ''), i_dict.get('inner_comment_haha_count', ''), i_dict.get('inner_comment_sad_count', ''), i_dict.get('inner_comment_angry_count', ''), i_dict.get('inner_comment_reactions_total_count', ''))
                                    self.todays_excel_file.writerow(values)
                            else:
                                        values = (page_url, page_name,  post_from, post_dict.get('post_url', ''), post_message, post_dict.get('post_on', ''), post_dict.get('post_picture', ''), post_dict.get('post_shares_count', ''),cmns_count, post_dict.get('post_reactions_total_count', ''), post_dict.get('post_like_count', ''), post_dict.get('post_love_count', ''), post_dict.get('post_wow_count', ''), post_dict.get('post_haha_count', ''), post_dict.get('post_sad_count', ''), post_dict.get('post_angry_count', ''), comment_from_name, c_dict.get('comment_message', ''), c_dict.get('comment_created_time', ''), c_dict.get('comment_reactions_total_count', ''), c_dict.get('comment_like_count', ''), c_dict.get('comment_love_count', ''), c_dict.get('comment_wow_count', ''), c_dict.get('comment_haha_count', ''), c_dict.get('comment_sad_count', ''), c_dict.get('comment_angry_count', ''), '', '', '', '', '', '', '', '', '', '' ,'')
                                        self.todays_excel_file.writerow(values)
	    	    else:
                        	values = (page_url, page_name, post_from, post_dict.get('post_url', ''), post_message, post_dict.get('post_on', ''), post_dict.get('post_picture', ''), post_dict.get('post_shares_count', ''),post_dict.get('post_comments_total_count', ''), post_dict.get('post_reactions_total_count', ''), post_dict.get('post_like_count', ''), post_dict.get('post_love_count', ''), post_dict.get('post_wow_count', ''), post_dict.get('post_haha_count', ''), post_dict.get('post_sad_count', ''), post_dict.get('post_angry_count', ''), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '')
                        	self.todays_excel_file.writerow(values)

if __name__ == 	'__main__':
	FacebookSheetScript()
