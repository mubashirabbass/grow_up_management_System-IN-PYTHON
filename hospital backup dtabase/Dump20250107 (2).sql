CREATE DATABASE  IF NOT EXISTS `hms2` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `hms2`;
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: hms2
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
-- Table structure for table `appointment`
--

DROP TABLE IF EXISTS `appointment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appointment` (
  `AppointmentID` int NOT NULL AUTO_INCREMENT,
  `PatientID` int DEFAULT NULL,
  `StaffID` int DEFAULT NULL,
  `AppointmentDate` date NOT NULL,
  `Reason` varchar(255) DEFAULT NULL,
  `AppointmentTime` time NOT NULL,
  `Purpose` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`AppointmentID`),
  KEY `PatientID` (`PatientID`),
  KEY `StaffID` (`StaffID`),
  CONSTRAINT `appointment_ibfk_1` FOREIGN KEY (`PatientID`) REFERENCES `patient` (`PatientID`),
  CONSTRAINT `appointment_ibfk_2` FOREIGN KEY (`StaffID`) REFERENCES `staff` (`StaffID`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointment`
--

LOCK TABLES `appointment` WRITE;
/*!40000 ALTER TABLE `appointment` DISABLE KEYS */;
INSERT INTO `appointment` VALUES (1,1,1,'2025-01-15',NULL,'10:00:00','Routine Checkup'),(2,2,2,'2025-01-16',NULL,'11:00:00','Asthma Consultation'),(3,3,3,'2025-01-17',NULL,'12:00:00','Diabetes Treatment'),(4,4,4,'2025-01-18',NULL,'09:00:00','Hypertension Checkup'),(5,5,5,'2025-01-19',NULL,'14:00:00','Heart Disease Consultation'),(6,6,6,'2025-01-20',NULL,'13:00:00','General Health Checkup'),(7,7,7,'2025-01-21',NULL,'15:00:00','Chronic Back Pain Consultation'),(8,8,8,'2025-01-22',NULL,'16:00:00','Migraine Treatment'),(9,9,9,'2025-01-23',NULL,'10:30:00','Allergy Checkup'),(10,10,10,'2025-01-24',NULL,'11:30:00','Arthritis Treatment'),(11,11,11,'2025-01-25',NULL,'12:30:00','Cholesterol Check'),(12,12,12,'2025-01-26',NULL,'14:30:00','General Health Checkup'),(13,13,13,'2025-01-27',NULL,'09:30:00','Gastric Consultation'),(14,14,14,'2025-01-28',NULL,'10:30:00','Obesity Treatment'),(15,15,15,'2025-01-29',NULL,'13:30:00','Liver Disease Consultation'),(16,16,16,'2025-01-30',NULL,'14:30:00','General Checkup'),(17,17,17,'2025-02-01',NULL,'09:00:00','Skin Allergy Treatment'),(18,18,18,'2025-02-02',NULL,'10:00:00','Headache Treatment'),(19,19,19,'2025-02-03',NULL,'11:00:00','Routine Checkup'),(20,20,20,'2025-02-04',NULL,'12:00:00','Thyroid Check'),(21,1,1,'2025-01-01',NULL,'10:00:00','Check-up'),(22,2,3,'2025-01-02',NULL,'11:00:00','Pain Management'),(23,3,5,'2025-01-03',NULL,'12:00:00','Surgical Consultation'),(24,4,7,'2025-01-04',NULL,'13:00:00','Routine Check-up'),(25,5,9,'2025-01-05',NULL,'14:00:00','Heart Disease Follow-up'),(26,6,2,'2025-01-06',NULL,'15:00:00','General Consultation'),(27,7,4,'2025-01-07',NULL,'16:00:00','Ophthalmic Consultation'),(28,8,8,'2025-01-08',NULL,'17:00:00','Chronic Pain Management'),(29,9,6,'2025-01-09',NULL,'18:00:00','Neurology Follow-up'),(30,10,3,'2025-01-10',NULL,'19:00:00','General Consultation'),(31,11,10,'2025-01-11',NULL,'10:00:00','Routine Check-up'),(32,12,12,'2025-01-12',NULL,'11:00:00','Gastroscopy'),(33,13,15,'2025-01-13',NULL,'12:00:00','Dental Check-up'),(34,14,14,'2025-01-14',NULL,'13:00:00','Skin Consultation'),(35,15,16,'2025-01-15',NULL,'14:00:00','Psychiatric Consultation'),(36,16,18,'2025-01-16',NULL,'15:00:00','Kidney Check-up'),(37,17,11,'2025-01-17',NULL,'16:00:00','Gastroenterology Consultation'),(38,18,17,'2025-01-18',NULL,'17:00:00','Urology Consultation'),(39,19,2,'2025-01-19',NULL,'18:00:00','General Consultation'),(40,20,1,'2025-01-20',NULL,'19:00:00','Cardiology Consultation');
/*!40000 ALTER TABLE `appointment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `billing`
--

DROP TABLE IF EXISTS `billing`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `billing` (
  `BillID` int NOT NULL AUTO_INCREMENT,
  `PatientID` int DEFAULT NULL,
  `Amount` decimal(10,2) DEFAULT NULL,
  `PaymentStatus` enum('Paid','Unpaid','Pending') DEFAULT NULL,
  `Date` date NOT NULL,
  `TotalAmount` decimal(10,2) DEFAULT NULL,
  `BillingDate` date NOT NULL,
  PRIMARY KEY (`BillID`),
  KEY `PatientID` (`PatientID`),
  CONSTRAINT `billing_ibfk_1` FOREIGN KEY (`PatientID`) REFERENCES `patient` (`PatientID`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `billing`
--

LOCK TABLES `billing` WRITE;
/*!40000 ALTER TABLE `billing` DISABLE KEYS */;
INSERT INTO `billing` VALUES (1,1,NULL,'Paid','2025-01-01',500.00,'2025-01-01'),(2,2,NULL,'Unpaid','2025-01-02',300.00,'2025-01-02'),(3,3,NULL,'Pending','2025-01-03',750.00,'2025-01-03'),(4,4,NULL,'Paid','2025-01-04',200.00,'2025-01-04'),(5,5,NULL,'Paid','2025-01-05',1000.00,'2025-01-05'),(6,6,NULL,'Unpaid','2025-01-06',450.00,'2025-01-06'),(7,7,NULL,'Paid','2025-01-07',600.00,'2025-01-07'),(8,8,NULL,'Pending','2025-01-08',1200.00,'2025-01-08'),(9,9,NULL,'Paid','2025-01-09',350.00,'2025-01-09'),(10,10,NULL,'Unpaid','2025-01-10',800.00,'2025-01-10'),(11,11,NULL,'Paid','2025-01-11',500.00,'2025-01-11'),(12,12,NULL,'Pending','2025-01-12',750.00,'2025-01-12'),(13,13,NULL,'Paid','2025-01-13',200.00,'2025-01-13'),(14,14,NULL,'Unpaid','2025-01-14',950.00,'2025-01-14'),(15,15,NULL,'Paid','2025-01-15',600.00,'2025-01-15'),(16,16,NULL,'Pending','2025-01-16',400.00,'2025-01-16'),(17,17,NULL,'Unpaid','2025-01-17',500.00,'2025-01-17'),(18,18,NULL,'Paid','2025-01-18',700.00,'2025-01-18'),(19,19,NULL,'Pending','2025-01-19',650.00,'2025-01-19'),(20,20,NULL,'Paid','2025-01-20',300.00,'2025-01-20'),(21,1,NULL,'Paid','2025-01-01',500.00,'2025-01-01'),(22,2,NULL,'Unpaid','2025-01-02',1000.00,'2025-01-02'),(23,3,NULL,'Paid','2025-01-03',1500.00,'2025-01-03'),(24,4,NULL,'Unpaid','2025-01-04',1200.00,'2025-01-04'),(25,5,NULL,'Paid','2025-01-05',1100.00,'2025-01-05'),(26,6,NULL,'Paid','2025-01-06',600.00,'2025-01-06'),(27,7,NULL,'Unpaid','2025-01-07',800.00,'2025-01-07'),(28,8,NULL,'Paid','2025-01-08',950.00,'2025-01-08'),(29,9,NULL,'Paid','2025-01-09',500.00,'2025-01-09'),(30,10,NULL,'Unpaid','2025-01-10',1200.00,'2025-01-10'),(31,11,NULL,'Paid','2025-01-11',750.00,'2025-01-11'),(32,12,NULL,'Unpaid','2025-01-12',950.00,'2025-01-12'),(33,13,NULL,'Paid','2025-01-13',1100.00,'2025-01-13'),(34,14,NULL,'Unpaid','2025-01-14',1300.00,'2025-01-14'),(35,15,NULL,'Paid','2025-01-15',900.00,'2025-01-15'),(36,16,NULL,'Unpaid','2025-01-16',700.00,'2025-01-16'),(37,17,NULL,'Paid','2025-01-17',1200.00,'2025-01-17'),(38,18,NULL,'Paid','2025-01-18',1000.00,'2025-01-18'),(39,19,NULL,'Unpaid','2025-01-19',1300.00,'2025-01-19'),(40,20,NULL,'Paid','2025-01-20',800.00,'2025-01-20');
/*!40000 ALTER TABLE `billing` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `department`
--

DROP TABLE IF EXISTS `department`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `department` (
  `DepartmentID` int NOT NULL AUTO_INCREMENT,
  `DepartmentName` varchar(100) NOT NULL,
  PRIMARY KEY (`DepartmentID`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `department`
--

LOCK TABLES `department` WRITE;
/*!40000 ALTER TABLE `department` DISABLE KEYS */;
INSERT INTO `department` VALUES (1,'Cardiology'),(2,'Orthopedics'),(3,'Neurology'),(4,'Pediatrics'),(5,'Dermatology'),(6,'Radiology'),(7,'Oncology'),(8,'Gastroenterology'),(9,'Psychiatry'),(10,'Surgery'),(11,'Emergency'),(12,'General Medicine'),(13,'Urology'),(14,'Ophthalmology'),(15,'Endocrinology'),(16,'ENT'),(17,'Dentistry'),(18,'Pulmonology'),(19,'Pathology'),(20,'Rheumatology');
/*!40000 ALTER TABLE `department` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medicalrecord`
--

DROP TABLE IF EXISTS `medicalrecord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medicalrecord` (
  `RecordID` int NOT NULL AUTO_INCREMENT,
  `PatientID` int DEFAULT NULL,
  `Diagnosis` text,
  `Treatment` text,
  `Date` date NOT NULL,
  `RecordDate` date NOT NULL,
  PRIMARY KEY (`RecordID`),
  KEY `PatientID` (`PatientID`),
  CONSTRAINT `medicalrecord_ibfk_1` FOREIGN KEY (`PatientID`) REFERENCES `patient` (`PatientID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medicalrecord`
--

LOCK TABLES `medicalrecord` WRITE;
/*!40000 ALTER TABLE `medicalrecord` DISABLE KEYS */;
/*!40000 ALTER TABLE `medicalrecord` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patient`
--

DROP TABLE IF EXISTS `patient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patient` (
  `PatientID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(100) NOT NULL,
  `DateOfBirth` date DEFAULT NULL,
  `Gender` enum('Male','Female','Other') DEFAULT NULL,
  `ContactInfo` varchar(100) DEFAULT NULL,
  `Address` text,
  `Age` int DEFAULT NULL,
  `MedicalHistory` text,
  PRIMARY KEY (`PatientID`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient`
--

LOCK TABLES `patient` WRITE;
/*!40000 ALTER TABLE `patient` DISABLE KEYS */;
INSERT INTO `patient` VALUES (1,'Ali Khan','1989-01-01','Male','0301-1234567','123 Street 1, Lahore',NULL,'No known allergies'),(2,'Fatima Bibi','1996-02-14','Female','0312-9876543','456 Street 2, Karachi',NULL,'Asthma'),(3,'Ahmed Raza','1983-03-25','Male','0321-6549870','789 Street 3, Islamabad',NULL,'Diabetes'),(4,'Sana Shah','1970-06-18','Female','0303-6543210','135 Street 4, Rawalpindi',NULL,'Hypertension'),(5,'Imran Ali','1960-11-10','Male','0333-7891234','246 Street 5, Peshawar',NULL,'Heart Disease'),(6,'Ayesha Khan','1997-09-30','Female','0345-9081234','567 Street 6, Quetta',NULL,'No known issues'),(7,'Muhammad Aslam','1963-04-12','Male','0355-1122334','123 Street 7, Multan',NULL,'Chronic Back Pain'),(8,'Nadia Malik','1990-07-21','Female','0366-7788899','234 Street 8, Faisalabad',NULL,'Migraine'),(9,'Umar Farooq','1978-02-02','Male','0377-3456789','345 Street 9, Sialkot',NULL,'No known allergies'),(10,'Samina Akhtar','1985-08-17','Female','0388-4567890','456 Street 10, Gujranwala',NULL,'Arthritis'),(11,'Zeeshan Tariq','1973-11-22','Male','0399-5678901','567 Street 11, Rawalpindi',NULL,'High Cholesterol'),(12,'Madiha Sadiq','2000-04-05','Female','0400-6789012','678 Street 12, Lahore',NULL,'No known issues'),(13,'Saeed Qureshi','1982-01-12','Male','0411-7890123','789 Street 13, Karachi',NULL,'Gastric issues'),(14,'Razia Aziz','1974-08-15','Female','0422-8901234','890 Street 14, Islamabad',NULL,'Obesity'),(15,'Shahid Iqbal','1985-06-20','Male','0433-9012345','123 Street 15, Peshawar',NULL,'Liver Disease'),(16,'Nashit Hussain','1994-09-12','Male','0444-2345678','234 Street 16, Quetta',NULL,'No known issues'),(17,'Kiran Butt','1992-11-25','Female','0455-3456789','345 Street 17, Faisalabad',NULL,'Skin Allergy'),(18,'Wasiq Shah','1981-02-10','Male','0466-4567890','456 Street 18, Multan',NULL,'Frequent Headaches'),(19,'Muneeb Ahmad','1996-03-01','Male','0477-5678901','567 Street 19, Sialkot',NULL,'No known issues'),(20,'Nazia Javed','1981-07-14','Female','0488-6789012','678 Street 20, Gujranwala',NULL,'Thyroid issues');
/*!40000 ALTER TABLE `patient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `patientoverview`
--

DROP TABLE IF EXISTS `patientoverview`;
/*!50001 DROP VIEW IF EXISTS `patientoverview`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `patientoverview` AS SELECT 
 1 AS `PatientID`,
 1 AS `Name`,
 1 AS `ContactInfo`,
 1 AS `AppointmentCount`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `staff`
--

DROP TABLE IF EXISTS `staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `staff` (
  `StaffID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(100) NOT NULL,
  `DepartmentID` int DEFAULT NULL,
  `ContactInfo` varchar(100) DEFAULT NULL,
  `Role` varchar(100) DEFAULT NULL,
  `Specialization` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`StaffID`),
  KEY `DepartmentID` (`DepartmentID`),
  CONSTRAINT `staff_ibfk_1` FOREIGN KEY (`DepartmentID`) REFERENCES `department` (`DepartmentID`)
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff`
--

LOCK TABLES `staff` WRITE;
/*!40000 ALTER TABLE `staff` DISABLE KEYS */;
INSERT INTO `staff` VALUES (1,'Dr. Asif Ali',NULL,'0301-1122334','Doctor','Cardiologist'),(2,'Dr. Rabia Aziz',NULL,'0311-2233445','Doctor','General Physician'),(3,'Dr. Imran Tariq',NULL,'0321-3344556','Doctor','Orthopedic'),(4,'Nurse Ayesha Khan',NULL,'0345-4455667','Nurse','ICU Nurse'),(5,'Nurse Samina Bibi',NULL,'0355-5566778','Nurse','Ward Nurse'),(6,'Dr. Shahid Iqbal',NULL,'0366-6677889','Doctor','Gastroenterologist'),(7,'Dr. Zainab Khan',NULL,'0377-7788990','Doctor','Dermatologist'),(8,'Nurse Rabia Qureshi',NULL,'0388-8899001','Nurse','Surgical Nurse'),(9,'Dr. Noman Farooq',NULL,'0399-9900112','Doctor','Pediatrician'),(10,'Nurse Uzma Shafiq',NULL,'0400-0011223','Nurse','Emergency Nurse'),(11,'Dr. Bilal Ahmed',NULL,'0411-1122334','Doctor','Neuro Physician'),(12,'Dr. Saeed Hassan',NULL,'0422-2233445','Doctor','Psychiatrist'),(13,'Nurse Kiran Butt',NULL,'0433-3344556','Nurse','Recovery Nurse'),(14,'Dr. Aamir Shah',NULL,'0444-4455667','Doctor','Endocrinologist'),(15,'Nurse Nazia Javed',NULL,'0455-5566778','Nurse','Preoperative Nurse'),(16,'Dr. Waqar Qureshi',NULL,'0466-6677889','Doctor','Ophthalmologist'),(17,'Dr. Mehmood Ali',NULL,'0477-7788990','Doctor','Urologist'),(18,'Nurse Muneeb Ahmad',NULL,'0488-8899001','Nurse','ICU Nurse'),(19,'Dr. Iqbal Rana',NULL,'0301-9900112','Doctor','General Surgeon'),(20,'Dr. Fariha Khan',NULL,'0311-0011223','Doctor','Radiologist'),(21,'Dr. Kamran',NULL,'0300-1112222','Doctor','Cardiology'),(22,'Nurse Maria',NULL,'0310-2223333','Nurse','General'),(23,'Dr. Saad',NULL,'0320-3334444','Doctor','Orthopedics'),(24,'Dr. Rabia',NULL,'0330-4445555','Doctor','Pediatrics'),(25,'Nurse Sana',NULL,'0340-5556666','Nurse','Surgical'),(26,'Dr. Hassan',NULL,'0350-6667777','Doctor','Neurology'),(27,'Dr. Adeel',NULL,'0360-7778888','Doctor','Cardiology'),(28,'Nurse Amna',NULL,'0370-8889999','Nurse','General'),(29,'Dr. Ayesha',NULL,'0380-9990000','Doctor','Gynecology'),(30,'Dr. Farhan',NULL,'0390-0001111','Doctor','Orthopedics'),(31,'Nurse Mehwish',NULL,'0400-1112222','Nurse','Surgical'),(32,'Dr. Muneeb',NULL,'0410-2223333','Doctor','Gastroenterology'),(33,'Nurse Zainab',NULL,'0420-3334444','Nurse','Cardiology'),(34,'Dr. Imran',NULL,'0430-4445555','Doctor','Dentistry'),(35,'Dr. Zahra',NULL,'0440-5556666','Doctor','Dermatology'),(36,'Dr. Ali',NULL,'0450-6667777','Doctor','Psychiatry'),(37,'Nurse Amina',NULL,'0460-7778888','Nurse','General'),(38,'Dr. Sarah',NULL,'0470-8889999','Doctor','Nephrology'),(39,'Dr. Shahbaz',NULL,'0480-9990000','Doctor','Urology'),(40,'Dr. Kamran',NULL,'0300-1112222','Doctor','Cardiology'),(41,'Nurse Maria',NULL,'0310-2223333','Nurse','General'),(42,'Dr. Saad',NULL,'0320-3334444','Doctor','Orthopedics'),(43,'Dr. Rabia',NULL,'0330-4445555','Doctor','Pediatrics'),(44,'Nurse Sana',NULL,'0340-5556666','Nurse','Surgical'),(45,'Dr. Hassan',NULL,'0350-6667777','Doctor','Neurology'),(46,'Dr. Adeel',NULL,'0360-7778888','Doctor','Cardiology'),(47,'Nurse Amna',NULL,'0370-8889999','Nurse','General'),(48,'Dr. Ayesha',NULL,'0380-9990000','Doctor','Gynecology'),(49,'Dr. Farhan',NULL,'0390-0001111','Doctor','Orthopedics'),(50,'Nurse Mehwish',NULL,'0400-1112222','Nurse','Surgical'),(51,'Dr. Muneeb',NULL,'0410-2223333','Doctor','Gastroenterology'),(52,'Nurse Zainab',NULL,'0420-3334444','Nurse','Cardiology'),(53,'Dr. Imran',NULL,'0430-4445555','Doctor','Dentistry'),(54,'Dr. Zahra',NULL,'0440-5556666','Doctor','Dermatology'),(55,'Dr. Ali',NULL,'0450-6667777','Doctor','Psychiatry'),(56,'Nurse Amina',NULL,'0460-7778888','Nurse','General'),(57,'Dr. Sarah',NULL,'0470-8889999','Doctor','Nephrology'),(58,'Dr. Shahbaz',NULL,'0480-9990000','Doctor','Urology');
/*!40000 ALTER TABLE `staff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Final view structure for view `patientoverview`
--

/*!50001 DROP VIEW IF EXISTS `patientoverview`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `patientoverview` AS select `patient`.`PatientID` AS `PatientID`,`patient`.`Name` AS `Name`,`patient`.`ContactInfo` AS `ContactInfo`,count(`appointment`.`AppointmentID`) AS `AppointmentCount` from (`patient` left join `appointment` on((`patient`.`PatientID` = `appointment`.`PatientID`))) group by `patient`.`PatientID`,`patient`.`Name`,`patient`.`ContactInfo` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-07  7:22:25
