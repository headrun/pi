linkedin_comments = """CREATE TABLE `Linkedin_comments` (
  `comment_sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `comment_main_sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `keyword_sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `comment_by` text COLLATE utf8_unicode_ci,
  `comment_datetime` text COLLATE utf8_unicode_ci,
  `commenter_by_image` text COLLATE utf8_unicode_ci,
  `commenter_by_public_url` text COLLATE utf8_unicode_ci,
  `comment_description` text COLLATE utf8_unicode_ci,
  `commenter_headline` text COLLATE utf8_unicode_ci,
  `commenter_member_token` text COLLATE utf8_unicode_ci,
  `comment_total_likes` text COLLATE utf8_unicode_ci,
  `comment_count` text COLLATE utf8_unicode_ci,
  `reference_url` text COLLATE utf8_unicode_ci,
  `keyword_url` text COLLATE utf8_unicode_ci,
  `aux_info` text COLLATE utf8_unicode_ci,
  `created_at` datetime DEFAULT NULL,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`comment_sk`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci """

linkedin_replies = """  CREATE TABLE `Linkedin_replies` (
  `sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `comment_sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `comment_main_sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `keyword_sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `reply_by` text COLLATE utf8_unicode_ci,
  `reply_datetime` text COLLATE utf8_unicode_ci,
  `replier_by_image` text COLLATE utf8_unicode_ci,
  `replier_by_public_url` text COLLATE utf8_unicode_ci,
  `reply_text` text COLLATE utf8_unicode_ci,
  `replier_headline` text COLLATE utf8_unicode_ci,
  `replier_member_token` text COLLATE utf8_unicode_ci,
  `reply_total_likes` text COLLATE utf8_unicode_ci,
  `reply_count` text COLLATE utf8_unicode_ci,
  `reference_url` text COLLATE utf8_unicode_ci,
  `keyword_url` text COLLATE utf8_unicode_ci,
  `aux_info` text COLLATE utf8_unicode_ci,
  `created_at` datetime DEFAULT NULL,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`sk`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

linkedin_crawl = """ CREATE TABLE `comments_crawl` (
  `sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
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
