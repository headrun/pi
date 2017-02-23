create table source(
src_id int not null auto_increment primary key,
source_id int(100) not null,
name varchar(100) not null,
is_active tinyint(1) not null DEFAULT 1,
`created_at` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
`modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
`deactivated_at` datetime NOT NULL,
KEY (`source_id`,`name`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci

create table indent(
  `indent_id` int(11) NOT NULL AUTO_INCREMENT primary key,
  `src_id` int not null ,
  `number` varchar(100) DEFAULT NULL,
  `factory` varchar(100) NOT NULL,
  `transporter_name` varchar(255) NOT NULL,
  `depot` varchar(100) NOT NULL,
  `proposed_vehicle_type` varchar(255) NOT NULL,
  `actual_vehicle_type` varchar(255) DEFAULT NULL,
  `vehicle_number` varchar(100) DEFAULT NULL,
  `driver_mobile_number` varchar(255) DEFAULT NULL,
  `vehicle_req_date` datetime NOT NULL,
  `trucks_needed` int(11) DEFAULT 1,
  `order_status` tinyint(1) DEFAULT 0,
  `source_date` varchar(255) NOT NULL,
  `source_mail_id` varchar(100) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY genuine(`number`,`vehicle_req_date`,`factory`,`depot`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci


ALTER TABLE indent modify COLUMN src_id INT NOT NULL, ADD CONSTRAINT source_indent_fk FOREIGN KEY(src_id)  REFERENCES source(src_id);
