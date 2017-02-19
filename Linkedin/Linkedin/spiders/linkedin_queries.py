ajax_one_url_params = "https://www.linkedin.com/profile/mappers?x-a=%2Cprofile_v2_contact_info%2Cprofile_v2_groups%2Cprofile_v2_skills%2Cprofile_v2_connections%2Cprofile_v2_follow%2Cprofile_v2_course_recommendations%2Cprofile_v2_endorsements&x-p=profile_v2_connections%2Edistance%3A1%2Ctop_card%2EprofileContactsIntegrationStatus%3A0%2Cprofile_v2_right_fixed_discovery%2Erecords%3A12%2Cprofile_v2_right_fixed_discovery%2Eoffset%3A0%2Cprofile_v2_browse_map%2EpageKey%3Anprofile_view_nonself%2Cprofile_v2_discovery%2Eoffset%3A0%2Cprofile_v2_discovery%2Erecords%3A12%2Cprofile_v2_discovery%2Erecords%3A12%2Ctop_card%2Etc%3Atrue%2Cprofile_v2_discovery%2Eoffset%3A0%2Cprofile_v2_summary_upsell%2EsummaryUpsell%3Atrue&x-oa=bottomAliases&id="
ajax_second_url_params = "&locale=en_US&snapshotID=&authType=name&invAcpt=&promoId=&notContactable=&primaryAction=&isPublic=false&sfd=true"
ajax_third_url_params = "&locale=en_US&snapshotID=&authToken=%s&authType=name&invAcpt=&promoId=&notContactable=&primaryAction=&isPublic=false&sfd=true"
selectall_params = 'select sk , name, aux_info, profile_url, connections from linkedin_profiles where sk in (select sk from linkedin_crawl where content_type != "updatedrecord")'
qry_params = 'insert into linkedin_profiles(sk, profile_url, aux_info, connections, created_at, modified_at) values (%s, %s, "{}", "{}", now(), now())  on duplicate key update modified_at = now(), sk =%s, profile_url = %s, aux_info = "{}", connections="{}"'
selectaux_params = 'select aux_info from linkedin_profiles where sk = "%s"'
selectconn_params = 'select connections from linkedin_profiles where sk = "%s"'
updateqry_params = "update linkedin_profiles set %s = '%s' where sk = '%s'"
update_getc_params = "update linkedin_crawl set content_type='%s' where sk ='%s'"
header1_params = ['Phone Number', 'Email','Skills', 'Groups', 'Recommendations' , 'Following News', 'Following Companies', 'Following Influencers', 'Following Schools', 'Connections', 'ResponseAvailable','OriginalUrl','EmailAddress']
header2_params = ['Linkedin', 'linkedin_firstName', 'linkedin_middleName', 'linkedin_lastName',\
            'linkedin_jobTitle', 'linkedin_company', 'linkedin_location', 'linkedin_industry',\
            'linkedin_connectionsCount', 'linkedin_summary', 'linkedin_experience1_title',\
            'linkedin_experience1_company', 'linkedin_experience1_dateStarted',\
            'linkedin_experience1_dateEnd', 'linkedin_experience1_city',\
            'linkedin_experience1_country', 'linkedin_experience2_title',\
            'linkedin_experience2_company', 'linkedin_experience2_dateStarted',\
            'linkedin_experience2_dateEnd', 'linkedin_experience2_city',\
            'linkedin_experience2_country', 'linkedin_experience3_title',\
            'linkedin_experience3_company', 'linkedin_experience3_dateStarted',\
            'linkedin_experience3_dateEnd', 'linkedin_experience3_city',\
            'linkedin_experience3_country', 'linkedin_experience4_title',\
            'linkedin_experience4_company', 'linkedin_experience4_dateStarted',\
            'linkedin_experience4_dateEnd', 'linkedin_experience4_city',\
            'linkedin_experience4_country',\
            'linkedin_experience5_title',\
            'linkedin_experience5_company', 'linkedin_experience5_dateStarted',\
            'linkedin_experience5_dateEnd', 'linkedin_experience5_city',\
            'linkedin_experience5_country', 'linkedin_experience6_title',\
            'linkedin_experience6_company', 'linkedin_experience6_dateStarted',\
            'linkedin_experience6_dateEnd', 'linkedin_experience6_city',\
            'linkedin_experience6_country', 'linkedin_experience7_title',\
            'linkedin_experience7_company', 'linkedin_experience7_dateStarted',\
            'linkedin_experience7_dateEnd', 'linkedin_experience7_city',\
            'linkedin_experience7_country', 'linkedin_experience8_title',\
            'linkedin_experience8_company', 'linkedin_experience8_dateStarted',\
            'linkedin_experience8_dateEnd', 'linkedin_experience8_city',\
            'linkedin_experience8_country',\
            'linkedin_honors1_title',\
            'linkedin_honors1_occupation', 'linkedin_honors1_issuer', 'linkedin_honors1_date',\
            'linkedin_honors1_description', 'linkedin_honors2_title', 'linkedin_honors2_occupation',\
            'linkedin_honors2_issuer', 'linkedin_honors2_date', 'linkedin_honors2_description',\
            'linkedin_honors3_title', 'linkedin_honors3_occupation', 'linkedin_honors3_issuer',\
            'linkedin_honors3_date', 'linkedin_honors3_description', 'linkedin_honors4_title', \
            'linkedin_honors4_occupation', 'linkedin_honors4_issuer', 'linkedin_honors4_date',\
            'linkedin_honors4_description',\
            'linkedin_honors5_title',\
            'linkedin_honors5_occupation', 'linkedin_honors5_issuer', 'linkedin_honors5_date',\
            'linkedin_honors5_description', 'linkedin_honors6_title', 'linkedin_honors6_occupation',\
            'linkedin_honors6_issuer', 'linkedin_honors6_date', 'linkedin_honors6_description',\
            'linkedin_honors7_title', 'linkedin_honors7_occupation', 'linkedin_honors7_issuer',\
            'linkedin_honors7_date', 'linkedin_honors7_description', 'linkedin_honors8_title', \
            'linkedin_honors8_occupation', 'linkedin_honors8_issuer', 'linkedin_honors8_date',\
            'linkedin_honors8_description',\
            'linkedin_education1_school',\
            'linkedin_education1_dateStarted', 'linkedin_education1_dateEnd', 'linkedin_education1_degree',\
            'linkedin_education1_fieldOfStudy', 'linkedin_education1_grade', 'linkedin_education1_activities',\
            'linkedin_education1_description', 'linkedin_education2_school', 'linkedin_education2_dateStarted',\
            'linkedin_education2_dateEnd', 'linkedin_education2_degree', 'linkedin_education2_fieldOfStudy',\
            'linkedin_education2_grade', 'linkedin_education2_activities', 'linkedin_education2_description',\
            'linkedin_education3_school', 'linkedin_education3_dateStarted', 'linkedin_education3_dateEnd',\
            'linkedin_education3_degree', 'linkedin_education3_fieldOfStudy', 'linkedin_education3_grade',\
            'linkedin_education3_activities', 'linkedin_education3_description', \
            'linkedin_education4_school',\
            'linkedin_education4_dateStarted', 'linkedin_education4_dateEnd', 'linkedin_education4_degree',\
            'linkedin_education4_fieldOfStudy', 'linkedin_education4_grade', 'linkedin_education4_activities',\
            'linkedin_education4_description',\
            'linkedin_education5_school',\
            'linkedin_education5_dateStarted', 'linkedin_education5_dateEnd', 'linkedin_education5_degree',\
            'linkedin_education5_fieldOfStudy', 'linkedin_education5_grade', 'linkedin_education5_activities',\
            'linkedin_education5_description', 'linkedin_education6_school', 'linkedin_education6_dateStarted',\
            'linkedin_education6_dateEnd', 'linkedin_education6_degree', 'linkedin_education6_fieldOfStudy',\
            'linkedin_education6_grade', 'linkedin_education6_activities', 'linkedin_education6_description',\
            'linkedin_education7_school', 'linkedin_education7_dateStarted', 'linkedin_education7_dateEnd',\
            'linkedin_education7_degree', 'linkedin_education7_fieldOfStudy', 'linkedin_education7_grade',\
            'linkedin_education7_activities', 'linkedin_education7_description', \
            'linkedin_education8_school',\
            'linkedin_education8_dateStarted', 'linkedin_education8_dateEnd', 'linkedin_education8_degree',\
            'linkedin_education8_fieldOfStudy', 'linkedin_education8_grade', 'linkedin_education8_activities',\
            'linkedin_education8_description',\
            'linkedin_language1',\
            'linkedin_language2', 'linkedin_language3', 'linkedin_additionalInfo_interests',\
            'linkedin_additionalInfo_maritalStatus']
original_url_list_params = {"https://www.linkedin.com/pub/hanafiah-hasni/5b/590/a75":"https://www.linkedin.com/in/hanafiah-hasni-a755905b","https://www.linkedin.com/pub/aaron-chong/3a/7a2/12":"https://www.linkedin.com/in/aaron-chong-0127a23a","https://www.linkedin.com/pub/alex-arroza-cpa-cisa-crisc/3/451/75b":"https://www.linkedin.com/in/alex-arroza-75b4513","https://www.linkedin.com/pub/japrin-thomas/3a/952/79a":"https://www.linkedin.com/in/japrin-thomas-79a9523a","https://www.linkedin.com/pub/ilyani-zahari/16/293/276":"https://www.linkedin.com/in/ilyanizahari","https://www.linkedin.com/pub/anwar-pazikadin/44/889/941":"https://www.linkedin.com/in/anwar-pazikadin-94188944","https://www.linkedin.com/pub/karthikeyan-vasudevan/23/39/5a0":"https://www.linkedin.com/in/karthikeyan-vasudevan-5a003923","https://www.linkedin.com/in/aajay-girit-b858154b":"https://www.linkedin.com/in/dr-aajay-girit-b858154b"}
update_get_params = "update linkedin_crawl set crawl_status=%s where sk ='%s'"
get_qry_params = "select sk, url,meta_data from linkedin_crawl where crawl_status=0 limit 1"#need to keep 30
meat_headers = {
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36',
        'Accept': 'text/html,*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        }

