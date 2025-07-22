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
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `user_type` enum('admin','doctor','patient','staff') NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9','admin'),(3,'admin1','240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9','admin'),(7,'riaz','db381077dfef404c823ce042706e86ee519df7cfecaffd9b97cf5a0dd34b8409','staff'),(8,'rizwan','41e0660aa2975f3f8338a316caba1b5f97ecc1afaee73790e6b3a1b7ae3f530c','patient'),(9,'staff1','10176e7b7b24d317acfcf8d2064cfd2f24e154f7b5a96603077d5ef813d6a6b6','staff'),(11,'doctor1','f348d5628621f3d8f59c8cabda0f8eb0aa7e0514a90be7571020b1336f26c113','doctor'),(12,'mb1','b75bdd4bf010afa5c0448eec8c6ed8fc899413c9391d46c1d6b1846839b4e03a','patient'),(14,'saeed','97b3650166ce2517ed20c1eb1567c1c8570832a16d239a3bb8762cc529b8fb71','doctor'),(15,'sh1','d6be7fb89a392fe342033e3eccff9cadfc4a58a19316e162e079d662762ce8b8','doctor'),(16,'patient1','d3d7b232f030f5c1c3cbdbcdaf876630549bbd7ede675a5fb0f8b88685b41de4','patient'),(17,'sh2','1c56416e18e2fe12e55cb8de8ab3bb54dedec94c942520403ccd2e8dca7bf8d5','patient'),(18,'sh3','cb1f678279bd25affa85a3b20513b6c9424fbc1145c37aebfb28cf4198256f15','patient'),(19,'dr1','dcc1fc6215de51d37bbd783d25e07dea383fde2cc718a47d0b0c7d955b2bc793','doctor'),(20,'dr2','e4f321bf5c0226f6446a6faa5c2cb0fa10c93efe4e7360a9cb65b774a0105a87','doctor'),(21,'staff2','00bbfdc27068d300bab70e46dc683a9d81355634eff13b1a491b498925b89a57','staff'),(22,'ahmedkhan','040631a2074b177ce100af9a96d42f4bef77febf24295f6dcbcc59594a29798b','doctor'),(23,'fatimazahra','1dca350d47682365b7bf55dd98f84e4a6a091f893b538f307174b34eae8817ca','doctor'),(24,'muhammadali','2f8436d80563b5f1bc5ddddd2ff60957b4410410ff2138b1cdb8a959752ca0d5','doctor'),(25,'ayeshasiddiqui','9ea0b83d9092dad46d261e18a1ee850ce7a16be291933ca98ab2009ba7ab3c4c','doctor'),(26,'imranmalik','84ad08e7423c5bfa94d93b8d6ab3875a699e9ba72790f37845a0bf24c20fb926','doctor'),(27,'sabaqamar','0a8e82f73fd703f7283cadd0ea69af2bd90f92560992787bccad0f7e6311988b','doctor'),(28,'hassanraza','b08a41949be33d0f14857935e10db53ebf73a87ea51bcf922cb7a43d1153edc7','doctor'),(29,'zainabakhtar','8a79eddbeb8a0286c8dc50b7147742e60773903c97276709bc53cb07bf532dd4','doctor'),(30,'bilalabbas','bb0a01d18dbe6e2f999a28805a467d7d9acded0a2b55348ce2be846dddcb27a5','doctor'),(31,'mariyamnafees','632d71e9c6e6c2e942d058e4172f5acdc062ae8baef026fe5936dd02dadc0b28','doctor'),(32,'usmanahmed','6cca293f8fa8b4df672b27ee2aafa5ba2538044ac78ed2897d3497894bcca895','patient'),(33,'saraiftikhar','5233c023368812b63b2b2b9f199ce2758ff50d747e6ef56068f8afe9e3b51379','patient'),(34,'alihassan','f8c96aa4525b73750b57e43a72112ad8c2b49c93d7177b89b45f845dd45bb7c2','patient'),(35,'noorfatima','00e8511538dabeb1477f9be53cd92992016962084925dffa42a03cda7bedf62b','patient'),(36,'zahidkhan','ca990f5c31379cb16bf564a92651ced70a6a969e4744595f5cd6531eb5dac985','patient'),(37,'hinaaslam','290a41ffb9364bf1ed0d49d725c93ded1bb8b377062a85c9904a0df65c96c147','patient'),(38,'farooqmalik','22f93eba904033b9ab7ecacb767d7913d1c3410b8b77d41f13d02a14c119972f','patient'),(39,'aminaqadir','3f1df1bb41448468cf6278474caa89279da01bffd390ab3fd4d6cff75b410d69','patient'),(40,'saadrehman','c535fc3600952985dd265e7f9141d81ea11fc3a0c440916c5fe18c6b0b80f5b8','patient'),(41,'maryambibi','2acfaec6c60c5f20e4b0f93051f4f53fbadd90faee715bc8da0da2c858e6311e','patient'),(42,'khalidmehmood','a18cedbf129e402bc5d8735e01a7b02ac925c09d7b51afbb205c75bdeb0d0206','staff'),(43,'rabiayousaf','1b92eecfa600b35a87dfe9dc42ddfc164fdadcff2336d0248c87b76619ff3297','staff'),(44,'naveedakram','e1b4188d289289272da448ee4dcced1e16907e90c3ebb99fac38a7e0caf0a818','staff'),(45,'saimabashir','186755b8906a652ab9ff5f76fbf9b7ade3ff1a4228e0b478b1b134887066d43a','staff'),(46,'junaidkhalil','e33bfb0be06776718eaac9431e12ec9aa4e19dd7c247542f8184ab09ca4e3a59','staff'),(47,'farahnaeem','788cae5a2ab8a20159acb21e5715e88ef8fe819f3d866c48ea650e586db688dc','staff'),(48,'waqasahmed','33c0c53951dc62bec4737fc79f0b99e6bd5c8e57d272c840b8e3954c22c02f54','staff'),(49,'saniyazeba','f78fb3ee9919f51a83310a7e97fc7d0194b272c6821ff7f9f4ea5079499e9d8b','staff'),(50,'asifraza','255ae9046a60af557aff05dee4fc59f6394e01235225d4ed88fc931641755ef9','staff'),(51,'nadiaakram','7784e332600e436d3bc549fa0f17024eeefe71ee8926cd30706d24aef47274e0','staff');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-08 10:08:40
