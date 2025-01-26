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
-- Table structure for table `cumulativereturnanalysis`
--

DROP TABLE IF EXISTS `cumulativereturnanalysis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cumulativereturnanalysis` (
  `Ticker` text,
  `Cumulative` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cumulativereturnanalysis`
--

LOCK TABLES `cumulativereturnanalysis` WRITE;
/*!40000 ALTER TABLE `cumulativereturnanalysis` DISABLE KEYS */;
INSERT INTO `cumulativereturnanalysis` VALUES ('ADANIENT',-0.0667085558697244),('ADANIPORTS',0.3672720712051984),('APOLLOHOSP',0.3547895564520082),('ASIANPAINT',-0.2193504586576575),('AXISBANK',0.0973536333509437),('BAJAJ-AUTO',0.890111533056243),('BAJAJFINSV',0.0254956599724542),('BAJFINANCE',-0.1611087403986156),('BEL',1.0176005747126422),('BHARTIARTL',0.6959904895709486),('BPCL',0.6747715022263889),('BRITANNIA',0.0785015960582371),('CIPLA',0.2567636117686831),('COALINDIA',0.4184652278177427),('DRREDDY',0.1117875386784337),('EICHERMOT',0.4877961448946721),('GRASIM',0.3578198804497743),('HCLTECH',0.5325744732380722),('HDFCBANK',0.1575213023440891),('HDFCLIFE',0.0862599636966283),('HEROMOTOCO',0.5897665472874369),('HINDALCO',0.3586831961662664),('HINDUNILVR',-0.0095791648102399),('ICICIBANK',0.3591938742954388),('INDUSINDBK',-0.3045840880590785),('INFY',0.3265341701534177),('ITC',0.0793632745878367),('JSWSTEEL',0.268873742291464),('KOTAKBANK',0.0199183578935162),('LT',0.1725372163019616),('M&M',0.95976974112137),('MARUTI',0.0692671234862623),('NESTLEIND',0.0070714132071396),('NTPC',0.515132669983416),('ONGC',0.3304442036836388),('POWERGRID',0.688549235780507),('RELIANCE',0.0917279221451512),('SBILIFE',0.1490966768540373),('SBIN',0.3534289742101286),('SHRIRAMFIN',0.4828949764562076),('SUNPHARMA',0.5728240395987554),('TATACONSUM',0.0975383186251728),('TATAMOTORS',0.2748811346603281),('TATASTEEL',0.1154687499999986),('TCS',0.2079627758726194),('TECHM',0.4368113797072903),('TITAN',0.0351818537348482),('TRENT',2.23092613277646),('ULTRACEMCO',0.3697094486387549),('WIPRO',0.4099149093599699);
/*!40000 ALTER TABLE `cumulativereturnanalysis` ENABLE KEYS */;
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