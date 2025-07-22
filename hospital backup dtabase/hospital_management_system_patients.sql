-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: hospital_management_system
-- ------------------------------------------------------
-- Server version	8.0.42

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
-- Table structure for table `patients`
--

DROP TABLE IF EXISTS `patients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patients` (
  `patient_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `date_of_birth` date NOT NULL,
  `gender` enum('Male','Female','Other') NOT NULL,
  `blood_type` enum('A+','A-','B+','B-','AB+','AB-','O+','O-') DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `address` text,
  `photo_path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`patient_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `patients_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patients`
--

LOCK TABLES `patients` WRITE;
/*!40000 ALTER TABLE `patients` DISABLE KEYS */;
INSERT INTO `patients` VALUES (3,8,'rizwan','ali','2000-12-24','Female','A-','0300','kgjjhgdsjj','C:/Users/Mubashir abbas/Desktop/Ap/3a5a1883-6a09-41da-9e79-12ad48ab78cf.png'),(5,12,'mubashir','abbass','2006-02-10','Male','A-','0300000','jgk','C:/Users/Mubashir abbas/Desktop/Ap/3a5a1883-6a09-41da-9e79-12ad48ab78cf.png'),(6,16,'patient1','hidhi','2006-10-10','Male','B+','0300','kkk',NULL),(7,17,'gj','kgh','2020-10-10','Female','A+','045','ujgy','E:/dps/462451460_1533119104240974_367555800900588276_n.jpg'),(8,18,'muzamil','riaz','2020-10-10','Male','A-','0300','grd','E:/dps/482301114_122095589516801165_933161461842315189_n.jpg'),(9,32,'Usman','Ahmed','1995-03-10','Male','A+','+923101234577','House 12, Street 5, Lahore',NULL),(10,33,'Sara','Iftikhar','1988-07-22','Female','B+','+923111234578','Flat 3, Gulberg, Karachi',NULL),(11,34,'Ali','Hassan','2000-11-05','Male','O+','+923121234579','Sector G-9, Islamabad',NULL),(12,35,'Noor','Fatima','1993-01-15','Female','AB+','+923131234580','Model Town, Rawalpindi',NULL),(13,36,'Zahid','Khan','1985-09-30','Male','A-','+923141234581','Peshawar Road, Peshawar',NULL),(14,37,'Hina','Aslam','1997-04-18','Female','B-','+923151234582','Saddar, Quetta',NULL),(15,38,'Farooq','Malik','1990-12-12','Male','O-','+923161234583','DHA Phase 5, Lahore',NULL),(16,39,'Amina','Qadir','1987-06-25','Female','AB-','+923171234584','Clifton, Karachi',NULL),(17,40,'Saad','Rehman','1998-02-08','Male','A+','+923181234585','F-11, Islamabad',NULL),(18,41,'Maryam','Bibi','1994-08-14','Female','B+','+923191234586','Cantt, Multan',NULL);
/*!40000 ALTER TABLE `patients` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-08 10:08:39
