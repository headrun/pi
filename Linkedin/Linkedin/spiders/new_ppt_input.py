
#db details

db_name='scratch'
db_user='root'
db_passwd='root'
db_host='localhost'
            

#queries
select_qry_member  = 'select Pm_id from pm_csv1 order by rand() limit 5' 
select_qry = 'select Lnkd_name, Lnkd_summary, Lnkd_headline, Lnkd_location, Lnkd_profile_url, Lnkd_profile_image from pm_csv1 where Pm_id = "%s"'
select_exp_qry = 'select  Lnkd_exp_company_name1, Lnkd_exp_title1, Lnkd_start_date1, Lnkd_end_date1, Lnkd_exp_location1 ,Lnkd_exp_company_name2, Lnkd_exp_title2, Lnkd_start_date2, Lnkd_end_date2, Lnkd_exp_location2, Lnkd_exp_company_name3, Lnkd_exp_title3, Lnkd_start_date3, Lnkd_end_date3, Lnkd_exp_location3, Lnkd_exp_company_name4, Lnkd_exp_title4, Lnkd_start_date4, Lnkd_end_date4, Lnkd_exp_location4, Lnkd_exp_company_name5, Lnkd_exp_title5, Lnkd_start_date5, Lnkd_end_date5, Lnkd_exp_location5,Lnkd_exp_company_name6, Lnkd_exp_title6, Lnkd_start_date6, Lnkd_end_date6, Lnkd_exp_location6, Lnkd_exp_company_name7, Lnkd_exp_title7, Lnkd_start_date7, Lnkd_end_date7, Lnkd_exp_location7 from pm_csv1 where pm_id ="%s"'

select_edu_qry = 'select Lnkd_edu_degree1, Lnkd_edu_field_of_study1, Lnkd_edu_school_name1, Lnkd_edu_degree2, Lnkd_edu_field_of_study2, Lnkd_edu_school_name2,Lnkd_edu_degree3, Lnkd_edu_field_of_study3, Lnkd_edu_school_name3,Lnkd_edu_degree4, Lnkd_edu_field_of_study4, Lnkd_edu_school_name4 from pm_csv1 where Pm_id ="%s" '


select_dur_qry = 'select Lnkd_exp_duration1,Lnkd_exp_duration2,Lnkd_exp_duration3,Lnkd_exp_duration4,Lnkd_exp_duration5,Lnkd_exp_duration6,Lnkd_exp_duration8,Lnkd_exp_duration9,Lnkd_exp_duration10,Lnkd_exp_duration11,Lnkd_exp_duration12,Lnkd_exp_duration13,Lnkd_exp_duration14,Lnkd_exp_duration15 from pm_csv1 where Pm_id ="%s"'


select_qry4_v2 = 'select Lnkd_exp_company_logo1 from pm_csv1 where Pm_id = "%s"'


select_qry3_v2_1 = 'select Lnkd_edu_degree1, Lnkd_edu_field_of_study1, Lnkd_edu_school_name1 from pm_csv1 where Pm_id="%s"'

select_qry6_v2 = 'select Lnkd_Accomplishments_languages from  pm_csv1  where Pm_id = "%s" '
