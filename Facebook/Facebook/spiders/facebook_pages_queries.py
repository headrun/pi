user_access_token = 'EAAHI1jm1ILoBAL0tqkltPFxT0Wuyil8BM5ZCgDXlcRnZAlZBuZCpY3X192OnmN74vGrQ5f3WZAmGrZAZAV1hMnmzQOiX4gPa3RtbHizDKv9MRgIUNMYGLYs5NnLD0n9b6cu5lN5IizmyJWq1FAZBbHFr1edSTuy5b0MZD'
graph_api = "https://graph.facebook.com/v2.10/"
graph_api1 = "/feed?fields=shares,permalink_url,is_verified,reactions.summary(true).limit(1000000),reactions.type(LIKE).summary(total_count).limit(0).as(like),reactions.type(LOVE).summary(total_count).limit(0).as(love),reactions.type(WOW).summary(total_count).limit(0).as(wow),reactions.type(HAHA).summary(total_count).limit(0).as(haha),reactions.type(SAD).summary(total_count).limit(0).as(sad),reactions.type(ANGRY).summary(total_count).limit(0).as(angry),full_picture,attachments,views,from,to,message,link,name,caption,description,created_time,updated_time,comments.summary(true).limit(1000000){reactions.summary(true).limit(1000000),reactions.type(LIKE).summary(total_count).limit(0).as(like),reactions.type(LOVE).summary(total_count).limit(0).as(love),reactions.type(WOW).summary(total_count).limit(0).as(wow),reactions.type(HAHA).summary(total_count).limit(0).as(haha),reactions.type(SAD).summary(total_count).limit(0).as(sad),reactions.type(ANGRY).summary(total_count).limit(0).as(angry),%20from,to,message,link,name,full_picture,attachments,caption,description,created_time,updated_time,like_count,comments.summary(true).limit(1000000){from,to,message,link,name,caption,full_picture,attachments,description,created_time,updated_time,like_count,reactions.summary(true).limit(1000000),reactions.type(LIKE).summary(total_count).limit(0).as(like),reactions.type(LOVE).summary(total_count).limit(0).as(love),reactions.type(WOW).summary(total_count).limit(0).as(wow),reactions.type(HAHA).summary(total_count).limit(0).as(haha),reactions.type(SAD).summary(total_count).limit(0).as(sad),reactions.type(ANGRY).summary(total_count).limit(0).as(angry)}}&access_token=EAAHI1jm1ILoBAL0tqkltPFxT0Wuyil8BM5ZCgDXlcRnZAlZBuZCpY3X192OnmN74vGrQ5f3WZAmGrZAZAV1hMnmzQOiX4gPa3RtbHizDKv9MRgIUNMYGLYs5NnLD0n9b6cu5lN5IizmyJWq1FAZBbHFr1edSTuy5b0MZD&limit=100&filter=stream"
get_query_param_fbp = "select sk, url, meta_data from facebook_pages_crawl where crawl_status=0 limit 15"
update_query_fbp = "update facebook_pages_crawl set crawl_status=%s where sk = '%s'"
facebook_pages_meta_query1 = 'insert into facebook_pages_meta(page_sk, page_url, page_id, page_name, created_at, modified_at, last_seen) values (%s, %s, %s, %s, now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(), page_sk=%s, page_url=%s, page_id=%s, page_name=%s'
facebook_pages_posts_query1 = 'insert into facebook_pages_posts(page_sk, page_id, post_sk, post_id, post_shares_count, post_url, post_message, post_created_time, post_updated_time, post_picture, post_from_name, post_from_id, post_to_name, post_to_id, post_comments_total_count, post_reactions_total_count, post_like_count, post_love_count, post_wow_count, post_haha_count, post_sad_count, post_angry_count, created_at, modified_at, last_seen) values (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(), page_sk=%s, page_id=%s, post_sk=%s, post_id=%s, post_shares_count=%s, post_url=%s, post_message=%s, post_created_time=%s, post_updated_time=%s, post_picture=%s, post_from_name=%s, post_from_id=%s, post_to_name=%s, post_to_id=%s, post_comments_total_count=%s, post_reactions_total_count=%s, post_like_count=%s, post_love_count=%s, post_wow_count=%s, post_haha_count=%s, post_sad_count=%s, post_angry_count=%s'
facebook_pages_posts_comments_query1 = 'insert into facebook_pages_posts_comments(page_sk, page_id, post_sk, post_id, comment_sk, comment_id, comment_from_id, comment_from_name, comment_message, comment_created_time, inner_comments_total_count, comment_reactions_total_count, comment_like_count, comment_love_count, comment_wow_count, comment_haha_count, comment_sad_count, comment_angry_count, created_at, modified_at, last_seen) values ( %s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(), page_sk=%s, page_id=%s, post_sk=%s, post_id=%s, comment_sk=%s, comment_id=%s, comment_from_id=%s, comment_from_name=%s, comment_message=%s, comment_created_time=%s, inner_comments_total_count=%s, comment_reactions_total_count=%s, comment_like_count=%s, comment_love_count=%s, comment_wow_count=%s, comment_haha_count=%s, comment_sad_count=%s, comment_angry_count=%s'
facebook_pages_posts_inner_comments_query1 = 'insert into facebook_pages_posts_inner_comments(page_sk, page_id, post_sk, post_id, comment_sk, comment_id, inner_comment_sk, inner_comment_id, inner_comment_from_id, inner_comment_from_name, inner_comment_message, inner_comment_created_time, innercomment_like_count, inner_comment_love_count, inner_comment_wow_count, inner_comment_haha_count, inner_comment_sad_count, inner_comment_angry_count, inner_comment_reactions_total_count, created_at, modified_at, last_seen) values (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(), page_sk=%s, page_id=%s, post_sk=%s, post_id=%s, comment_sk=%s, comment_id=%s, inner_comment_sk=%s, inner_comment_id=%s, inner_comment_from_id=%s, inner_comment_from_name=%s, inner_comment_message=%s, inner_comment_created_time=%s, innercomment_like_count=%s, inner_comment_love_count=%s, inner_comment_wow_count=%s, inner_comment_haha_count=%s, inner_comment_sad_count=%s, inner_comment_angry_count=%s, inner_comment_reactions_total_count=%s'
facebook_pages_posts_reactions_query1 = 'insert into facebook_pages_posts_reactions(reaction_sk, page_sk, page_id, post_sk, post_id, member_id, member_name, reaction_type, created_at, modified_at, last_seen) values(  %s, %s, %s, %s,%s, %s, %s, %s, now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(), reaction_sk=%s, page_sk=%s, page_id=%s, post_sk=%s, post_id=%s, member_id=%s, member_name=%s, reaction_type=%s'
facebook_pages_posts_comments_reactions_query1 = 'insert into facebook_pages_posts_comments_reactions(reaction_sk, page_sk, page_id, post_sk, post_id, comment_sk, comment_id, member_id, member_name, reaction_type, created_at, modified_at, last_seen) values(  %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(), reaction_sk=%s, page_sk=%s, page_id=%s, post_sk=%s, post_id=%s, comment_sk=%s, comment_id=%s, member_id=%s, member_name=%s, reaction_type=%s'
facebook_pages_posts_comments_inner_reactions_query1 = 'insert into facebook_pages_posts_comments_inner_reactions(reaction_sk, page_sk, page_id, post_sk, post_id, comment_sk, comment_id, inner_comment_sk, inner_comment_id, member_id, member_name, reaction_type, created_at, modified_at, last_seen) values(  %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(), reaction_sk=%s, page_sk=%s, page_id=%s, post_sk=%s, post_id=%s, comment_sk=%s, comment_id=%s, inner_comment_sk=%s, inner_comment_id=%s, member_id=%s, member_name=%s, reaction_type=%s'
