
#db details

db_name='FACEBOOK'
db_user='root'
db_passwd='root'
db_host='localhost'
            

#queries

select_qry = 'select name, sk, summary, headline, location from linkedin_meta where member_id = "%s" '
select_qry1 = 'select exp_title, exp_company_name, start_date, end_date, exp_location from linkedin_experiences \
        where profile_sk ="%s" limit 4'
select_qry2 = 'select  profile_image,image_path from linkedin_meta where member_id = "%s" limit 1'
select_qry3 = 'select edu_school_name, edu_degree, edu_start_year, edu_end_year from linkedin_educations \
        where profile_sk="%s" limit 2'
select_qry4 = 'select exp_duration from linkedin_experiences where profile_sk ="%s"'

