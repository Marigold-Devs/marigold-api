-- -------------------------------------------------------------
-- TablePlus 4.5.2(402)
--
-- https://tableplus.com/
--
-- Database: marigold_db
-- Generation Time: 2022-02-13 16:18:26.4600
-- -------------------------------------------------------------


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=89 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS `branch_products`;
CREATE TABLE `branch_products` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `balance` decimal(10,3) NOT NULL,
  `branch_id` bigint NOT NULL,
  `product_price_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `branch_products_branch_id_fab0c63e_fk_branches_id` (`branch_id`),
  KEY `branch_products_product_price_id_ba82ccc5_fk_product_prices_id` (`product_price_id`),
  CONSTRAINT `branch_products_branch_id_fab0c63e_fk_branches_id` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`),
  CONSTRAINT `branch_products_product_price_id_ba82ccc5_fk_product_prices_id` FOREIGN KEY (`product_price_id`) REFERENCES `product_prices` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS `branches`;
CREATE TABLE `branches` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS `clients`;
CREATE TABLE `clients` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` varchar(250) NOT NULL,
  `address` varchar(50) NOT NULL,
  `landline` varchar(50) DEFAULT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `type` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS `deliveries`;
CREATE TABLE `deliveries` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `delivery_type` varchar(20) NOT NULL,
  `status` varchar(20) NOT NULL,
  `datetime_delivery` datetime(6) NOT NULL,
  `datetime_created` datetime(6) NOT NULL,
  `prepared_by` varchar(50) NOT NULL,
  `checked_by` varchar(50) NOT NULL,
  `pulled_out_by` varchar(50) NOT NULL,
  `delivered_by` varchar(50) NOT NULL,
  `branch_id` bigint NOT NULL,
  `customer_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `datetime_completed` datetime(6) DEFAULT NULL,
  `payment_status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `deliveries_branch_id_841079b3_fk_branches_id` (`branch_id`),
  KEY `deliveries_customer_id_0979af68_fk_clients_id` (`customer_id`),
  KEY `deliveries_user_id_3e30f5c5_fk_users_id` (`user_id`),
  CONSTRAINT `deliveries_branch_id_841079b3_fk_branches_id` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`),
  CONSTRAINT `deliveries_customer_id_0979af68_fk_clients_id` FOREIGN KEY (`customer_id`) REFERENCES `clients` (`id`),
  CONSTRAINT `deliveries_user_id_3e30f5c5_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS `delivery_products`;
CREATE TABLE `delivery_products` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `quantity` decimal(10,3) NOT NULL,
  `branch_product_id` bigint NOT NULL,
  `delivery_id` bigint NOT NULL,
  `price` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `delivery_products_branch_product_id_fa9c5d37_fk_branch_pr` (`branch_product_id`),
  KEY `delivery_products_delivery_id_ee9c1e7f_fk_deliveries_id` (`delivery_id`),
  CONSTRAINT `delivery_products_branch_product_id_fa9c5d37_fk_branch_pr` FOREIGN KEY (`branch_product_id`) REFERENCES `branch_products` (`id`),
  CONSTRAINT `delivery_products_delivery_id_ee9c1e7f_fk_deliveries_id` FOREIGN KEY (`delivery_id`) REFERENCES `deliveries` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_users_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS `notifications`;
CREATE TABLE `notifications` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `branch_product_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `notifications_branch_product_id_1b45cb50_fk_branch_products_id` (`branch_product_id`),
  CONSTRAINT `notifications_branch_product_id_1b45cb50_fk_branch_products_id` FOREIGN KEY (`branch_product_id`) REFERENCES `branch_products` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS `preorder_products`;
CREATE TABLE `preorder_products` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `quantity` decimal(10,3) NOT NULL,
  `branch_product_id` bigint NOT NULL,
  `preorder_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `preorder_products_branch_product_id_ec96aa9b_fk_branch_pr` (`branch_product_id`),
  KEY `preorder_products_preorder_id_f7a47c7b_fk_preorders_id` (`preorder_id`),
  CONSTRAINT `preorder_products_branch_product_id_ec96aa9b_fk_branch_pr` FOREIGN KEY (`branch_product_id`) REFERENCES `branch_products` (`id`),
  CONSTRAINT `preorder_products_preorder_id_f7a47c7b_fk_preorders_id` FOREIGN KEY (`preorder_id`) REFERENCES `preorders` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS `preorder_transaction_products`;
CREATE TABLE `preorder_transaction_products` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `quantity` decimal(10,3) NOT NULL,
  `preorder_product_id` bigint NOT NULL,
  `preorder_transaction_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `preorder_transaction_preorder_product_id_b7411731_fk_preorder_` (`preorder_product_id`),
  KEY `preorder_transaction_preorder_transaction_d479aa4a_fk_preorder_` (`preorder_transaction_id`),
  CONSTRAINT `preorder_transaction_preorder_product_id_b7411731_fk_preorder_` FOREIGN KEY (`preorder_product_id`) REFERENCES `preorder_products` (`id`),
  CONSTRAINT `preorder_transaction_preorder_transaction_d479aa4a_fk_preorder_` FOREIGN KEY (`preorder_transaction_id`) REFERENCES `preorder_transactions` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=80 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS `preorder_transactions`;
CREATE TABLE `preorder_transactions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `preorder_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `datetime_created` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `preorder_transactions_preorder_id_8e732bf1_fk_preorders_id` (`preorder_id`),
  KEY `preorder_transactions_user_id_c45b4ed2_fk_users_id` (`user_id`),
  CONSTRAINT `preorder_transactions_preorder_id_8e732bf1_fk_preorders_id` FOREIGN KEY (`preorder_id`) REFERENCES `preorders` (`id`),
  CONSTRAINT `preorder_transactions_user_id_c45b4ed2_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS `preorders`;
CREATE TABLE `preorders` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `delivery_type` varchar(20) NOT NULL,
  `status` varchar(20) NOT NULL,
  `datetime_created` datetime(6) NOT NULL,
  `branch_id` bigint NOT NULL,
  `supplier_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `datetime_fulfilled` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `preorders_branch_id_1bffcf0d_fk_branches_id` (`branch_id`),
  KEY `preorders_supplier_id_262cfdb7_fk_clients_id` (`supplier_id`),
  KEY `preorders_user_id_2ade4dbb_fk_users_id` (`user_id`),
  CONSTRAINT `preorders_branch_id_1bffcf0d_fk_branches_id` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`),
  CONSTRAINT `preorders_supplier_id_262cfdb7_fk_clients_id` FOREIGN KEY (`supplier_id`) REFERENCES `clients` (`id`),
  CONSTRAINT `preorders_user_id_2ade4dbb_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS `product_prices`;
CREATE TABLE `product_prices` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `price_market` decimal(10,2) DEFAULT NULL,
  `price_delivery` decimal(10,2) DEFAULT NULL,
  `price_pickup` decimal(10,2) DEFAULT NULL,
  `price_special` decimal(10,2) DEFAULT NULL,
  `reorder_point` decimal(10,3) NOT NULL,
  `product_id` bigint NOT NULL,
  `unit_type_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `product_prices_product_id_46988f16_fk_products_id` (`product_id`),
  KEY `product_prices_unit_type_id_a55b34e9_fk_unit_types_id` (`unit_type_id`),
  CONSTRAINT `product_prices_product_id_46988f16_fk_products_id` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`),
  CONSTRAINT `product_prices_unit_type_id_a55b34e9_fk_unit_types_id` FOREIGN KEY (`unit_type_id`) REFERENCES `unit_types` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS `products`;
CREATE TABLE `products` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `unit_cost` decimal(10,2) NOT NULL,
  `vat_type` varchar(5) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS `transaction_products`;
CREATE TABLE `transaction_products` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `price` decimal(10,2) NOT NULL,
  `quantity` decimal(10,3) NOT NULL,
  `branch_product_id` bigint NOT NULL,
  `transaction_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `transaction_products_branch_product_id_0b32f8dd_fk_branch_pr` (`branch_product_id`),
  KEY `transaction_products_transaction_id_27e15717_fk_transactions_id` (`transaction_id`),
  CONSTRAINT `transaction_products_branch_product_id_0b32f8dd_fk_branch_pr` FOREIGN KEY (`branch_product_id`) REFERENCES `branch_products` (`id`),
  CONSTRAINT `transaction_products_transaction_id_27e15717_fk_transactions_id` FOREIGN KEY (`transaction_id`) REFERENCES `transactions` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS `transactions`;
CREATE TABLE `transactions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `datetime_created` datetime(6) NOT NULL,
  `branch_id` bigint NOT NULL,
  `cashier_id` bigint NOT NULL,
  `amount_tendered` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `transactions_branch_id_e792b986_fk_branches_id` (`branch_id`),
  KEY `transactions_cashier_id_1c2e6357_fk_users_id` (`cashier_id`),
  CONSTRAINT `transactions_branch_id_e792b986_fk_branches_id` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`),
  CONSTRAINT `transactions_cashier_id_1c2e6357_fk_users_id` FOREIGN KEY (`cashier_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS `unit_types`;
CREATE TABLE `unit_types` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(20) NOT NULL,
  `first_name` varchar(30) DEFAULT NULL,
  `last_name` varchar(30) DEFAULT NULL,
  `user_type` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS `users_groups`;
CREATE TABLE `users_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_groups_user_id_group_id_fc7788e8_uniq` (`user_id`,`group_id`),
  KEY `users_groups_group_id_2f3517aa_fk_auth_group_id` (`group_id`),
  CONSTRAINT `users_groups_group_id_2f3517aa_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `users_groups_user_id_f500bee5_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS `users_user_permissions`;
CREATE TABLE `users_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_user_permissions_user_id_permission_id_3b86cbdf_uniq` (`user_id`,`permission_id`),
  KEY `users_user_permissio_permission_id_6d08dcd2_fk_auth_perm` (`permission_id`),
  CONSTRAINT `users_user_permissio_permission_id_6d08dcd2_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `users_user_permissions_user_id_92473840_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS `web_requests_webrequest`;
CREATE TABLE `web_requests_webrequest` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `time` datetime(6) NOT NULL,
  `host` varchar(1000) NOT NULL,
  `path` varchar(1000) NOT NULL,
  `method` varchar(50) NOT NULL,
  `uri` varchar(2000) NOT NULL,
  `status_code` int NOT NULL,
  `get` longtext,
  `post` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=127 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add branch', 6, 'add_branch'),
(22, 'Can change branch', 6, 'change_branch'),
(23, 'Can delete branch', 6, 'delete_branch'),
(24, 'Can view branch', 6, 'view_branch'),
(25, 'Can add branch product', 7, 'add_branchproduct'),
(26, 'Can change branch product', 7, 'change_branchproduct'),
(27, 'Can delete branch product', 7, 'delete_branchproduct'),
(28, 'Can view branch product', 7, 'view_branchproduct'),
(29, 'Can add delivery', 8, 'add_delivery'),
(30, 'Can change delivery', 8, 'change_delivery'),
(31, 'Can delete delivery', 8, 'delete_delivery'),
(32, 'Can view delivery', 8, 'view_delivery'),
(33, 'Can add delivery product', 9, 'add_deliveryproduct'),
(34, 'Can change delivery product', 9, 'change_deliveryproduct'),
(35, 'Can delete delivery product', 9, 'delete_deliveryproduct'),
(36, 'Can view delivery product', 9, 'view_deliveryproduct'),
(37, 'Can add notification', 10, 'add_notification'),
(38, 'Can change notification', 10, 'change_notification'),
(39, 'Can delete notification', 10, 'delete_notification'),
(40, 'Can view notification', 10, 'view_notification'),
(41, 'Can add preorder', 11, 'add_preorder'),
(42, 'Can change preorder', 11, 'change_preorder'),
(43, 'Can delete preorder', 11, 'delete_preorder'),
(44, 'Can view preorder', 11, 'view_preorder'),
(45, 'Can add preorder product', 12, 'add_preorderproduct'),
(46, 'Can change preorder product', 12, 'change_preorderproduct'),
(47, 'Can delete preorder product', 12, 'delete_preorderproduct'),
(48, 'Can view preorder product', 12, 'view_preorderproduct'),
(49, 'Can add preorder transaction', 13, 'add_preordertransaction'),
(50, 'Can change preorder transaction', 13, 'change_preordertransaction'),
(51, 'Can delete preorder transaction', 13, 'delete_preordertransaction'),
(52, 'Can view preorder transaction', 13, 'view_preordertransaction'),
(53, 'Can add preorder transaction product', 14, 'add_preordertransactionproduct'),
(54, 'Can change preorder transaction product', 14, 'change_preordertransactionproduct'),
(55, 'Can delete preorder transaction product', 14, 'delete_preordertransactionproduct'),
(56, 'Can view preorder transaction product', 14, 'view_preordertransactionproduct'),
(57, 'Can add product', 15, 'add_product'),
(58, 'Can change product', 15, 'change_product'),
(59, 'Can delete product', 15, 'delete_product'),
(60, 'Can view product', 15, 'view_product'),
(61, 'Can add unit type', 16, 'add_unittype'),
(62, 'Can change unit type', 16, 'change_unittype'),
(63, 'Can delete unit type', 16, 'delete_unittype'),
(64, 'Can view unit type', 16, 'view_unittype'),
(65, 'Can add product price', 17, 'add_productprice'),
(66, 'Can change product price', 17, 'change_productprice'),
(67, 'Can delete product price', 17, 'delete_productprice'),
(68, 'Can view product price', 17, 'view_productprice'),
(69, 'Can add client', 18, 'add_client'),
(70, 'Can change client', 18, 'change_client'),
(71, 'Can delete client', 18, 'delete_client'),
(72, 'Can view client', 18, 'view_client'),
(73, 'Can add user', 19, 'add_user'),
(74, 'Can change user', 19, 'change_user'),
(75, 'Can delete user', 19, 'delete_user'),
(76, 'Can view user', 19, 'view_user'),
(77, 'Can add web request', 20, 'add_webrequest'),
(78, 'Can change web request', 20, 'change_webrequest'),
(79, 'Can delete web request', 20, 'delete_webrequest'),
(80, 'Can view web request', 20, 'view_webrequest'),
(81, 'Can add transaction', 21, 'add_transaction'),
(82, 'Can change transaction', 21, 'change_transaction'),
(83, 'Can delete transaction', 21, 'delete_transaction'),
(84, 'Can view transaction', 21, 'view_transaction'),
(85, 'Can add transaction product', 22, 'add_transactionproduct'),
(86, 'Can change transaction product', 22, 'change_transactionproduct'),
(87, 'Can delete transaction product', 22, 'delete_transactionproduct'),
(88, 'Can view transaction product', 22, 'view_transactionproduct');

INSERT INTO `branch_products` (`id`, `balance`, `branch_id`, `product_price_id`) VALUES
(1, 8.000, 1, 1),
(2, 10.000, 1, 2),
(3, 10.000, 1, 3),
(4, 0.000, 2, 1),
(5, 0.000, 2, 2),
(6, 0.000, 2, 3),
(7, 12.000, 1, 4),
(8, 10.000, 1, 5),
(9, 10.000, 1, 6),
(10, 0.000, 2, 4),
(11, 0.000, 2, 5),
(12, 0.000, 2, 6),
(13, 10.000, 1, 7),
(14, 10.000, 1, 8),
(15, 10.000, 1, 9),
(16, 0.000, 2, 7),
(17, 0.000, 2, 8),
(18, 0.000, 2, 9),
(19, 10.000, 1, 10),
(20, 10.000, 1, 11),
(21, 10.000, 1, 12),
(22, 0.000, 2, 10),
(23, 0.000, 2, 11),
(24, 0.000, 2, 12),
(25, 10.000, 1, 13),
(26, 10.000, 1, 14),
(27, 10.000, 1, 15),
(28, 0.000, 2, 13),
(29, 0.000, 2, 14),
(30, 0.000, 2, 15),
(31, 10.000, 1, 16),
(32, 10.000, 1, 17),
(33, 10.000, 1, 18),
(34, 0.000, 2, 16),
(35, 0.000, 2, 17),
(36, 0.000, 2, 18),
(37, 10.000, 1, 19),
(38, 10.000, 1, 20),
(39, 0.000, 2, 19),
(40, 0.000, 2, 20),
(41, 10.000, 1, 21),
(42, 10.000, 1, 22),
(43, 10.000, 1, 23),
(44, 0.000, 2, 21),
(45, 0.000, 2, 22),
(46, 0.000, 2, 23),
(47, 0.000, 1, 24),
(48, 0.000, 1, 25),
(49, 0.000, 2, 24),
(50, 0.000, 2, 25),
(51, 0.000, 1, 26),
(52, 0.000, 1, 27),
(53, 0.000, 2, 26),
(54, 0.000, 2, 27);

INSERT INTO `branches` (`id`, `name`) VALUES
(1, 'Humay-Humay'),
(2, 'Branch 2');

INSERT INTO `clients` (`id`, `name`, `description`, `address`, `landline`, `phone`, `type`) VALUES
(1, 'Mr. Jonathan', 'Usually arrives 10mins before delivery time.', 'Cebu City', '123123', '0905 123 4567', 'supplier'),
(2, 'Mr. Andrew', 'Call customer first before delivery.', '0314 Santa Ana', '1234567', '+639055625909', 'customer'),
(3, 'Mr. Juan', 'customer description here', 'Cebu', '123 4567', '0905 123 4567', 'customer'),
(4, 'Ms. Jane', 'supplier description here', 'Cebu', '123 4567', '0905 123 456', 'supplier');

INSERT INTO `deliveries` (`id`, `delivery_type`, `status`, `datetime_delivery`, `datetime_created`, `prepared_by`, `checked_by`, `pulled_out_by`, `delivered_by`, `branch_id`, `customer_id`, `user_id`, `datetime_completed`, `payment_status`) VALUES
(8, 'delivery', 'delivered', '2022-01-17 02:00:01.000000', '2022-01-16 08:32:30.822890', '', '', '', '', 1, 2, 1, '2022-01-16 08:39:53.000000', 'unpaid'),
(9, 'delivery', 'delivered', '2022-01-16 08:46:52.000000', '2022-01-16 08:47:21.533062', 'test', 'test', 'test', 'test', 1, 2, 1, '2022-02-11 17:41:56.406046', 'paid'),
(10, 'delivery', 'pending', '2022-02-11 16:00:00.000000', '2022-02-11 17:10:37.656290', '', '', '', '', 1, 2, 1, NULL, 'unpaid'),
(11, 'delivery', 'delivered', '2022-02-13 06:05:29.000000', '2022-02-13 06:05:41.123273', '', '', '', '', 1, 2, 1, '2022-02-13 06:05:55.092913', 'paid'),
(12, 'delivery', 'delivered', '2022-02-13 06:27:39.000000', '2022-02-13 06:27:48.784672', '', '', '', '', 1, 2, 1, '2022-02-13 06:28:20.726593', 'paid');

INSERT INTO `delivery_products` (`id`, `quantity`, `branch_product_id`, `delivery_id`, `price`) VALUES
(28, 5.000, 1, 8, 2090.00),
(29, 10.000, 7, 8, 1970.00),
(30, 1.000, 1, 9, 2090.00),
(31, 1.000, 7, 9, 1970.00),
(32, 1.000, 1, 10, 2090.00),
(33, 1.000, 2, 10, 90.00),
(34, 1.000, 3, 10, 90.00),
(35, 1.000, 7, 10, 1970.00),
(36, 1.000, 8, 10, 165.00),
(37, 1.000, 9, 10, 165.00),
(38, 1.000, 13, 10, 1105.00),
(39, 1.000, 14, 10, 25.00),
(40, 1.000, 15, 10, 25.00),
(41, 1.000, 19, 10, 1786.00),
(42, 1.000, 20, 10, 52.00),
(43, 1.000, 21, 10, 52.00),
(44, 1.000, 25, 10, 1148.00),
(45, 1.000, 26, 10, 50.00),
(46, 1.000, 27, 10, 50.00),
(47, 1.000, 31, 10, 1148.00),
(48, 1.000, 32, 10, 50.00),
(49, 1.000, 33, 10, 50.00),
(50, 1.000, 37, 10, 1.00),
(51, 1.000, 38, 10, 1.00),
(52, 1.000, 41, 10, 1.00),
(53, 1.000, 42, 10, 1.00),
(54, 1.000, 43, 10, 1.00),
(55, 1.000, 1, 11, 2090.00),
(56, 1.000, 1, 12, 2090.00);

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(2, 'auth', 'permission'),
(3, 'auth', 'group'),
(4, 'contenttypes', 'contenttype'),
(5, 'sessions', 'session'),
(6, 'branches', 'branch'),
(7, 'branches', 'branchproduct'),
(8, 'deliveries', 'delivery'),
(9, 'deliveries', 'deliveryproduct'),
(10, 'notifications', 'notification'),
(11, 'preorders', 'preorder'),
(12, 'preorders', 'preorderproduct'),
(13, 'preorders', 'preordertransaction'),
(14, 'preorders', 'preordertransactionproduct'),
(15, 'products', 'product'),
(16, 'products', 'unittype'),
(17, 'products', 'productprice'),
(18, 'users', 'client'),
(19, 'users', 'user'),
(20, 'web_requests', 'webrequest'),
(21, 'transactions', 'transaction'),
(22, 'transactions', 'transactionproduct');

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2021-12-04 12:51:22.651613'),
(2, 'contenttypes', '0002_remove_content_type_name', '2021-12-04 12:51:22.708936'),
(3, 'auth', '0001_initial', '2021-12-04 12:51:22.845919'),
(4, 'auth', '0002_alter_permission_name_max_length', '2021-12-04 12:51:22.883715'),
(5, 'auth', '0003_alter_user_email_max_length', '2021-12-04 12:51:22.894070'),
(6, 'auth', '0004_alter_user_username_opts', '2021-12-04 12:51:22.910845'),
(7, 'auth', '0005_alter_user_last_login_null', '2021-12-04 12:51:22.931219'),
(8, 'auth', '0006_require_contenttypes_0002', '2021-12-04 12:51:22.938905'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2021-12-04 12:51:23.083591'),
(10, 'auth', '0008_alter_user_username_max_length', '2021-12-04 12:51:23.132440'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2021-12-04 12:51:23.154958'),
(12, 'auth', '0010_alter_group_name_max_length', '2021-12-04 12:51:23.201826'),
(13, 'auth', '0011_update_proxy_permissions', '2021-12-04 12:51:23.248296'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2021-12-04 12:51:23.285283'),
(15, 'users', '0001_initial', '2021-12-04 12:51:23.701608'),
(16, 'admin', '0001_initial', '2021-12-04 12:51:23.911815'),
(17, 'admin', '0002_logentry_remove_auto_add', '2021-12-04 12:51:23.928735'),
(18, 'admin', '0003_logentry_add_action_flag_choices', '2021-12-04 12:51:23.944810'),
(19, 'products', '0001_initial', '2021-12-04 12:51:24.093691'),
(20, 'branches', '0001_initial', '2021-12-04 12:51:24.240628'),
(21, 'users', '0002_alter_client_description', '2021-12-04 12:51:24.285612'),
(22, 'deliveries', '0001_initial', '2021-12-04 12:51:24.557392'),
(23, 'deliveries', '0002_rename_delivered_out_by_delivery_delivered_by', '2021-12-04 12:51:24.621452'),
(24, 'deliveries', '0003_deliveryproduct_price', '2021-12-04 12:51:24.686174'),
(25, 'deliveries', '0004_delivery_datetime_completed', '2021-12-04 12:51:24.751072'),
(26, 'notifications', '0001_initial', '2021-12-04 12:51:24.831189'),
(27, 'preorders', '0001_initial', '2021-12-04 12:51:24.999792'),
(28, 'preorders', '0002_initial', '2021-12-04 12:51:25.398949'),
(29, 'preorders', '0003_preorder_datetime_fulfilled', '2021-12-04 12:51:25.463043'),
(30, 'preorders', '0004_alter_preorder_datetime_fulfilled', '2021-12-04 12:51:25.525724'),
(31, 'preorders', '0005_preordertransaction_datetime_created', '2021-12-04 12:51:25.581286'),
(32, 'sessions', '0001_initial', '2021-12-04 12:51:25.617908'),
(33, 'web_requests', '0001_initial', '2021-12-04 12:51:25.653876'),
(34, 'transactions', '0001_initial', '2021-12-23 08:06:20.801796'),
(35, 'transactions', '0002_transaction_amount_tendered', '2021-12-24 03:59:09.284034'),
(36, 'deliveries', '0005_delivery_payment_status', '2022-02-11 17:35:53.325882'),
(37, 'deliveries', '0006_alter_delivery_payment_status', '2022-02-11 17:36:59.676724');

INSERT INTO `preorder_products` (`id`, `quantity`, `branch_product_id`, `preorder_id`) VALUES
(37, 10.000, 1, 12),
(38, 10.000, 7, 12),
(39, 5.000, 1, 13),
(40, 10.000, 7, 13),
(41, 10.000, 1, 14),
(42, 10.000, 2, 14),
(43, 10.000, 3, 14),
(44, 10.000, 7, 14),
(45, 10.000, 8, 14),
(46, 10.000, 9, 14),
(47, 10.000, 13, 14),
(48, 10.000, 14, 14),
(49, 10.000, 15, 14),
(50, 10.000, 19, 14),
(51, 10.000, 20, 14),
(52, 10.000, 21, 14),
(53, 10.000, 25, 14),
(54, 10.000, 26, 14),
(55, 10.000, 27, 14),
(56, 10.000, 31, 14),
(57, 10.000, 32, 14),
(58, 10.000, 33, 14),
(59, 10.000, 37, 15),
(60, 10.000, 38, 15),
(61, 10.000, 41, 15),
(62, 10.000, 42, 15),
(63, 10.000, 43, 15);

INSERT INTO `preorder_transaction_products` (`id`, `quantity`, `preorder_product_id`, `preorder_transaction_id`) VALUES
(51, 10.000, 37, 15),
(52, 0.000, 38, 15),
(53, 0.000, 37, 16),
(54, 10.000, 38, 16),
(55, 5.000, 39, 17),
(56, 10.000, 40, 17),
(57, 10.000, 41, 18),
(58, 10.000, 42, 18),
(59, 10.000, 43, 18),
(60, 10.000, 44, 18),
(61, 10.000, 45, 18),
(62, 10.000, 46, 18),
(63, 10.000, 47, 18),
(64, 10.000, 48, 18),
(65, 10.000, 49, 18),
(66, 10.000, 50, 18),
(67, 10.000, 51, 18),
(68, 10.000, 52, 18),
(69, 10.000, 53, 18),
(70, 10.000, 54, 18),
(71, 10.000, 55, 18),
(72, 10.000, 56, 18),
(73, 10.000, 57, 18),
(74, 10.000, 58, 18),
(75, 10.000, 59, 19),
(76, 10.000, 60, 19),
(77, 10.000, 61, 19),
(78, 10.000, 62, 19),
(79, 10.000, 63, 19);

INSERT INTO `preorder_transactions` (`id`, `preorder_id`, `user_id`, `datetime_created`) VALUES
(15, 12, 1, '2022-01-16 08:22:52.418552'),
(16, 12, 1, '2022-01-16 08:23:29.977709'),
(17, 13, 1, '2022-01-16 08:41:34.976192'),
(18, 14, 1, '2022-02-11 17:07:13.794121'),
(19, 15, 1, '2022-02-11 17:09:50.053143');

INSERT INTO `preorders` (`id`, `delivery_type`, `status`, `datetime_created`, `branch_id`, `supplier_id`, `user_id`, `datetime_fulfilled`) VALUES
(12, 'delivery', 'delivered', '2022-01-16 08:20:13.624674', 1, 4, 1, '2022-01-16 08:23:39.479767'),
(13, 'delivery', 'delivered', '2022-01-16 08:41:16.916349', 1, 4, 1, '2022-01-16 08:41:38.588290'),
(14, 'delivery', 'delivered', '2022-02-11 17:06:58.388112', 1, 4, 1, '2022-02-11 17:07:16.259897'),
(15, 'delivery', 'delivered', '2022-02-11 17:09:42.615639', 1, 1, 1, '2022-02-11 17:09:51.176057');

INSERT INTO `product_prices` (`id`, `price_market`, `price_delivery`, `price_pickup`, `price_special`, `reorder_point`, `product_id`, `unit_type_id`) VALUES
(1, 2090.00, 2090.00, 2090.00, 2090.00, 5.000, 1, 5),
(2, 90.00, 90.00, 90.00, 90.00, 0.000, 1, 15),
(3, 90.00, 90.00, 90.00, 90.00, 0.000, 1, 18),
(4, 1970.00, 1970.00, 1970.00, 1970.00, 5.000, 2, 5),
(5, 165.00, 165.00, 165.00, 165.00, 0.000, 2, 15),
(6, 165.00, 165.00, 165.00, 165.00, 0.000, 2, 18),
(7, 1105.00, 1105.00, 1105.00, 1105.00, 5.000, 3, 5),
(8, 25.00, 25.00, 25.00, 25.00, 0.000, 3, 15),
(9, 25.00, 25.00, 25.00, 25.00, 0.000, 3, 18),
(10, 1786.00, 1786.00, 1786.00, 1786.00, 5.000, 4, 5),
(11, 52.00, 52.00, 52.00, 52.00, 0.000, 4, 15),
(12, 52.00, 52.00, 52.00, 52.00, 0.000, 4, 18),
(13, 1148.00, 1148.00, 1148.00, 1148.00, 5.000, 5, 5),
(14, 50.00, 50.00, 50.00, 50.00, 0.000, 5, 15),
(15, 50.00, 50.00, 50.00, 50.00, 0.000, 5, 18),
(16, 1148.00, 1148.00, 1148.00, 1148.00, 5.000, 6, 5),
(17, 50.00, 50.00, 50.00, 50.00, 0.000, 6, 15),
(18, 50.00, 50.00, 50.00, 50.00, 0.000, 6, 18),
(19, 1.00, 1.00, 1.00, 1.00, 1.000, 7, 3),
(20, 1.00, 1.00, 1.00, 1.00, 0.000, 7, 15),
(21, 1.00, 1.00, 1.00, 1.00, 1.000, 8, 1),
(22, 1.00, 1.00, 1.00, 1.00, 1.000, 8, 3),
(23, 1.00, 1.00, 1.00, 1.00, 1.000, 8, 15),
(24, 1.00, 1.00, 1.00, 1.00, 5.000, 9, 3),
(25, 1.00, 1.00, 1.00, 1.00, 0.000, 9, 5),
(26, 1.00, 1.00, 1.00, 1.00, 0.000, 10, 3),
(27, 1.00, 1.00, 1.00, 1.00, 1.000, 10, 4);

INSERT INTO `products` (`id`, `name`, `unit_cost`, `vat_type`) VALUES
(1, 'VETSIN-24X500GMS', 2040.00, 'vat-e'),
(2, 'VETSIN-12X1KILO', 1920.00, 'vat'),
(3, 'GINISA-48X100GMS', 1055.00, 'vat'),
(4, 'GINISA-36X250GMS', 1736.00, 'vat'),
(5, 'CRISPY-ORIG.24X238GRAMS', 1098.00, 'vat'),
(6, 'CRISPY-GARLIC24X238GMS.', 1098.00, 'vat'),
(7, 'Product 1', 100.00, 'vat-e'),
(8, 'Product 2', 1.00, 'vat-e'),
(9, 'Product 3', 1.00, 'vat-e'),
(10, 'Product 4', 1.00, 'vat-e');

INSERT INTO `transaction_products` (`id`, `price`, `quantity`, `branch_product_id`, `transaction_id`) VALUES
(9, 1970.00, 2.000, 7, 8),
(10, 2090.00, 1.000, 1, 8),
(11, 2090.00, 1.000, 1, 9),
(12, 2090.00, 1.000, 1, 10),
(13, 1970.00, 1.000, 7, 11),
(14, 1970.00, 1.000, 7, 12),
(15, 2090.00, 1.000, 1, 12),
(16, 1970.00, 1.000, 7, 13),
(17, 2090.00, 1.000, 1, 13),
(18, 2090.00, 1.000, 1, 14),
(19, 2090.00, 1.000, 1, 15),
(20, 2090.00, 1.000, 1, 16),
(21, 1970.00, 2.000, 7, 17),
(22, 2090.00, 1.000, 1, 17);

INSERT INTO `transactions` (`id`, `datetime_created`, `branch_id`, `cashier_id`, `amount_tendered`) VALUES
(8, '2022-01-16 09:11:45.979984', 1, 1, 6100.00),
(9, '2022-02-01 13:58:37.422429', 1, 1, 2100.00),
(10, '2022-02-01 13:59:24.826640', 1, 1, 2100.00),
(11, '2022-02-01 14:17:31.863126', 1, 1, 2000.00),
(12, '2022-02-01 14:17:56.543038', 1, 1, 5000.00),
(13, '2022-02-01 14:27:13.316919', 1, 1, 5000.00),
(14, '2022-02-01 14:28:09.063893', 1, 1, 2100.00),
(15, '2022-02-01 14:29:02.002916', 1, 1, 2100.00),
(16, '2022-02-01 14:29:41.408136', 1, 1, 2100.00),
(17, '2022-02-01 14:30:43.134211', 1, 1, 6100.00);

INSERT INTO `unit_types` (`id`, `name`) VALUES
(1, '100s'),
(2, '5 Kilo'),
(3, 'Bag'),
(4, 'Bottle'),
(5, 'Box'),
(6, 'Bundle'),
(7, 'Can'),
(8, 'Case'),
(9, 'Container'),
(10, 'Cup'),
(11, 'Dozen'),
(12, 'Drum'),
(13, 'Gallon'),
(14, 'Kilo'),
(15, 'Pack'),
(16, 'Pail'),
(17, 'Per box'),
(18, 'Piece'),
(19, 'Ream'),
(20, 'Sack'),
(21, 'Tie');

INSERT INTO `users` (`id`, `password`, `last_login`, `is_staff`, `is_superuser`, `username`, `first_name`, `last_name`, `user_type`) VALUES
(1, 'pbkdf2_sha256$260000$2gphIjV4VI5fsOWboiROYj$m10QdiH8ngujD19U5v+CFdaTt9eVxqI/ms7RWhUPAy4=', NULL, 1, 1, 'andrew', 'Andrew', 'Oplas', NULL);

INSERT INTO `web_requests_webrequest` (`id`, `time`, `host`, `path`, `method`, `uri`, `status_code`, `get`, `post`) VALUES
(1, '2021-12-04 15:07:10.851053', '127.0.0.1:8000', '/v1/users/login/', 'POST', 'http://127.0.0.1:8000/v1/users/login/', 200, NULL, '\"{\\\"login\\\":\\\"andrew\\\",\\\"password\\\":\\\"123456\\\"}\"'),
(2, '2021-12-04 15:07:23.861142', '127.0.0.1:8000', '/v1/branches/', 'POST', 'http://127.0.0.1:8000/v1/branches/', 200, NULL, '\"{\\\"name\\\":\\\"Humay-Humay\\\"}\"'),
(3, '2021-12-04 15:07:28.973172', '127.0.0.1:8000', '/v1/branches/', 'POST', 'http://127.0.0.1:8000/v1/branches/', 200, NULL, '\"{\\\"name\\\":\\\"Branch 2\\\"}\"'),
(4, '2021-12-04 15:15:32.419923', '127.0.0.1:8000', '/v1/products/', 'POST', 'http://127.0.0.1:8000/v1/products/', 200, NULL, '\"{\\\"name\\\":\\\"VETSIN-24X500GMS\\\",\\\"unit_cost\\\":\\\"2040\\\",\\\"vat_type\\\":\\\"vat-e\\\",\\\"product_prices\\\":[{\\\"unit_type_id\\\":5,\\\"price_market\\\":\\\"2090\\\",\\\"price_delivery\\\":\\\"2090\\\",\\\"price_pickup\\\":\\\"2090\\\",\\\"price_special\\\":\\\"2090\\\",\\\"reorder_point\\\":\\\"5\\\"},{\\\"unit_type_id\\\":15,\\\"price_market\\\":\\\"90\\\",\\\"price_delivery\\\":\\\"90\\\",\\\"price_pickup\\\":\\\"90\\\",\\\"price_special\\\":\\\"90\\\",\\\"reorder_point\\\":\\\"0\\\"},{\\\"unit_type_id\\\":18,\\\"price_market\\\":\\\"90\\\",\\\"price_delivery\\\":\\\"90\\\",\\\"price_pickup\\\":\\\"90\\\",\\\"price_special\\\":\\\"90\\\",\\\"reorder_point\\\":\\\"0\\\"}]}\"'),
(5, '2021-12-04 15:16:28.226651', '127.0.0.1:8000', '/v1/products/', 'POST', 'http://127.0.0.1:8000/v1/products/', 200, NULL, '\"{\\\"name\\\":\\\"VETSIN-12X1KILO\\\",\\\"unit_cost\\\":\\\"1920\\\",\\\"vat_type\\\":\\\"vat\\\",\\\"product_prices\\\":[{\\\"unit_type_id\\\":5,\\\"price_market\\\":\\\"1970\\\",\\\"price_delivery\\\":\\\"1970\\\",\\\"price_pickup\\\":\\\"1970\\\",\\\"price_special\\\":\\\"1970\\\",\\\"reorder_point\\\":\\\"5\\\"},{\\\"unit_type_id\\\":15,\\\"price_market\\\":\\\"165\\\",\\\"price_delivery\\\":\\\"165\\\",\\\"price_pickup\\\":\\\"165\\\",\\\"price_special\\\":\\\"165\\\",\\\"reorder_point\\\":\\\"0\\\"},{\\\"unit_type_id\\\":18,\\\"price_market\\\":\\\"165\\\",\\\"price_delivery\\\":\\\"165\\\",\\\"price_pickup\\\":\\\"165\\\",\\\"price_special\\\":\\\"165\\\",\\\"reorder_point\\\":\\\"0\\\"}]}\"'),
(6, '2021-12-04 15:17:29.710634', '127.0.0.1:8000', '/v1/products/', 'POST', 'http://127.0.0.1:8000/v1/products/', 200, NULL, '\"{\\\"name\\\":\\\"GINISA-48X100GMS\\\",\\\"unit_cost\\\":\\\"1055\\\",\\\"vat_type\\\":\\\"vat\\\",\\\"product_prices\\\":[{\\\"unit_type_id\\\":5,\\\"price_market\\\":\\\"1105\\\",\\\"price_delivery\\\":\\\"1105\\\",\\\"price_pickup\\\":\\\"1105\\\",\\\"price_special\\\":\\\"1105\\\",\\\"reorder_point\\\":\\\"5\\\"},{\\\"unit_type_id\\\":15,\\\"price_market\\\":\\\"25\\\",\\\"price_delivery\\\":\\\"25\\\",\\\"price_pickup\\\":\\\"25\\\",\\\"price_special\\\":\\\"25\\\",\\\"reorder_point\\\":\\\"0\\\"},{\\\"unit_type_id\\\":18,\\\"price_market\\\":\\\"25\\\",\\\"price_delivery\\\":\\\"25\\\",\\\"price_pickup\\\":\\\"25\\\",\\\"price_special\\\":\\\"25\\\",\\\"reorder_point\\\":\\\"0\\\"}]}\"'),
(7, '2021-12-04 15:18:20.278520', '127.0.0.1:8000', '/v1/products/', 'POST', 'http://127.0.0.1:8000/v1/products/', 200, NULL, '\"{\\\"name\\\":\\\"GINISA-36X250GMS\\\",\\\"unit_cost\\\":\\\"1736\\\",\\\"vat_type\\\":\\\"vat\\\",\\\"product_prices\\\":[{\\\"unit_type_id\\\":5,\\\"price_market\\\":\\\"1786\\\",\\\"price_delivery\\\":\\\"1786\\\",\\\"price_pickup\\\":\\\"1786\\\",\\\"price_special\\\":\\\"1786\\\",\\\"reorder_point\\\":\\\"5\\\"},{\\\"unit_type_id\\\":15,\\\"price_market\\\":\\\"52\\\",\\\"price_delivery\\\":\\\"52\\\",\\\"price_pickup\\\":\\\"52\\\",\\\"price_special\\\":\\\"52\\\",\\\"reorder_point\\\":\\\"0\\\"},{\\\"unit_type_id\\\":18,\\\"price_market\\\":\\\"52\\\",\\\"price_delivery\\\":\\\"52\\\",\\\"price_pickup\\\":\\\"52\\\",\\\"price_special\\\":\\\"52\\\",\\\"reorder_point\\\":\\\"0\\\"}]}\"'),
(8, '2021-12-04 15:19:30.875944', '127.0.0.1:8000', '/v1/products/', 'POST', 'http://127.0.0.1:8000/v1/products/', 200, NULL, '\"{\\\"name\\\":\\\"CRISPY-ORIG.24X238GRAMS\\\",\\\"unit_cost\\\":\\\"1098\\\",\\\"vat_type\\\":\\\"vat\\\",\\\"product_prices\\\":[{\\\"unit_type_id\\\":5,\\\"price_market\\\":\\\"1148\\\",\\\"price_delivery\\\":\\\"1148\\\",\\\"price_pickup\\\":\\\"1148\\\",\\\"price_special\\\":\\\"1148\\\",\\\"reorder_point\\\":\\\"5\\\"},{\\\"unit_type_id\\\":15,\\\"price_market\\\":\\\"50\\\",\\\"price_delivery\\\":\\\"50\\\",\\\"price_pickup\\\":\\\"50\\\",\\\"price_special\\\":\\\"50\\\",\\\"reorder_point\\\":\\\"0\\\"},{\\\"unit_type_id\\\":18,\\\"price_market\\\":\\\"50\\\",\\\"price_delivery\\\":\\\"50\\\",\\\"price_pickup\\\":\\\"50\\\",\\\"price_special\\\":\\\"50\\\",\\\"reorder_point\\\":\\\"0\\\"}]}\"'),
(9, '2021-12-04 15:20:27.020195', '127.0.0.1:8000', '/v1/products/', 'POST', 'http://127.0.0.1:8000/v1/products/', 200, NULL, '\"{\\\"name\\\":\\\"CRISPY-GARLIC24X238GMS.\\\",\\\"unit_cost\\\":\\\"1098\\\",\\\"vat_type\\\":\\\"vat\\\",\\\"product_prices\\\":[{\\\"unit_type_id\\\":5,\\\"price_market\\\":\\\"1148\\\",\\\"price_delivery\\\":\\\"1148\\\",\\\"price_pickup\\\":\\\"1148\\\",\\\"price_special\\\":\\\"1148\\\",\\\"reorder_point\\\":\\\"5\\\"},{\\\"unit_type_id\\\":15,\\\"price_market\\\":\\\"50\\\",\\\"price_delivery\\\":\\\"50\\\",\\\"price_pickup\\\":\\\"50\\\",\\\"price_special\\\":\\\"50\\\",\\\"reorder_point\\\":\\\"0\\\"},{\\\"unit_type_id\\\":18,\\\"price_market\\\":\\\"50\\\",\\\"price_delivery\\\":\\\"50\\\",\\\"price_pickup\\\":\\\"50\\\",\\\"price_special\\\":\\\"50\\\",\\\"reorder_point\\\":\\\"0\\\"}]}\"'),
(10, '2021-12-04 15:20:57.101581', '127.0.0.1:8000', '/v1/users/login/', 'POST', 'http://127.0.0.1:8000/v1/users/login/', 200, NULL, '\"{\\\"login\\\":\\\"andrew\\\",\\\"password\\\":\\\"123456\\\"}\"'),
(11, '2021-12-04 15:39:52.891730', '127.0.0.1:8000', '/v1/preorders/', 'POST', 'http://127.0.0.1:8000/v1/preorders/', 200, NULL, '\"{\\\"branch_id\\\":1,\\\"delivery_type\\\":\\\"delivery\\\",\\\"supplier\\\":{\\\"name\\\":\\\"Mr. Jonathan\\\",\\\"description\\\":\\\"Usually arrives 10mins before delivery time. \\\",\\\"address\\\":\\\"Cebu City\\\",\\\"landline\\\":\\\"123123\\\",\\\"phone\\\":\\\"0905 123 4567\\\"},\\\"preorder_products\\\":[{\\\"branch_product_id\\\":13,\\\"quantity\\\":10},{\\\"branch_product_id\\\":19,\\\"quantity\\\":10},{\\\"branch_product_id\\\":25,\\\"quantity\\\":10},{\\\"branch_product_id\\\":31,\\\"quantity\\\":10}]}\"'),
(12, '2021-12-04 15:43:32.968202', '127.0.0.1:8000', '/v1/preorders/1/', 'PATCH', 'http://127.0.0.1:8000/v1/preorders/1/', 200, NULL, '\"{\\\"status\\\":\\\"approved\\\"}\"'),
(13, '2021-12-04 15:44:30.705377', '127.0.0.1:8000', '/v1/preorder-transactions/', 'POST', 'http://127.0.0.1:8000/v1/preorder-transactions/', 204, NULL, '\"{\\\"preorder_id\\\":1,\\\"preorder_transaction_products\\\":[{\\\"preorder_product_id\\\":1,\\\"quantity\\\":5},{\\\"preorder_product_id\\\":2,\\\"quantity\\\":5},{\\\"preorder_product_id\\\":3,\\\"quantity\\\":5},{\\\"preorder_product_id\\\":4,\\\"quantity\\\":5}]}\"'),
(14, '2021-12-04 15:45:43.510746', '127.0.0.1:8000', '/v1/preorder-transactions/', 'POST', 'http://127.0.0.1:8000/v1/preorder-transactions/', 204, NULL, '\"{\\\"preorder_id\\\":1,\\\"preorder_transaction_products\\\":[{\\\"preorder_product_id\\\":1,\\\"quantity\\\":5},{\\\"preorder_product_id\\\":2,\\\"quantity\\\":5},{\\\"preorder_product_id\\\":3,\\\"quantity\\\":5},{\\\"preorder_product_id\\\":4,\\\"quantity\\\":5}]}\"'),
(15, '2021-12-04 15:47:22.759341', '127.0.0.1:8000', '/v1/preorders/1/', 'PATCH', 'http://127.0.0.1:8000/v1/preorders/1/', 200, NULL, '\"{\\\"status\\\":\\\"delivered\\\"}\"'),
(16, '2021-12-04 16:11:04.696351', '127.0.0.1:8000', '/v1/preorder-transactions/', 'POST', 'http://127.0.0.1:8000/v1/preorder-transactions/', 204, NULL, '\"{\\\"preorder_id\\\":1,\\\"preorder_transaction_products\\\":[{\\\"preorder_product_id\\\":1,\\\"quantity\\\":5},{\\\"preorder_product_id\\\":2,\\\"quantity\\\":5},{\\\"preorder_product_id\\\":3,\\\"quantity\\\":5},{\\\"preorder_product_id\\\":4,\\\"quantity\\\":5}]}\"'),
(17, '2021-12-04 16:11:09.841951', '127.0.0.1:8000', '/v1/preorder-transactions/', 'POST', 'http://127.0.0.1:8000/v1/preorder-transactions/', 204, NULL, '\"{\\\"preorder_id\\\":1,\\\"preorder_transaction_products\\\":[{\\\"preorder_product_id\\\":1,\\\"quantity\\\":7},{\\\"preorder_product_id\\\":2,\\\"quantity\\\":7},{\\\"preorder_product_id\\\":3,\\\"quantity\\\":7},{\\\"preorder_product_id\\\":4,\\\"quantity\\\":7}]}\"'),
(18, '2021-12-04 16:23:24.442036', '127.0.0.1:8000', '/v1/preorders/1/', 'PATCH', 'http://127.0.0.1:8000/v1/preorders/1/', 200, NULL, '\"{\\\"status\\\":\\\"delivered\\\"}\"'),
(19, '2021-12-04 16:24:59.747246', '127.0.0.1:8000', '/v1/preorders/', 'POST', 'http://127.0.0.1:8000/v1/preorders/', 200, NULL, '\"{\\\"branch_id\\\":1,\\\"delivery_type\\\":\\\"pickup\\\",\\\"supplier\\\":{\\\"id\\\":1,\\\"name\\\":\\\"Mr. Jonathan\\\",\\\"description\\\":\\\"Usually arrives 10mins before delivery time.\\\",\\\"address\\\":\\\"Cebu City\\\",\\\"landline\\\":\\\"123123\\\",\\\"phone\\\":\\\"0905 123 4567\\\"},\\\"preorder_products\\\":[{\\\"branch_product_id\\\":1,\\\"quantity\\\":10},{\\\"branch_product_id\\\":7,\\\"quantity\\\":10},{\\\"branch_product_id\\\":13,\\\"quantity\\\":10},{\\\"branch_product_id\\\":19,\\\"quantity\\\":10}]}\"'),
(20, '2021-12-04 16:25:17.806812', '127.0.0.1:8000', '/v1/preorders/2/', 'PATCH', 'http://127.0.0.1:8000/v1/preorders/2/', 200, NULL, '\"{\\\"status\\\":\\\"approved\\\"}\"'),
(21, '2021-12-04 16:25:29.081337', '127.0.0.1:8000', '/v1/preorder-transactions/', 'POST', 'http://127.0.0.1:8000/v1/preorder-transactions/', 204, NULL, '\"{\\\"preorder_id\\\":2,\\\"preorder_transaction_products\\\":[{\\\"preorder_product_id\\\":5,\\\"quantity\\\":10},{\\\"preorder_product_id\\\":6,\\\"quantity\\\":10},{\\\"preorder_product_id\\\":7,\\\"quantity\\\":10},{\\\"preorder_product_id\\\":8,\\\"quantity\\\":10}]}\"'),
(22, '2021-12-04 16:25:32.356035', '127.0.0.1:8000', '/v1/preorders/2/', 'PATCH', 'http://127.0.0.1:8000/v1/preorders/2/', 200, NULL, '\"{\\\"status\\\":\\\"delivered\\\"}\"'),
(23, '2021-12-04 16:28:38.778700', '127.0.0.1:8000', '/v1/deliveries/', 'POST', 'http://127.0.0.1:8000/v1/deliveries/', 200, NULL, '\"{\\\"branch_id\\\":1,\\\"delivery_type\\\":\\\"market\\\",\\\"datetime_delivery\\\":\\\"2021-12-06 10:00:10\\\",\\\"customer\\\":{\\\"name\\\":\\\"Mr. Andrew\\\",\\\"description\\\":\\\"Call customer first before delivery.\\\",\\\"address\\\":\\\"0314 Santa Ana\\\",\\\"landline\\\":\\\"1234567\\\",\\\"phone\\\":\\\"+639055625909\\\"},\\\"delivery_products\\\":[{\\\"branch_product_id\\\":1,\\\"quantity\\\":10,\\\"price\\\":\\\"2090.00\\\"},{\\\"branch_product_id\\\":7,\\\"quantity\\\":10,\\\"price\\\":\\\"1970.00\\\"},{\\\"branch_product_id\\\":13,\\\"quantity\\\":10,\\\"price\\\":\\\"1105.00\\\"},{\\\"branch_product_id\\\":19,\\\"quantity\\\":10,\\\"price\\\":\\\"1786.00\\\"}]}\"'),
(24, '2021-12-04 16:52:32.057384', '127.0.0.1:8000', '/v1/deliveries/1/', 'PATCH', 'http://127.0.0.1:8000/v1/deliveries/1/', 200, NULL, '\"{\\\"status\\\":\\\"delivered\\\",\\\"prepared_by\\\":\\\"Christina\\\",\\\"checked_by\\\":\\\"Venz\\\",\\\"pulled_out_by\\\":\\\"Wena\\\",\\\"delivered_by\\\":\\\"Daryl\\\",\\\"datetime_completed\\\":\\\"2021-12-05 00:52:31\\\"}\"'),
(25, '2021-12-04 16:53:19.360639', '127.0.0.1:8000', '/v1/deliveries/', 'POST', 'http://127.0.0.1:8000/v1/deliveries/', 200, NULL, '\"{\\\"branch_id\\\":1,\\\"delivery_type\\\":\\\"delivery\\\",\\\"datetime_delivery\\\":\\\"2021-12-05 04:56:52\\\",\\\"customer\\\":{\\\"id\\\":2,\\\"name\\\":\\\"Mr. Andrew\\\",\\\"description\\\":\\\"Call customer first before delivery.\\\",\\\"address\\\":\\\"0314 Santa Ana\\\",\\\"landline\\\":\\\"1234567\\\",\\\"phone\\\":\\\"+639055625909\\\"},\\\"delivery_products\\\":[{\\\"branch_product_id\\\":13,\\\"quantity\\\":12,\\\"price\\\":\\\"1105.00\\\"},{\\\"branch_product_id\\\":19,\\\"quantity\\\":12,\\\"price\\\":\\\"1786.00\\\"},{\\\"branch_product_id\\\":25,\\\"quantity\\\":12,\\\"price\\\":\\\"1148.00\\\"},{\\\"branch_product_id\\\":31,\\\"quantity\\\":12,\\\"price\\\":\\\"1148.00\\\"}]}\"'),
(26, '2021-12-04 16:54:50.987720', '127.0.0.1:8000', '/v1/deliveries/', 'POST', 'http://127.0.0.1:8000/v1/deliveries/', 200, NULL, '\"{\\\"branch_id\\\":1,\\\"delivery_type\\\":\\\"delivery\\\",\\\"datetime_delivery\\\":\\\"2021-12-05 00:00:00\\\",\\\"customer\\\":{\\\"id\\\":2,\\\"name\\\":\\\"Mr. Andrew\\\",\\\"description\\\":\\\"Call customer first before delivery.\\\",\\\"address\\\":\\\"0314 Santa Ana\\\",\\\"landline\\\":\\\"1234567\\\",\\\"phone\\\":\\\"+639055625909\\\"},\\\"delivery_products\\\":[{\\\"branch_product_id\\\":13,\\\"quantity\\\":10,\\\"price\\\":\\\"1105.00\\\"},{\\\"branch_product_id\\\":19,\\\"quantity\\\":10,\\\"price\\\":\\\"1786.00\\\"},{\\\"branch_product_id\\\":25,\\\"quantity\\\":10,\\\"price\\\":\\\"1148.00\\\"},{\\\"branch_product_id\\\":31,\\\"quantity\\\":10,\\\"price\\\":\\\"1148.00\\\"}]}\"'),
(27, '2021-12-04 16:56:10.835173', '127.0.0.1:8000', '/v1/preorders/', 'POST', 'http://127.0.0.1:8000/v1/preorders/', 200, NULL, '\"{\\\"branch_id\\\":1,\\\"delivery_type\\\":\\\"delivery\\\",\\\"supplier\\\":{\\\"id\\\":1,\\\"name\\\":\\\"Mr. Jonathan\\\",\\\"description\\\":\\\"Usually arrives 10mins before delivery time.\\\",\\\"address\\\":\\\"Cebu City\\\",\\\"landline\\\":\\\"123123\\\",\\\"phone\\\":\\\"0905 123 4567\\\"},\\\"preorder_products\\\":[{\\\"branch_product_id\\\":13,\\\"quantity\\\":10},{\\\"branch_product_id\\\":25,\\\"quantity\\\":10},{\\\"branch_product_id\\\":19,\\\"quantity\\\":10},{\\\"branch_product_id\\\":31,\\\"quantity\\\":10}]}\"'),
(28, '2021-12-04 16:57:33.246052', '127.0.0.1:8000', '/v1/deliveries/2/', 'PATCH', 'http://127.0.0.1:8000/v1/deliveries/2/', 200, NULL, '\"{\\\"status\\\":\\\"delivered\\\",\\\"prepared_by\\\":\\\"\\\",\\\"checked_by\\\":\\\"\\\",\\\"pulled_out_by\\\":\\\"\\\",\\\"delivered_by\\\":\\\"\\\",\\\"datetime_completed\\\":\\\"2021-12-05 00:57:33\\\"}\"'),
(29, '2021-12-04 16:57:48.854946', '127.0.0.1:8000', '/v1/preorders/3/', 'PATCH', 'http://127.0.0.1:8000/v1/preorders/3/', 200, NULL, '\"{\\\"status\\\":\\\"approved\\\"}\"'),
(30, '2021-12-04 16:57:58.100296', '127.0.0.1:8000', '/v1/preorder-transactions/', 'POST', 'http://127.0.0.1:8000/v1/preorder-transactions/', 204, NULL, '\"{\\\"preorder_id\\\":3,\\\"preorder_transaction_products\\\":[{\\\"preorder_product_id\\\":9,\\\"quantity\\\":10},{\\\"preorder_product_id\\\":10,\\\"quantity\\\":10},{\\\"preorder_product_id\\\":11,\\\"quantity\\\":10},{\\\"preorder_product_id\\\":12,\\\"quantity\\\":10}]}\"'),
(31, '2021-12-04 16:58:00.864265', '127.0.0.1:8000', '/v1/preorders/3/', 'PATCH', 'http://127.0.0.1:8000/v1/preorders/3/', 200, NULL, '\"{\\\"status\\\":\\\"delivered\\\"}\"'),
(32, '2021-12-04 18:04:26.828139', '127.0.0.1:8000', '/v1/preorders/', 'POST', 'http://127.0.0.1:8000/v1/preorders/', 200, NULL, '\"{\\\"branch_id\\\":1,\\\"delivery_type\\\":\\\"delivery\\\",\\\"supplier\\\":{\\\"id\\\":1,\\\"name\\\":\\\"Mr. Jonathan\\\",\\\"description\\\":\\\"Usually arrives 10mins before delivery time.\\\",\\\"address\\\":\\\"Cebu City\\\",\\\"landline\\\":\\\"123123\\\",\\\"phone\\\":\\\"0905 123 4567\\\"},\\\"preorder_products\\\":[{\\\"branch_product_id\\\":1,\\\"quantity\\\":10},{\\\"branch_product_id\\\":7,\\\"quantity\\\":10},{\\\"branch_product_id\\\":13,\\\"quantity\\\":10},{\\\"branch_product_id\\\":25,\\\"quantity\\\":10},{\\\"branch_product_id\\\":19,\\\"quantity\\\":10},{\\\"branch_product_id\\\":31,\\\"quantity\\\":10}]}\"'),
(33, '2021-12-04 18:04:31.865505', '127.0.0.1:8000', '/v1/preorders/4/', 'PATCH', 'http://127.0.0.1:8000/v1/preorders/4/', 200, NULL, '\"{\\\"status\\\":\\\"approved\\\"}\"'),
(34, '2021-12-04 18:04:37.897975', '127.0.0.1:8000', '/v1/preorder-transactions/', 'POST', 'http://127.0.0.1:8000/v1/preorder-transactions/', 204, NULL, '\"{\\\"preorder_id\\\":4,\\\"preorder_transaction_products\\\":[{\\\"preorder_product_id\\\":13,\\\"quantity\\\":10},{\\\"preorder_product_id\\\":14,\\\"quantity\\\":10},{\\\"preorder_product_id\\\":15,\\\"quantity\\\":10},{\\\"preorder_product_id\\\":16,\\\"quantity\\\":10},{\\\"preorder_product_id\\\":17,\\\"quantity\\\":10},{\\\"preorder_product_id\\\":18,\\\"quantity\\\":10}]}\"'),
(35, '2021-12-04 18:12:26.030632', '127.0.0.1:8000', '/v1/preorders/4/', 'PATCH', 'http://127.0.0.1:8000/v1/preorders/4/', 200, NULL, '\"{\\\"status\\\":\\\"delivered\\\"}\"'),
(36, '2021-12-04 18:18:54.570901', '127.0.0.1:8000', '/v1/deliveries/', 'POST', 'http://127.0.0.1:8000/v1/deliveries/', 200, NULL, '\"{\\\"branch_id\\\":1,\\\"delivery_type\\\":\\\"delivery\\\",\\\"datetime_delivery\\\":\\\"2021-12-05 02:17:47\\\",\\\"customer\\\":{\\\"id\\\":2,\\\"name\\\":\\\"Mr. Andrew\\\",\\\"description\\\":\\\"Call customer first before delivery.\\\",\\\"address\\\":\\\"0314 Santa Ana\\\",\\\"landline\\\":\\\"1234567\\\",\\\"phone\\\":\\\"+639055625909\\\"},\\\"delivery_products\\\":[{\\\"branch_product_id\\\":1,\\\"quantity\\\":10,\\\"price\\\":\\\"2090.00\\\"},{\\\"branch_product_id\\\":7,\\\"quantity\\\":10,\\\"price\\\":\\\"1970.00\\\"},{\\\"branch_product_id\\\":13,\\\"quantity\\\":10,\\\"price\\\":\\\"1105.00\\\"},{\\\"branch_product_id\\\":19,\\\"quantity\\\":4,\\\"price\\\":\\\"1786.00\\\"},{\\\"branch_product_id\\\":25,\\\"quantity\\\":4,\\\"price\\\":\\\"1148.00\\\"},{\\\"branch_product_id\\\":31,\\\"quantity\\\":4,\\\"price\\\":\\\"1148.00\\\"}]}\"'),
(37, '2021-12-04 18:19:29.959956', '127.0.0.1:8000', '/v1/deliveries/4/', 'PATCH', 'http://127.0.0.1:8000/v1/deliveries/4/', 200, NULL, '\"{\\\"status\\\":\\\"delivered\\\",\\\"prepared_by\\\":\\\"\\\",\\\"checked_by\\\":\\\"\\\",\\\"pulled_out_by\\\":\\\"\\\",\\\"delivered_by\\\":\\\"\\\",\\\"datetime_completed\\\":\\\"2021-12-05 02:19:29\\\"}\"'),
(38, '2021-12-04 18:20:12.504320', '127.0.0.1:8000', '/v1/deliveries/', 'POST', 'http://127.0.0.1:8000/v1/deliveries/', 200, NULL, '\"{\\\"branch_id\\\":1,\\\"delivery_type\\\":\\\"delivery\\\",\\\"datetime_delivery\\\":\\\"2021-12-05 02:19:53\\\",\\\"customer\\\":{\\\"id\\\":2,\\\"name\\\":\\\"Mr. Andrew\\\",\\\"description\\\":\\\"Call customer first before delivery.\\\",\\\"address\\\":\\\"0314 Santa Ana\\\",\\\"landline\\\":\\\"1234567\\\",\\\"phone\\\":\\\"+639055625909\\\"},\\\"delivery_products\\\":[{\\\"branch_product_id\\\":19,\\\"quantity\\\":6,\\\"price\\\":\\\"1786.00\\\"},{\\\"branch_product_id\\\":25,\\\"quantity\\\":2,\\\"price\\\":\\\"1148.00\\\"},{\\\"branch_product_id\\\":31,\\\"quantity\\\":2,\\\"price\\\":\\\"1148.00\\\"}]}\"'),
(39, '2021-12-04 18:20:19.194160', '127.0.0.1:8000', '/v1/deliveries/5/', 'PATCH', 'http://127.0.0.1:8000/v1/deliveries/5/', 200, NULL, '\"{\\\"status\\\":\\\"delivered\\\",\\\"prepared_by\\\":\\\"\\\",\\\"checked_by\\\":\\\"\\\",\\\"pulled_out_by\\\":\\\"\\\",\\\"delivered_by\\\":\\\"\\\",\\\"datetime_completed\\\":\\\"2021-12-05 02:20:19\\\"}\"'),
(40, '2021-12-04 18:20:47.592692', '127.0.0.1:8000', '/v1/preorders/', 'POST', 'http://127.0.0.1:8000/v1/preorders/', 200, NULL, '\"{\\\"branch_id\\\":1,\\\"delivery_type\\\":\\\"delivery\\\",\\\"supplier\\\":{\\\"id\\\":1,\\\"name\\\":\\\"Mr. Jonathan\\\",\\\"description\\\":\\\"Usually arrives 10mins before delivery time.\\\",\\\"address\\\":\\\"Cebu City\\\",\\\"landline\\\":\\\"123123\\\",\\\"phone\\\":\\\"0905 123 4567\\\"},\\\"preorder_products\\\":[{\\\"branch_product_id\\\":1,\\\"quantity\\\":15},{\\\"branch_product_id\\\":7,\\\"quantity\\\":15},{\\\"branch_product_id\\\":13,\\\"quantity\\\":15},{\\\"branch_product_id\\\":19,\\\"quantity\\\":15},{\\\"branch_product_id\\\":25,\\\"quantity\\\":15},{\\\"branch_product_id\\\":31,\\\"quantity\\\":15}]}\"'),
(41, '2021-12-04 18:20:52.035206', '127.0.0.1:8000', '/v1/preorders/5/', 'PATCH', 'http://127.0.0.1:8000/v1/preorders/5/', 200, NULL, '\"{\\\"status\\\":\\\"approved\\\"}\"'),
(42, '2021-12-04 18:20:59.894130', '127.0.0.1:8000', '/v1/preorder-transactions/', 'POST', 'http://127.0.0.1:8000/v1/preorder-transactions/', 204, NULL, '\"{\\\"preorder_id\\\":5,\\\"preorder_transaction_products\\\":[{\\\"preorder_product_id\\\":19,\\\"quantity\\\":15},{\\\"preorder_product_id\\\":20,\\\"quantity\\\":15},{\\\"preorder_product_id\\\":21,\\\"quantity\\\":15},{\\\"preorder_product_id\\\":22,\\\"quantity\\\":15},{\\\"preorder_product_id\\\":23,\\\"quantity\\\":15},{\\\"preorder_product_id\\\":24,\\\"quantity\\\":15}]}\"'),
(43, '2021-12-04 18:21:06.314289', '127.0.0.1:8000', '/v1/preorders/5/', 'PATCH', 'http://127.0.0.1:8000/v1/preorders/5/', 200, NULL, '\"{\\\"status\\\":\\\"delivered\\\"}\"'),
(44, '2021-12-05 11:51:17.512092', '127.0.0.1:8000', '/v1/users/login/', 'POST', 'http://127.0.0.1:8000/v1/users/login/', 200, NULL, '\"{\\\"login\\\":\\\"andrew\\\",\\\"password\\\":\\\"123456\\\"}\"'),
(45, '2021-12-05 12:58:23.090209', '127.0.0.1:8000', '/v1/users/login/', 'POST', 'http://127.0.0.1:8000/v1/users/login/', 200, NULL, '\"{\\\"login\\\":\\\"andrew\\\",\\\"password\\\":\\\"123456\\\",\\\"branchId\\\":1}\"'),
(46, '2021-12-24 04:00:02.985652', '127.0.0.1:8000', '/v1/transactions/', 'POST', 'http://127.0.0.1:8000/v1/transactions/', 200, NULL, '\"{\\\"amount_tendered\\\":1500,\\\"branch_id\\\":1,\\\"transaction_products\\\":[{\\\"branch_product_id\\\":31,\\\"price\\\":\\\"1148.00\\\",\\\"quantity\\\":\\\"1\\\"}]}\"'),
(47, '2021-12-24 04:00:58.915199', '127.0.0.1:8000', '/v1/transactions/', 'POST', 'http://127.0.0.1:8000/v1/transactions/', 200, NULL, '\"{\\\"amount_tendered\\\":2100,\\\"branch_id\\\":1,\\\"transaction_products\\\":[{\\\"branch_product_id\\\":1,\\\"price\\\":\\\"2090.00\\\",\\\"quantity\\\":\\\"1\\\"}]}\"'),
(48, '2021-12-24 04:01:35.053415', '127.0.0.1:8000', '/v1/transactions/', 'POST', 'http://127.0.0.1:8000/v1/transactions/', 200, NULL, '\"{\\\"amount_tendered\\\":32000,\\\"branch_id\\\":1,\\\"transaction_products\\\":[{\\\"branch_product_id\\\":1,\\\"price\\\":\\\"2090.00\\\",\\\"quantity\\\":\\\"15\\\"}]}\"'),
(49, '2021-12-24 04:06:41.410514', '127.0.0.1:8000', '/v1/transactions/', 'POST', 'http://127.0.0.1:8000/v1/transactions/', 200, NULL, '\"{\\\"amount_tendered\\\":30000,\\\"branch_id\\\":1,\\\"transaction_products\\\":[{\\\"branch_product_id\\\":7,\\\"price\\\":\\\"1970.00\\\",\\\"quantity\\\":\\\"15\\\"}]}\"'),
(50, '2021-12-24 04:11:18.571947', '127.0.0.1:8000', '/v1/transactions/', 'POST', 'http://127.0.0.1:8000/v1/transactions/', 200, NULL, '\"{\\\"amount_tendered\\\":2000,\\\"branch_id\\\":1,\\\"transaction_products\\\":[{\\\"branch_product_id\\\":13,\\\"price\\\":\\\"1105.00\\\",\\\"quantity\\\":\\\"1\\\"}]}\"'),
(51, '2021-12-24 04:11:33.144156', '127.0.0.1:8000', '/v1/transactions/', 'POST', 'http://127.0.0.1:8000/v1/transactions/', 200, NULL, '\"{\\\"amount_tendered\\\":2000,\\\"branch_id\\\":1,\\\"transaction_products\\\":[{\\\"branch_product_id\\\":13,\\\"price\\\":\\\"1105.00\\\",\\\"quantity\\\":\\\"1\\\"}]}\"'),
(52, '2022-01-13 06:44:37.632809', '127.0.0.1:8000', '/v1/users/login/', 'POST', 'http://127.0.0.1:8000/v1/users/login/', 200, NULL, '\"{\\\"login\\\":\\\"andrew\\\",\\\"password\\\":\\\"123456\\\",\\\"branchId\\\":1}\"'),
(53, '2022-01-15 09:15:27.751626', '127.0.0.1:8000', '/v1/users/login/', 'POST', 'http://127.0.0.1:8000/v1/users/login/', 200, NULL, '\"{\\\"login\\\":\\\"andrew\\\",\\\"password\\\":\\\"123456\\\"}\"'),
(54, '2022-01-15 10:38:37.856497', '127.0.0.1:8000', '/v1/preorders/', 'POST', 'http://127.0.0.1:8000/v1/preorders/', 200, NULL, '\"{\\\"branch_id\\\":1,\\\"delivery_type\\\":\\\"delivery\\\",\\\"supplier\\\":{\\\"id\\\":1,\\\"name\\\":\\\"Mr. Jonathan\\\",\\\"description\\\":\\\"Usually arrives 10mins before delivery time.\\\",\\\"address\\\":\\\"Cebu City\\\",\\\"landline\\\":\\\"123123\\\",\\\"phone\\\":\\\"0905 123 4567\\\"},\\\"preorder_products\\\":[]}\"'),
(55, '2022-01-15 10:38:50.993117', '127.0.0.1:8000', '/v1/preorders/6/', 'PATCH', 'http://127.0.0.1:8000/v1/preorders/6/', 200, NULL, '\"{\\\"status\\\":\\\"cancelled\\\"}\"'),
(56, '2022-01-15 10:42:26.401714', '127.0.0.1:8000', '/v1/preorders/', 'POST', 'http://127.0.0.1:8000/v1/preorders/', 200, NULL, '\"{\\\"branch_id\\\":1,\\\"delivery_type\\\":\\\"delivery\\\",\\\"supplier\\\":{\\\"id\\\":1,\\\"name\\\":\\\"Mr. Jonathan\\\",\\\"description\\\":\\\"Usually arrives 10mins before delivery time.\\\",\\\"address\\\":\\\"Cebu City\\\",\\\"landline\\\":\\\"123123\\\",\\\"phone\\\":\\\"0905 123 4567\\\"},\\\"preorder_products\\\":[{\\\"branch_product_id\\\":1,\\\"quantity\\\":5},{\\\"branch_product_id\\\":7,\\\"quantity\\\":5}]}\"'),
(57, '2022-01-15 10:43:57.298642', '127.0.0.1:8000', '/v1/preorders/7/', 'PATCH', 'http://127.0.0.1:8000/v1/preorders/7/', 200, NULL, '\"{\\\"status\\\":\\\"approved\\\"}\"'),
(58, '2022-01-15 10:47:40.525995', '127.0.0.1:8000', '/v1/preorder-transactions/', 'POST', 'http://127.0.0.1:8000/v1/preorder-transactions/', 204, NULL, '\"{\\\"preorder_id\\\":7,\\\"preorder_transaction_products\\\":[{\\\"preorder_product_id\\\":25,\\\"quantity\\\":5},{\\\"preorder_product_id\\\":26,\\\"quantity\\\":0}]}\"'),
(59, '2022-01-15 10:48:08.258445', '127.0.0.1:8000', '/v1/preorder-transactions/', 'POST', 'http://127.0.0.1:8000/v1/preorder-transactions/', 204, NULL, '\"{\\\"preorder_id\\\":7,\\\"preorder_transaction_products\\\":[{\\\"preorder_product_id\\\":25,\\\"quantity\\\":0},{\\\"preorder_product_id\\\":26,\\\"quantity\\\":5}]}\"'),
(60, '2022-01-15 10:56:38.864608', '127.0.0.1:8000', '/v1/preorders/7/', 'PATCH', 'http://127.0.0.1:8000/v1/preorders/7/', 200, NULL, '\"{\\\"status\\\":\\\"delivered\\\"}\"'),
(61, '2022-01-15 11:00:40.872913', '127.0.0.1:8000', '/v1/deliveries/', 'POST', 'http://127.0.0.1:8000/v1/deliveries/', 200, NULL, '\"{\\\"branch_id\\\":1,\\\"delivery_type\\\":\\\"delivery\\\",\\\"datetime_delivery\\\":\\\"2022-01-17 15:00:57\\\",\\\"customer\\\":{\\\"id\\\":2,\\\"name\\\":\\\"Mr. Andrew\\\",\\\"description\\\":\\\"Call customer first before delivery.\\\",\\\"address\\\":\\\"0314 Santa Ana\\\",\\\"landline\\\":\\\"1234567\\\",\\\"phone\\\":\\\"+639055625909\\\"},\\\"delivery_products\\\":[{\\\"branch_product_id\\\":1,\\\"quantity\\\":6,\\\"price\\\":\\\"2090.00\\\"},{\\\"branch_product_id\\\":7,\\\"quantity\\\":6,\\\"price\\\":\\\"1970.00\\\"}]}\"'),
(62, '2022-01-15 11:01:08.961661', '127.0.0.1:8000', '/v1/deliveries/6/', 'PATCH', 'http://127.0.0.1:8000/v1/deliveries/6/', 200, NULL, '\"{\\\"status\\\":\\\"delivered\\\",\\\"prepared_by\\\":\\\"\\\",\\\"checked_by\\\":\\\"\\\",\\\"pulled_out_by\\\":\\\"\\\",\\\"delivered_by\\\":\\\"\\\",\\\"datetime_completed\\\":\\\"2022-01-15 19:01:08\\\"}\"'),
(63, '2022-01-15 11:02:08.861874', '127.0.0.1:8000', '/v1/preorders/', 'POST', 'http://127.0.0.1:8000/v1/preorders/', 200, NULL, '\"{\\\"branch_id\\\":1,\\\"delivery_type\\\":\\\"delivery\\\",\\\"supplier\\\":{\\\"id\\\":1,\\\"name\\\":\\\"Mr. Jonathan\\\",\\\"description\\\":\\\"Usually arrives 10mins before delivery time.\\\",\\\"address\\\":\\\"Cebu City\\\",\\\"landline\\\":\\\"123123\\\",\\\"phone\\\":\\\"0905 123 4567\\\"},\\\"preorder_products\\\":[{\\\"branch_product_id\\\":1,\\\"quantity\\\":10},{\\\"branch_product_id\\\":7,\\\"quantity\\\":10}]}\"'),
(64, '2022-01-15 11:02:12.028890', '127.0.0.1:8000', '/v1/preorders/8/', 'PATCH', 'http://127.0.0.1:8000/v1/preorders/8/', 200, NULL, '\"{\\\"status\\\":\\\"approved\\\"}\"'),
(65, '2022-01-15 11:02:16.395932', '127.0.0.1:8000', '/v1/preorder-transactions/', 'POST', 'http://127.0.0.1:8000/v1/preorder-transactions/', 204, NULL, '\"{\\\"preorder_id\\\":8,\\\"preorder_transaction_products\\\":[{\\\"preorder_product_id\\\":27,\\\"quantity\\\":10},{\\\"preorder_product_id\\\":28,\\\"quantity\\\":10}]}\"'),
(66, '2022-01-15 11:02:20.934341', '127.0.0.1:8000', '/v1/preorders/8/', 'PATCH', 'http://127.0.0.1:8000/v1/preorders/8/', 200, NULL, '\"{\\\"status\\\":\\\"delivered\\\"}\"'),
(67, '2022-01-16 01:02:17.948549', '127.0.0.1:8000', '/v1/preorders/', 'POST', 'http://127.0.0.1:8000/v1/preorders/', 200, NULL, '\"{\\\"branch_id\\\":1,\\\"delivery_type\\\":\\\"delivery\\\",\\\"supplier\\\":{\\\"id\\\":1,\\\"name\\\":\\\"Mr. Jonathan\\\",\\\"description\\\":\\\"Usually arrives 10mins before delivery time.\\\",\\\"address\\\":\\\"Cebu City\\\",\\\"landline\\\":\\\"123123\\\",\\\"phone\\\":\\\"0905 123 4567\\\"},\\\"preorder_products\\\":[{\\\"branch_product_id\\\":13,\\\"quantity\\\":10},{\\\"branch_product_id\\\":19,\\\"quantity\\\":10}]}\"'),
(68, '2022-01-16 01:03:08.279368', '127.0.0.1:8000', '/v1/preorders/9/', 'PATCH', 'http://127.0.0.1:8000/v1/preorders/9/', 200, NULL, '\"{\\\"status\\\":\\\"cancelled\\\"}\"'),
(69, '2022-01-16 01:03:48.096332', '127.0.0.1:8000', '/v1/preorders/', 'POST', 'http://127.0.0.1:8000/v1/preorders/', 200, NULL, '\"{\\\"branch_id\\\":1,\\\"delivery_type\\\":\\\"delivery\\\",\\\"supplier\\\":{\\\"id\\\":1,\\\"name\\\":\\\"Mr. Jonathan\\\",\\\"description\\\":\\\"Usually arrives 10mins before delivery time.\\\",\\\"address\\\":\\\"Cebu City\\\",\\\"landline\\\":\\\"123123\\\",\\\"phone\\\":\\\"0905 123 4567\\\"},\\\"preorder_products\\\":[{\\\"branch_product_id\\\":13,\\\"quantity\\\":10},{\\\"branch_product_id\\\":19,\\\"quantity\\\":10}]}\"'),
(70, '2022-01-16 01:03:53.248413', '127.0.0.1:8000', '/v1/preorders/10/', 'PATCH', 'http://127.0.0.1:8000/v1/preorders/10/', 200, NULL, '\"{\\\"status\\\":\\\"approved\\\"}\"'),
(71, '2022-01-16 01:04:39.942020', '127.0.0.1:8000', '/v1/preorder-transactions/', 'POST', 'http://127.0.0.1:8000/v1/preorder-transactions/', 204, NULL, '\"{\\\"preorder_id\\\":10,\\\"preorder_transaction_products\\\":[{\\\"preorder_product_id\\\":31,\\\"quantity\\\":10},{\\\"preorder_product_id\\\":32,\\\"quantity\\\":0}]}\"'),
(72, '2022-01-16 01:05:01.227040', '127.0.0.1:8000', '/v1/preorder-transactions/', 'POST', 'http://127.0.0.1:8000/v1/preorder-transactions/', 204, NULL, '\"{\\\"preorder_id\\\":10,\\\"preorder_transaction_products\\\":[{\\\"preorder_product_id\\\":31,\\\"quantity\\\":0},{\\\"preorder_product_id\\\":32,\\\"quantity\\\":10}]}\"'),
(73, '2022-01-16 01:05:19.329560', '127.0.0.1:8000', '/v1/preorders/10/', 'PATCH', 'http://127.0.0.1:8000/v1/preorders/10/', 200, NULL, '\"{\\\"status\\\":\\\"delivered\\\"}\"'),
(74, '2022-01-16 01:10:06.120445', '127.0.0.1:8000', '/v1/deliveries/', 'POST', 'http://127.0.0.1:8000/v1/deliveries/', 200, NULL, '\"{\\\"branch_id\\\":1,\\\"delivery_type\\\":\\\"delivery\\\",\\\"datetime_delivery\\\":\\\"2022-01-17 10:00:26\\\",\\\"customer\\\":{\\\"name\\\":\\\"Mr. Juan\\\",\\\"description\\\":\\\"customer description here\\\",\\\"address\\\":\\\"Cebu\\\",\\\"landline\\\":\\\"123 4567\\\",\\\"phone\\\":\\\"0905 123 4567\\\"},\\\"delivery_products\\\":[{\\\"branch_product_id\\\":1,\\\"quantity\\\":5,\\\"price\\\":\\\"2090.00\\\"},{\\\"branch_product_id\\\":7,\\\"quantity\\\":5,\\\"price\\\":\\\"1970.00\\\"},{\\\"branch_product_id\\\":13,\\\"quantity\\\":5,\\\"price\\\":\\\"1105.00\\\"},{\\\"branch_product_id\\\":19,\\\"quantity\\\":5,\\\"price\\\":\\\"1786.00\\\"}]}\"'),
(75, '2022-01-16 01:13:26.584584', '127.0.0.1:8000', '/v1/deliveries/7/', 'PATCH', 'http://127.0.0.1:8000/v1/deliveries/7/', 200, NULL, '\"{\\\"status\\\":\\\"delivered\\\",\\\"prepared_by\\\":\\\"Andrew\\\",\\\"checked_by\\\":\\\"Andrew\\\",\\\"pulled_out_by\\\":\\\"\\\",\\\"delivered_by\\\":\\\"Andrew, Jonathan\\\",\\\"datetime_completed\\\":\\\"2022-01-16 09:13:26\\\"}\"'),
(76, '2022-01-16 01:20:12.570578', '127.0.0.1:8000', '/v1/preorders/', 'POST', 'http://127.0.0.1:8000/v1/preorders/', 200, NULL, '\"{\\\"branch_id\\\":1,\\\"delivery_type\\\":\\\"delivery\\\",\\\"supplier\\\":{\\\"id\\\":1,\\\"name\\\":\\\"Mr. Jonathan\\\",\\\"description\\\":\\\"Usually arrives 10mins before delivery time.\\\",\\\"address\\\":\\\"Cebu City\\\",\\\"landline\\\":\\\"123123\\\",\\\"phone\\\":\\\"0905 123 4567\\\"},\\\"preorder_products\\\":[{\\\"branch_product_id\\\":1,\\\"quantity\\\":5},{\\\"branch_product_id\\\":7,\\\"quantity\\\":5},{\\\"branch_product_id\\\":13,\\\"quantity\\\":5},{\\\"branch_product_id\\\":19,\\\"quantity\\\":5}]}\"'),
(77, '2022-01-16 01:20:20.151710', '127.0.0.1:8000', '/v1/preorders/11/', 'PATCH', 'http://127.0.0.1:8000/v1/preorders/11/', 200, NULL, '\"{\\\"status\\\":\\\"approved\\\"}\"'),
(78, '2022-01-16 01:20:40.965687', '127.0.0.1:8000', '/v1/preorder-transactions/', 'POST', 'http://127.0.0.1:8000/v1/preorder-transactions/', 204, NULL, '\"{\\\"preorder_id\\\":11,\\\"preorder_transaction_products\\\":[{\\\"preorder_product_id\\\":33,\\\"quantity\\\":5},{\\\"preorder_product_id\\\":34,\\\"quantity\\\":5},{\\\"preorder_product_id\\\":35,\\\"quantity\\\":5},{\\\"preorder_product_id\\\":36,\\\"quantity\\\":5}]}\"'),
(79, '2022-01-16 01:20:48.181736', '127.0.0.1:8000', '/v1/preorders/11/', 'PATCH', 'http://127.0.0.1:8000/v1/preorders/11/', 200, NULL, '\"{\\\"status\\\":\\\"delivered\\\"}\"'),
(80, '2022-01-16 01:35:47.053441', '127.0.0.1:8000', '/v1/users/login/', 'POST', 'http://127.0.0.1:8000/v1/users/login/', 200, NULL, '\"{\\\"login\\\":\\\"andrew\\\",\\\"password\\\":\\\"123456\\\",\\\"branchId\\\":1}\"'),
(81, '2022-01-16 01:37:38.171321', '127.0.0.1:8000', '/v1/transactions/', 'POST', 'http://127.0.0.1:8000/v1/transactions/', 200, NULL, '\"{\\\"amount_tendered\\\":6100,\\\"branch_id\\\":1,\\\"transaction_products\\\":[{\\\"branch_product_id\\\":7,\\\"price\\\":\\\"1970.00\\\",\\\"quantity\\\":\\\"2\\\"},{\\\"branch_product_id\\\":1,\\\"price\\\":\\\"2090.00\\\",\\\"quantity\\\":\\\"1\\\"}]}\"'),
(82, '2022-01-16 05:56:01.025343', '127.0.0.1:8000', '/v1/users/login/', 'POST', 'http://127.0.0.1:8000/v1/users/login/', 200, NULL, '\"{\\\"login\\\":\\\"andrew\\\",\\\"password\\\":\\\"123456\\\"}\"'),
(83, '2022-01-16 06:37:15.806674', '127.0.0.1:8000', '/v1/users/login/', 'POST', 'http://127.0.0.1:8000/v1/users/login/', 200, NULL, '\"{\\\"login\\\":\\\"andrew\\\",\\\"password\\\":\\\"123456\\\"}\"'),
(84, '2022-01-16 06:37:22.730613', '127.0.0.1:8000', '/v1/users/login/', 'POST', 'http://127.0.0.1:8000/v1/users/login/', 200, NULL, '\"{\\\"login\\\":\\\"andrew\\\",\\\"password\\\":\\\"123456\\\"}\"'),
(85, '2022-01-16 08:15:47.962543', '127.0.0.1:8000', '/v1/users/login/', 'POST', 'http://127.0.0.1:8000/v1/users/login/', 200, NULL, '\"{\\\"login\\\":\\\"andrew\\\",\\\"password\\\":\\\"123456\\\"}\"'),
(86, '2022-01-16 08:20:13.769213', '127.0.0.1:8000', '/v1/preorders/', 'POST', 'http://127.0.0.1:8000/v1/preorders/', 200, NULL, '\"{\\\"branch_id\\\":1,\\\"delivery_type\\\":\\\"delivery\\\",\\\"supplier\\\":{\\\"name\\\":\\\"Ms. Jane\\\",\\\"description\\\":\\\"supplier description here\\\",\\\"address\\\":\\\"Cebu\\\",\\\"landline\\\":\\\"123 4567\\\",\\\"phone\\\":\\\"0905 123 456\\\"},\\\"preorder_products\\\":[{\\\"branch_product_id\\\":1,\\\"quantity\\\":10},{\\\"branch_product_id\\\":7,\\\"quantity\\\":10}]}\"'),
(87, '2022-01-16 08:21:41.245641', '127.0.0.1:8000', '/v1/preorders/12/', 'PATCH', 'http://127.0.0.1:8000/v1/preorders/12/', 200, NULL, '\"{\\\"status\\\":\\\"approved\\\"}\"'),
(88, '2022-01-16 08:22:52.427269', '127.0.0.1:8000', '/v1/preorder-transactions/', 'POST', 'http://127.0.0.1:8000/v1/preorder-transactions/', 204, NULL, '\"{\\\"preorder_id\\\":12,\\\"preorder_transaction_products\\\":[{\\\"preorder_product_id\\\":37,\\\"quantity\\\":10},{\\\"preorder_product_id\\\":38,\\\"quantity\\\":0}]}\"'),
(89, '2022-01-16 08:23:29.984389', '127.0.0.1:8000', '/v1/preorder-transactions/', 'POST', 'http://127.0.0.1:8000/v1/preorder-transactions/', 204, NULL, '\"{\\\"preorder_id\\\":12,\\\"preorder_transaction_products\\\":[{\\\"preorder_product_id\\\":37,\\\"quantity\\\":0},{\\\"preorder_product_id\\\":38,\\\"quantity\\\":10}]}\"'),
(90, '2022-01-16 08:23:39.595898', '127.0.0.1:8000', '/v1/preorders/12/', 'PATCH', 'http://127.0.0.1:8000/v1/preorders/12/', 200, NULL, '\"{\\\"status\\\":\\\"delivered\\\"}\"'),
(91, '2022-01-16 08:32:30.860780', '127.0.0.1:8000', '/v1/deliveries/', 'POST', 'http://127.0.0.1:8000/v1/deliveries/', 200, NULL, '\"{\\\"branch_id\\\":1,\\\"delivery_type\\\":\\\"delivery\\\",\\\"datetime_delivery\\\":\\\"2022-01-17 10:00:01\\\",\\\"customer\\\":{\\\"id\\\":2,\\\"name\\\":\\\"Mr. Andrew\\\",\\\"description\\\":\\\"Call customer first before delivery.\\\",\\\"address\\\":\\\"0314 Santa Ana\\\",\\\"landline\\\":\\\"1234567\\\",\\\"phone\\\":\\\"+639055625909\\\"},\\\"delivery_products\\\":[{\\\"branch_product_id\\\":1,\\\"quantity\\\":5,\\\"price\\\":\\\"2090.00\\\"},{\\\"branch_product_id\\\":7,\\\"quantity\\\":10,\\\"price\\\":\\\"1970.00\\\"}]}\"'),
(92, '2022-01-16 08:39:53.726887', '127.0.0.1:8000', '/v1/deliveries/8/', 'PATCH', 'http://127.0.0.1:8000/v1/deliveries/8/', 200, NULL, '\"{\\\"status\\\":\\\"delivered\\\",\\\"prepared_by\\\":\\\"\\\",\\\"checked_by\\\":\\\"\\\",\\\"pulled_out_by\\\":\\\"\\\",\\\"delivered_by\\\":\\\"\\\",\\\"datetime_completed\\\":\\\"2022-01-16 16:39:53\\\"}\"'),
(93, '2022-01-16 08:41:16.965869', '127.0.0.1:8000', '/v1/preorders/', 'POST', 'http://127.0.0.1:8000/v1/preorders/', 200, NULL, '\"{\\\"branch_id\\\":1,\\\"delivery_type\\\":\\\"delivery\\\",\\\"supplier\\\":{\\\"id\\\":4,\\\"name\\\":\\\"Ms. Jane\\\",\\\"description\\\":\\\"supplier description here\\\",\\\"address\\\":\\\"Cebu\\\",\\\"landline\\\":\\\"123 4567\\\",\\\"phone\\\":\\\"0905 123 456\\\"},\\\"preorder_products\\\":[{\\\"branch_product_id\\\":1,\\\"quantity\\\":5},{\\\"branch_product_id\\\":7,\\\"quantity\\\":10}]}\"'),
(94, '2022-01-16 08:41:21.949656', '127.0.0.1:8000', '/v1/preorders/13/', 'PATCH', 'http://127.0.0.1:8000/v1/preorders/13/', 200, NULL, '\"{\\\"status\\\":\\\"approved\\\"}\"'),
(95, '2022-01-16 08:41:34.982789', '127.0.0.1:8000', '/v1/preorder-transactions/', 'POST', 'http://127.0.0.1:8000/v1/preorder-transactions/', 204, NULL, '\"{\\\"preorder_id\\\":13,\\\"preorder_transaction_products\\\":[{\\\"preorder_product_id\\\":39,\\\"quantity\\\":5},{\\\"preorder_product_id\\\":40,\\\"quantity\\\":10}]}\"'),
(96, '2022-01-16 08:41:38.685590', '127.0.0.1:8000', '/v1/preorders/13/', 'PATCH', 'http://127.0.0.1:8000/v1/preorders/13/', 200, NULL, '\"{\\\"status\\\":\\\"delivered\\\"}\"'),
(97, '2022-01-16 08:47:21.573752', '127.0.0.1:8000', '/v1/deliveries/', 'POST', 'http://127.0.0.1:8000/v1/deliveries/', 200, NULL, '\"{\\\"branch_id\\\":1,\\\"delivery_type\\\":\\\"delivery\\\",\\\"datetime_delivery\\\":\\\"2022-01-16 16:46:52\\\",\\\"customer\\\":{\\\"id\\\":2,\\\"name\\\":\\\"Mr. Andrew\\\",\\\"description\\\":\\\"Call customer first before delivery.\\\",\\\"address\\\":\\\"0314 Santa Ana\\\",\\\"landline\\\":\\\"1234567\\\",\\\"phone\\\":\\\"+639055625909\\\"},\\\"delivery_products\\\":[{\\\"branch_product_id\\\":1,\\\"quantity\\\":1,\\\"price\\\":\\\"2090.00\\\"},{\\\"branch_product_id\\\":7,\\\"quantity\\\":1,\\\"price\\\":\\\"1970.00\\\"}]}\"'),
(98, '2022-01-16 09:07:34.735431', '127.0.0.1:8000', '/v1/users/login/', 'POST', 'http://127.0.0.1:8000/v1/users/login/', 200, NULL, '\"{\\\"login\\\":\\\"andrew\\\",\\\"password\\\":\\\"123456\\\",\\\"branchId\\\":1}\"'),
(99, '2022-01-16 09:11:46.029850', '127.0.0.1:8000', '/v1/transactions/', 'POST', 'http://127.0.0.1:8000/v1/transactions/', 200, NULL, '\"{\\\"amount_tendered\\\":6100,\\\"branch_id\\\":1,\\\"transaction_products\\\":[{\\\"branch_product_id\\\":7,\\\"price\\\":\\\"1970.00\\\",\\\"quantity\\\":\\\"2\\\"},{\\\"branch_product_id\\\":1,\\\"price\\\":\\\"2090.00\\\",\\\"quantity\\\":\\\"1\\\"}]}\"'),
(100, '2022-02-01 13:58:37.611219', '127.0.0.1:8000', '/v1/transactions/', 'POST', 'http://127.0.0.1:8000/v1/transactions/', 200, NULL, '\"{\\\"amount_tendered\\\":2100,\\\"branch_id\\\":1,\\\"transaction_products\\\":[{\\\"branch_product_id\\\":1,\\\"price\\\":\\\"2090.00\\\",\\\"quantity\\\":\\\"1\\\"}]}\"'),
(101, '2022-02-01 13:59:24.865446', '127.0.0.1:8000', '/v1/transactions/', 'POST', 'http://127.0.0.1:8000/v1/transactions/', 200, NULL, '\"{\\\"amount_tendered\\\":2100,\\\"branch_id\\\":1,\\\"transaction_products\\\":[{\\\"branch_product_id\\\":1,\\\"price\\\":\\\"2090.00\\\",\\\"quantity\\\":\\\"1\\\"}]}\"'),
(102, '2022-02-01 14:17:31.902549', '127.0.0.1:8000', '/v1/transactions/', 'POST', 'http://127.0.0.1:8000/v1/transactions/', 200, NULL, '\"{\\\"amount_tendered\\\":2000,\\\"branch_id\\\":1,\\\"transaction_products\\\":[{\\\"branch_product_id\\\":7,\\\"price\\\":\\\"1970.00\\\",\\\"quantity\\\":\\\"1\\\"}]}\"'),
(103, '2022-02-01 14:17:56.596051', '127.0.0.1:8000', '/v1/transactions/', 'POST', 'http://127.0.0.1:8000/v1/transactions/', 200, NULL, '\"{\\\"amount_tendered\\\":5000,\\\"branch_id\\\":1,\\\"transaction_products\\\":[{\\\"branch_product_id\\\":7,\\\"price\\\":\\\"1970.00\\\",\\\"quantity\\\":\\\"1\\\"},{\\\"branch_product_id\\\":1,\\\"price\\\":\\\"2090.00\\\",\\\"quantity\\\":\\\"1\\\"}]}\"'),
(104, '2022-02-01 14:27:13.366731', '127.0.0.1:8000', '/v1/transactions/', 'POST', 'http://127.0.0.1:8000/v1/transactions/', 200, NULL, '\"{\\\"amount_tendered\\\":5000,\\\"branch_id\\\":1,\\\"transaction_products\\\":[{\\\"branch_product_id\\\":7,\\\"price\\\":\\\"1970.00\\\",\\\"quantity\\\":\\\"1\\\"},{\\\"branch_product_id\\\":1,\\\"price\\\":\\\"2090.00\\\",\\\"quantity\\\":\\\"1\\\"}]}\"'),
(105, '2022-02-01 14:28:09.094881', '127.0.0.1:8000', '/v1/transactions/', 'POST', 'http://127.0.0.1:8000/v1/transactions/', 200, NULL, '\"{\\\"amount_tendered\\\":2100,\\\"branch_id\\\":1,\\\"transaction_products\\\":[{\\\"branch_product_id\\\":1,\\\"price\\\":\\\"2090.00\\\",\\\"quantity\\\":\\\"1\\\"}]}\"'),
(106, '2022-02-01 14:29:02.060201', '127.0.0.1:8000', '/v1/transactions/', 'POST', 'http://127.0.0.1:8000/v1/transactions/', 200, NULL, '\"{\\\"amount_tendered\\\":2100,\\\"branch_id\\\":1,\\\"transaction_products\\\":[{\\\"branch_product_id\\\":1,\\\"price\\\":\\\"2090.00\\\",\\\"quantity\\\":\\\"1\\\"}]}\"'),
(107, '2022-02-01 14:29:41.462850', '127.0.0.1:8000', '/v1/transactions/', 'POST', 'http://127.0.0.1:8000/v1/transactions/', 200, NULL, '\"{\\\"amount_tendered\\\":2100,\\\"branch_id\\\":1,\\\"transaction_products\\\":[{\\\"branch_product_id\\\":1,\\\"price\\\":\\\"2090.00\\\",\\\"quantity\\\":\\\"1\\\"}]}\"'),
(108, '2022-02-01 14:30:43.228540', '127.0.0.1:8000', '/v1/transactions/', 'POST', 'http://127.0.0.1:8000/v1/transactions/', 200, NULL, '\"{\\\"amount_tendered\\\":6100,\\\"branch_id\\\":1,\\\"transaction_products\\\":[{\\\"branch_product_id\\\":7,\\\"price\\\":\\\"1970.00\\\",\\\"quantity\\\":\\\"2\\\"},{\\\"branch_product_id\\\":1,\\\"price\\\":\\\"2090.00\\\",\\\"quantity\\\":\\\"1\\\"}]}\"'),
(109, '2022-02-11 17:06:58.792050', '127.0.0.1:8000', '/v1/preorders/', 'POST', 'http://127.0.0.1:8000/v1/preorders/', 200, NULL, '\"{\\\"branch_id\\\":1,\\\"delivery_type\\\":\\\"delivery\\\",\\\"supplier\\\":{\\\"id\\\":4,\\\"name\\\":\\\"Ms. Jane\\\",\\\"description\\\":\\\"supplier description here\\\",\\\"address\\\":\\\"Cebu\\\",\\\"landline\\\":\\\"123 4567\\\",\\\"phone\\\":\\\"0905 123 456\\\"},\\\"preorder_products\\\":[{\\\"branch_product_id\\\":1,\\\"quantity\\\":10},{\\\"branch_product_id\\\":2,\\\"quantity\\\":10},{\\\"branch_product_id\\\":3,\\\"quantity\\\":10},{\\\"branch_product_id\\\":7,\\\"quantity\\\":10},{\\\"branch_product_id\\\":8,\\\"quantity\\\":10},{\\\"branch_product_id\\\":9,\\\"quantity\\\":10},{\\\"branch_product_id\\\":13,\\\"quantity\\\":10},{\\\"branch_product_id\\\":14,\\\"quantity\\\":10},{\\\"branch_product_id\\\":15,\\\"quantity\\\":10},{\\\"branch_product_id\\\":19,\\\"quantity\\\":10},{\\\"branch_product_id\\\":20,\\\"quantity\\\":10},{\\\"branch_product_id\\\":21,\\\"quantity\\\":10},{\\\"branch_product_id\\\":25,\\\"quantity\\\":10},{\\\"branch_product_id\\\":26,\\\"quantity\\\":10},{\\\"branch_product_id\\\":27,\\\"quantity\\\":10},{\\\"branch_product_id\\\":31,\\\"quantity\\\":10},{\\\"branch_product_id\\\":32,\\\"quantity\\\":10},{\\\"branch_product_id\\\":33,\\\"quantity\\\":10}]}\"'),
(110, '2022-02-11 17:07:03.385576', '127.0.0.1:8000', '/v1/preorders/14/', 'PATCH', 'http://127.0.0.1:8000/v1/preorders/14/', 200, NULL, '\"{\\\"status\\\":\\\"approved\\\"}\"'),
(111, '2022-02-11 17:07:13.815772', '127.0.0.1:8000', '/v1/preorder-transactions/', 'POST', 'http://127.0.0.1:8000/v1/preorder-transactions/', 204, NULL, '\"{\\\"preorder_id\\\":14,\\\"preorder_transaction_products\\\":[{\\\"preorder_product_id\\\":41,\\\"quantity\\\":10},{\\\"preorder_product_id\\\":42,\\\"quantity\\\":10},{\\\"preorder_product_id\\\":43,\\\"quantity\\\":10},{\\\"preorder_product_id\\\":44,\\\"quantity\\\":10},{\\\"preorder_product_id\\\":45,\\\"quantity\\\":10},{\\\"preorder_product_id\\\":46,\\\"quantity\\\":10},{\\\"preorder_product_id\\\":47,\\\"quantity\\\":10},{\\\"preorder_product_id\\\":48,\\\"quantity\\\":10},{\\\"preorder_product_id\\\":49,\\\"quantity\\\":10},{\\\"preorder_product_id\\\":50,\\\"quantity\\\":10},{\\\"preorder_product_id\\\":51,\\\"quantity\\\":10},{\\\"preorder_product_id\\\":52,\\\"quantity\\\":10},{\\\"preorder_product_id\\\":53,\\\"quantity\\\":10},{\\\"preorder_product_id\\\":54,\\\"quantity\\\":10},{\\\"preorder_product_id\\\":55,\\\"quantity\\\":10},{\\\"preorder_product_id\\\":56,\\\"quantity\\\":10},{\\\"preorder_product_id\\\":57,\\\"quantity\\\":10},{\\\"preorder_product_id\\\":58,\\\"quantity\\\":10}]}\"'),
(112, '2022-02-11 17:07:16.879026', '127.0.0.1:8000', '/v1/preorders/14/', 'PATCH', 'http://127.0.0.1:8000/v1/preorders/14/', 200, NULL, '\"{\\\"status\\\":\\\"delivered\\\"}\"'),
(113, '2022-02-11 17:08:33.408009', '127.0.0.1:8000', '/v1/products/', 'POST', 'http://127.0.0.1:8000/v1/products/', 200, NULL, '\"{\\\"name\\\":\\\"Product 1\\\",\\\"unit_cost\\\":\\\"100\\\",\\\"vat_type\\\":\\\"vat-e\\\",\\\"product_prices\\\":[{\\\"unit_type_id\\\":3,\\\"price_market\\\":\\\"1\\\",\\\"price_delivery\\\":\\\"1\\\",\\\"price_pickup\\\":\\\"1\\\",\\\"price_special\\\":\\\"1\\\",\\\"reorder_point\\\":\\\"1\\\"},{\\\"unit_type_id\\\":15,\\\"price_market\\\":\\\"1\\\",\\\"price_delivery\\\":\\\"1\\\",\\\"price_pickup\\\":\\\"1\\\",\\\"price_special\\\":\\\"1\\\",\\\"reorder_point\\\":\\\"0\\\"}]}\"'),
(114, '2022-02-11 17:09:02.207596', '127.0.0.1:8000', '/v1/products/', 'POST', 'http://127.0.0.1:8000/v1/products/', 200, NULL, '\"{\\\"name\\\":\\\"Product 2\\\",\\\"unit_cost\\\":\\\"1\\\",\\\"vat_type\\\":\\\"vat-e\\\",\\\"product_prices\\\":[{\\\"unit_type_id\\\":1,\\\"price_market\\\":\\\"1\\\",\\\"price_delivery\\\":\\\"1\\\",\\\"price_pickup\\\":\\\"1\\\",\\\"price_special\\\":\\\"1\\\",\\\"reorder_point\\\":\\\"1\\\"},{\\\"unit_type_id\\\":3,\\\"price_market\\\":\\\"1\\\",\\\"price_delivery\\\":\\\"1\\\",\\\"price_pickup\\\":\\\"1\\\",\\\"price_special\\\":\\\"1\\\",\\\"reorder_point\\\":\\\"1\\\"},{\\\"unit_type_id\\\":15,\\\"price_market\\\":\\\"1\\\",\\\"price_delivery\\\":\\\"1\\\",\\\"price_pickup\\\":\\\"1\\\",\\\"price_special\\\":\\\"1\\\",\\\"reorder_point\\\":\\\"1\\\"}]}\"'),
(115, '2022-02-11 17:09:42.727743', '127.0.0.1:8000', '/v1/preorders/', 'POST', 'http://127.0.0.1:8000/v1/preorders/', 200, NULL, '\"{\\\"branch_id\\\":1,\\\"delivery_type\\\":\\\"delivery\\\",\\\"supplier\\\":{\\\"id\\\":1,\\\"name\\\":\\\"Mr. Jonathan\\\",\\\"description\\\":\\\"Usually arrives 10mins before delivery time.\\\",\\\"address\\\":\\\"Cebu City\\\",\\\"landline\\\":\\\"123123\\\",\\\"phone\\\":\\\"0905 123 4567\\\"},\\\"preorder_products\\\":[{\\\"branch_product_id\\\":37,\\\"quantity\\\":10},{\\\"branch_product_id\\\":38,\\\"quantity\\\":10},{\\\"branch_product_id\\\":41,\\\"quantity\\\":10},{\\\"branch_product_id\\\":42,\\\"quantity\\\":10},{\\\"branch_product_id\\\":43,\\\"quantity\\\":10}]}\"'),
(116, '2022-02-11 17:09:45.123824', '127.0.0.1:8000', '/v1/preorders/15/', 'PATCH', 'http://127.0.0.1:8000/v1/preorders/15/', 200, NULL, '\"{\\\"status\\\":\\\"approved\\\"}\"'),
(117, '2022-02-11 17:09:50.062941', '127.0.0.1:8000', '/v1/preorder-transactions/', 'POST', 'http://127.0.0.1:8000/v1/preorder-transactions/', 204, NULL, '\"{\\\"preorder_id\\\":15,\\\"preorder_transaction_products\\\":[{\\\"preorder_product_id\\\":59,\\\"quantity\\\":10},{\\\"preorder_product_id\\\":60,\\\"quantity\\\":10},{\\\"preorder_product_id\\\":61,\\\"quantity\\\":10},{\\\"preorder_product_id\\\":62,\\\"quantity\\\":10},{\\\"preorder_product_id\\\":63,\\\"quantity\\\":10}]}\"'),
(118, '2022-02-11 17:09:51.363221', '127.0.0.1:8000', '/v1/preorders/15/', 'PATCH', 'http://127.0.0.1:8000/v1/preorders/15/', 200, NULL, '\"{\\\"status\\\":\\\"delivered\\\"}\"'),
(119, '2022-02-11 17:10:37.980420', '127.0.0.1:8000', '/v1/deliveries/', 'POST', 'http://127.0.0.1:8000/v1/deliveries/', 200, NULL, '\"{\\\"branch_id\\\":1,\\\"delivery_type\\\":\\\"delivery\\\",\\\"datetime_delivery\\\":\\\"2022-02-12 00:00:00\\\",\\\"customer\\\":{\\\"id\\\":2,\\\"name\\\":\\\"Mr. Andrew\\\",\\\"description\\\":\\\"Call customer first before delivery.\\\",\\\"address\\\":\\\"0314 Santa Ana\\\",\\\"landline\\\":\\\"1234567\\\",\\\"phone\\\":\\\"+639055625909\\\"},\\\"delivery_products\\\":[{\\\"branch_product_id\\\":1,\\\"quantity\\\":1,\\\"price\\\":\\\"2090.00\\\"},{\\\"branch_product_id\\\":2,\\\"quantity\\\":1,\\\"price\\\":\\\"90.00\\\"},{\\\"branch_product_id\\\":3,\\\"quantity\\\":1,\\\"price\\\":\\\"90.00\\\"},{\\\"branch_product_id\\\":7,\\\"quantity\\\":1,\\\"price\\\":\\\"1970.00\\\"},{\\\"branch_product_id\\\":8,\\\"quantity\\\":1,\\\"price\\\":\\\"165.00\\\"},{\\\"branch_product_id\\\":9,\\\"quantity\\\":1,\\\"price\\\":\\\"165.00\\\"},{\\\"branch_product_id\\\":13,\\\"quantity\\\":1,\\\"price\\\":\\\"1105.00\\\"},{\\\"branch_product_id\\\":14,\\\"quantity\\\":1,\\\"price\\\":\\\"25.00\\\"},{\\\"branch_product_id\\\":15,\\\"quantity\\\":1,\\\"price\\\":\\\"25.00\\\"},{\\\"branch_product_id\\\":19,\\\"quantity\\\":1,\\\"price\\\":\\\"1786.00\\\"},{\\\"branch_product_id\\\":20,\\\"quantity\\\":1,\\\"price\\\":\\\"52.00\\\"},{\\\"branch_product_id\\\":21,\\\"quantity\\\":1,\\\"price\\\":\\\"52.00\\\"},{\\\"branch_product_id\\\":25,\\\"quantity\\\":1,\\\"price\\\":\\\"1148.00\\\"},{\\\"branch_product_id\\\":26,\\\"quantity\\\":1,\\\"price\\\":\\\"50.00\\\"},{\\\"branch_product_id\\\":27,\\\"quantity\\\":1,\\\"price\\\":\\\"50.00\\\"},{\\\"branch_product_id\\\":31,\\\"quantity\\\":1,\\\"price\\\":\\\"1148.00\\\"},{\\\"branch_product_id\\\":32,\\\"quantity\\\":1,\\\"price\\\":\\\"50.00\\\"},{\\\"branch_product_id\\\":33,\\\"quantity\\\":1,\\\"price\\\":\\\"50.00\\\"},{\\\"branch_product_id\\\":37,\\\"quantity\\\":1,\\\"price\\\":\\\"1.00\\\"},{\\\"branch_product_id\\\":38,\\\"quantity\\\":1,\\\"price\\\":\\\"1.00\\\"},{\\\"branch_product_id\\\":41,\\\"quantity\\\":1,\\\"price\\\":\\\"1.00\\\"},{\\\"branch_product_id\\\":42,\\\"quantity\\\":1,\\\"price\\\":\\\"1.00\\\"},{\\\"branch_product_id\\\":43,\\\"quantity\\\":1,\\\"price\\\":\\\"1.00\\\"}]}\"'),
(120, '2022-02-11 17:41:56.493837', '127.0.0.1:8000', '/v1/deliveries/9/', 'PATCH', 'http://127.0.0.1:8000/v1/deliveries/9/', 200, NULL, '\"{\\\"status\\\":\\\"delivered\\\",\\\"payment_status\\\":\\\"paid\\\",\\\"prepared_by\\\":\\\"test\\\",\\\"checked_by\\\":\\\"test\\\",\\\"pulled_out_by\\\":\\\"test\\\",\\\"delivered_by\\\":\\\"test\\\"}\"'),
(121, '2022-02-12 09:53:01.620224', '127.0.0.1:8000', '/v1/products/', 'POST', 'http://127.0.0.1:8000/v1/products/', 200, NULL, '\"{\\\"name\\\":\\\"Product 3\\\",\\\"unit_cost\\\":\\\"1\\\",\\\"vat_type\\\":\\\"vat-e\\\",\\\"product_prices\\\":[{\\\"unit_type_id\\\":3,\\\"price_market\\\":\\\"1\\\",\\\"price_delivery\\\":\\\"1\\\",\\\"price_pickup\\\":\\\"1\\\",\\\"price_special\\\":\\\"1\\\",\\\"reorder_point\\\":\\\"5\\\"},{\\\"unit_type_id\\\":5,\\\"price_market\\\":\\\"1\\\",\\\"price_delivery\\\":\\\"1\\\",\\\"price_pickup\\\":\\\"1\\\",\\\"price_special\\\":\\\"1\\\",\\\"reorder_point\\\":\\\"0\\\"}]}\"'),
(122, '2022-02-12 09:53:22.220574', '127.0.0.1:8000', '/v1/products/', 'POST', 'http://127.0.0.1:8000/v1/products/', 200, NULL, '\"{\\\"name\\\":\\\"Product 4\\\",\\\"unit_cost\\\":\\\"1\\\",\\\"vat_type\\\":\\\"vat-e\\\",\\\"product_prices\\\":[{\\\"unit_type_id\\\":3,\\\"price_market\\\":\\\"1\\\",\\\"price_delivery\\\":\\\"1\\\",\\\"price_pickup\\\":\\\"1\\\",\\\"price_special\\\":\\\"1\\\",\\\"reorder_point\\\":0},{\\\"unit_type_id\\\":4,\\\"price_market\\\":\\\"1\\\",\\\"price_delivery\\\":\\\"1\\\",\\\"price_pickup\\\":\\\"1\\\",\\\"price_special\\\":\\\"1\\\",\\\"reorder_point\\\":\\\"1\\\"}]}\"'),
(123, '2022-02-13 06:05:41.178767', '127.0.0.1:8000', '/v1/deliveries/', 'POST', 'http://127.0.0.1:8000/v1/deliveries/', 200, NULL, '\"{\\\"branch_id\\\":1,\\\"delivery_type\\\":\\\"delivery\\\",\\\"datetime_delivery\\\":\\\"2022-02-13 14:05:29\\\",\\\"customer\\\":{\\\"id\\\":2,\\\"name\\\":\\\"Mr. Andrew\\\",\\\"description\\\":\\\"Call customer first before delivery.\\\",\\\"address\\\":\\\"0314 Santa Ana\\\",\\\"landline\\\":\\\"1234567\\\",\\\"phone\\\":\\\"+639055625909\\\"},\\\"delivery_products\\\":[{\\\"branch_product_id\\\":1,\\\"quantity\\\":1,\\\"price\\\":\\\"2090.00\\\"}]}\"'),
(124, '2022-02-13 06:05:55.135609', '127.0.0.1:8000', '/v1/deliveries/11/', 'PATCH', 'http://127.0.0.1:8000/v1/deliveries/11/', 200, NULL, '\"{\\\"status\\\":\\\"delivered\\\",\\\"payment_status\\\":\\\"paid\\\",\\\"prepared_by\\\":\\\"\\\",\\\"checked_by\\\":\\\"\\\",\\\"pulled_out_by\\\":\\\"\\\",\\\"delivered_by\\\":\\\"\\\"}\"'),
(125, '2022-02-13 06:27:48.808842', '127.0.0.1:8000', '/v1/deliveries/', 'POST', 'http://127.0.0.1:8000/v1/deliveries/', 200, NULL, '\"{\\\"branch_id\\\":1,\\\"delivery_type\\\":\\\"delivery\\\",\\\"datetime_delivery\\\":\\\"2022-02-13 14:27:39\\\",\\\"customer\\\":{\\\"id\\\":2,\\\"name\\\":\\\"Mr. Andrew\\\",\\\"description\\\":\\\"Call customer first before delivery.\\\",\\\"address\\\":\\\"0314 Santa Ana\\\",\\\"landline\\\":\\\"1234567\\\",\\\"phone\\\":\\\"+639055625909\\\"},\\\"delivery_products\\\":[{\\\"branch_product_id\\\":1,\\\"quantity\\\":1,\\\"price\\\":\\\"2090.00\\\"}]}\"'),
(126, '2022-02-13 06:28:20.768954', '127.0.0.1:8000', '/v1/deliveries/12/', 'PATCH', 'http://127.0.0.1:8000/v1/deliveries/12/', 200, NULL, '\"{\\\"status\\\":\\\"delivered\\\",\\\"payment_status\\\":\\\"paid\\\",\\\"prepared_by\\\":\\\"\\\",\\\"checked_by\\\":\\\"\\\",\\\"pulled_out_by\\\":\\\"\\\",\\\"delivered_by\\\":\\\"\\\"}\"');



/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;