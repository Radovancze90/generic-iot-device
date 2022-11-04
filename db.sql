-- Adminer 4.8.1 MySQL 5.5.5-10.5.17-MariaDB-1:10.5.17+maria~ubu2004 dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_czech_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_czech_ci;


DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_czech_ci;


DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_czech_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_czech_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_czech_ci;

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1,	'Can add log entry',	1,	'add_logentry'),
(2,	'Can change log entry',	1,	'change_logentry'),
(3,	'Can delete log entry',	1,	'delete_logentry'),
(4,	'Can view log entry',	1,	'view_logentry'),
(5,	'Can add permission',	2,	'add_permission'),
(6,	'Can change permission',	2,	'change_permission'),
(7,	'Can delete permission',	2,	'delete_permission'),
(8,	'Can view permission',	2,	'view_permission'),
(9,	'Can add group',	3,	'add_group'),
(10,	'Can change group',	3,	'change_group'),
(11,	'Can delete group',	3,	'delete_group'),
(12,	'Can view group',	3,	'view_group'),
(13,	'Can add user',	4,	'add_user'),
(14,	'Can change user',	4,	'change_user'),
(15,	'Can delete user',	4,	'delete_user'),
(16,	'Can view user',	4,	'view_user'),
(17,	'Can add content type',	5,	'add_contenttype'),
(18,	'Can change content type',	5,	'change_contenttype'),
(19,	'Can delete content type',	5,	'delete_contenttype'),
(20,	'Can view content type',	5,	'view_contenttype'),
(21,	'Can add session',	6,	'add_session'),
(22,	'Can change session',	6,	'change_session'),
(23,	'Can delete session',	6,	'delete_session'),
(24,	'Can view session',	6,	'view_session'),
(25,	'Can add device log',	7,	'add_devicelog'),
(26,	'Can change device log',	7,	'change_devicelog'),
(27,	'Can delete device log',	7,	'delete_devicelog'),
(28,	'Can view device log',	7,	'view_devicelog'),
(29,	'Can add device action',	8,	'add_deviceaction'),
(30,	'Can change device action',	8,	'change_deviceaction'),
(31,	'Can delete device action',	8,	'delete_deviceaction'),
(32,	'Can view device action',	8,	'view_deviceaction'),
(33,	'Can add device',	9,	'add_device'),
(34,	'Can change device',	9,	'change_device'),
(35,	'Can delete device',	9,	'delete_device'),
(36,	'Can view device',	9,	'view_device'),
(37,	'Can add user device',	10,	'add_userdevice'),
(38,	'Can change user device',	10,	'change_userdevice'),
(39,	'Can delete user device',	10,	'delete_userdevice'),
(40,	'Can view user device',	10,	'view_userdevice'),
(41,	'Can add user profile',	11,	'add_userprofile'),
(42,	'Can change user profile',	11,	'change_userprofile'),
(43,	'Can delete user profile',	11,	'delete_userprofile'),
(44,	'Can view user profile',	11,	'view_userprofile'),
(45,	'Can add user terms and conditions',	12,	'add_usertermsandconditions'),
(46,	'Can change user terms and conditions',	12,	'change_usertermsandconditions'),
(47,	'Can delete user terms and conditions',	12,	'delete_usertermsandconditions'),
(48,	'Can view user terms and conditions',	12,	'view_usertermsandconditions'),
(49,	'Can add device cron',	13,	'add_devicecron'),
(50,	'Can change device cron',	13,	'change_devicecron'),
(51,	'Can delete device cron',	13,	'delete_devicecron'),
(52,	'Can view device cron',	13,	'view_devicecron'),
(53,	'Can add region',	14,	'add_region'),
(54,	'Can change region',	14,	'change_region'),
(55,	'Can delete region',	14,	'delete_region'),
(56,	'Can view region',	14,	'view_region'),
(57,	'Can add client',	15,	'add_client'),
(58,	'Can change client',	15,	'change_client'),
(59,	'Can delete client',	15,	'delete_client'),
(60,	'Can view client',	15,	'view_client');

DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_czech_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_czech_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_czech_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_czech_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_czech_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_czech_ci;


DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_czech_ci;


DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_czech_ci;


DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_czech_ci DEFAULT NULL,
  `object_repr` varchar(200) COLLATE utf8mb4_czech_ci NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext COLLATE utf8mb4_czech_ci NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_czech_ci;


DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_czech_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_czech_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_czech_ci;


DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_czech_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_czech_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_czech_ci;

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1,	'contenttypes',	'0001_initial',	'2021-03-03 19:56:38.365333'),
(2,	'auth',	'0001_initial',	'2021-03-03 19:56:42.995586'),
(3,	'admin',	'0001_initial',	'2021-03-03 19:57:02.752652'),
(4,	'admin',	'0002_logentry_remove_auto_add',	'2021-03-03 19:57:06.396315'),
(5,	'admin',	'0003_logentry_add_action_flag_choices',	'2021-03-03 19:57:06.453847'),
(6,	'contenttypes',	'0002_remove_content_type_name',	'2021-03-03 19:57:09.391736'),
(7,	'auth',	'0002_alter_permission_name_max_length',	'2021-03-03 19:57:11.232272'),
(8,	'auth',	'0003_alter_user_email_max_length',	'2021-03-03 19:57:12.038078'),
(9,	'auth',	'0004_alter_user_username_opts',	'2021-03-03 19:57:12.177114'),
(10,	'auth',	'0005_alter_user_last_login_null',	'2021-03-03 19:57:13.740971'),
(11,	'auth',	'0006_require_contenttypes_0002',	'2021-03-03 19:57:13.784860'),
(12,	'auth',	'0007_alter_validators_add_error_messages',	'2021-03-03 19:57:13.932860'),
(13,	'auth',	'0008_alter_user_username_max_length',	'2021-03-03 19:57:14.127459'),
(14,	'auth',	'0009_alter_user_last_name_max_length',	'2021-03-03 19:57:14.393141'),
(15,	'auth',	'0010_alter_group_name_max_length',	'2021-03-03 19:57:14.584251'),
(16,	'auth',	'0011_update_proxy_permissions',	'2021-03-03 19:57:14.624462'),
(17,	'auth',	'0012_alter_user_first_name_max_length',	'2021-03-03 19:57:14.816935'),
(18,	'sessions',	'0001_initial',	'2021-03-03 19:57:15.486801'),
(19,	'main',	'0001_initial',	'2021-03-03 20:09:21.956451'),
(20,	'main',	'0002_auto_20210303_2110',	'2021-03-03 20:10:46.684181'),
(21,	'main',	'0003_auto_20210303_2122',	'2021-03-03 20:22:36.502572'),
(22,	'main',	'0004_userdevice',	'2021-03-07 12:40:48.019067'),
(23,	'main',	'0005_auto_20210314_1128',	'2021-03-14 10:28:22.726603'),
(24,	'main',	'0006_auto_20210314_1942',	'2021-03-14 18:42:47.066167'),
(25,	'main',	'0007_auto_20210323_1454',	'2021-03-23 13:54:33.684880'),
(26,	'main',	'0008_auto_20210323_1627',	'2021-03-23 15:27:58.991388'),
(27,	'main',	'0009_auto_20210324_1542',	'2021-03-24 14:42:42.448027'),
(28,	'main',	'0010_devicecron',	'2021-03-24 15:19:26.931918'),
(29,	'main',	'0011_auto_20210329_1135',	'2021-03-29 09:36:02.719432'),
(30,	'main',	'0012_auto_20210329_1139',	'2021-03-29 09:39:21.502029'),
(31,	'main',	'0013_region',	'2021-03-29 13:25:10.234910'),
(32,	'main',	'0014_device_name',	'2021-03-29 16:11:11.562969'),
(33,	'main',	'0015_client',	'2021-03-31 15:21:31.004826'),
(34,	'main',	'0016_device_outage_report_for',	'2021-08-24 17:53:39.104945'),
(35,	'main',	'0017_userdevice_outage_notification',	'2021-09-14 15:21:37.238456'),
(36,	'main',	'0018_client_outage_notification',	'2021-09-14 15:21:37.283456'),
(37,	'main',	'0019_alter_client_outage_notification',	'2021-10-19 18:40:08.332387');

DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_czech_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_czech_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_czech_ci;


DROP TABLE IF EXISTS `main_client`;
CREATE TABLE `main_client` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `phone` varchar(100) COLLATE utf8mb4_czech_ci NOT NULL,
  `user_id` int(11) NOT NULL,
  `outage_notification` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `main_client_user_id_a1b993d0_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_czech_ci;


DROP TABLE IF EXISTS `main_device`;
CREATE TABLE `main_device` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mac` varchar(12) COLLATE utf8mb4_czech_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `password` varchar(100) COLLATE utf8mb4_czech_ci DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `name` varchar(100) COLLATE utf8mb4_czech_ci DEFAULT NULL,
  `outage_report_for` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `main_device_user_id_b4aeba14_fk_auth_user_id` (`user_id`),
  CONSTRAINT `main_device_user_id_b4aeba14_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_czech_ci;


DROP TABLE IF EXISTS `main_deviceaction`;
CREATE TABLE `main_deviceaction` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action` varchar(100) COLLATE utf8mb4_czech_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `finished_at` datetime(6) DEFAULT NULL,
  `device_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `main_deviceaction_device_id_17ee8841_fk_main_device_id` (`device_id`),
  KEY `main_deviceaction_user_id_075c6e1d_fk_auth_user_id` (`user_id`),
  CONSTRAINT `main_deviceaction_device_id_17ee8841_fk_main_device_id` FOREIGN KEY (`device_id`) REFERENCES `main_device` (`id`),
  CONSTRAINT `main_deviceaction_user_id_075c6e1d_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_czech_ci;


DROP TABLE IF EXISTS `main_devicecron`;
CREATE TABLE `main_devicecron` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `day_of_week` varchar(100) COLLATE utf8mb4_czech_ci NOT NULL,
  `day_of_month` varchar(100) COLLATE utf8mb4_czech_ci NOT NULL,
  `hour` varchar(100) COLLATE utf8mb4_czech_ci NOT NULL,
  `minute` varchar(100) COLLATE utf8mb4_czech_ci NOT NULL,
  `action` varchar(100) COLLATE utf8mb4_czech_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `device_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `main_devicecron_device_id_5112323c_fk_main_device_id` (`device_id`),
  CONSTRAINT `main_devicecron_device_id_5112323c_fk_main_device_id` FOREIGN KEY (`device_id`) REFERENCES `main_device` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_czech_ci;


DROP TABLE IF EXISTS `main_devicelog`;
CREATE TABLE `main_devicelog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `option` varchar(100) COLLATE utf8mb4_czech_ci NOT NULL,
  `value` varchar(100) COLLATE utf8mb4_czech_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `device_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `main_device_device__be3b20_idx` (`device_id`,`option`),
  KEY `main_device_device__71ac9b_idx` (`device_id`,`option`,`created_at`),
  CONSTRAINT `main_devicelog_device_id_f7037d5a_fk_main_device_id` FOREIGN KEY (`device_id`) REFERENCES `main_device` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_czech_ci;


DROP TABLE IF EXISTS `main_region`;
CREATE TABLE `main_region` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_czech_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_czech_ci;


DROP TABLE IF EXISTS `main_region_devices`;
CREATE TABLE `main_region_devices` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `region_id` int(11) NOT NULL,
  `device_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `main_region_devices_region_id_device_id_45138933_uniq` (`region_id`,`device_id`),
  KEY `main_region_devices_device_id_aead98c8_fk_main_device_id` (`device_id`),
  CONSTRAINT `main_region_devices_device_id_aead98c8_fk_main_device_id` FOREIGN KEY (`device_id`) REFERENCES `main_device` (`id`),
  CONSTRAINT `main_region_devices_region_id_8f040565_fk_main_region_id` FOREIGN KEY (`region_id`) REFERENCES `main_region` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_czech_ci;


DROP TABLE IF EXISTS `main_userdevice`;
CREATE TABLE `main_userdevice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_czech_ci NOT NULL,
  `device_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `address_city` varchar(100) COLLATE utf8mb4_czech_ci DEFAULT NULL,
  `address_country` varchar(100) COLLATE utf8mb4_czech_ci DEFAULT NULL,
  `address_postal_code` varchar(100) COLLATE utf8mb4_czech_ci DEFAULT NULL,
  `address_street` varchar(100) COLLATE utf8mb4_czech_ci DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `outage_notification` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `main_userdevice_device_id_de42de22_fk_main_device_id` (`device_id`),
  KEY `main_userdevice_user_id_052eb9f4_fk_auth_user_id` (`user_id`),
  CONSTRAINT `main_userdevice_device_id_de42de22_fk_main_device_id` FOREIGN KEY (`device_id`) REFERENCES `main_device` (`id`),
  CONSTRAINT `main_userdevice_user_id_052eb9f4_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_czech_ci;


DROP TABLE IF EXISTS `main_usertermsandconditions`;
CREATE TABLE `main_usertermsandconditions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `main_usertermsandconditions_user_id_b607679e_fk_auth_user_id` (`user_id`),
  CONSTRAINT `main_usertermsandconditions_user_id_b607679e_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_czech_ci;


-- 2022-11-04 20:23:09
