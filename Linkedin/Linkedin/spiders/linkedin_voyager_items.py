from linkedin_voyager_functions import *
from Linkedin.items import *

class Voyagerapiitems(scrapy.Spider):

        def __init__(self, name=None, **kwargs):
                super(Voyagerapiitems, self).__init__(name, **kwargs)
	
	def get_track_item(self, sk, member_id, login_mail, machine_ip, crawl_status):
		linkedin_track_ = Linkedintrack()
		linkedin_track_['sk'] =  normalize(sk)
		linkedin_track_['member_id'] =  normalize(member_id)
		linkedin_track_['login_mail_id'] = normalize(login_mail)
		linkedin_track_['machine_ip'] = normalize(machine_ip)
		linkedin_track_['crawl_status'] = normalize(crawl_status)
		return linkedin_track_

	def get_testscores_item(self, sk , test_score_name, test_score, test_score_description, test_score_day, test_score_month, test_score_year):
		linkedin_testscore_ = Linkedintestscore()
		linkedin_testscore_['sk'] = md5("%s%s%s%s" % (sk, str(test_score), test_score_name, test_score_description))
		linkedin_testscore_['profile_sk'] = normalize(sk)
		linkedin_testscore_['testscore_name'] = normalize(test_score_name)
		linkedin_testscore_['testscore_description'] = normalize(test_score_description)
		linkedin_testscore_['testscore'] = normalize(str(test_score))
		linkedin_testscore_['testscore_day'] = normalize(str(test_score_day))
		linkedin_testscore_['testscore_month'] = normalize(str(test_score_month))
		linkedin_testscore_['testscore_year'] = normalize(str(test_score_year))
		return linkedin_testscore_

        def get_certifications_item(self, sk,  cer_id, cer_name, cer_iso_stdate,au_com_name, au_media_logo, certifications_licence):
                linkedin_cer_ = Linkedincertifications()
                linkedin_cer_['sk'] = md5("%s%s%s%s%s" % (sk, cer_id, cer_name, cer_iso_stdate, au_com_name))
                linkedin_cer_['profile_sk'] = normalize(sk)
                linkedin_cer_['certification_id'] = normalize(cer_id)
                linkedin_cer_['certification_date'] = normalize(cer_iso_stdate)
                linkedin_cer_['certification_title'] = normalize(cer_name)
                linkedin_cer_['certification_company_logo'] = normalize(au_media_logo)
                linkedin_cer_['certification_company_name'] = normalize(au_com_name)
                linkedin_cer_['certification_licence'] = normalize(certifications_licence)
                if cer_id or cer_name or au_media_logo:
                        return linkedin_cer_
                else :  
                        return ''

        def get_educations_item(self, sk, edu_start_year, edu_start_month, formatedustart, edu_end_year, formatedusend, edu_end_month, edu_degree, edu_field_ofstdy, edu_name, edu_schoologo, edu_grade, edu_activities, edu_id, edu_scho_id):
                linkedin_educations_ = Linkedineducations()
                linkedin_educations_['sk'] = md5("%s%s%s%s%s%s"%(sk, edu_degree, edu_field_ofstdy, edu_name, edu_id, edu_scho_id))
                linkedin_educations_['profile_sk'] = normalize(sk)
                linkedin_educations_['edu_start_year'] = normalize(edu_start_year)
                linkedin_educations_['edu_start_month'] = normalize(edu_start_month)
                linkedin_educations_['edu_start_date'] = normalize(formatedustart)
                linkedin_educations_['edu_end_year'] = normalize(edu_end_year)
                linkedin_educations_['edu_end_date'] = normalize(formatedusend)
                linkedin_educations_['edu_end_month'] = normalize(edu_end_month)
                linkedin_educations_['edu_degree'] = normalize(edu_degree)
                linkedin_educations_['edu_field_of_study'] = normalize(edu_field_ofstdy)
                linkedin_educations_['edu_school_name'] = normalize(edu_name.replace('&#39;',''))
                linkedin_educations_['school_logo'] = normalize(edu_schoologo)
                linkedin_educations_['edu_grade'] = normalize(edu_grade)
                linkedin_educations_['edu_activities'] = normalize(edu_activities)
                linkedin_educations_['post_article_id'] = ''
                linkedin_educations_['education_id'] = normalize(edu_id)
                linkedin_educations_['school_id'] = normalize(edu_scho_id)
                if edu_degree or edu_field_ofstdy or edu_name:
                        return linkedin_educations_
                else:
                        return ''

        def get_skills_item(self, sk, ski_name, ski_endo_count, public_topic_url, member_topic_url):
                linkedin_ski_ = Linkedinskills()
                linkedin_ski_['sk'] = md5("%s%s%s%s"%(sk, ski_name, ski_endo_count, public_topic_url))
                linkedin_ski_['profile_sk']= normalize(sk)
                linkedin_ski_['skill_name'] = normalize(ski_name)
                linkedin_ski_['endoresement_count'] = normalize(ski_endo_count)
                linkedin_ski_['member_topic_skill_url'] = normalize(member_topic_url)
                linkedin_ski_['public_topic_skill_url'] = normalize(public_topic_url)
                if ski_name:
                        return linkedin_ski_
                else:
                        return ''

        def get_volunteers_item(self, sk, volun_interests, vol_desc, vol_cause, vol_org_name, vol_role, vol_media_logo, vol_start_date_year, vol_start_date_month, vol_single_date_iso, end_month, end_year, organization_id):
                linkedin_volun_ = Linkedinvolunteerexp()
                linkedin_volun_['sk'] = md5("%s%s%s%s%s"%(sk,volun_interests, vol_desc, vol_cause, vol_org_name))
                linkedin_volun_['profile_sk'] = normalize(sk)
                linkedin_volun_['volunteer_interests'] = normalize(volun_interests)
                linkedin_volun_['volunteer_role'] = normalize(vol_role)
                linkedin_volun_['volunteer_cause'] = normalize(vol_cause)
                linkedin_volun_['organization_name'] = normalize(vol_org_name)
                linkedin_volun_['organization_logo'] = normalize(vol_media_logo)
                linkedin_volun_['description'] = normalize(vol_desc)
                linkedin_volun_['start_date_year'] = normalize(vol_start_date_year)
                linkedin_volun_['start_date_month'] = normalize(vol_start_date_month)
                linkedin_volun_['volunteer_date'] = normalize(vol_single_date_iso)
                linkedin_volun_['end_date_year'] = normalize(end_year)
                linkedin_volun_['end_date_month'] = normalize(end_month)
                linkedin_volun_['organization_id'] = normalize(organization_id)
                if linkedin_volun_['volunteer_role'] or linkedin_volun_['volunteer_cause'] or linkedin_volun_['organization_name']:
                        return linkedin_volun_
                else:   
                        return ''

        def get_given_item(self, sk, giv_lastname, giv_fullname, giv_text, giv_title, giv_recom_id, giv_date_relationship, giv_mem_pic, giv_mem_id, giv_profile_link, giv_created_date):

                linkedin_give_rec_ = Linkedingivenrecommendations()
                linkedin_give_rec_['sk'] = md5("%s%s%s%s%s%s%s"%(sk, giv_lastname, giv_fullname, giv_text, giv_title, giv_recom_id, giv_mem_id))
                linkedin_give_rec_['profile_sk'] = normalize(sk)
                linkedin_give_rec_['last_name'] = normalize(giv_lastname)
                linkedin_give_rec_['name'] = normalize(giv_fullname)
                linkedin_give_rec_['date_and_relationship'] = normalize(giv_date_relationship)
                linkedin_give_rec_['title'] = normalize(giv_title)
                linkedin_give_rec_['created_date'] = normalize(giv_created_date)
                linkedin_give_rec_['summary'] = normalize(giv_text)
                linkedin_give_rec_['profile_image'] =  normalize(giv_mem_pic)
                linkedin_give_rec_['profile_member_id'] = normalize(giv_mem_id)
                linkedin_give_rec_['profile_url'] = normalize(giv_profile_link)
                linkedin_give_rec_['recommendation_id'] = normalize(giv_recom_id)
                if giv_lastname or giv_fullname or giv_title or giv_mem_id or giv_recom_id:
                        return linkedin_give_rec_
                else:
                        return ''

        def get_projects_item(self, sk, pro_title, pro_url, pro_desc, pro_team_mates, pro_startdate_iso, pro_enddate_iso, team_mates_list):
                linkedin_proj_ = Linkedinprojects()
                linkedin_proj_['sk'] = md5("%s%s%s%s%s"%(sk,pro_title, pro_url, pro_desc, pro_team_mates))
                linkedin_proj_['profile_sk'] = normalize(sk)
                linkedin_proj_['project_date'] = ''
                linkedin_proj_['number_of_project_members'] = normalize(pro_team_mates)
                linkedin_proj_['project_member_names'] = normalize(team_mates_list)
                linkedin_proj_['project_occupation_name'] = ''
                linkedin_proj_['project_title'] = normalize(pro_title)
                linkedin_proj_['project_url']  = normalize(pro_url)
                linkedin_proj_['project_start_date'] = normalize(pro_startdate_iso)
                linkedin_proj_['project_end_date'] = normalize(pro_enddate_iso)
                linkedin_proj_['project_description'] = normalize(pro_desc)
                if linkedin_proj_['project_title'] or linkedin_proj_['project_description']:
                        return linkedin_proj_
                else:
                        return ''

        def get_posts_item(self, sk, post_url, post_image, post_title, post_author_id, post_state, post_date, sk_post):
                linkedin_posts_ = Linkedinposts()
                linkedin_posts_['sk'] = normalize(md5("%s%s%s%s%s"%(sk_post, post_title, sk, post_date, post_state)))
                linkedin_posts_['profile_sk'] = normalize(sk)
                linkedin_posts_['post_url'] = normalize(post_url)
                linkedin_posts_['post_image'] = normalize(post_image)
                linkedin_posts_['post_title'] = normalize(post_title)
                linkedin_posts_['post_author_id'] = normalize(post_author_id)
                linkedin_posts_['post_state'] = normalize(post_state)
                linkedin_posts_['post_date'] = normalize(post_date)
                linkedin_posts_['post_article_id'] = normalize(sk_post)
                if post_title or post_url or post_date:
                        return linkedin_posts_
                else:
                        return ''

        def get_received_item(self, sk, rec_role, rec_id, rec_memid,  rec_name_full, rec_text, rec_mem_pic, rec_profile_link, rec_headline, rec_date_rela, rec_fmt_Datec, rec_organization):

                linkedin_rec_ = Linkedinrecrecommendations()
                linkedin_rec_['sk'] = md5("%s%s%s%s%s%s%s"%(sk, rec_role, rec_id, rec_fmt_Datec, rec_date_rela, rec_profile_link, rec_mem_pic))
                linkedin_rec_['profile_sk'] = normalize(sk)
                linkedin_rec_['role'] = normalize(rec_role)
                linkedin_rec_['profile_member_id'] = normalize(rec_memid)
                linkedin_rec_['id'] = normalize(rec_id)
                linkedin_rec_['edu_start_date'] = ''
                linkedin_rec_['name'] = normalize(rec_name_full)
                linkedin_rec_['organization'] = normalize(rec_organization)
                linkedin_rec_['created_date'] = normalize(rec_fmt_Datec)
                linkedin_rec_['date_and_relationship'] = normalize(rec_date_rela)
                linkedin_rec_['headline'] = normalize(rec_headline)
                linkedin_rec_['profile_url'] = normalize(rec_profile_link)
                linkedin_rec_['profile_image'] = normalize(rec_mem_pic)
                linkedin_rec_['summary'] = normalize(rec_text)
                if rec_id or rec_name_full or rec_headline or rec_mem_pic or rec_role:
                        return linkedin_rec_
                else:
                        return ''

        def get_experiences_item(self, sk, pos_fmt_location, pos_position_id, pos_company_id, pos_startdate_iso, pos_summary, pos_company_name, pos_cpny_url, pos_title, pos_enddate_iso, pos_media_image, pos_fmt_duration):
                linkedin_epx_ = Linkedinexperiences()
                linkedin_epx_['sk']= md5("%s%s%s%s%s%s"%(sk, pos_fmt_location, pos_position_id, pos_company_id, pos_startdate_iso, pos_summary))
                linkedin_epx_['profile_sk'] = normalize(sk)
                linkedin_epx_['exp_location'] = normalize(pos_fmt_location)
                linkedin_epx_['exp_company_name'] = normalize(pos_company_name)
                linkedin_epx_['exp_company_url'] = normalize(pos_cpny_url)
                linkedin_epx_['exp_title']  =normalize(pos_title)
                linkedin_epx_['start_date'] = normalize(pos_startdate_iso)
                linkedin_epx_['end_date'] = normalize(pos_enddate_iso)
                linkedin_epx_['exp_company_logo'] = normalize(pos_media_image)
                linkedin_epx_['exp_duration'] = normalize(pos_fmt_duration)
                linkedin_epx_['exp_company_id'] = normalize(pos_company_id)
                linkedin_epx_['exp_position_id'] = normalize(pos_position_id)
                linkedin_epx_['exp_summary'] = normalize(pos_summary)
                if pos_title or pos_cpny_url or pos_fmt_location:
                        return linkedin_epx_
                else:
                        return ''

        def get_orgs_item(self, sk, org_name, org_position, org_st_dateiso, org_desc, org_ended_dateiso, org_occupation_name ):
                linkedin_org_ = Linkedinorganizations()
                linkedin_org_['sk'] = md5("%s%s%s%s%s"%(sk, org_name, org_position, org_st_dateiso, org_desc))
                linkedin_org_['profile_sk'] = normalize(sk)
                linkedin_org_['name'] = normalize(org_name)
                linkedin_org_['position'] = normalize(org_position)
                linkedin_org_['start_date'] = normalize(org_st_dateiso)
                linkedin_org_['end_date'] = normalize(org_ended_dateiso)
                linkedin_org_['description']  = normalize(org_desc)
                linkedin_org_['occupation_name'] = normalize(org_occupation_name)
                if linkedin_org_['name'] or linkedin_org_['position']:
                        return linkedin_org_
                else:
                        return ''

        def get_public_item(self, sk, publication_title, publisher_name, pulication_description, publication_url, publication_date):
                linkedin_public_ = Linkedinpublications()
                linkedin_public_['sk'] = '%s%s%s%s'%(sk, publication_title, publisher_name, pulication_description)
                linkedin_public_['profile_sk'] = normalize(sk)
                linkedin_public_['publication_title'] = normalize(publication_title)
                linkedin_public_['publication_url'] = normalize(publication_url)
                linkedin_public_['publisher'] = normalize(publisher_name)
                linkedin_public_['publication_description'] = normalize(pulication_description)
                linkedin_public_['publication_date'] = normalize(publication_date)
                if publication_title or pulication_description or publisher_name:
                        return linkedin_public_
                else:
                        return ''

        def get_honors_item(self, sk, hon_title, hon_issuer, hon_on, hon_desc, hon_id):

                linkedin_hon_ = Linkedinhonors()
                linkedin_hon_['sk']  = md5("%s%s%s%s%s%s"%(sk, hon_title, hon_issuer, hon_on, hon_desc, hon_id))
                linkedin_hon_['profile_sk'] = normalize(sk)
                linkedin_hon_['honor_on'] = normalize(hon_on)
                linkedin_hon_['honor_issuer'] = normalize(hon_issuer)
                linkedin_hon_['honor_summary'] = normalize(hon_desc)
                linkedin_hon_['honor_title'] = normalize(hon_title)
                if hon_title or hon_issuer or hon_desc:
                        return linkedin_hon_
                else:
                        return ''

        def get_channel_item(self, sk, foc_followerscount, foc_name, foc_link_channel, foc_image):
                linkedin_foc_ = Linkedinfollowchannels()
                linkedin_foc_['sk'] = md5("%s%s%s%s%s"%(sk, foc_followerscount, foc_name, foc_link_channel, foc_image))
                linkedin_foc_['profile_sk'] = normalize(sk)
                linkedin_foc_['channel_followers'] = normalize(foc_followerscount)
                linkedin_foc_['channel_title'] = normalize(foc_name)
                linkedin_foc_['channel_link'] =normalize(foc_link_channel)
                linkedin_foc_['channel_image'] = normalize(foc_image)
                if linkedin_foc_['channel_title']:
                        return linkedin_foc_
                else:
                        return ''

        def get_influencers_item(self, sk, inf_titf, inf_profile_url, inf_headline, inf_first_name, inf_last_name, inf_member_logo, inf_fol):
                linkedin_inf_ = Linkedinfollowinfluencers()
                linkedin_inf_['sk'] = md5("%s%s%s%s"%(inf_titf, sk, inf_profile_url, inf_headline))
                linkedin_inf_['profile_sk'] = normalize(sk)
                linkedin_inf_['inflencer_name'] = normalize(inf_titf)
                linkedin_inf_['influencer_firstname'] = normalize(inf_first_name)
                linkedin_inf_['influencer_lastname'] = normalize(inf_last_name)
                linkedin_inf_['influencer_image'] = normalize(inf_member_logo)
                linkedin_inf_['influencer_profile_url'] = normalize(inf_profile_url)
                linkedin_inf_['influencer_headline'] = normalize(inf_headline)
                linkedin_inf_['influencer_followers_count'] = normalize(inf_fol)
                if linkedin_inf_['inflencer_name']:
                        return linkedin_inf_
                else:
                        return ''

        def get_companies_item(self, sk, comp_canonicalname, comp_logo, comp_link, companies_count):
                linkedin_comp_ = Linkedinfollowcompanies()
                linkedin_comp_['sk'] = md5("%s%s%s%s%s"%(sk, comp_canonicalname, comp_logo, comp_link, companies_count))
                linkedin_comp_['profile_sk'] = normalize(sk)
                linkedin_comp_['company_canonical_name'] =  normalize(comp_canonicalname)
                linkedin_comp_['total_followee_count'] = normalize(str(companies_count))
                linkedin_comp_['company_logo'] = normalize(comp_logo)
                linkedin_comp_['company_universal_name'] = ''
                linkedin_comp_['company_url'] = normalize(comp_link)
                if linkedin_comp_['company_canonical_name'] or linkedin_comp_['company_universal_name']:
                        return linkedin_comp_
                else:
                        return ''

        def get_schools_item(self, sk, foll_schools_counts, sch_name, sch_link, sch_image):
                linkedin_scho_ = Linkedinfollowschools()
                linkedin_scho_['sk'] = md5("%s%s%s%s"%(sk, sch_image, sch_name, str(foll_schools_counts)))
                linkedin_scho_['profile_sk'] = normalize(sk)
                linkedin_scho_['school_name'] = normalize(sch_name)
                linkedin_scho_['school_image'] = normalize(sch_image)
                linkedin_scho_['school_region'] = ''
                linkedin_scho_['school_link'] = normalize(sch_link)
                linkedin_scho_['total_followee_count'] = normalize(str(foll_schools_counts))
                if sch_name or sch_link:
                        return linkedin_scho_
                else:
                        return ''


        def get_groups_item(self, sk, grp_desc , grp_link, grp_name, grp_members, grp_id, grp_logo):
                linkedin_groups_ = Linkedingroups()
                linkedin_groups_['sk'] = md5("%s%s%s%s%s"%(sk, grp_link, grp_name, grp_members, grp_id))
                linkedin_groups_['profile_sk'] = normalize(sk)
                linkedin_groups_['group_link'] = normalize(grp_link)
                linkedin_groups_['group_name'] = normalize(grp_name)
                linkedin_groups_['no_of_members'] = normalize(grp_members)
                linkedin_groups_['group_logo'] = normalize(grp_logo)
                linkedin_groups_['group_id'] = normalize(str(grp_id))
                linkedin_groups_['group_description'] = normalize(grp_desc)
                if grp_link or grp_name or grp_members or grp_id:
                        return linkedin_groups_
                else:
                        return ''



