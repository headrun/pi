qry_params = 'insert into facebook_profiles(sk, profile_url,aux_info_read_followers,aux_info_books_likes,aux_info_read_books,aux_info_tvshow_likes, aux_info_tvshow_watched, aux_info_movie_likes, aux_info_movie_watched, aux_info_inspirational_people,aux_info_sports, aux_info, aux_info_clothing, aux_info_friends, aux_info_atheletes, aux_info_teams, aux_info_book,aux_info_work, aux_info_education, aux_info_family, aux_info_music, aux_info_games, aux_info_websites, aux_info_restaurants, aux_info_activities, aux_info_interests, aux_info_tvshows, aux_info_movies, aux_info_others, created_at, modified_at) values (%s, %s,"{}","{}","{}","{}","{}","{}","{}", "{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}", now(), now())  on duplicate key update modified_at = now(), sk =%s, profile_url = %s, aux_info = "{}", aux_info_clothing="{}", aux_info_friends="{}", aux_info_atheletes="{}", aux_info_teams="{}", aux_info_book="{}", aux_info_music="{}", aux_info_games="{}", aux_info_websites="{}", aux_info_restaurants="{}", aux_info_activities="{}", aux_info_interests="{}", aux_info_tvshows="{}", aux_info_movies="{}", aux_info_others="{}", aux_info_work="{}",aux_info_family="{}",aux_info_education="{}",aux_info_sports="{}", aux_info_inspirational_people="{}",aux_info_tvshow_likes="{}",aux_info_tvshow_watched="{}",aux_info_movie_likes="{}",aux_info_movie_watched="{}", aux_info_read_books="{}",aux_info_books_likes="{}",aux_info_read_followers="{}"'
updateqry_params = "update facebook_profiles set %s = '%s' where sk = '%s'"
selectaux_params = 'select aux_info from facebook_profiles where sk = "%s"'
selectauxkeys_params = 'select %s from facebook_profiles where sk = "%s"'
#selectall_params = 'select sk , name, profile_id, aux_info,aux_info_read_followers,aux_info_books_likes,aux_info_read_books,aux_info_movie_watched,aux_info_movie_likes,aux_info_tvshow_watched, aux_info_tvshow_likes, aux_info_inspirational_people, aux_info_sports, aux_info_family, aux_info_education, aux_info_work, aux_info_clothing, aux_info_friends, aux_info_atheletes, aux_info_teams, aux_info_book, aux_info_music, aux_info_games, aux_info_websites, aux_info_restaurants, aux_info_activities, aux_info_interests, aux_info_tvshows, aux_info_movies, aux_info_others, profile_url from facebook_profiles where sk in (select sk from facebook_crawl where content_type = "updatedrecord")'

#selectall_params = "select sk , name, profile_id, aux_info,aux_info_read_followers,aux_info_books_likes,aux_info_read_books,aux_info_movie_watched,aux_info_movie_likes,aux_info_tvshow_watched, aux_info_tvshow_likes, aux_info_inspirational_people, aux_info_sports, aux_info_family, aux_info_education, aux_info_work, aux_info_clothing, aux_info_friends, aux_info_atheletes, aux_info_teams, aux_info_book, aux_info_music, aux_info_games, aux_info_websites, aux_info_restaurants, aux_info_activities, aux_info_interests, aux_info_tvshows, aux_info_movies, aux_info_others, profile_url from facebook_profiles where date(modified_at) > '2017-04-18'  and profile_url like '%ratanjit.uppal%' or profile_url like '%ritesh.menon.77%' or profile_url like '%raman.jain.5095%' or profile_url like '%vinodkumar.biyani%' or profile_url like '%/rishi.pal.77%' or profile_url like '%sudhirdhiman19%' or profile_url like '%wadehra.nikhil%' or profile_url like '%sunny.wadhwa.5245%' or profile_url like '%rakesh.sinha.75098364%' or profile_url like '%ratanjit.uppal%' or profile_url like '%ritesh.menon.7%'"

selectall_params = selectall_params = 'select sk , name, profile_id, aux_info,aux_info_read_followers,aux_info_books_likes,aux_info_read_books,aux_info_movie_watched,aux_info_movie_likes,aux_info_tvshow_watched, aux_info_tvshow_likes, aux_info_inspirational_people, aux_info_sports, aux_info_family, aux_info_education, aux_info_work, aux_info_clothing, aux_info_friends, aux_info_atheletes, aux_info_teams, aux_info_book, aux_info_music, aux_info_games, aux_info_websites, aux_info_restaurants, aux_info_activities, aux_info_interests, aux_info_tvshows, aux_info_movies, aux_info_others, profile_url from facebook_profiles where date(modified_at) >= "2017-06-19"'

header_params = ['Name', 'profile_id', 'profile_url', 'original_url', 'fb_current_city', 'fb_home_town', 'fb_birthday', 'fb_gender', 'fb_professional_skills','no_of_friends','fb_mobile','fb_instagram','fb_websites','fb_interested_in','fb_languages','fb_religious_views','fb_political_views','fb_relationship','fb_address','fb_google_talk','fb_email','fb_other_name','fb_nick_name','fb_messenger','fb_home_phone','fb_facebook','fb_others','fb_clothing','fb_activities','fb_interests','fb_music','fb_books','fb_movies','fb_tvshows','fb_favaourite_athelets','fb_favourite_teams','fb_games','fb_restaurants','fb_websites','fb_works','fb_education','fb_favourite_sports','fb_friends','fb_inspirational_people','fb_tvshow_likes','fb_tvshows_watched','fb_movies_likes','fb_movie_watched','fb_book_likes','fb_read_books','fb_following','fb_family_members','fb_response_status', 'EmailAddress']
get_qry_params = "select sk, url,meta_data from facebook_crawl where crawl_status=0 limit 30"#3"#need to keep 30
#get_qry_params = "select sk, url,meta_data from facebook_crawl where  modified_at > '2017-04-19 07:05:14' and crawl_status=0 limit 20"
update_get_params = "update facebook_crawl set crawl_status=%s where sk ='%s'"
update_getc_params = "update facebook_crawl set content_type='%s' where sk ='%s'"



