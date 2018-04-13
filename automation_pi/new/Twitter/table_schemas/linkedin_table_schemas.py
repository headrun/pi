linkedin_meta = """CREATE TABLE `linkedin_meta` (
  `sk` varchar(35) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `profile_url` text COLLATE utf8_unicode_ci,
  `profileview_url` text COLLATE utf8_unicode_ci,
  `name` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `first_name` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `last_name` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `member_id` int(20) DEFAULT '0',
  `headline` text COLLATE utf8_unicode_ci,
  `no_of_followers` int(20) DEFAULT '0',
  `profile_post_url` text COLLATE utf8_unicode_ci,
  `summary` text COLLATE utf8_unicode_ci,
  `number_of_connections` int(20) DEFAULT '0',
  `industry` text COLLATE utf8_unicode_ci,
  `location` text COLLATE utf8_unicode_ci,
  `languages` text COLLATE utf8_unicode_ci,
  `emails` text COLLATE utf8_unicode_ci,
  `websites` text COLLATE utf8_unicode_ci,
  `addresses` text COLLATE utf8_unicode_ci,
  `message_handles` text COLLATE utf8_unicode_ci,
  `phone_numbers` text COLLATE utf8_unicode_ci,
  `birthday` varchar(100) COLLATE utf8_unicode_ci DEFAULT '',
  `birth_year` varchar(100) COLLATE utf8_unicode_ci DEFAULT '',
  `birth_month` varchar(100) COLLATE utf8_unicode_ci DEFAULT '',
  `twitter_accounts` text COLLATE utf8_unicode_ci,
  `profile_image` text COLLATE utf8_unicode_ci,
  `interests` text COLLATE utf8_unicode_ci,
  `location_postal_code` int(20) DEFAULT '0',
  `location_country_code` varchar(10) COLLATE utf8_unicode_ci DEFAULT '',
  `background_image` text COLLATE utf8_unicode_ci,
  `image_path` text COLLATE utf8_unicode_ci,
  `created_at` datetime NOT NULL,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_seen` datetime NOT NULL,
  PRIMARY KEY (`sk`),
  KEY `sk` (`sk`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci """

linkedin_certifications = """ CREATE TABLE `linkedin_certifications` (
  `sk` varchar(35) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `profile_sk` varchar(35) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT '',
  `certification_id` varchar(20) NOT NULL DEFAULT '',
  `certification_date` varchar(20) NOT NULL DEFAULT '',
  `certification_title` text CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `certification_company_logo` text CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `certification_company_name` text CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `certification_license` text CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `created_at` datetime NOT NULL,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_seen` datetime NOT NULL,
  PRIMARY KEY (`sk`),
  KEY `sk` (`sk`,`profile_sk`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

linkedin_courses = """CREATE TABLE `linkedin_courses` (
  `sk` varchar(35) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `profile_sk` varchar(35) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `course_name` text COLLATE utf8_unicode_ci,
  `course_number` varchar(25) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `created_at` datetime NOT NULL,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_seen` datetime NOT NULL,
  PRIMARY KEY (`sk`),
  KEY `sk` (`sk`,`profile_sk`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

linkedin_crawl = """ CREATE TABLE `linkedin_crawl` (
  `sk` varchar(300) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `url` text COLLATE utf8_unicode_ci,
  `crawl_type` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `content_type` varchar(25) COLLATE utf8_unicode_ci NOT NULL,
  `related_type` varchar(50) COLLATE utf8_unicode_ci DEFAULT '',
  `crawl_status` int(3) NOT NULL DEFAULT '0',
  `meta_data` text COLLATE utf8_unicode_ci,
  `created_at` datetime NOT NULL,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`sk`,`content_type`,`crawl_status`),
  KEY `sk` (`sk`),
  KEY `type` (`crawl_type`),
  KEY `type_time` (`crawl_type`,`modified_at`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

linkedin_educations = """ CREATE TABLE `linkedin_educations` (
  `sk` varchar(35) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `profile_sk` varchar(35) COLLATE utf8_unicode_ci DEFAULT '',
  `edu_start_year` varchar(15) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `edu_start_month` varchar(15) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `edu_start_date` varchar(25) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `edu_end_year` varchar(10) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `edu_end_date` varchar(20) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `edu_end_month` varchar(10) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `edu_degree` varchar(500) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `edu_field_of_study` varchar(500) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `edu_school_name` varchar(500) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `school_logo` text COLLATE utf8_unicode_ci,
  `edu_grade` text COLLATE utf8_unicode_ci,
  `edu_activities` text COLLATE utf8_unicode_ci,
  `post_article_id` varchar(25) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `education_id` varchar(25) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `school_id` varchar(25) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `created_at` datetime NOT NULL,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_seen` datetime NOT NULL,
  PRIMARY KEY (`sk`),
  KEY `sk` (`sk`,`profile_sk`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci """

linkedin_experiences = """ CREATE TABLE `linkedin_experiences` (
  `sk` varchar(35) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `profile_sk` varchar(35) COLLATE utf8_unicode_ci DEFAULT '',
  `exp_location` text COLLATE utf8_unicode_ci,
  `exp_company_name` text COLLATE utf8_unicode_ci,
  `exp_company_url` text COLLATE utf8_unicode_ci,
  `exp_title` text COLLATE utf8_unicode_ci,
  `start_date` varchar(20) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `end_date` varchar(20) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `exp_company_logo` text COLLATE utf8_unicode_ci,
  `exp_duration` varchar(20) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `exp_company_id` varchar(20) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `exp_position_id` varchar(20) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `exp_summary` text COLLATE utf8_unicode_ci,
  `created_at` datetime NOT NULL,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_seen` datetime NOT NULL,
  PRIMARY KEY (`sk`),
  KEY `sk` (`sk`,`profile_sk`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

linkedin_following_channels = """CREATE TABLE `linkedin_following_channels` (
  `sk` varchar(35) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `profile_sk` varchar(35) COLLATE utf8_unicode_ci DEFAULT '',
  `channel_followers` int(20) DEFAULT '0',
  `channel_title` text COLLATE utf8_unicode_ci,
  `channel_link` text COLLATE utf8_unicode_ci,
  `channel_image` text COLLATE utf8_unicode_ci,
  `created_at` datetime NOT NULL,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_seen` datetime NOT NULL,
  PRIMARY KEY (`sk`),
  KEY `sk` (`sk`,`profile_sk`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci """

linkedin_following_companies = """CREATE TABLE `linkedin_following_companies` (
  `sk` varchar(35) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `profile_sk` varchar(35) COLLATE utf8_unicode_ci DEFAULT '',
  `company_canonical_name` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `total_followee_count` int(20) DEFAULT '0',
  `company_logo` text COLLATE utf8_unicode_ci,
  `company_universal_name` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `company_url` text COLLATE utf8_unicode_ci,
  `created_at` datetime NOT NULL,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_seen` datetime NOT NULL,
  PRIMARY KEY (`sk`),
  KEY `sk` (`sk`,`profile_sk`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci """

linkedin_following_influencers = """ CREATE TABLE `linkedin_following_influencers` (
  `sk` varchar(35) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `profile_sk` varchar(35) COLLATE utf8_unicode_ci DEFAULT '',
  `inflencer_name` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `influencer_firstname` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `influencer_lastname` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `influencer_image` text COLLATE utf8_unicode_ci,
  `influencer_profile_url` text COLLATE utf8_unicode_ci,
  `influencer_headline` text COLLATE utf8_unicode_ci,
  `influencer_followers_count` int(20) DEFAULT '0',
  `created_at` datetime NOT NULL,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_seen` datetime NOT NULL,
  PRIMARY KEY (`sk`),
  KEY `sk` (`sk`,`profile_sk`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

linkedin_following_schools = """ CREATE TABLE `linkedin_following_schools` (
  `sk` varchar(35) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `profile_sk` varchar(35) COLLATE utf8_unicode_ci DEFAULT '',
  `school_name` text COLLATE utf8_unicode_ci,
  `school_image` text COLLATE utf8_unicode_ci,
  `school_region` text COLLATE utf8_unicode_ci,
  `school_link` text COLLATE utf8_unicode_ci,
  `total_followee_count` int(20) DEFAULT '0',
  `created_at` datetime NOT NULL,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_seen` datetime NOT NULL,
  PRIMARY KEY (`sk`),
  KEY `sk` (`sk`,`profile_sk`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

linkedin_given_recommendations = """ CREATE TABLE `linkedin_given_recommendations` (
  `sk` varchar(35) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `profile_sk` varchar(35) COLLATE utf8_unicode_ci DEFAULT '',
  `last_name` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `name` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `date_and_relationship` text COLLATE utf8_unicode_ci,
  `title` text COLLATE utf8_unicode_ci,
  `created_date` text COLLATE utf8_unicode_ci,
  `summary` text COLLATE utf8_unicode_ci,
  `profile_image` text COLLATE utf8_unicode_ci,
  `profile_member_id` int(20) DEFAULT '0',
  `profile_url` text COLLATE utf8_unicode_ci,
  `recommendation_id` varchar(25) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `created_at` datetime NOT NULL,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_seen` datetime NOT NULL,
  PRIMARY KEY (`sk`),
  KEY `sk` (`sk`,`profile_sk`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

linkedin_groups = """CREATE TABLE `linkedin_groups` (
  `sk` varchar(35) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `profile_sk` varchar(35) COLLATE utf8_unicode_ci DEFAULT '',
  `group_link` text COLLATE utf8_unicode_ci,
  `group_name` text COLLATE utf8_unicode_ci,
  `no_of_members` varchar(25) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `group_logo` text COLLATE utf8_unicode_ci,
  `group_id` varchar(25) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `group_description` text COLLATE utf8_unicode_ci,
  `created_at` datetime NOT NULL,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_seen` datetime NOT NULL,
  PRIMARY KEY (`sk`),
  KEY `sk` (`sk`,`profile_sk`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci """

linkedin_honors = """ CREATE TABLE `linkedin_honors` (
  `sk` varchar(35) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `profile_sk` varchar(35) COLLATE utf8_unicode_ci DEFAULT '',
  `honor_on` varchar(20) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `honor_issuer` text COLLATE utf8_unicode_ci,
  `honor_summary` text COLLATE utf8_unicode_ci,
  `honor_title` text COLLATE utf8_unicode_ci,
  `occupation` text COLLATE utf8_unicode_ci,
  `created_at` datetime NOT NULL,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_seen` datetime NOT NULL,
  PRIMARY KEY (`sk`),
  KEY `sk` (`sk`,`profile_sk`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

linkedin_loginlimit = """ CREATE TABLE `linkedin_loginlimit` (
  `sk` varchar(35) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `login_mail_id` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `count` int(25) DEFAULT '0',
  `login_date` datetime NOT NULL,
  `proxy_ip` varchar(50) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `created_at` datetime NOT NULL,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_seen` datetime NOT NULL,
  PRIMARY KEY (`sk`,`login_date`,`proxy_ip`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

linkedin_organizations = """CREATE TABLE `linkedin_organizations` (
  `sk` varchar(35) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `profile_sk` varchar(35) COLLATE utf8_unicode_ci DEFAULT '',
  `name` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `position` text COLLATE utf8_unicode_ci,
  `start_date` varchar(25) COLLATE utf8_unicode_ci DEFAULT '',
  `end_date` varchar(25) COLLATE utf8_unicode_ci DEFAULT '',
  `description` text COLLATE utf8_unicode_ci,
  `occupation_name` text COLLATE utf8_unicode_ci,
  `created_at` datetime NOT NULL,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_seen` datetime NOT NULL,
  PRIMARY KEY (`sk`),
  KEY `sk` (`sk`,`profile_sk`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci """

linkedin_posts = """CREATE TABLE `linkedin_posts` (
  `sk` varchar(35) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `profile_sk` varchar(35) COLLATE utf8_unicode_ci DEFAULT '',
  `post_url` text COLLATE utf8_unicode_ci,
  `post_image` text COLLATE utf8_unicode_ci,
  `post_title` text COLLATE utf8_unicode_ci,
  `post_author_id` varchar(25) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `post_state` text COLLATE utf8_unicode_ci,
  `post_date` varchar(25) COLLATE utf8_unicode_ci DEFAULT '',
  `post_article_id` varchar(25) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `created_at` datetime NOT NULL,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_seen` datetime NOT NULL,
  PRIMARY KEY (`sk`),
  KEY `sk` (`sk`,`profile_sk`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci """

linkedin_projects = """CREATE TABLE `linkedin_projects` (
  `sk` varchar(35) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `profile_sk` varchar(35) COLLATE utf8_unicode_ci DEFAULT '',
  `project_date` varchar(25) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `number_of_project_members` int(20) DEFAULT '0',
  `project_member_names` text COLLATE utf8_unicode_ci,
  `project_occupation_name` text COLLATE utf8_unicode_ci,
  `project_title` text COLLATE utf8_unicode_ci,
  `project_url` text COLLATE utf8_unicode_ci,
  `project_start_date` varchar(20) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `project_end_date` varchar(20) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `project_description` text COLLATE utf8_unicode_ci,
  `created_at` datetime NOT NULL,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_seen` datetime NOT NULL,
  PRIMARY KEY (`sk`),
  KEY `sk` (`sk`,`profile_sk`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci """

linkedin_publications = """CREATE TABLE `linkedin_publications` (
  `sk` varchar(35) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `profile_sk` varchar(35) COLLATE utf8_unicode_ci DEFAULT '',
  `publication_title` text COLLATE utf8_unicode_ci,
  `publication_url` text COLLATE utf8_unicode_ci,
  `publisher` text COLLATE utf8_unicode_ci,
  `publication_description` text COLLATE utf8_unicode_ci,
  `publication_date` varchar(15) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `created_at` datetime NOT NULL,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_seen` datetime NOT NULL,
  PRIMARY KEY (`sk`),
  KEY `sk` (`sk`,`profile_sk`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

linkedin_received_recommendations = """CREATE TABLE `linkedin_received_recommendations` (
  `sk` varchar(35) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `profile_sk` varchar(35) COLLATE utf8_unicode_ci DEFAULT '',
  `role` varchar(15) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `profile_member_id` int(20) DEFAULT '0',
  `id` varchar(25) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `edu_start_date` varchar(15) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `name` varchar(500) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `organization` text COLLATE utf8_unicode_ci,
  `created_date` varchar(25) COLLATE utf8_unicode_ci DEFAULT '',
  `date_and_relationship` text COLLATE utf8_unicode_ci,
  `headline` text COLLATE utf8_unicode_ci,
  `profile_url` text COLLATE utf8_unicode_ci,
  `profile_image` text COLLATE utf8_unicode_ci,
  `summary` text COLLATE utf8_unicode_ci,
  `created_at` datetime NOT NULL,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_seen` datetime NOT NULL,
  PRIMARY KEY (`sk`),
  KEY `sk` (`sk`,`profile_sk`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

linkedin_skills = """CREATE TABLE `linkedin_skills` (
  `sk` varchar(35) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `profile_sk` varchar(35) COLLATE utf8_unicode_ci DEFAULT '',
  `skill_name` varchar(400) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `endoresement_count` int(20) DEFAULT '0',
  `member_topic_skill_url` text COLLATE utf8_unicode_ci,
  `public_topic_skill_url` text COLLATE utf8_unicode_ci,
  `created_at` datetime NOT NULL,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_seen` datetime NOT NULL,
  PRIMARY KEY (`sk`),
  KEY `sk` (`sk`,`profile_sk`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

linkedin_testscore = """CREATE TABLE `linkedin_testscore` (
  `sk` varchar(35) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `profile_sk` varchar(35) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `testscore_name` text COLLATE utf8_unicode_ci,
  `testscore_description` text COLLATE utf8_unicode_ci,
  `testscore` text COLLATE utf8_unicode_ci,
  `testscore_day` varchar(25) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `testscore_month` varchar(25) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `testscore_year` varchar(25) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `created_at` datetime NOT NULL,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_seen` datetime NOT NULL,
  PRIMARY KEY (`sk`),
  KEY `sk` (`sk`,`profile_sk`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

linkedin_track = """CREATE TABLE `linkedin_track` (
  `sk` varchar(35) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `member_id` int(25) DEFAULT '0',
  `login_mail_id` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `machine_ip` varchar(50) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `crawl_status` int(3) NOT NULL DEFAULT '0',
  `given_key` text COLLATE utf8_unicode_ci,
  `aux_info` text COLLATE utf8_unicode_ci,
  `created_at` datetime NOT NULL,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_seen` datetime NOT NULL,
  PRIMARY KEY (`sk`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

linkedin_volunteer_experiences = """CREATE TABLE `linkedin_volunteer_experiences` (
  `sk` varchar(35) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `profile_sk` varchar(35) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT '',
  `volunteer_interests` text CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `volunteer_role` varchar(255) NOT NULL DEFAULT '',
  `volunteer_cause` text CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `organization_name` text CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `organization_logo` text CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `description` text CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `start_date_year` varchar(15) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT '',
  `start_date_month` varchar(15) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT '',
  `volunteer_date` varchar(15) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT '',
  `end_date_year` varchar(10) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT '',
  `end_date_month` varchar(10) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT '',
  `organization_id` varchar(10) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT '',
  `created_at` datetime NOT NULL,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_seen` datetime NOT NULL,
  PRIMARY KEY (`sk`),
  KEY `sk` (`sk`,`profile_sk`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

LINKEDIN_TABLES = {"linkedin_meta":linkedin_meta,
                    "linkedin_certifications":linkedin_certifications,
                    "linkedin_courses":linkedin_courses,
                    "linkedin_crawl":linkedin_crawl,
                    "linkedin_educations":linkedin_educations,
                    "linkedin_experiences": linkedin_experiences,
                    "linkedin_following_channels":linkedin_following_channels,
                    "linkedin_following_companies": linkedin_following_companies,
                    "linkedin_following_influencers": linkedin_following_influencers,
                    "linkedin_following_schools": linkedin_following_schools,
                    "linkedin_given_recommendations": linkedin_given_recommendations,
                    "linkedin_groups":linkedin_groups,
                    "linkedin_honors":linkedin_honors,
                    "linkedin_loginlimit":linkedin_loginlimit,
                    "linkedin_organizations":linkedin_organizations,
                    "linkedin_posts": linkedin_posts,
                    "linkedin_projects": linkedin_projects,
                    "linkedin_publications": linkedin_publications,
                    "linkedin_received_recommendations": linkedin_received_recommendations,
                    "linkedin_skills": linkedin_skills,
                    "linkedin_testscore" : linkedin_testscore,
                    "linkedin_track":linkedin_track,
                    "linkedin_volunteer_experiences":linkedin_volunteer_experiences}
