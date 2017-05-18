social_profiles_query = "insert into social_profiles (sk, profile_sk, name, biography, type_name, followers, profile_url, created_at, modified_at)values(%s, %s, %s, %s, %s, %s, %s, now(), now()) on duplicate key update modified_at = now(), sk=%s"
organizations_query = "insert into organizations (sk, profile_sk, organization, headline, is_current, start_date, end_date, created_at, modified_at)values(%s, %s, %s, %s, %s, %s, %s, now(), now()) on duplicate key update modified_at = now(), sk=%s"
profile_details_query = "insert into profile_details (sk, name, family_name, websites, age, gender, state, city, country, location, continent, likelihood,created_at, modified_at)values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), now()) on duplicate key update modified_at = now(), sk=%s"
profile_richmedia_query = "insert into RichMedia (sk, profile_sk, type_name, image_url,  created_at, modified_at)values(%s, %s, %s, %s, now(), now()) on duplicate key update modified_at = now(), sk=%s"
update_get_params = "update fullcontact_crawl set crawl_status=%s where sk ='%s'"
get_query_param = "select sk, email, meta_data from fullcontact_crawl where crawl_status=0 limit 250"
update_get_paramsemail = "update fullcontact_crawl set meta_data='%s' where sk ='%s'"
query1_full = 'select name, family_name, websites, age, gender, country, state, city, continent, location, likelihood from profile_details where sk = "%s"'
query2_full = 'select name, biography, type_name, followers, profile_url from social_profiles where profile_sk="%s" and (type_name like "%s" or type_name like "%s" or type_name like "%s")'
query3_full = 'select type_name, image_url from RichMedia where profile_sk="%s"'
query4_full = 'select organization, headline, is_current, start_date, end_date from organizations where profile_sk="%s"'
list_variables = ['name', 'biography', 'type_name', 'followers', 'profile_url']
variables_organizations = ['organization', 'headline', 'is_current', 'start_date', 'end_date']
variables_richmedia = ['type_name', 'image_url']
