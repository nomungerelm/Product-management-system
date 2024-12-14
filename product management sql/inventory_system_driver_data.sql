-- MySQL dump 10.13  Distrib 8.0.40, for macos14 (x86_64)
--
-- Host: 127.0.0.1    Database: inventory_system
-- ------------------------------------------------------
-- Server version	8.3.0

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
-- Table structure for table `driver_data`
--

DROP TABLE IF EXISTS `driver_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `driver_data` (
  `driverId` int NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `gender` varchar(50) DEFAULT NULL,
  `contact` varchar(30) DEFAULT NULL,
  `work_shift` varchar(50) DEFAULT NULL,
  `salary` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`driverId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `driver_data`
--

LOCK TABLES `driver_data` WRITE;
/*!40000 ALTER TABLE `driver_data` DISABLE KEYS */;
INSERT INTO `driver_data` VALUES (1,'Nomungerel','nomun0808@gmail.com','Female','99890767','Morning','2000'),(2,'Josh King','josh6890@gmail.com','Male','89786757','Evening','3500'),(3,'Blake','blake7890@gmail.com','Female','87679087','Morning','1800'),(4,'Maria','maria3456@gmail.com','Female','78654321','Night','3000'),(5,'Muham','muham3456@gmail.com','Male','98789678','Night','2400'),(6,'Sarah','sarah7689@gmail.com','Female','89234534','Evening','2100'),(7,'Bob','bobby6756@gmail.com','Male','76543422','Night','2700'),(8,'Ted','teddy6751@gmail.com','Male','90807322','Evening','2350'),(9,'Ghana','ghana3456@gmail.com','Male','98070776','Evening','2560'),(10,'Noah','noah6705@gmail.com','Male','98987070','Morning','1800'),(11,'Kelly','kelly2324@gmail.com','Female','90989898','Morning','2700');
/*!40000 ALTER TABLE `driver_data` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-14 14:26:05
