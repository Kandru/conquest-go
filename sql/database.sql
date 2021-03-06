-- MySQL dump 10.13  Distrib 5.7.12, for Win64 (x86_64)
--
-- Host: 10.99.0.12    Database: csgo_1
-- ------------------------------------------------------
-- Server version	5.5.5-10.0.25-MariaDB-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `classes`
--

DROP TABLE IF EXISTS `classes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `classes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_bin NOT NULL,
  `can_have_medkit` int(1) NOT NULL DEFAULT '0',
  `can_have_ammobox` int(1) NOT NULL DEFAULT '0',
  `can_have_tugs` int(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `classes`
--

LOCK TABLES `classes` WRITE;
/*!40000 ALTER TABLE `classes` DISABLE KEYS */;
INSERT INTO `classes` VALUES (1,'Support',0,1,0),(2,'Engineer',0,0,0),(3,'Recon',0,0,1),(4,'Assault',1,0,0);
/*!40000 ALTER TABLE `classes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `flags`
--

DROP TABLE IF EXISTS `flags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `flags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `map` varchar(255) COLLATE utf8_bin NOT NULL,
  `name` varchar(255) COLLATE utf8_bin NOT NULL,
  `orderby` int(11) NOT NULL,
  `X` float NOT NULL,
  `Y` float NOT NULL,
  `Z` float NOT NULL,
  `spawn_X` float NOT NULL,
  `spawn_Y` float NOT NULL,
  `spawn_Z` float NOT NULL,
  `distance` int(11) NOT NULL,
  `timer` int(11) NOT NULL,
  `status` varchar(255) COLLATE utf8_bin NOT NULL,
  `type` varchar(255) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flags`
--

LOCK TABLES `flags` WRITE;
/*!40000 ALTER TABLE `flags` DISABLE KEYS */;
INSERT INTO `flags` VALUES (1,'cs_office','Snowman',3,-1280.82,871.263,-323.752,-1168.48,1112.97,-385.93,500,5,'none','none'),(2,'cs_office','Bathroom',4,665.659,-214.234,-159.968,665.8,-126.83,-159.968,200,5,'none','none'),(3,'cs_office','Garage Yard',5,1214.07,-1646.14,-322.808,1045.25,-1949.68,-282.334,600,6,'none','none'),(4,'cs_office','CT Spawn',1,-1183.05,-1853.4,-335.968,-1366.52,-1862.71,-335.97,600,120,'CT','none'),(5,'cs_office','T Spawn',2,1584.69,333.506,-159.968,1463.65,608.93,-159.968,600,120,'T','none'),(6,'de_dust2','A Ramp',1,1341.39,2922.95,132.87,1151.96,2974.8,130.58,600,6,'CT','none'),(7,'de_dust2','Long',3,633.45,502.89,2.32,557.82,372.5,7.192,200,6,'none','none'),(8,'de_dust2','T Camp',2,-1479.14,-497.622,134.066,-1108.12,-394.803,133.18,600,6,'T','none'),(9,'de_dust2','Dark',4,-1926.4,1200.24,32.031,-2109.8,1140.19,32.04,500,6,'none','none'),(10,'de_dust2','Plateu',5,-1919.42,2762.73,32.03,-2053.6,3016.64,32.04,400,6,'none','none'),(11,'de_dust2','Outside B',6,-448.9,2186.16,-127.39,-548.667,1851.77,-122.9,500,12,'none','none'),(12,'de_dust2','Terrorist MID',7,-397.925,431.422,5.943,-662.804,378.55,5.45,400,12,'none','none'),(13,'fauquier','A',3,-73.213,-220.57,64.031,-22.208,633.3,64.1,400,6,'none','none'),(14,'fauquier','T Spawn',2,1850.11,22.877,352.04,1652.69,-292.529,352.04,200,120,'T','none'),(15,'fauquier','B',4,-896.031,784.636,64.04,-1189.99,561.418,64.04,100,6,'none','none'),(16,'fauquier','C',5,-886.595,1229.25,320.04,-1533.83,1406.84,376.031,200,6,'none','none'),(17,'fauquier','CT Spawn',1,-2674.6,-750.458,790.515,-2921.47,-442.245,752.04,700,120,'CT','none'),(18,'fauquier','E',6,-34.739,-641.99,608.031,521.675,-918.871,616.032,500,6,'none','none'),(19,'fauquier','D',7,-947.663,320.939,512.04,-1230.05,481.318,512.04,200,6,'none','none'),(21,'de_cbble','CT Spawn',1,-2540.69,-1575.17,167.21,-2752.49,-1672.32,48.032,400,120,'CT','none'),(22,'de_cbble','Dropper',3,-860.42,-373.59,165.04,-813.81,-119.94,128.004,300,6,'none','none'),(23,'de_cbble','Fountain',4,278.64,-990.08,-51.65,690.39,-945.16,-107.37,400,6,'none','none'),(24,'de_cbble','Courtyard',5,-2442.31,2423.29,16.04,-2492.53,2526.78,16.04,500,6,'none','none'),(25,'de_cbble','T Spawn',2,42.37,1277.99,36.04,414.05,1114.42,38.34,400,120,'T','none'),(26,'de_cbble','Middle',6,-2335.94,196.16,-239.97,-2317.45,272.45,-239.97,200,6,'none','');
/*!40000 ALTER TABLE `flags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `players`
--

DROP TABLE IF EXISTS `players`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `players` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `steamid` varchar(255) COLLATE utf8_bin NOT NULL,
  `username` varchar(255) COLLATE utf8_bin NOT NULL,
  `group` int(11) NOT NULL DEFAULT '0',
  `rank` text COLLATE utf8_bin NOT NULL,
  `cash` int(11) NOT NULL DEFAULT '0',
  `class` int(11) NOT NULL DEFAULT '0',
  `skin` text COLLATE utf8_bin NOT NULL,
  `change_skin` int(1) NOT NULL DEFAULT '0',
  `change_class` int(1) NOT NULL DEFAULT '0',
  `change_loadout1` int(1) NOT NULL DEFAULT '0',
  `loadout1` text COLLATE utf8_bin NOT NULL,
  `spawn_menu_active` int(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `players`
--

LOCK TABLES `players` WRITE;
/*!40000 ALTER TABLE `players` DISABLE KEYS */;
/*!40000 ALTER TABLE `players` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ranks`
--

DROP TABLE IF EXISTS `ranks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ranks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_bin NOT NULL,
  `points_needed` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ranks`
--

LOCK TABLES `ranks` WRITE;
/*!40000 ALTER TABLE `ranks` DISABLE KEYS */;
INSERT INTO `ranks` VALUES (1,'1',1000),(2,'2',1000),(3,'3',1000),(4,'4',1000),(5,'5',1000),(6,'6',1000),(7,'7',1000),(8,'8',1000),(9,'9',1000),(10,'10',1000),(11,'11',1000),(12,'12',1000),(13,'13',1000),(14,'14',1000),(15,'15',1000),(16,'16',1000),(17,'17',1000),(18,'18',1000),(19,'19',1000),(20,'20',1000),(21,'21',1000),(22,'22',1000),(23,'23',1000),(24,'24',1000),(25,'25',1000),(26,'26',1000),(27,'27',1000),(28,'28',1000),(29,'29',1000),(30,'30',1000),(31,'31',1000),(32,'32',1000),(33,'33',1000),(34,'34',1000),(35,'35',1000),(36,'36',1000),(37,'37',1000),(38,'38',1000),(39,'39',1000),(40,'40',1000),(41,'41',1000),(42,'42',1000),(43,'43',1000),(44,'44',1000),(45,'45',1000),(46,'46',1000),(47,'47',1000),(48,'48',1000),(49,'49',1000),(50,'50',1000),(51,'51',1000),(52,'52',1000),(53,'53',1000),(54,'54',1000),(55,'55',1000),(56,'56',1000),(57,'57',1000),(58,'58',1000),(59,'59',1000),(60,'60',1000);
/*!40000 ALTER TABLE `ranks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `skins`
--

DROP TABLE IF EXISTS `skins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `skins` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `team` varchar(2) COLLATE utf8_bin DEFAULT '',
  `modelpath` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `downloadlist` text COLLATE utf8_bin,
  `group` int(11) DEFAULT '99',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `skins`
--

LOCK TABLES `skins` WRITE;
/*!40000 ALTER TABLE `skins` DISABLE KEYS */;
INSERT INTO `skins` VALUES (1,'Rayman','','models/player/custom_player/voikanaa/rayman.mdl','models/player/custom_player/voikanaa/rayman.mdl\nmodels/player/custom_player/voikanaa/rayman.phy\nmodels/player/custom_player/voikanaa/rayman.vvd\nmodels/player/custom_player/voikanaa/rayman.dx90.vtx\nmaterials/models/player/voikanaa/rayman/rayman_sheet.vtf\nmaterials/models/player/voikanaa/rayman/rayman_sheet_bump.vtf\nmaterials/models/player/voikanaa/rayman/rayman_sheet.vmt',99),(2,'Shadow Company (MW2)','','models/player/custom_player/voikanaa/mw2/shadowcompany.mdl','materials/models/player/voikanaa/mw2/shadowcompany/eyes.vmt\nmaterials/models/player/voikanaa/mw2/shadowcompany/eyes.vtf\nmaterials/models/player/voikanaa/mw2/shadowcompany/eyes_n.vtf\nmaterials/models/player/voikanaa/mw2/shadowcompany/shad_co_head.vmt\nmaterials/models/player/voikanaa/mw2/shadowcompany/shad_co_head.vtf\nmaterials/models/player/voikanaa/mw2/shadowcompany/shad_co_head_n.vtf\nmaterials/models/player/voikanaa/mw2/shadowcompany/shad_co_headgear.vmt\nmaterials/models/player/voikanaa/mw2/shadowcompany/shad_co_headgear.vtf\nmaterials/models/player/voikanaa/mw2/shadowcompany/shad_co_headgear_n.vtf\nmaterials/models/player/voikanaa/mw2/shadowcompany/shad_co_low_body.vmt\nmaterials/models/player/voikanaa/mw2/shadowcompany/shad_co_low_body.vtf\nmaterials/models/player/voikanaa/mw2/shadowcompany/shad_co_low_body_n.vtf\nmaterials/models/player/voikanaa/mw2/shadowcompany/shad_co_smg.vmt\nmaterials/models/player/voikanaa/mw2/shadowcompany/shad_co_smg.vtf\nmaterials/models/player/voikanaa/mw2/shadowcompany/shad_co_smg_n.vtf\nmaterials/models/player/voikanaa/mw2/shadowcompany/shad_co_up_body.vmt\nmaterials/models/player/voikanaa/mw2/shadowcompany/shad_co_up_body.vtf\nmaterials/models/player/voikanaa/mw2/shadowcompany/shad_co_up_body_n.vtf\nmaterials/models/player/voikanaa/mw2/shadowcompany/shadow_co_visor.vmt\nmaterials/models/player/voikanaa/mw2/shadowcompany/shadow_co_visor.vtf\nmodels/player/custom_player/voikanaa/mw2/shadowcompany.mdl\nmodels/player/custom_player/voikanaa/mw2/shadowcompany.phy\nmodels/player/custom_player/voikanaa/mw2/shadowcompany.vvd\nmodels/player/custom_player/voikanaa/mw2/shadowcompany.dx90.vtx',99),(7,'Nanosuit','','models/player/custom_player/kuristaja/nanosuit/nanosuitv3.mdl','materials/models/player/kuristaja/nanosuit/nanosuit_arms.vmt\nmaterials/models/player/kuristaja/nanosuit/nanosuit_arms_vmodel.vmt\nmaterials/models/player/kuristaja/nanosuit/nanosuit_arms2.vmt\nmaterials/models/player/kuristaja/nanosuit/nanosuit_arms2_vmodel.vmt\nmaterials/models/player/kuristaja/nanosuit/nanosuit_hands.vmt\nmaterials/models/player/kuristaja/nanosuit/nanosuit_hands_vmodel.vmt\nmaterials/models/player/kuristaja/nanosuit/nanosuit_hands2.vmt\nmaterials/models/player/kuristaja/nanosuit/nanosuit_hands2_vmodel.vmt\nmaterials/models/player/kuristaja/nanosuit/nanosuit_helmet.vmt\nmaterials/models/player/kuristaja/nanosuit/nanosuit_helmet_pt.vmt\nmaterials/models/player/kuristaja/nanosuit/nanosuit_helmet2.vmt\nmaterials/models/player/kuristaja/nanosuit/nanosuit_helmet3.vmt\nmaterials/models/player/kuristaja/nanosuit/nanosuit_legs.vmt\nmaterials/models/player/kuristaja/nanosuit/nanosuit_legs2.vmt\nmaterials/models/player/kuristaja/nanosuit/nanosuit_legs3.vmt\nmaterials/models/player/kuristaja/nanosuit/nanosuit_torso.vmt\nmaterials/models/player/kuristaja/nanosuit/nanosuit_torso2.vmt\nmaterials/models/player/kuristaja/nanosuit/nanosuit_visor.vmt\nmaterials/models/player/kuristaja/nanosuit/nanosuit_arms.vtf\nmaterials/models/player/kuristaja/nanosuit/nanosuit_arms_normal.vtf\nmaterials/models/player/kuristaja/nanosuit/nanosuit_hands.vtf\nmaterials/models/player/kuristaja/nanosuit/nanosuit_hands_normal.vtf\nmaterials/models/player/kuristaja/nanosuit/nanosuit_helmet.vtf\nmaterials/models/player/kuristaja/nanosuit/nanosuit_helmet_normal.vtf\nmaterials/models/player/kuristaja/nanosuit/nanosuit_helmet_pt.vtf\nmaterials/models/player/kuristaja/nanosuit/nanosuit_legs.vtf\nmaterials/models/player/kuristaja/nanosuit/nanosuit_legs_normal.vtf\nmaterials/models/player/kuristaja/nanosuit/nanosuit_torso.vtf\nmaterials/models/player/kuristaja/nanosuit/nanosuit_torso_normal.vtf\nmaterials/models/player/kuristaja/nanosuit/nanosuit_visor.vtf\nmaterials/models/player/kuristaja/nanosuit/nanosuit_visor_normal.vtf\nmodels/player/custom_player/kuristaja/nanosuit/nanosuitv3.dx90.vtx\nmodels/player/custom_player/kuristaja/nanosuit/nanosuitv3.mdl\nmodels/player/custom_player/kuristaja/nanosuit/nanosuitv3.phy\nmodels/player/custom_player/kuristaja/nanosuit/nanosuitv3.vvd\nmodels/player/custom_player/kuristaja/nanosuit/nanosuit_arms.dx90.vtx\nmodels/player/custom_player/kuristaja/nanosuit/nanosuit_arms.mdl\nmodels/player/custom_player/kuristaja/nanosuit/nanosuit_arms.vvd',99),(8,'Guard #1','CT','models/player/custom_player/kuristaja/jailbreak/guard1/guard1.mdl','materials/models/player/kuristaja/jailbreak/shared/brown_eye01_an_d.vmt\nmaterials/models/player/kuristaja/jailbreak/shared/police_body_d.vmt\nmaterials/models/player/kuristaja/jailbreak/shared/prisoner1_body.vmt\nmaterials/models/player/kuristaja/jailbreak/shared/tex_0086_0.vmt\nmaterials/models/player/kuristaja/jailbreak/shared/brown_eye_normal.vtf\nmaterials/models/player/kuristaja/jailbreak/shared/brown_eye01_an_d.vtf\nmaterials/models/player/kuristaja/jailbreak/shared/police_body_d.vtf\nmaterials/models/player/kuristaja/jailbreak/shared/police_body_normal.vtf\nmaterials/models/player/kuristaja/jailbreak/shared/prisoner1_body.vtf\nmaterials/models/player/kuristaja/jailbreak/shared/prisoner1_body_normal.vtf\nmaterials/models/player/kuristaja/jailbreak/shared/tex_0086_0.vtf\nmaterials/models/player/kuristaja/jailbreak/shared/tex_0086_1.vtf\nmaterials/models/player/kuristaja/jailbreak/guard1/hair01_ao_d.vmt\nmaterials/models/player/kuristaja/jailbreak/guard1/hair01_ao_d2.vmt\nmaterials/models/player/kuristaja/jailbreak/guard1/sewell01_head01_au_d.vmt\nmaterials/models/player/kuristaja/jailbreak/guard1/hair01_ao_d.vtf\nmaterials/models/player/kuristaja/jailbreak/guard1/hair01_ao_normal.vtf\nmaterials/models/player/kuristaja/jailbreak/guard1/sewell01_head01_au_d.vtf\nmaterials/models/player/kuristaja/jailbreak/guard1/sewell01_head01_au_normal.vtf\nmodels/player/custom_player/kuristaja/jailbreak/guard1/guard1.dx90.vtx\nmodels/player/custom_player/kuristaja/jailbreak/guard1/guard1.mdl\nmodels/player/custom_player/kuristaja/jailbreak/guard1/guard1.phy\nmodels/player/custom_player/kuristaja/jailbreak/guard1/guard1.vvd\nmodels/player/custom_player/kuristaja/jailbreak/guard1/guard1_arms.dx90.vtx\nmodels/player/custom_player/kuristaja/jailbreak/guard1/guard1_arms.mdl\nmodels/player/custom_player/kuristaja/jailbreak/guard1/guard1_arms.vvd',1),(9,'Prisoner #5','T','models/player/custom_player/kuristaja/jailbreak/prisoner5/prisoner5.mdl','materials/models/player/kuristaja/jailbreak/prisoner5/denise_head01_d.vmt\nmaterials/models/player/kuristaja/jailbreak/prisoner5/lara_brow_d.vmt\nmaterials/models/player/kuristaja/jailbreak/prisoner5/lara_eye_d.vmt\nmaterials/models/player/kuristaja/jailbreak/prisoner5/lara_face_d.vmt\nmaterials/models/player/kuristaja/jailbreak/prisoner5/lara_hair1_d.vmt\nmaterials/models/player/kuristaja/jailbreak/prisoner5/lara_hair1_d_tr.vmt\nmaterials/models/player/kuristaja/jailbreak/prisoner5/lara_hair2_d.vmt\nmaterials/models/player/kuristaja/jailbreak/prisoner5/lara_hair2_d_tr.vmt\nmaterials/models/player/kuristaja/jailbreak/prisoner5/lara_lashes_d.vmt\nmaterials/models/player/kuristaja/jailbreak/prisoner5/lara_mouth_d.vmt\nmaterials/models/player/kuristaja/jailbreak/prisoner5/lara_sh_d.vmt\nmaterials/models/player/kuristaja/jailbreak/prisoner5/shirt_d.vmt\nmaterials/models/player/kuristaja/jailbreak/prisoner5/denise_head01_d.vtf\nmaterials/models/player/kuristaja/jailbreak/prisoner5/denise_head01_normal.vtf\nmaterials/models/player/kuristaja/jailbreak/prisoner5/lara_brow_d.vtf\nmaterials/models/player/kuristaja/jailbreak/prisoner5/lara_eye_d.vtf\nmaterials/models/player/kuristaja/jailbreak/prisoner5/lara_eye_normal.vtf\nmaterials/models/player/kuristaja/jailbreak/prisoner5/lara_face_d.vtf\nmaterials/models/player/kuristaja/jailbreak/prisoner5/lara_face_normal.vtf\nmaterials/models/player/kuristaja/jailbreak/prisoner5/lara_hair1_d.vtf\nmaterials/models/player/kuristaja/jailbreak/prisoner5/lara_hair1_normal.vtf\nmaterials/models/player/kuristaja/jailbreak/prisoner5/lara_hair2_d.vtf\nmaterials/models/player/kuristaja/jailbreak/prisoner5/lara_hair2_normal.vtf\nmaterials/models/player/kuristaja/jailbreak/prisoner5/lara_lashes_d.vtf\nmaterials/models/player/kuristaja/jailbreak/prisoner5/lara_mouth_d.vtf\nmaterials/models/player/kuristaja/jailbreak/prisoner5/lara_sh_d.vtf\nmaterials/models/player/kuristaja/jailbreak/prisoner5/shirt_d.vtf\nmaterials/models/player/kuristaja/jailbreak/prisoner5/shirt_normal.vtf\nmodels/player/custom_player/kuristaja/jailbreak/prisoner5/prisoner5.dx90.vtx\nmodels/player/custom_player/kuristaja/jailbreak/prisoner5/prisoner5.mdl\nmodels/player/custom_player/kuristaja/jailbreak/prisoner5/prisoner5.phy\nmodels/player/custom_player/kuristaja/jailbreak/prisoner5/prisoner5.vvd\nmodels/player/custom_player/kuristaja/jailbreak/prisoner5/prisoner5_arms.dx90.vtx\nmodels/player/custom_player/kuristaja/jailbreak/prisoner5/prisoner5_arms.mdl\nmodels/player/custom_player/kuristaja/jailbreak/prisoner5/prisoner5_arms.vvd',1);
/*!40000 ALTER TABLE `skins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sounds`
--

DROP TABLE IF EXISTS `sounds`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sounds` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(255) COLLATE utf8_bin DEFAULT '',
  `name` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `file` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sounds`
--

LOCK TABLES `sounds` WRITE;
/*!40000 ALTER TABLE `sounds` DISABLE KEYS */;
INSERT INTO `sounds` VALUES (1,'endround','Monsta','conquestgo/endround/monsta.mp3'),(2,'endround','bad','conquestgo/endround/bad.mp3'),(3,'endround','badboys','conquestgo/endround/badboys.mp3'),(4,'endround','djgotusfallininlove','conquestgo/endround/djogotusfallininlove.mp3'),(5,'endround','fuckthapolice','conquestgo/endround/fuckthapolice.mp3'),(6,'endround','llelujah','conquestgo/endround/llelujah.mp3'),(7,'endround','moveit','conquestgo/endround/moveit.mp3'),(8,'endround','paperplanes','conquestgo/endround/paperplanes.mp3'),(9,'endround','partyrockanthem','conquestgo/endround/partyrockanthem.mp3'),(10,'endround','pussykiller','conquestgo/endround/pussykiller.mp3'),(11,'endround','sweat','conquestgo/endround/sweat.mp3');
/*!40000 ALTER TABLE `sounds` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `weapons`
--

DROP TABLE IF EXISTS `weapons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `weapons` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_bin NOT NULL,
  `slug` varchar(255) COLLATE utf8_bin NOT NULL,
  `rank` int(11) NOT NULL,
  `class` int(11) NOT NULL,
  `team` varchar(2) COLLATE utf8_bin DEFAULT NULL,
  `type` int(11) NOT NULL,
  `amount` int(11) NOT NULL DEFAULT '1',
  `max_ammo` int(11) NOT NULL DEFAULT '120',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=112 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `weapons`
--

LOCK TABLES `weapons` WRITE;
/*!40000 ALTER TABLE `weapons` DISABLE KEYS */;
INSERT INTO `weapons` VALUES (1,'Famas','weapon_famas',1,4,'CT',1,1,90),(2,'M4A1-S','weapon_m4a1_silencer',6,4,'CT',1,1,40),(3,'M4A4','weapon_m4a1',16,4,'CT',1,1,90),(4,'AUG','weapon_aug',31,4,'CT',1,1,90),(5,'USP-S','weapon_usp_silencer',1,4,'CT',2,1,24),(6,'P2000','weapon_hkp2000',6,4,'CT',2,1,24),(7,'P250','weapon_p250',11,4,'CT',2,1,26),(8,'Five-Seven','weapon_fiveseven',26,4,'CT',2,1,100),(9,'CZ75 Auto','weapon_cz75a',36,4,'CT',2,1,12),(10,'Deagle','weapon_deagle',56,4,'CT',2,1,35),(11,'R8 Revolver','weapon_revolver',56,4,'CT',2,1,8),(12,'HE Grenade 1x','weapon_hegrenade',1,4,'CT',3,1,0),(13,'Flashbang 1x','weapon_flashbang',1,4,'CT',3,1,0),(14,'MP9','weapon_mp9',1,2,'CT',1,1,120),(15,'MP7','weapon_mp7',6,2,'CT',1,1,120),(16,'PP-Bizon','weapon_bizon',16,2,'CT',1,1,120),(17,'UMP-45','weapon_ump45',31,2,'CT',1,1,100),(18,'P90','weapon_p90',51,2,'CT',1,1,100),(19,'USP-S','weapon_usp_silencer',1,2,'CT',2,1,24),(20,'P2000','weapon_hkp2000',6,2,'CT',2,1,24),(21,'P250','weapon_p250',11,2,'CT',2,1,26),(22,'Five-Seven','weapon_fiveseven',26,2,'CT',2,1,100),(23,'CZ75 Auto','weapon_cz75a',36,2,'CT',2,1,12),(24,'Deagle','weapon_deagle',56,2,'CT',2,1,35),(25,'R8 Revolver','weapon_revolver',56,2,'CT',2,1,8),(26,'Incendiary Grenade 1x','weapon_incgrenade',1,2,'CT',3,1,0),(27,'Smoke Grenade 1x','weapon_smokegrenade',1,2,'CT',3,1,0),(28,'MP9','weapon_mp9',1,1,'CT',1,1,120),(29,'Nova','weapon_nova',6,1,'CT',1,1,32),(30,'XM1014','weapon_xm1014',11,1,'CT',1,1,32),(31,'Mag-7','weapon_mag7',26,1,'CT',1,1,32),(32,'M249','weapon_m249',46,1,'CT',1,1,200),(33,'Negev','weapon_negev',56,1,'CT',1,1,200),(34,'USP-S','weapon_usp_silencer',1,1,'CT',2,1,24),(35,'P2000','weapon_hkp2000',6,1,'CT',2,1,24),(36,'P250','weapon_p250',11,1,'CT',2,1,26),(37,'Five-Seven','weapon_fiveseven',26,1,'CT',2,1,100),(38,'CZ75 Auto','weapon_cz75a',36,1,'CT',2,1,12),(39,'Deagle','weapon_deagle',56,1,'CT',2,1,35),(40,'R8 Revolver','weapon_revolver',56,1,'CT',2,1,8),(41,'Flashbang 2x','weapon_flashbang',1,1,'CT',3,2,0),(42,'SSG08','weapon_ssg08',1,3,'CT',1,1,90),(43,'SCAR-20','weapon_scar20',31,3,'CT',1,1,90),(44,'AWP','weapon_awp',46,3,'CT',1,1,30),(45,'USP-S','weapon_usp_silencer',1,3,'CT',2,1,24),(46,'P2000','weapon_hkp2000',6,3,'CT',2,1,24),(47,'P250','weapon_p250',11,3,'CT',2,1,26),(48,'Five-Seven','weapon_fiveseven',26,3,'CT',2,1,100),(49,'CZ75 Auto','weapon_cz75a',36,3,'CT',2,1,12),(50,'Deagle','weapon_deagle',56,3,'CT',2,1,35),(51,'R8 Revolver','weapon_revolver',56,3,'CT',2,1,8),(52,'Decoy Grenade 1x','weapon_decoy',1,3,'CT',3,1,0),(53,'Smoke Grenade 1x','weapon_smokegrenade',1,3,'CT',3,1,0),(54,'Galil AR','weapon_galilar',1,4,'T',1,1,90),(55,'AK-47','weapon_ak47',31,4,'T',1,1,90),(56,'SG 556','weapon_sg556',51,4,'T',1,1,90),(57,'Glock-18','weapon_glock',1,4,'T',2,1,120),(58,'Dual Barettas','weapon_elite',6,4,'T',2,1,120),(59,'P250','weapon_p250',11,4,'T',2,1,26),(60,'TEC-9','weapon_tec9',26,4,'T',2,1,120),(61,'CZ75 Auto','weapon_cz75a',36,4,'T',2,1,12),(62,'Deagle','weapon_deagle',56,4,'T',2,1,35),(63,'R8 Revolver','weapon_revolver',56,4,'T',2,1,8),(64,'HE Grenade 1x','weapon_hegrenade',1,4,'T',3,1,0),(65,'Flashbang 1x','weapon_flashbang',1,4,'T',3,1,0),(66,'Mac-10','weapon_mac10',1,2,'T',1,1,100),(67,'MP7','weapon_mp7',6,2,'T',1,1,120),(68,'PP-Bizon','weapon_bizon',16,2,'T',1,1,120),(69,'UMP-45','weapon_ump45',31,2,'T',1,1,100),(70,'P90','weapon_p90',51,2,'T',1,1,100),(71,'Glock-18','weapon_glock',1,2,'T',2,1,120),(72,'Dual Barettas','weapon_elite',6,2,'T',2,1,120),(73,'P250','weapon_p250',11,2,'T',2,1,26),(74,'TEC-9','weapon_tec9',26,2,'T',2,1,120),(75,'CZ75 Auto','weapon_cz75a',36,2,'T',2,1,12),(76,'Deagle','weapon_deagle',56,2,'T',2,1,35),(77,'R8 Revolver','weapon_revolver',56,2,'T',2,1,8),(78,'Molotov Cocktail 1x','weapon_molotov',1,2,'T',3,1,0),(79,'Smoke Grenade 1x','weapon_smokegrenade',1,2,'T',3,1,0),(80,'Mac-10','weapon_mac10',1,1,'T',1,1,100),(81,'Nova','weapon_nova',6,1,'T',1,1,32),(82,'XM1014','weapon_xm1014',11,1,'T',1,1,32),(83,'Sawed-Off','weapon_sawedoff',26,1,'T',1,1,32),(84,'M249','weapon_m249',46,1,'T',1,1,200),(85,'Negev','weapon_negev',56,1,'T',1,1,200),(86,'Glock-18','weapon_glock',1,1,'T',2,1,120),(87,'Dual Barettas','weapon_elite',6,1,'T',2,1,120),(88,'P250','weapon_p250',11,1,'T',2,1,26),(89,'TEC-9','weapon_tec9',26,1,'T',2,1,120),(90,'CZ75 Auto','weapon_cz75a',36,1,'T',2,1,12),(91,'Deagle','weapon_deagle',56,1,'T',2,1,35),(92,'R8 Revolver','weapon_revolver',56,1,'T',2,1,8),(93,'Flashbang 2x','weapon_flashbang',1,1,'T',3,2,0),(94,'SSG08','weapon_ssg08',1,3,'T',1,1,90),(95,'G3SG1','weapon_g3sg1',31,3,'T',1,1,90),(96,'AWP','weapon_awp',46,3,'T',1,1,30),(97,'Glock-18','weapon_glock',1,3,'T',2,1,120),(98,'Dual Barettas','weapon_elite',6,3,'T',2,1,120),(99,'P250','weapon_p250',11,3,'T',2,1,26),(100,'TEC-9','weapon_tec9',26,3,'T',2,1,120),(101,'CZ75 Auto','weapon_cz75a',36,3,'T',2,1,12),(102,'Deagle','weapon_deagle',56,3,'T',2,1,35),(103,'R8 Revolver','weapon_revolver',56,3,'T',2,1,8),(104,'Decoy Grenade 1x','weapon_decoy',1,3,'T',3,1,0),(105,'Smoke Grenade 1x','weapon_smokegrenade',1,3,'T',3,1,0),(106,'Medkit','weapon_c4',1,4,'CT',3,1,0),(107,'Medkit','weapon_c4',1,4,'T',3,1,0),(108,'Ammobox','weapon_c4',1,1,'CT',3,1,0),(109,'Ammobox','weapon_c4',1,1,'T',3,1,0),(110,'TUGS','weapon_c4',1,3,'CT',3,1,0),(111,'TUGS','weapon_c4',1,3,'T',3,1,0);
/*!40000 ALTER TABLE `weapons` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-08-07 18:34:40
