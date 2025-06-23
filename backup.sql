-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: sardorbot
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `deals`
--

DROP TABLE IF EXISTS `deals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `deals` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `amount` int DEFAULT NULL,
  `check_photo` text,
  `card_number` text,
  `status` enum('pending','completed','cancelled') DEFAULT 'pending',
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deals`
--

LOCK TABLES `deals` WRITE;
/*!40000 ALTER TABLE `deals` DISABLE KEYS */;
INSERT INTO `deals` VALUES (1,123456789,500,'photo_url','1234-5678-9012-3456','cancelled');
/*!40000 ALTER TABLE `deals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `referals`
--

DROP TABLE IF EXISTS `referals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `referals` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `referal_id` bigint NOT NULL,
  `xp` int DEFAULT '0',
  `ton` decimal(18,8) DEFAULT '0.00000000',
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`referal_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `referals`
--

LOCK TABLES `referals` WRITE;
/*!40000 ALTER TABLE `referals` DISABLE KEYS */;
INSERT INTO `referals` VALUES (1,6413896128,6411800470,10,0.00800000),(2,6413896128,6667196814,10,0.00800000),(3,6411800470,6667196814,10,0.00800000),(4,6411800470,7730825456,10,0.00800000),(5,6413896128,7579944629,10,0.00800000),(6,5451556891,7658974274,10,0.00800000),(7,7896800762,6413896128,10,0.00800000),(8,5451556891,7703345908,10,0.00800000),(9,7703345908,7836184631,10,0.00800000);
/*!40000 ALTER TABLE `referals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trades`
--

DROP TABLE IF EXISTS `trades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trades` (
  `id` varchar(32) NOT NULL,
  `user_id` bigint NOT NULL,
  `coin` varchar(50) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `status` enum('pending','approved','closed') DEFAULT 'pending',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `xp` int DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trades`
--

LOCK TABLES `trades` WRITE;
/*!40000 ALTER TABLE `trades` DISABLE KEYS */;
INSERT INTO `trades` VALUES ('1',5451556891,'TONCOIN',123.00,'approved','2025-02-28 16:29:58',0),('12345678',123456789,'TONCOIN',100.00,'approved','2025-02-28 18:27:29',1000),('cc369f3d',6413896128,'NOTCOIN',100.00,'approved','2025-02-28 18:51:09',1000);
/*!40000 ALTER TABLE `trades` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transactions`
--

DROP TABLE IF EXISTS `transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transactions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` bigint DEFAULT NULL,
  `coin` varchar(50) DEFAULT NULL,
  `amount` decimal(10,2) DEFAULT NULL,
  `xp` int DEFAULT NULL,
  `telegram_id` bigint DEFAULT NULL,
  `date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `confirmed` tinyint(1) DEFAULT '0',
  `username` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transactions`
--

LOCK TABLES `transactions` WRITE;
/*!40000 ALTER TABLE `transactions` DISABLE KEYS */;
INSERT INTO `transactions` VALUES (1,NULL,NULL,NULL,50,7896800762,'2025-02-15 10:38:13',1,NULL),(2,NULL,NULL,NULL,50,7896800762,'2025-02-15 10:40:09',1,NULL),(3,NULL,NULL,NULL,50,7896800762,'2025-02-15 10:40:11',1,NULL),(4,NULL,NULL,NULL,50,7896800762,'2025-02-15 10:40:56',1,NULL),(5,NULL,NULL,NULL,50,7896800762,'2025-02-15 10:43:58',1,NULL),(6,NULL,NULL,NULL,50,7896800762,'2025-02-15 10:45:05',1,NULL),(7,NULL,NULL,NULL,50,7896800762,'2025-02-15 10:45:34',1,NULL),(8,NULL,NULL,NULL,50,7896800762,'2025-02-15 10:52:18',1,NULL),(9,NULL,NULL,NULL,50,7896800762,'2025-02-15 10:56:10',1,NULL),(10,NULL,NULL,NULL,0,7658974274,'2025-02-16 10:16:26',1,'Удалённый🐍 аккаунт'),(11,NULL,NULL,NULL,0,7896800762,'2025-02-16 10:20:58',1,'millioner.not'),(12,NULL,NULL,NULL,0,5451556891,'2025-02-16 10:28:04',0,'sardor'),(13,NULL,NULL,NULL,0,7896800762,'2025-02-16 10:28:17',1,'millioner.not'),(14,NULL,'MEMEFI',1000.00,20000,7896800762,'2025-02-16 10:45:12',1,'millioner.not'),(15,NULL,'NOTCOIN',1000.00,50000,7896800762,'2025-02-16 10:49:40',1,'millioner.not'),(16,NULL,'TONCOIN',1.00,10,7896800762,'2025-02-16 10:52:06',1,'millioner.not'),(17,NULL,'NOTCOIN',12.00,600,5451556891,'2025-02-16 10:53:34',0,'sardor'),(18,NULL,'NOTCOIN',1234.00,61700,7896800762,'2025-02-16 10:56:25',1,'millioner.not'),(19,NULL,'NOTCOIN',12.00,600,6413896128,'2025-02-17 13:08:33',1,'memcoinstoreuz'),(20,NULL,'MEMEFI',123.00,2460,6413896128,'2025-02-17 13:09:41',1,'memcoinstoreuz'),(21,NULL,'NOTCOIN',12.00,600,7738023453,'2025-02-17 13:11:43',1,'Kotman 🐾🦒'),(22,NULL,'NOTCOIN',12.00,600,6413896128,'2025-02-18 12:04:07',1,'memcoinstoreuz'),(23,NULL,'NOTCOIN',123.00,6150,6413896128,'2025-02-18 13:12:24',1,'memcoinstoreuz'),(24,NULL,'NOTCOIN',123.00,6150,6411800470,'2025-02-18 17:41:12',1,'Noma\'lum foydalanuvchi'),(25,NULL,'NOTCOIN',12.00,600,7579944629,'2025-02-18 17:52:53',1,'Noma\'lum foydalanuvchi'),(26,NULL,'MEMEFI',123.00,2460,5451556891,'2025-02-20 12:14:51',1,'Noma\'lum foydalanuvchi'),(27,NULL,'MEMEFI',123.00,2460,5451556891,'2025-02-20 16:37:53',1,'Noma\'lum foydalanuvchi'),(28,NULL,'USDT',11.00,110,7703345908,'2025-02-20 16:41:04',1,'Noma\'lum foydalanuvchi'),(29,NULL,'NOTCOIN',123.00,6150,6667196814,'2025-02-21 17:05:55',1,'Noma\'lum foydalanuvchi'),(30,NULL,'NOTCOIN',123.00,6150,6667196814,'2025-02-21 17:38:10',1,'Noma\'lum foydalanuvchi'),(31,NULL,'NOTCOIN',123.00,6150,6667196814,'2025-02-21 17:41:20',1,'Noma\'lum foydalanuvchi'),(32,NULL,'NOTCOIN',123.00,6150,6667196814,'2025-02-21 17:44:48',1,'Noma\'lum foydalanuvchi'),(33,NULL,'NOTCOIN',123123.00,6156150,5451556891,'2025-02-21 17:45:47',1,'Noma\'lum foydalanuvchi'),(34,NULL,'MEMEFI',2.00,40,6667196814,'2025-02-21 18:32:56',1,'Noma\'lum foydalanuvchi'),(35,NULL,'USDT',1.00,10,7896800762,'2025-02-21 18:36:26',1,'Noma\'lum foydalanuvchi'),(36,NULL,'NOTCOIN',123.00,6150,7896800762,'2025-02-21 18:51:46',1,'Noma\'lum foydalanuvchi'),(37,NULL,'NOTCOIN',32323.00,1616150,6667196814,'2025-02-21 18:52:35',1,'Noma\'lum foydalanuvchi'),(38,NULL,'NOTCOIN',12.00,600,6667196814,'2025-02-21 18:56:00',1,'Noma\'lum foydalanuvchi'),(39,NULL,'NOTCOIN',2.00,100,6667196814,'2025-02-21 18:59:47',1,'Noma\'lum foydalanuvchi'),(40,NULL,'NOTCOIN',123.00,6150,7896800762,'2025-02-22 15:10:48',1,'Noma\'lum foydalanuvchi'),(41,NULL,'NOTCOIN',123.00,6150,5451556891,'2025-02-26 09:47:56',1,'Noma\'lum foydalanuvchi'),(42,NULL,'NOTCOIN',123.00,6150,5451556891,'2025-02-27 13:23:52',1,'Noma\'lum foydalanuvchi'),(43,NULL,'NOTCOIN',123.00,6150,5451556891,'2025-02-27 13:37:50',1,'Noma\'lum foydalanuvchi'),(44,NULL,'NOTCOIN',11.00,550,5451556891,'2025-02-27 13:53:17',1,'Noma\'lum foydalanuvchi'),(45,NULL,'NOTCOIN',123.00,6150,6413896128,'2025-02-28 16:11:26',1,'Noma\'lum foydalanuvchi'),(46,NULL,'MEMEFI',12.00,240,6413896128,'2025-02-28 16:18:02',1,'Noma\'lum foydalanuvchi'),(47,NULL,'NOTCOIN',1234.00,61700,6413896128,'2025-02-28 16:30:19',1,'Noma\'lum foydalanuvchi'),(48,NULL,'NOTCOIN',123.00,6150,6413896128,'2025-02-28 18:19:39',1,'Noma\'lum foydalanuvchi'),(49,NULL,'TONCOIN',12.00,120,6413896128,'2025-02-28 18:20:34',1,'Noma\'lum foydalanuvchi'),(50,NULL,'MEMEFI',11.00,110,6413896128,'2025-02-28 18:33:14',1,'Noma\'lum foydalanuvchi'),(51,NULL,'NOTCOIN',111.00,1110,6413896128,'2025-02-28 18:38:58',1,'Noma\'lum foydalanuvchi'),(52,NULL,'TONCOIN',100.00,1000,6413896128,'2025-02-28 18:46:25',1,'Noma\'lum foydalanuvchi'),(53,NULL,'NOTCOIN',1000.00,10000,7896800762,'2025-04-05 16:11:49',1,'Noma\'lum foydalanuvchi'),(54,NULL,'MEMEFI',123.00,1230,5451556891,'2025-04-05 17:27:01',1,'Noma\'lum foydalanuvchi');
/*!40000 ALTER TABLE `transactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` bigint NOT NULL,
  `username` varchar(255) DEFAULT NULL,
  `xp` int DEFAULT '0',
  `ton` decimal(18,8) DEFAULT '0.00000000',
  `bonus_token` decimal(10,2) DEFAULT '0.00',
  `bonus_codes` text,
  `wallet_address` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (5451556891,'sardortete',20,-1.98400000,3.00,NULL,'UQB1NTMNh25eWKpSvhGq2LStBQ-PyiyJFMNr_nP5a2F8h32R'),(6411800470,'notbillioners',20,0.01600000,0.00,NULL,NULL),(6413896128,'memcoinstoreuz',30,-5.97600000,2.00,NULL,'UQBqkXTjkTX0y9wClBDjsk6Up9fEeYkCtl3sfJxHvVNiK3Le'),(6667196814,'redbullstars',0,0.00000000,1.00,NULL,'UQBjC1fmzjYlF5n8veJCIsFIaDR2u2Fm0P_SoAUf_-fkrpPn'),(7579944629,'soqqa_community',0,0.00000000,0.00,NULL,NULL),(7658974274,'communitysoqqa',0,0.00000000,0.00,NULL,NULL),(7703345908,'nimet',10,0.00800000,0.00,NULL,NULL),(7730825456,'Paws2 🐾🦒',0,0.00000000,0.00,NULL,NULL),(7836184631,'birbaloxup',0,0.00000000,0.00,NULL,NULL),(7896800762,'notmillioners',10,0.00800000,2.00,NULL,'UQB4X3doJMkflGPNAjFVrp3dM_AKc3v--XhWpDOajaG5nDIx');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `withdrawal_requests`
--

DROP TABLE IF EXISTS `withdrawal_requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `withdrawal_requests` (
  `id` int NOT NULL AUTO_INCREMENT,
  `request_id` varchar(255) NOT NULL,
  `user_id` bigint NOT NULL,
  `amount` decimal(10,8) NOT NULL,
  `source` varchar(255) NOT NULL,
  `address` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `status` enum('pending','completed') DEFAULT 'pending',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `withdrawal_requests`
--

LOCK TABLES `withdrawal_requests` WRITE;
/*!40000 ALTER TABLE `withdrawal_requests` DISABLE KEYS */;
INSERT INTO `withdrawal_requests` VALUES (1,'710af47c',5451556891,3.00000000,'BONUS TOKEN','UQB1NTMNh25eWKpSvhGq2LStBQ-PyiyJFMNr_nP5a2F8h32R','2025-02-27 09:20:49','completed'),(2,'eb463dd6',5451556891,3.00000000,'BONUS TOKEN','UQB1NTMNh25eWKpSvhGq2LStBQ-PyiyJFMNr_nP5a2F8h32R','2025-02-27 09:26:06','completed'),(3,'48243bb9',7896800762,2.00000000,'BONUS TOKEN','UQB4X3doJMkflGPNAjFVrp3dM_AKc3v--XhWpDOajaG5nDIx','2025-02-27 09:28:31','completed'),(4,'895883c1',7896800762,2.00000000,'BONUS TOKEN','UQB4X3doJMkflGPNAjFVrp3dM_AKc3v--XhWpDOajaG5nDIx','2025-02-27 09:31:38','completed'),(5,'5d019972',7896800762,2.00000000,'BONUS TOKEN','UQB4X3doJMkflGPNAjFVrp3dM_AKc3v--XhWpDOajaG5nDIx','2025-02-27 09:34:08','completed'),(6,'e5e1d682',7896800762,2.00000000,'BONUS TOKEN','UQB4X3doJMkflGPNAjFVrp3dM_AKc3v--XhWpDOajaG5nDIx','2025-02-27 09:40:01','completed'),(7,'6e5b7b26',7896800762,2.00000000,'BONUS TOKEN','UQB4X3doJMkflGPNAjFVrp3dM_AKc3v--XhWpDOajaG5nDIx','2025-02-27 10:13:47','completed'),(8,'e734ef41',7896800762,2.00000000,'BONUS TOKEN','UQB4X3doJMkflGPNAjFVrp3dM_AKc3v--XhWpDOajaG5nDIx','2025-02-27 13:26:27','completed'),(9,'b493feba',7896800762,1.00000000,'BONUS TOKEN','UQB4X3doJMkflGPNAjFVrp3dM_AKc3v--XhWpDOajaG5nDIx','2025-02-27 13:42:16','completed'),(10,'68fd55ad',6413896128,2.00000000,'BONUS TOKEN','UQBqkXTjkTX0y9wClBDjsk6Up9fEeYkCtl3sfJxHvVNiK3Le','2025-02-27 13:44:55','completed'),(11,'1a86352e',6413896128,2.00000000,'BONUS TOKEN','UQBqkXTjkTX0y9wClBDjsk6Up9fEeYkCtl3sfJxHvVNiK3Le','2025-02-27 15:01:19','completed'),(12,'f142e428',6413896128,2.00000000,'BONUS TOKEN','UQBqkXTjkTX0y9wClBDjsk6Up9fEeYkCtl3sfJxHvVNiK3Le','2025-02-27 15:03:41','completed'),(13,'ff2aa28a',5451556891,2.00000000,'BONUS TOKEN','UQB1NTMNh25eWKpSvhGq2LStBQ-PyiyJFMNr_nP5a2F8h32R','2025-02-28 15:56:09','completed'),(14,'2909d6f0',6413896128,2.00000000,'BONUS TOKEN','UQBqkXTjkTX0y9wClBDjsk6Up9fEeYkCtl3sfJxHvVNiK3Le','2025-02-28 15:57:47','completed');
/*!40000 ALTER TABLE `withdrawal_requests` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-05 23:27:26
