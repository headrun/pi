from generic_functions import *

class Fbpagescsc(object):
	def __init__(self, *args, **kwargs):
		self.con, self.cur = get_mysql_connection('localhost', 'FACEBOOK', '')
		self.excel_file_name = 'facebook_pages_comments_%s.csv' % str(datetime.datetime.now().date())
		if os.path.isfile(self.excel_file_name):
			os.system('rm %s'%self.excel_file_name)
		oupf = open(self.excel_file_name, 'ab+')
		self.todays_excel_file  = csv.writer(oupf)
		self.query1 = 'select * from %s'
		self.query2 = 'select * from %s where %s = "%s"'
		self.headers1 = ['page_url', 'page_name', 'page_id', 'post_id', 'post_shares_count', 'post_url', 'post_message', 'post_created_time', 'post_updated_time', 'post_picture', 'post_from_name', 'post_from_id', 'post_to_name', 'post_to_id', 'post_comments_total_count', 'post_reactions_total_count', 'post_like_count', 'post_love_count', 'post_wow_count', 'post_haha_count', 'post_sad_count', 'post_angry_count', 'post_reactions_data','comment_id', 'comment_from_id', 'comment_from_name', 'comment_message', 'comment_created_time', 'inner_comments_total_count', 'comment_reactions_total_count', 'comment_like_count', 'comment_love_count', 'comment_wow_count', 'comment_haha_count', 'comment_sad_count', 'comment_angry_count', 'comment_reactions_data','inner_comment_id', 'inner_comment_from_id', 'inner_comment_from_name', 'inner_comment_message', 'inner_comment_created_time', 'innercomment_like_count', 'inner_comment_love_count', 'inner_comment_wow_count', 'inner_comment_haha_count', 'inner_comment_sad_count', 'inner_comment_angry_count', 'inner_comment_reactions_total_count', 'inner_comment_reactions_data']
		self.vals_ = ['member_id', 'member_name', 'reaction_type']
		self.todays_excel_file.writerow(self.headers1)

	def reactions_data(self, post_reaction_data, start_c, end_c):
		final_to_update = []
		for post_r_da in post_reaction_data:
			re_p = filter(None, map(lambda t,q: (t+':-'+q) if q else '', self.vals_, list(post_r_da)[start_c:end_c]))
			final_to_update.append(', '.join(re_p))
		final_to_update = '<>'.join(final_to_update).strip('<>')
		return final_to_update


	def main(self):
		records = fetchmany(self.cur, self.query1%('facebook_pages_meta'))
		for rec in records:
			rec = list(rec)[:-3]
			pg_sk, pg_url, page_id, page_name = rec
			main_values =[pg_url, page_id, page_name]
			post_records = fetchall(self.cur, self.query2 % ('facebook_pages_posts', 'page_sk', pg_sk))
			for pos_rec in post_records:
				pos_rec1 = list(pos_rec)[2:-4]
				here_values = main_values + pos_rec1[1:]
				post_reaction_data = fetchmany(self.cur, self.query2 % ('facebook_pages_posts_reactions', 'post_sk', pos_rec1[0]))
				final_to_update = self.reactions_data(post_reaction_data, 5, -3)
				here_values = here_values + [final_to_update] 
					
				callfun = fetchmany(self.cur, self.query2 % ('facebook_pages_posts_comments', 'post_sk', pos_rec1[0]))
				if not callfun:
					callfun = ((['' for i in range(21)]),)
				for clfun in callfun:
					calf1 = list(clfun)[4:-3]
					her_va = here_values + calf1[1:]
					comment_reaction_data = fetchmany(self.cur, self.query2 % ('facebook_pages_posts_comments_reactions', 'comment_sk', calf1[0]))
					final_to_update1 = self.reactions_data(comment_reaction_data, 7, -3)
					her_va = her_va + [final_to_update1]
					innerfunc = fetchmany(self.cur, self.query2 % ('facebook_pages_posts_inner_comments', 'comment_sk', calf1[0]))
					if not innerfunc or calf1[0] == '':
						innerfunc = ((['' for i in range(22)]),)
					for innclfu in innerfunc:
						calf3 = list(innclfu)[6:-3]
						her_va3 = her_va + calf3[1:]
						inner_comment_reaction_data = fetchmany(self.cur, self.query2 % ('facebook_pages_posts_comments_inner_reactions', 'inner_comment_sk', calf3[0]))
						final_to_update2 = self.reactions_data(inner_comment_reaction_data, 9, -3)
						her_va3 = her_va3 + [final_to_update2]
						her_va3 = [normalize(i) for i in her_va3]
						print len(self.headers1)
						print len(her_va3)
						self.todays_excel_file.writerow(her_va3)
		
		
		
	
if __name__ == '__main__':
	Fbpagescsc().main()
	
