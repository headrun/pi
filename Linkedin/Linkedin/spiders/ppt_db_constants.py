
#db details

db_name='FACEBOOK'
db_user='root'
db_passwd='root'
db_host='localhost'
            

#queries

select_qry = 'select name, sk, summary, headline, location, profile_url from linkedin_meta where member_id = "%s" '
select_qry1 = 'select  exp_company_name,exp_title, start_date, end_date, exp_location from linkedin_experiences \
        where profile_sk ="%s" limit 4'
select_qry2 = 'select  profile_image,image_path from linkedin_meta where member_id = "%s" limit 1'
select_qry3 = 'select edu_school_name, edu_degree, edu_start_year, edu_end_year from linkedin_educations \
        where profile_sk="%s" limit 2'
select_qry4 = 'select exp_duration from linkedin_experiences where profile_sk ="%s"'

select_qry1_v2 = 'select  exp_company_name,exp_title, start_date, end_date, exp_location from linkedin_experiences \
        where profile_sk ="%s" limit 7' 
select_qry3_v2 = 'select edu_degree, edu_start_year, edu_end_year from linkedin_educations \
        where profile_sk="%s" limit 2'

select_qry4_v2 = 'select company_logo from linkedin_following_companies where company_canonical_name = "%s" limit 1'

select_qry5_v2 = 'select honor_issuer,honor_on from linkedin_honors where profile_sk = "%s" limit 2'

select_qry3_v2_1 = 'select edu_degree,edu_field_of_study, edu_school_name from linkedin_educations \
        where profile_sk="%s" limit 4'

select_qry6_v2 = 'select languages from linkedin_meta where sk = "%s" '
