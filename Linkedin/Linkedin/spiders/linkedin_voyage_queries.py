domain_premium = "https://www.linkedin.com"
update_get_params = "update linkedin_crawl set crawl_status=%s where sk ='%s'"
main_profile_api = "https://www.linkedin.com/voyager/api/identity/profiles/%s"
positions_api = "%s%s" %(main_profile_api, "/positions")
feature_skills_api = "%s%s" %(main_profile_api, "/featuredSkills?includeHiddenEndorsers=true&count=50")
volunteer_exp_api = "%s%s" %(main_profile_api, "/volunteerExperiences")
recommendation_rec_api = "%s%s" %(main_profile_api, "/recommendations?q=received")
recommendation_giv_api = "%s%s" %(main_profile_api, "/recommendations?q=given")
projects_api = "%s%s" %(main_profile_api, "/projects")
posts_api = "%s%s" %(main_profile_api, "/posts")
organizations_api = "%s%s" %(main_profile_api, "/organizations")
honors_api = "%s%s" %(main_profile_api, "/honors")
publications_api = "%s%s" %(main_profile_api, "/publications")
courses_api = "%s%s" %(main_profile_api, "/courses")
certifications_api = "%s%s" %(main_profile_api, "/certifications")
educations_api = "%s%s" %(main_profile_api, "/educations")
entity_api = "/following?entityType=%s&q=followedEntities"
groups_api = "%s%s" %(main_profile_api, (entity_api % "GROUP"))
schools_api =  "%s%s" %(main_profile_api, (entity_api % "SCHOOL"))
company_api = "%s%s" %(main_profile_api, (entity_api % "COMPANY"))
influencers_api = "%s%s" %(main_profile_api, (entity_api % "INFLUENCER"))
channel_api = "%s%s" %(main_profile_api, (entity_api % "CHANNEL"))
profile_view_url = "https://www.linkedin.com/profile/view?id=%s&authType=name&authToken=%s"

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
		 ]
