profile_details  = """CREATE TABLE `profile_details` (
  `sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `name` varchar(512) COLLATE utf8_unicode_ci NOT NULL,
  `family_name` varchar(512) COLLATE utf8_unicode_ci NOT NULL,
  `websites` text COLLATE utf8_unicode_ci,
  `age` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `gender` varchar(150) COLLATE utf8_unicode_ci NOT NULL,
  `country` varchar(150) COLLATE utf8_unicode_ci NOT NULL,
  `state` varchar(150) COLLATE utf8_unicode_ci NOT NULL,
  `city` varchar(150) COLLATE utf8_unicode_ci NOT NULL,
  `continent` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `location` varchar(300) COLLATE utf8_unicode_ci NOT NULL,
  `likelihood` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `created_at` datetime NOT NULL,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `last_seen` datetime NOT NULL,
  PRIMARY KEY (`sk`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci """

social_profiles = """ CREATE TABLE `social_profiles` (
  `sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `profile_sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `name` varchar(512) COLLATE utf8_unicode_ci NOT NULL,
  `biography` text COLLATE utf8_unicode_ci,
  `type_name` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `followers` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `profile_url` text COLLATE utf8_unicode_ci,
  `created_at` datetime NOT NULL,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `last_seen` datetime NOT NULL,
  PRIMARY KEY (`sk`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci """

RichMedia = """ CREATE TABLE `RichMedia` (
  `sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `profile_sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `type_name` varchar(25) COLLATE utf8_unicode_ci NOT NULL,
  `image_url` text COLLATE utf8_unicode_ci,
  `created_at` datetime NOT NULL,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `last_seen` datetime NOT NULL,
  PRIMARY KEY (`sk`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci """

organizations = """ CREATE TABLE `organizations` (
  `sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `profile_sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `organization` text COLLATE utf8_unicode_ci,
  `headline` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `is_current` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `start_date` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `end_date` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `created_at` datetime NOT NULL,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `last_seen` datetime NOT NULL,
  PRIMARY KEY (`sk`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci """

TABLES = {"organizations":organizations,
        'RichMedia':RichMedia,
        "profile_details":profile_details,
        "social_profiles":social_profiles}
