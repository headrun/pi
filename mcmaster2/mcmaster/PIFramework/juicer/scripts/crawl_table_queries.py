CRAWL_TABLE_CREATE_QUERY = """
    CREATE TABLE `#CRAWL-TABLE#` (
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

SECTIONS_TABLE_CREATE_QUERY = """
    CREATE TABLE `#SECTION-TABLE#` (
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

# Crawl table related Querires
CRAWL_TABLE_SELECT_QUERY = 'SELECT sk, url, meta_data FROM %s WHERE content_type="%s" AND crawl_status=0 ORDER BY crawl_type DESC LIMIT %s;'

CRAWL_TABLE_QUERY = '(sk, url, meta_data, crawl_type, content_type, related_type, crawl_status, created_at, modified_at) VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW()) ON DUPLICATE KEY UPDATE url=%s, meta_data=%s, crawl_type=%s, crawl_status=%s, modified_at=NOW();'

SECTIONS_TABLE_QUERY = '(sk, section, content_type, created_at) VALUES (%s, %s, %s, NOW());'

UPDATE_QUERY = 'UPDATE %s SET crawl_status=9, modified_at=NOW() WHERE content_type="%s" AND crawl_status=0 AND sk="%s";'
DELETE_QUERY = 'DELETE FROM %s WHERE crawl_status=9 AND content_type="%s" AND sk IN (%s);'

UPDATE_WITH_9_STATUS = 'UPDATE %s SET crawl_status=%s, modified_at=NOW() WHERE crawl_status=9 AND content_type="%s" AND sk="%s";'
DELETE_EXISTING_SKS = 'DELETE FROM %s WHERE crawl_status=%s AND content_type="%s" AND sk IN (%s);'
