domain_premium = "https://www.linkedin.com"
update_get_params = "update linkedin_crawl set crawl_status=%s where sk ='%s'"
main_profile_api = "https://www.linkedin.com/voyager/api/identity/profiles/%s"
start_end_count = '?start=0&count=100'
start_end_an = '&start=0&count=100'
positions_api = "%s%s%s" % (main_profile_api, "/positions", start_end_count)
feature_skills_api = "%s%s%s" % (
    main_profile_api, "/featuredSkills?includeHiddenEndorsers=true", start_end_an)
volunteer_exp_api = "%s%s%s" % (
    main_profile_api, "/volunteerExperiences", start_end_count)
recommendation_rec_api = "%s%s%s" % (
    main_profile_api, "/recommendations?q=received", start_end_an)
recommendation_giv_api = "%s%s%s" % (
    main_profile_api, "/recommendations?q=given", start_end_an)
projects_api = "%s%s%s" % (main_profile_api, "/projects", start_end_count)
posts_api = "%s%s%s" % (main_profile_api, "/posts", start_end_count)
testscores_api = "%s%s%s" % (main_profile_api, '/testScores', start_end_count)
organizations_api = "%s%s%s" % (
    main_profile_api, "/organizations", start_end_count)
honors_api = "%s%s%s" % (main_profile_api, "/honors", start_end_count)
publications_api = "%s%s%s" % (
    main_profile_api, "/publications", start_end_count)
courses_api = "%s%s%s" % (main_profile_api, "/courses", start_end_count)
certifications_api = "%s%s%s" % (
    main_profile_api, "/certifications", start_end_count)
educations_api = "%s%s%s" % (main_profile_api, "/educations", start_end_count)
entity_api = "/following?entityType=%s&q=followedEntities&start=0&count=100"
groups_api = "%s%s" % (main_profile_api, (entity_api % "GROUP"))
schools_api = "%s%s" % (main_profile_api, (entity_api % "SCHOOL"))
company_api = "%s%s" % (main_profile_api, (entity_api % "COMPANY"))
influencers_api = "%s%s" % (main_profile_api, (entity_api % "INFLUENCER"))
channel_api = "%s%s" % (main_profile_api, (entity_api % "CHANNEL"))
profile_view_url = "https://www.linkedin.com/profile/view?id=%s&authType=name&authToken=%s"
profile_images_path = "/root/Linkedin/Linkedin/spiders/images/full/"

api_whole_list = [	(positions_api, 'experiences'),
                   (feature_skills_api, 'skills'),
                   (volunteer_exp_api, 'volunteer'),
                   (recommendation_rec_api, 'received'),
                   (recommendation_giv_api, 'given'),
                   (projects_api, 'projects'),
                   (posts_api, 'posts'),
                   (organizations_api, 'organizations'),
                   (honors_api, 'honors'),
                   (publications_api, 'publications'),
                   (courses_api, 'courses'),
                   (certifications_api, 'certifications'),
                   (educations_api, 'educations'),
                   (groups_api, 'groups'),
                   (schools_api, 'schools'),
                   (company_api, 'companies'),
                   (influencers_api, 'influencers'),
                   (channel_api, 'channel'),
                   (testscores_api, 'testscores')
                   ]
insert_count_qry = "insert into linkedin_loginlimit(sk, login_mail_id, count, login_date, proxy_ip, created_at, modified_at, last_seen) values ('%s', '%s', %s, '%s', '%s', now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(), sk='%s', login_mail_id='%s', count=%s, login_date='%s', proxy_ip='%s'"
get_insert_count_qry = 'select count from linkedin_loginlimit where sk="%s" and login_date="%s" and proxy_ip = "%s"'

selectmailparams = "select sk, email, pass from linkedin_mails where crawl_status = 0 limit 1"
update_based_table = "update %s set crawl_status=%s where sk = '%s'"
