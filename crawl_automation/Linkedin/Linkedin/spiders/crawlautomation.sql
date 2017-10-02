-- MySQL dump 10.13  Distrib 5.5.54, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: CRAWL_AUTOMATION
-- ------------------------------------------------------
-- Server version	5.5.54-0ubuntu0.14.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `linkedin_certifications`
--

DROP TABLE IF EXISTS `linkedin_certifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `linkedin_certifications` (
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
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `linkedin_courserecommendations`
--

DROP TABLE IF EXISTS `linkedin_courserecommendations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `linkedin_courserecommendations` (
  `sk` varchar(25) NOT NULL DEFAULT '',
  `profile_sk` varchar(25) NOT NULL DEFAULT '',
  `course_title` text CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `duration_seconds` varchar(10) NOT NULL DEFAULT '',
  `duration_minutes` varchar(10) NOT NULL DEFAULT '',
  `duration_hrs` varchar(10) NOT NULL DEFAULT '',
  `no_of_viewers` varchar(10) NOT NULL DEFAULT '',
  `course_image` text CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `course_url` text CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `created_at` datetime NOT NULL,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_seen` datetime NOT NULL,
  PRIMARY KEY (`sk`),
  KEY `sk` (`sk`,`profile_sk`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `linkedin_courses`
--

DROP TABLE IF EXISTS `linkedin_courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `linkedin_courses` (
  `sk` varchar(35) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `profile_sk` varchar(35) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `course_name` text COLLATE utf8_unicode_ci,
  `course_number` varchar(25) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `created_at` datetime NOT NULL,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_seen` datetime NOT NULL,
  PRIMARY KEY (`sk`),
  KEY `sk` (`sk`,`profile_sk`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `linkedin_crawl`
--

DROP TABLE IF EXISTS `linkedin_crawl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `linkedin_crawl` (
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
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `linkedin_educations`
--

DROP TABLE IF EXISTS `linkedin_educations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `linkedin_educations` (
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
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `linkedin_experiences`
--

DROP TABLE IF EXISTS `linkedin_experiences`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `linkedin_experiences` (
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
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `linkedin_following_channels`
--

DROP TABLE IF EXISTS `linkedin_following_channels`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `linkedin_following_channels` (
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
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `linkedin_following_companies`
--

DROP TABLE IF EXISTS `linkedin_following_companies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `linkedin_following_companies` (
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
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `linkedin_following_influencers`
--

DROP TABLE IF EXISTS `linkedin_following_influencers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `linkedin_following_influencers` (
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
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `linkedin_following_schools`
--

DROP TABLE IF EXISTS `linkedin_following_schools`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `linkedin_following_schools` (
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
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `linkedin_given_recommendations`
--

DROP TABLE IF EXISTS `linkedin_given_recommendations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `linkedin_given_recommendations` (
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
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `linkedin_groups`
--

DROP TABLE IF EXISTS `linkedin_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `linkedin_groups` (
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
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `linkedin_honors`
--

DROP TABLE IF EXISTS `linkedin_honors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `linkedin_honors` (
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
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `linkedin_loginlimit`
--

DROP TABLE IF EXISTS `linkedin_loginlimit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `linkedin_loginlimit` (
  `sk` varchar(35) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `login_mail_id` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `count` int(25) DEFAULT '0',
  `login_date` datetime NOT NULL,
  `proxy_ip` varchar(50) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `created_at` datetime NOT NULL,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_seen` datetime NOT NULL,
  PRIMARY KEY (`sk`,`login_date`,`proxy_ip`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `linkedin_meta`
--

DROP TABLE IF EXISTS `linkedin_meta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `linkedin_meta` (
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
  `location_postal_code` varchar(10) COLLATE utf8_unicode_ci DEFAULT '',
  `location_country_code` varchar(10) COLLATE utf8_unicode_ci DEFAULT '',
  `background_image` text COLLATE utf8_unicode_ci,
  `image_path` text COLLATE utf8_unicode_ci,
  `created_at` datetime NOT NULL,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_seen` datetime NOT NULL,
  PRIMARY KEY (`sk`),
  KEY `sk` (`sk`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `linkedin_metaconnections`
--

DROP TABLE IF EXISTS `linkedin_metaconnections`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `linkedin_metaconnections` (
  `sk` varchar(25) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `profile_url` text COLLATE utf8_unicode_ci,
  `profileview_url` text COLLATE utf8_unicode_ci,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `first_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `last_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `member_id` varchar(25) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `headline` text COLLATE utf8_unicode_ci,
  `no_of_followers` varchar(20) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `profile_post_url` text COLLATE utf8_unicode_ci,
  `summary` text COLLATE utf8_unicode_ci,
  `number_of_connections` varchar(15) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `industry` text COLLATE utf8_unicode_ci,
  `location` text COLLATE utf8_unicode_ci,
  `languages` text COLLATE utf8_unicode_ci,
  `emails` text COLLATE utf8_unicode_ci,
  `websites` text COLLATE utf8_unicode_ci,
  `addresses` text COLLATE utf8_unicode_ci,
  `message_handles` text COLLATE utf8_unicode_ci,
  `phone_numbers` text COLLATE utf8_unicode_ci,
  `birthday` text COLLATE utf8_unicode_ci,
  `birth_year` text COLLATE utf8_unicode_ci,
  `birth_month` text COLLATE utf8_unicode_ci,
  `twitter_accounts` text COLLATE utf8_unicode_ci,
  `profile_image` text COLLATE utf8_unicode_ci,
  `interests` text COLLATE utf8_unicode_ci,
  `created_at` datetime NOT NULL,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_seen` datetime NOT NULL,
  PRIMARY KEY (`sk`),
  KEY `sk` (`sk`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `linkedin_organizations`
--

DROP TABLE IF EXISTS `linkedin_organizations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `linkedin_organizations` (
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
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `linkedin_posts`
--

DROP TABLE IF EXISTS `linkedin_posts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `linkedin_posts` (
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
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `linkedin_profiles`
--

DROP TABLE IF EXISTS `linkedin_profiles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `linkedin_profiles` (
  `sk` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `name` varchar(512) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `aux_info` text COLLATE utf8_unicode_ci,
  `connections` text COLLATE utf8_unicode_ci,
  `profile_url` text COLLATE utf8_unicode_ci,
  `created_at` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`sk`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `linkedin_projects`
--

DROP TABLE IF EXISTS `linkedin_projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `linkedin_projects` (
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
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `linkedin_publications`
--

DROP TABLE IF EXISTS `linkedin_publications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `linkedin_publications` (
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
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `linkedin_received_recommendations`
--

DROP TABLE IF EXISTS `linkedin_received_recommendations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `linkedin_received_recommendations` (
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
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `linkedin_skills`
--

DROP TABLE IF EXISTS `linkedin_skills`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `linkedin_skills` (
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
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `linkedin_testscore`
--

DROP TABLE IF EXISTS `linkedin_testscore`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `linkedin_testscore` (
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
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `linkedin_track`
--

DROP TABLE IF EXISTS `linkedin_track`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `linkedin_track` (
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
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `linkedin_volunteer_experiences`
--

DROP TABLE IF EXISTS `linkedin_volunteer_experiences`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `linkedin_volunteer_experiences` (
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
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-09-18  8:21:48
