-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: stockanalysis
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `gainers`
--

DROP TABLE IF EXISTS `gainers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gainers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `month` varchar(7) NOT NULL,
  `ticker` varchar(10) NOT NULL,
  `percentage_return` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `month` (`month`,`ticker`)
) ENGINE=InnoDB AUTO_INCREMENT=586 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gainers`
--

LOCK TABLES `gainers` WRITE;
/*!40000 ALTER TABLE `gainers` DISABLE KEYS */;
INSERT INTO `gainers` VALUES (131,'2023-11','TRENT',0.26),(132,'2023-11','BPCL',0.24),(133,'2023-11','HEROMOTOCO',0.20),(134,'2023-11','BAJAJ-AUTO',0.14),(135,'2023-11','EICHERMOT',0.14),(136,'2023-12','BEL',0.31),(137,'2023-12','ADANIPORTS',0.23),(138,'2023-12','NTPC',0.20),(139,'2023-12','ULTRACEMCO',0.20),(140,'2023-12','ADANIENT',0.19),(141,'2024-01','ONGC',0.22),(142,'2024-01','SHRIRAMFIN',0.19),(143,'2024-01','ADANIPORTS',0.16),(144,'2024-01','BHARTIARTL',0.12),(145,'2024-01','BPCL',0.12),(146,'2024-02','TRENT',0.28),(147,'2024-02','BPCL',0.21),(148,'2024-02','SBIN',0.18),(149,'2024-02','M&M',0.17),(150,'2024-02','SUNPHARMA',0.15),(151,'2024-03','MARUTI',0.13),(152,'2024-03','BAJAJ-AUTO',0.12),(153,'2024-03','BAJFINANCE',0.11),(154,'2024-03','HINDALCO',0.11),(155,'2024-03','TATASTEEL',0.11),(156,'2024-04','BEL',0.17),(157,'2024-04','HINDALCO',0.16),(158,'2024-04','EICHERMOT',0.14),(159,'2024-04','AXISBANK',0.11),(160,'2024-04','SBIN',0.10),(161,'2024-05','BEL',0.23),(162,'2024-05','M&M',0.21),(163,'2024-05','HEROMOTOCO',0.15),(164,'2024-05','BRITANNIA',0.08),(165,'2024-05','TRENT',0.08),(166,'2024-06','SHRIRAMFIN',0.26),(167,'2024-06','ULTRACEMCO',0.18),(168,'2024-06','WIPRO',0.18),(169,'2024-06','TRENT',0.18),(170,'2024-06','TECHM',0.15),(171,'2024-07','ONGC',0.21),(172,'2024-07','INFY',0.20),(173,'2024-07','TATAMOTORS',0.17),(174,'2024-07','HDFCLIFE',0.17),(175,'2024-07','SBILIFE',0.15),(176,'2024-08','TRENT',0.27),(177,'2024-08','BAJAJ-AUTO',0.14),(178,'2024-08','SHRIRAMFIN',0.10),(179,'2024-08','BAJAJFINSV',0.09),(180,'2024-08','CIPLA',0.08),(181,'2024-09','BAJAJ-AUTO',0.16),(182,'2024-09','M&M',0.13),(183,'2024-09','SHRIRAMFIN',0.13),(184,'2024-09','BAJAJFINSV',0.13),(185,'2024-09','NESTLEIND',0.10),(186,'2024-10','TECHM',0.05),(187,'2024-10','WIPRO',0.04),(188,'2024-10','SBIN',0.02),(189,'2024-10','HCLTECH',0.02),(190,'2024-10','ICICIBANK',0.00),(191,'2024-11','M&M',0.11),(192,'2024-11','POWERGRID',0.06),(193,'2024-11','LT',0.06),(194,'2024-11','INFY',0.06),(195,'2024-11','CIPLA',0.05);
/*!40000 ALTER TABLE `gainers` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-26 22:54:44