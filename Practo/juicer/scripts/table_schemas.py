movie_table = """
    CREATE TABLE `Movie` (
      `sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
      `title` varchar(512) COLLATE utf8_unicode_ci NOT NULL,
      `original_title` varchar(512) COLLATE utf8_unicode_ci NOT NULL,
      `other_titles` text COLLATE utf8_unicode_ci NOT NULL,
      `description` text COLLATE utf8_unicode_ci,
      `genres` text COLLATE utf8_unicode_ci,
      `sub_genres` text COLLATE utf8_unicode_ci,
      `category` text COLLATE utf8_unicode_ci,
      `duration` int(11) DEFAULT '0',
      `languages` text COLLATE utf8_unicode_ci,
      `original_languages` text COLLATE utf8_unicode_ci,
      `metadata_language` text COLLATE utf8_unicode_ci,
      `aka` text COLLATE utf8_unicode_ci,
      `production_country` varchar(200) COLLATE utf8_unicode_ci DEFAULT '',
      `aux_info` text COLLATE utf8_unicode_ci,
      `reference_url` text COLLATE utf8_unicode_ci,
      `created_at` datetime NOT NULL,
      `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      `last_seen` datetime NOT NULL,
      PRIMARY KEY (`sk`)
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
"""

tvshow_table = """
    CREATE TABLE `Tvshow` (
      `sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
      `title` varchar(512) COLLATE utf8_unicode_ci NOT NULL,
      `original_title` varchar(512) COLLATE utf8_unicode_ci NOT NULL,
      `other_titles` text COLLATE utf8_unicode_ci NOT NULL,
      `description` text COLLATE utf8_unicode_ci,
      `genres` text COLLATE utf8_unicode_ci,
      `sub_genres` text COLLATE utf8_unicode_ci,
      `category` text COLLATE utf8_unicode_ci,
      `duration` int(11) DEFAULT '0',
      `languages` text COLLATE utf8_unicode_ci,
      `original_languages` text COLLATE utf8_unicode_ci,
      `metadata_language` text COLLATE utf8_unicode_ci,
      `aka` text COLLATE utf8_unicode_ci,
      `production_country` varchar(200) COLLATE utf8_unicode_ci DEFAULT '',
      `aux_info` text COLLATE utf8_unicode_ci,
      `reference_url` text COLLATE utf8_unicode_ci,
      `created_at` datetime NOT NULL,
      `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      `last_seen` datetime NOT NULL,
      PRIMARY KEY (`sk`)
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
"""

season_table = """
    CREATE TABLE `Season` (
      `sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
      `tvshow_sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
      `title` varchar(512) COLLATE utf8_unicode_ci NOT NULL,
      `original_title` varchar(512) COLLATE utf8_unicode_ci NOT NULL,
      `other_titles` text COLLATE utf8_unicode_ci NOT NULL,
      `description` text COLLATE utf8_unicode_ci,
      `season_number` int(5) DEFAULT '0',
      `genres` text COLLATE utf8_unicode_ci,
      `sub_genres` text COLLATE utf8_unicode_ci,
      `category` text COLLATE utf8_unicode_ci,
      `duration`  int(11) DEFAULT '0',
      `languages` text COLLATE utf8_unicode_ci,
      `original_languages` text COLLATE utf8_unicode_ci,
      `metadata_language` text COLLATE utf8_unicode_ci,
      `aka` text COLLATE utf8_unicode_ci,
      `production_country` varchar(200) COLLATE utf8_unicode_ci DEFAULT '',
      `aux_info` text COLLATE utf8_unicode_ci,
      `reference_url` text COLLATE utf8_unicode_ci,
      `created_at` datetime NOT NULL,
      `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      `last_seen` datetime NOT NULL,
      PRIMARY KEY (`sk`, `tvshow_sk`),
      KEY `season_sk` (`sk`),
      KEY `tvshow_sk` (`tvshow_sk`)
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
"""

episode_table = """
    CREATE TABLE `Episode` (
      `sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
      `season_sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
      `tvshow_sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
      `title` varchar(512) COLLATE utf8_unicode_ci NOT NULL,
      `show_title` varchar(512) COLLATE utf8_unicode_ci NOT NULL,
      `original_title` varchar(512) COLLATE utf8_unicode_ci NOT NULL,
      `other_titles` text COLLATE utf8_unicode_ci NOT NULL,
      `description` text COLLATE utf8_unicode_ci,
      `episode_number` int(11) DEFAULT '0',
      `season_number`  int(11) DEFAULT '0',
      `genres` text COLLATE utf8_unicode_ci,
      `sub_genres` text COLLATE utf8_unicode_ci,
      `category` text COLLATE utf8_unicode_ci,
      `duration` int(11) DEFAULT '0',
      `languages` text COLLATE utf8_unicode_ci,
      `original_languages` text COLLATE utf8_unicode_ci,
      `metadata_language` text COLLATE utf8_unicode_ci,
      `aka` text COLLATE utf8_unicode_ci,
      `production_country` varchar(200) COLLATE utf8_unicode_ci DEFAULT '',
      `aux_info` text COLLATE utf8_unicode_ci,
      `reference_url` text COLLATE utf8_unicode_ci,
      `created_at` datetime NOT NULL,
      `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      `last_seen` datetime NOT NULL,
      PRIMARY KEY (`sk`),
      KEY `episode_sk` (`sk`),
      KEY `season_sk` (`season_sk`),
      KEY `tvshow_sk` (`tvshow_sk`)
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
"""

other_media_table = """
    CREATE TABLE `OtherMedia` (
      `sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
      `program_sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
      `program_type` varchar(25) COLLATE utf8_unicode_ci NOT NULL,
      `media_type` varchar(25) COLLATE utf8_unicode_ci DEFAULT '',
      `title` varchar(512) COLLATE utf8_unicode_ci NOT NULL,
      `description` text COLLATE utf8_unicode_ci,
      `genres` text COLLATE utf8_unicode_ci,
      `sub_genres` text COLLATE utf8_unicode_ci,
      `duration` int(11) DEFAULT '0',
      `languages` text COLLATE utf8_unicode_ci,
      `original_languages` text COLLATE utf8_unicode_ci,
      `metadata_language` text COLLATE utf8_unicode_ci,
      `aka` text COLLATE utf8_unicode_ci,
      `production_country` varchar(200) COLLATE utf8_unicode_ci DEFAULT '',
      `aux_info` text COLLATE utf8_unicode_ci,
      `reference_url` text COLLATE utf8_unicode_ci,
      `created_at` datetime NOT NULL,
      `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      `last_seen` datetime NOT NULL,
      PRIMARY KEY (`sk`, `program_sk`, `program_type`),
      KEY `other_media_sk` (`sk`),
      KEY `program_sk` (`program_sk`),
      KEY `program_sk_type` (`program_sk`,`program_type`)
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
"""

related_programs_table = """
    CREATE TABLE `RelatedPrograms` (
      `program_sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
      `program_type` varchar(25) COLLATE utf8_unicode_ci NOT NULL,
      `related_sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
      `related_rank` int(5) DEFAULT '0',
      `created_at` datetime NOT NULL,
      `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      `last_seen` datetime NOT NULL,
      PRIMARY KEY (`program_sk`,`program_type`,`related_sk`),
      KEY `rel_prgms_program_sk_type` (`program_sk`,`program_type`)
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
"""

richmedia_table = """
    CREATE TABLE `RichMedia` (
      `sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
      `program_sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
      `program_type` varchar(25) COLLATE utf8_unicode_ci NOT NULL,
      `media_type` varchar(50) COLLATE utf8_unicode_ci DEFAULT '',
      `image_type` varchar(25) COLLATE utf8_unicode_ci DEFAULT '',
      `size` varchar(50) COLLATE utf8_unicode_ci DEFAULT '',
      `dimensions` varchar(15) COLLATE utf8_unicode_ci DEFAULT '',
      `description` text COLLATE utf8_unicode_ci,
      `image_url` text COLLATE utf8_unicode_ci,
      `reference_url` text COLLATE utf8_unicode_ci,
      `aux_info` text COLLATE utf8_unicode_ci,
      `created_at` datetime NOT NULL,
      `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      `last_seen` datetime NOT NULL,
      PRIMARY KEY (`sk`,`program_sk`,`program_type`),
      KEY `richmedia_sk` (`sk`),
      KEY `richmedia_program_sk_type` (`program_sk`,`program_type`)
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
"""

program_relases_table = """
    CREATE TABLE `ProgramReleases` (
      `program_sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
      `program_type` varchar(25) COLLATE utf8_unicode_ci NOT NULL,
      `company_name` varchar(150) COLLATE utf8_unicode_ci NOT NULL,
      `region` varchar(25) COLLATE utf8_unicode_ci DEFAULT '',
      `relation` varchar(25) COLLATE utf8_unicode_ci DEFAULT '',
      `company_rights` text COLLATE utf8_unicode_ci,
      `release_date` date DEFAULT '0000-00-00',
      `release_year` int(4) NOT NULL DEFAULT '0',
      `country` varchar(25) COLLATE utf8_unicode_ci DEFAULT '',
      `studio` varchar(50) COLLATE utf8_unicode_ci DEFAULT '',
      `is_imax` int(1) DEFAULT '0',
      `is_giant_screens` int(1) DEFAULT '0',
      `aux_info` text COLLATE utf8_unicode_ci,
      `created_at` datetime NOT NULL,
      `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      `last_seen` datetime NOT NULL,
      PRIMARY KEY (`program_sk`,`program_type`,`country`,`company_name`,`relation`),
      KEY `prgm_releases_program_sk_type` (`program_sk`,`program_type`),
      KEY `prgm_releases_country` (`country`)
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
"""

crew_table = """
    CREATE TABLE `Crew` (
      `sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
      `name` varchar(512) COLLATE utf8_unicode_ci NOT NULL,
      `original_name` varchar(512) COLLATE utf8_unicode_ci NOT NULL,
      `description` text COLLATE utf8_unicode_ci,
      `aka` text COLLATE utf8_unicode_ci,
      `gender` varchar(5) COLLATE utf8_unicode_ci DEFAULT '',
      `age` int(4) DEFAULT '0', 
      `blood_group` varchar(5) COLLATE utf8_unicode_ci DEFAULT '',
      `birth_date` date DEFAULT '0000-00-00',
      `birth_place` varchar(100) COLLATE utf8_unicode_ci DEFAULT '',
      `death_date` date DEFAULT '0000-00-00',
      `death_place` varchar(512) COLLATE utf8_unicode_ci DEFAULT '',
      `constellation` varchar(100) COLLATE utf8_unicode_ci DEFAULT '',
      `country` varchar(100) COLLATE utf8_unicode_ci DEFAULT '',
      `occupation` varchar(250) COLLATE utf8_unicode_ci DEFAULT '',
      `biography` text COLLATE utf8_unicode_ci,
      `height` varchar(10) COLLATE utf8_unicode_ci DEFAULT '',
      `weight` varchar(10) COLLATE utf8_unicode_ci DEFAULT '',
      `rating` float(6,2) DEFAULT '0.0',
      `top_rated_works` text COLLATE utf8_unicode_ci,
      `num_of_ratings` int(11) DEFAULT '0',
      `family_members` varchar(512) COLLATE utf8_unicode_ci DEFAULT '',
      `recent_films` text COLLATE utf8_unicode_ci,
      `image` text COLLATE utf8_unicode_ci,
      `videos` text COLLATE utf8_unicode_ci,
      `reference_url` text COLLATE utf8_unicode_ci,
      `aux_info` text COLLATE utf8_unicode_ci,
      `created_at` datetime NOT NULL,
      `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
      `last_seen` datetime NOT NULL,
      PRIMARY KEY (`sk`)
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
"""

program_crew_table = """
    CREATE TABLE `ProgramCrew` (
      `program_sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
      `program_type` varchar(25) COLLATE utf8_unicode_ci NOT NULL,
      `crew_sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
      `role` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
      `description` text COLLATE utf8_unicode_ci,
      `role_title` varchar(512) COLLATE utf8_unicode_ci DEFAULT '',
      `rank` int(5) DEFAULT '0',
      `aux_info` text COLLATE utf8_unicode_ci,
      `created_at` datetime NOT NULL,
      `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
      `last_seen` datetime NOT NULL,
      PRIMARY KEY (`program_sk`,`program_type`,`crew_sk`,`role`),
      KEY `crew_sk` (`crew_sk`),
      KEY `prgm_crew_program_sk_type` (`program_sk`,`program_type`)
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
"""

news_table = """
    CREATE TABLE `News` (
      `sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
      `program_sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
      `program_type` varchar(25) COLLATE utf8_unicode_ci NOT NULL,
      `title` varchar(512) COLLATE utf8_unicode_ci NOT NULL,
      `description` text COLLATE utf8_unicode_ci,
      `published_at` datetime DEFAULT '0000-00-00 00:00:00',
      `reference_url` text COLLATE utf8_unicode_ci,
      `aux_info` text COLLATE utf8_unicode_ci,
      `created_at` datetime NOT NULL,
      `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      `last_seen` datetime NOT NULL,
      PRIMARY KEY (`sk`,`program_sk`,`program_type`),
      KEY `news_program_sk_type` (`program_sk`,`program_type`)
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
"""

award_table = """
    CREATE TABLE `Award` (
      `program_sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
      `program_type` varchar(25) COLLATE utf8_unicode_ci NOT NULL,
      `award_name` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
      `award_category` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
      `year` int(4) NOT NULL DEFAULT '0',
      `winner` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
      `winner_sk` varchar(110) COLLATE utf8_unicode_ci NOT NULL,
      `winner_type` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
      `winner_flag` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
      `aux_info` text COLLATE utf8_unicode_ci,
      `created_at` datetime NOT NULL,
      `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      `last_seen` datetime NOT NULL,
      PRIMARY KEY (`program_sk`,`program_type`,`award_category`,`year`,`winner_sk`),
      KEY `award_program_sk_type` (`program_sk`,`program_type`)
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
"""

popularity_table = """
    CREATE TABLE `Popularity` (
      `program_sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
      `program_type` varchar(25) COLLATE utf8_unicode_ci NOT NULL,
      `no_of_views` int(11) DEFAULT '0',
      `no_of_ratings` int(11) DEFAULT '0',
      `no_of_reviews` int(11) DEFAULT '0',
      `no_of_comments` int(11) DEFAULT '0',
      `no_of_likes` int(11) DEFAULT '0',
      `no_of_dislikes` int(11) DEFAULT '0',
      `aux_info` text COLLATE utf8_unicode_ci,
      `created_at` datetime NOT NULL,
      `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      `last_seen` datetime NOT NULL,
      PRIMARY KEY (`program_sk`,`program_type`),
      KEY `pop_program_sk_type` (`program_sk`,`program_type`)
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
"""

rating_table = """
	CREATE TABLE `Rating` (   `program_sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,   `program_type` varchar(25) COLLATE utf8_unicode_ci NOT NULL,   `rating` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,   `rating_type` varchar(50) COLLATE utf8_unicode_ci NOT NULL,   `rating_reason` varchar(255) COLLATE utf8_unicode_ci DEFAULT '',   `created_at` datetime NOT NULL,   `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,   `last_seen` datetime DEFAULT NULL,   PRIMARY KEY (`program_sk`,`program_type`,`rating_type`),   KEY `rating_type` (`rating_type`),   KEY `rating_program_sk_type` (`program_sk`,`program_type`) ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
    """

availability_table = """
    CREATE TABLE `Availability` (
      `program_sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
      `program_type` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
      `country_code` varchar(15) COLLATE utf8_unicode_ci NOT NULL,
      `platform_id` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
      `template_id` text COLLATE utf8_unicode_ci,
      `template_values` text COLLATE utf8_unicode_ci NOT NULL,
      `with_subscription` varchar(5) COLLATE utf8_unicode_ci NOT NULL,
      `subscription_type` varchar(40) COLLATE utf8_unicode_ci DEFAULT '',
      `medium_type` varchar(40) COLLATE utf8_unicode_ci DEFAULT '',
      `price_type` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
      `purchase_type` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
      `price` float(6,2) DEFAULT '0.00',
      `price_currency` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
      `duration` int(11) DEFAULT '0',
      `quality` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
      `audio_languages` text COLLATE utf8_unicode_ci NOT NULL,
      `subtitle_languages` text COLLATE utf8_unicode_ci,
      `is_3d` int(1) NOT NULL DEFAULT '0',
      `content_start_timestamp` timestamp DEFAULT '0000-00-00 00:00:00',
      `content_expiry_timestamp` timestamp DEFAULT '0000-00-00 00:00:00',
      `last_refreshed_timestamp` timestamp DEFAULT '0000-00-00 00:00:00',
      `reference_url` text COLLATE utf8_unicode_ci,
      `scraper_args` text COLLATE utf8_unicode_ci NOT NULL,
      `is_valid` int(1) DEFAULT '1',
      `last_modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      PRIMARY KEY (`program_sk`,`program_type`,`with_subscription`,`subscription_type`,`quality`,`platform_id`,`country_code`,`medium_type`,`purchase_type`),
      KEY `avail_program_sk` (`program_sk`),
      KEY `program_content_type` (`program_sk`,`program_type`)
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
"""

charts_table = """
    CREATE TABLE `Charts` (
      `program_sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
      `program_type` varchar(25) COLLATE utf8_unicode_ci NOT NULL,
      `chart_type` varchar(50) COLLATE utf8_unicode_ci DEFAULT '',
      `program_rank` int(5) DEFAULT '0',
      `week_number` int(3) DEFAULT '0',
      `week_end_date` date DEFAULT '0000-00-00',
      `no_of_weeks` int(11) DEFAULT '0',
      `currency` VARCHAR(5) DEFAULT '',
      `present_week_units` int(11) DEFAULT '0',
      `total_units` BIGINT(15) DEFAULT '0',
      `present_week_spending` BIGINT(15) DEFAULT '0',
      `total_spending` BIGINT DEFAULT '0',
      `market_share` FLOAT(6,2) DEFAULT '0.0',
      `reference_url` text COLLATE utf8_unicode_ci,
      `created_at` datetime NOT NULL,
      `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      `last_seen` datetime NOT NULL,
      PRIMARY KEY (`program_sk`,`program_type`,`chart_type`),
      KEY `charts_program_sk_type` (`program_sk`,`program_type`)
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
"""

boxoffice_table = """
    CREATE TABLE `Boxoffice` (
      `program_sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
      `program_rank` int(5) DEFAULT '0',
      `weekend_gross` BIGINT DEFAULT '0',
      `total_gross` BIGINT DEFAULT '0',
      `opening_gross` INT(11) DEFAULT '0',
      `top_ten_gross` BIGINT DEFAULT '0',
      `avg_gross` varchar(50) COLLATE utf8_unicode_ci DEFAULT '0',
      `currency` VARCHAR(5) NOT NULL,
      `location` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
      `no_of_locations` int(11) DEFAULT '0',
      `gross_type` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
      `year` int(4) DEFAULT '0',
      `month` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
      `quarter` int(4) DEFAULT '0',
      `date` date NOT NULL DEFAULT '0000-00-00',
      `weekday` varchar(20) COLLATE utf8_unicode_ci DEFAULT '',
      `day_number` int(4) DEFAULT '0',
      `week_number` int(4) NOT NULL DEFAULT '0',
      `tickets_sold` varchar(50) COLLATE utf8_unicode_ci DEFAULT '0',
      `visitors` int(11) DEFAULT '0',
      `release_strategy` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
      `created_at` datetime DEFAULT NULL,
      `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      `last_seen` datetime NOT NULL,
      PRIMARY KEY (`program_sk`,`year`,`date`,`gross_type`,`month`,`quarter`,`release_strategy`,`day_number`,`week_number`,`location`)
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
"""

review_table = """
    CREATE TABLE `Review` (
      `program_sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
      `program_type` varchar(25) COLLATE utf8_unicode_ci NOT NULL,
      `title` varchar(512) COLLATE utf8_unicode_ci NOT NULL,
      `reviewed_on` datetime DEFAULT '0000-00-00 00:00:00',
      `reviewed_by` varchar(150) COLLATE utf8_unicode_ci DEFAULT '',
      `rating` int(4) DEFAULT '0',
      `review` text COLLATE utf8_unicode_ci,
      `review_url` text COLLATE utf8_unicode_ci,
      `created_at` datetime NOT NULL,
      `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      `last_seen` datetime NOT NULL,
      PRIMARY KEY (`program_sk`,`program_type`,`reviewed_by`,`reviewed_on`),
      KEY `reviews_progam_sk_type` (`program_sk`,`program_type`)
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
"""

theater_table = """
    CREATE TABLE `Theater` (
      `sk` varchar(150) COLLATE utf8_unicode_ci NOT NULL,
      `name` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
      `screen` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
      `location` varchar(100) COLLATE utf8_unicode_ci DEFAULT '',
      `firm_name` varchar(150) COLLATE utf8_unicode_ci DEFAULT '',
      `is_3d` int(1) DEFAULT '0',
      `no_of_rooms` int(5) DEFAULT '0',
      `no_of_seats` int(5) DEFAULT '0',
      `contact_numbers` varchar(250) COLLATE utf8_unicode_ci DEFAULT '',
      `zipcode` int(6) DEFAULT '0',
      `latitude` float(6,3) DEFAULT '0.000',
      `longitude` float(6,3) DEFAULT '0.000',
      `address` text COLLATE utf8_unicode_ci,
      `theater_url` text COLLATE utf8_unicode_ci NOT NULL,
      `created_at` datetime NOT NULL,
      `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      `last_seen` datetime DEFAULT NULL,
      PRIMARY KEY (`sk`,`location`,`screen`),
      KEY `theater_sk` (`sk`)
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
"""

theater_avail_table = """
    CREATE TABLE `TheaterAvailability` (
      `program_sk` varchar(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
      `program_type` varchar(25) COLLATE utf8_unicode_ci NOT NULL,
      `theater_sk` varchar(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
      `show_time` datetime DEFAULT '0000-00-00 00:00:00',
      `ticket_booking_link` text,
      `is_3d` int(1) DEFAULT '0',
      `created_at` datetime DEFAULT NULL,
      `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      `last_seen` datetime DEFAULT NULL,
      PRIMARY KEY (`program_sk`,`theater_sk`),
      KEY `theater_avail_program_sk` (`program_sk`)
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
"""

primetimes_table = """
    CREATE TABLE `Primetimes` (
      `program_sk` varchar(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
      `program_type` varchar(25) CHARACTER SET utf8 COLLATE utf8_unicode_ci,
      `program_title` varchar(512) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
      `report_date` date DEFAULT '0000-00-00',
      `scope` varchar(25) CHARACTER SET utf8 COLLATE utf8_unicode_ci,
      `viewers_count` BIGINT DEFAULT '0',
      `market_share` FLOAT(6,2) DEFAULT '0.0',
      `reference_url` text CHARACTER SET utf8 COLLATE utf8_unicode_ci,
      `created_at` datetime NOT NULL,
      `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      `last_seen` datetime NOT NULL,
      PRIMARY KEY (`program_sk`,`program_type`)
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
"""

program_charts_table = """
    CREATE TABLE `ProgramCharts` (
      `program_sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
      `program_type` varchar(25) COLLATE utf8_unicode_ci NOT NULL,
      `channel_sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
      `program_title` varchar(150) COLLATE utf8_unicode_ci NOT NULL,
      `hour` int(3) DEFAULT '0',
      `minute` int(3) DEFAULT '0',
      `rank` int(5) DEFAULT '0',
      `no_of_views` int(11) DEFAULT '0',
      `votes` int(11) DEFAULT '0',
      `rating` float(6,2) DEFAULT '0.0',
      `weekday` varchar(50) COLLATE utf8_unicode_ci DEFAULT '',
      `week` varchar(50) COLLATE utf8_unicode_ci DEFAULT '',
      `month` varchar(15) COLLATE utf8_unicode_ci DEFAULT '',
      `year` int(4) DEFAULT '0',
      `reference_url` text COLLATE utf8_unicode_ci,
      `created_at` datetime NOT NULL,
      `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      `last_seen` datetime NOT NULL,
      PRIMARY KEY (`program_sk`,`week`,`year`,`month`,`weekday`,`channel_sk`)
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
"""

channel_table = """
    CREATE TABLE `Channel` (
      `sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
      `title` varchar(512) COLLATE utf8_unicode_ci NOT NULL,
      `description` text COLLATE utf8_unicode_ci,
      `genres` text COLLATE utf8_unicode_ci,
      `sub_genres` text COLLATE utf8_unicode_ci,
      `image` text COLLATE utf8_unicode_ci,
      `time_zone_offset` varchar(10) COLLATE utf8_unicode_ci DEFAULT '',
      `reference_url` text COLLATE utf8_unicode_ci,
      `created_at` datetime NOT NULL,
      `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      `last_seen` datetime NOT NULL,
      PRIMARY KEY (`sk`)
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
"""

channel_charts_table = """
    CREATE TABLE `ChannelCharts` (
      `channel_sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
      `chart_type` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
      `daily_reach_count` int(11) DEFAULT '0',
      `daily_reach_count_in_percentage` float(5,2) DEFAULT '0.0',
      `weekly_reach_count` int(11) DEFAULT '0',
      `weekly_reach_count_in_percentage` float(5,2) DEFAULT '0.0',
      `avg_pp_weekly_viewing` int(11) DEFAULT '0',
      `share` float(5,2) DEFAULT '0.0',
      `week` varchar(100) COLLATE utf8_unicode_ci DEFAULT '',
      `month` varchar(10) COLLATE utf8_unicode_ci DEFAULT '',
      `year` int(4) DEFAULT '0',
      `reference_url` text COLLATE utf8_unicode_ci,
      `created_at` datetime NOT NULL,
      `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      `last_seen` datetime NOT NULL,
      PRIMARY KEY (`channel_sk`,`chart_type`,`week`,`month`),
      KEY `channel_sk_type` (`channel_sk`,`chart_type`)
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
"""

schedule_table = """
    CREATE TABLE `Schedules` (
      `channel_sk` varchar(100) NOT NULL,
      `program_sk` varchar(100) NOT NULL,
      `program_type` varchar(25) NOT NULL,
      `start_datetime` datetime DEFAULT '0000-00-00 00:00:00',
      `duration` int(11) NOT NULL DEFAULT '0',
      `attributes` varchar(100) DEFAULT '',
      `created_at` datetime NOT NULL,
      `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      `last_seen` datetime DEFAULT NULL,
      PRIMARY KEY (`program_sk`,`program_type`,`start_datetime`,`channel_sk`),
      KEY `schedule_program_sk_type` (`program_sk`,`program_type`),
      KEY `schedule_channel_sk` (`channel_sk`)
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
"""

other_links_table = """
    CREATE TABLE `OtherLinks` (
      `sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
      `program_sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
      `program_type` varchar(25) COLLATE utf8_unicode_ci NOT NULL,
      `url_type` varchar(25) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
      `url` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
      `created_at` datetime NOT NULL,
      `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      `last_seen` datetime NOT NULL,
      PRIMARY KEY (`sk`,`program_sk`,`program_type`,`url_type`),
      KEY `otherlinks_program_sk_type` (`sk`),
      KEY `otherlink_type` (`url_type`)
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci
    """

locations_table = """
    CREATE TABLE `Locations` (
      `sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
      `country` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
      `state` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
      `region` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
      `sub_region` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
      `zipcode` int(10) COLLATE utf8_unicode_ci DEFAULT '0',
      `other_id` varchar(20) COLLATE utf8_unicode_ci DEFAULT '',
      `created_at` datetime NOT NULL,
      `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      `last_seen` datetime NOT NULL,
      PRIMARY KEY (`sk`)
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
"""

lineup_table = """
    CREATE TABLE `Lineup` (
      `channel_sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
      `location_sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
      `stream_quality` varchar(5) DEFAULT NULL COLLATE utf8_unicode_ci,
      `tuner_number` int(11) NOT NULL DEFAULT '0',
      `created_at` datetime NOT NULL,
      `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      `last_seen` datetime NOT NULL,
      PRIMARY KEY (`channel_sk`,`location_sk`,`tuner_number`)
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE utf8_unicode_ci;
"""

created_table = """
    CREATE TABLE `created_info` (
          `program_sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
          `program_type` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
          `created_at` datetime NOT NULL,
          PRIMARY KEY (`program_sk`, `program_type`),
          KEY `sk_type` (`program_sk`, `program_type`)
        ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
"""

crawl_table = """
    CREATE TABLE `<CRAWL_TABLE>` (
      `sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
      `url` text COLLATE utf8_unicode_ci,
      `crawl_type` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
      `content_type` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
      `related_type` varchar(50) COLLATE utf8_unicode_ci NULL DEFAULT '',
      `crawl_status` int(3) COLLATE utf8_unicode_ci NOT NULL DEFAULT '0',
      `meta_data` text COLLATE utf8_unicode_ci,
      `created_at` datetime NOT NULL,
      `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      PRIMARY KEY (`sk`,`content_type`,`crawl_status`),
      KEY `sk` (`sk`),
      KEY `type` (`crawl_type`),
      KEY `type_time` (`crawl_type`,`modified_at`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE utf8_unicode_ci;
"""

sections_table = """
    CREATE TABLE `<SECTION_TABLE>` (
      `sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
      `section` varchar(200) COLLATE utf8_unicode_ci DEFAULT '',
      `content_type` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
      `rank` int(5) DEFAULT '0',
      `created_at` datetime NOT NULL,
      `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      PRIMARY KEY (`sk`,`section`,`content_type`),
      KEY `sk` (`sk`),
      KEY `type` (`content_type`),
      KEY `type_time` (`content_type`,`created_at`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE utf8_unicode_ci;
"""

TABLES = {
    'movie': movie_table, 'tvshow': tvshow_table, 'season': season_table, 'episode': episode_table,
    'other_media': other_media_table, 'releated_programs': related_programs_table, 'rich_media': richmedia_table,
    'program_releases': program_relases_table, 'crew': crew_table, 'program_crew': program_crew_table,
    'news': news_table, 'award': award_table, 'popularity': popularity_table, 'rating': rating_table,
    'availability': availability_table, 'charts': charts_table, 'boxoffice': boxoffice_table, 'review': review_table,
    'theater': theater_table, 'theater_availability': theater_avail_table, 'primetimes': primetimes_table,
    'program_charts': program_charts_table, 'channel': channel_table, 'channel_charts': channel_charts_table,
    'schedule': schedule_table, 'other_links': other_links_table, 'locations': locations_table, 'lineup': lineup_table,
    'created_info': created_info
}
