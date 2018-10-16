--
-- Table structure for table `tbl_ENV`
--

DROP TABLE IF EXISTS `tbl_ENV`;

CREATE TABLE `tbl_ENV` (
  `id` int(32) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `room` varchar(50) NOT NULL,
  `vocabulary` text NOT NULL,
  `delay` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tbl_ENV`
--

INSERT INTO `tbl_ENV` VALUES (1,'Wall Screen','$rid=0$','Screen flickers with distorted image in what appears to be a brief glitch in the broadcast|It makes a quiet buzzing sound|Screen goes off for a second or two, then returns to normal|The animation of spinning Earth freezes briefly',15),(2,'Sink tap','$rid=4$','<drip>|<drip> <drip>',1);

--
-- Table structure for table `tbl_Items`
--

DROP TABLE IF EXISTS `tbl_Items`;

CREATE TABLE `tbl_Items` (
  `id` int(32) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `long_description` varchar(2000) NOT NULL,
  `short_description` varchar(500) NOT NULL,
  `clo_head` tinyint(1) NOT NULL,
  `clo_larm` tinyint(1) NOT NULL,
  `clo_rarm` tinyint(1) NOT NULL,
  `clo_lhand` tinyint(1) NOT NULL,
  `clo_rhand` tinyint(1) NOT NULL,
  `clo_chest` tinyint(1) NOT NULL,
  `clo_lleg` tinyint(1) NOT NULL,
  `clo_rleg` tinyint(1) NOT NULL,
  `clo_feet` tinyint(1) NOT NULL,
  `imp_head` tinyint(1) NOT NULL,
  `imp_larm` tinyint(1) NOT NULL,
  `imp_rarm` tinyint(1) NOT NULL,
  `imp_lhand` tinyint(1) NOT NULL,
  `imp_rhand` tinyint(1) NOT NULL,
  `imp_chest` tinyint(1) NOT NULL,
  `imp_lleg` tinyint(1) NOT NULL,
  `imp_rleg` tinyint(1) NOT NULL,
  `imp_feet` tinyint(1) NOT NULL,
  `mod_str` int(32) NOT NULL,
  `mod_per` int(32) NOT NULL,
  `mod_endu` int(32) NOT NULL,
  `mod_cha` int(32) NOT NULL,
  `mod_inte` int(32) NOT NULL,
  `mod_agi` int(32) NOT NULL,
  `mod_luc` int(32) NOT NULL,
  `weight` int(32) NOT NULL,
  `article` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=200003 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tbl_Items`
--

INSERT INTO `tbl_Items` VALUES (200001,'Journal Page','It is a slightly crumpled piece of paper. Appears to have been ripped out of an A4 notebook of some sort.','It is a crumpled piece of paper.',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,1,'a'),(200002,'Empty Bottle','It is a brown, glass beer bottle with its label taken off. With the contents long gone, it is bone dry inside. Shame..','It is an empty beer bottle.',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,'an');

--
-- Table structure for table `tbl_NPC`
--

DROP TABLE IF EXISTS `tbl_NPC`;

CREATE TABLE `tbl_NPC` (
  `id` int(32) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `room` varchar(50) NOT NULL,
  `lvl` int(11) NOT NULL,
  `exp` int(11) NOT NULL,
  `str` int(11) NOT NULL,
  `per` int(11) NOT NULL,
  `endu` int(11) NOT NULL,
  `cha` int(11) NOT NULL,
  `inte` int(11) NOT NULL,
  `agi` int(11) NOT NULL,
  `luc` int(11) NOT NULL,
  `cred` int(11) NOT NULL,
  `inv` varchar(200) NOT NULL,
  `isAttackable` tinyint(1) NOT NULL,
  `isStealable` tinyint(1) NOT NULL,
  `isKillable` tinyint(1) NOT NULL,
  `isAggressive` tinyint(1) NOT NULL,
  `vocabulary` text NOT NULL,
  `delay` int(11) NOT NULL,
  `lookDescription` text NOT NULL,
  `clo_head` int(11) NOT NULL,
  `clo_larm` int(11) NOT NULL,
  `clo_rarm` int(11) NOT NULL,
  `clo_lhand` int(11) NOT NULL,
  `clo_rhand` int(11) NOT NULL,
  `clo_chest` int(11) NOT NULL,
  `clo_lleg` int(11) NOT NULL,
  `clo_rleg` int(11) NOT NULL,
  `clo_feet` int(11) NOT NULL,
  `imp_head` int(11) NOT NULL,
  `imp_larm` int(11) NOT NULL,
  `imp_rarm` int(11) NOT NULL,
  `imp_lhand` int(11) NOT NULL,
  `imp_rhand` int(11) NOT NULL,
  `imp_chest` int(11) NOT NULL,
  `imp_lleg` int(11) NOT NULL,
  `imp_rleg` int(11) NOT NULL,
  `imp_feet` int(11) NOT NULL,
  `hp` int(11) NOT NULL,
  `charge` int(11) NOT NULL,
  `isInCombat` tinyint(1) NOT NULL,
  `respawn` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=90003 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tbl_NPC`
--

INSERT INTO `tbl_NPC` VALUES (90000,'Cleaning Bot','$rid=0$',1,0,1,2,1,0,0,1,2,0,'inventory',1,1,1,0,'Beep Bop!|Eeeeek!|Whir Whirrr!|Systems operational!|Buzzzzz!',50,'It\'s an automated, autonomous cleaning robot. It slowly drives around the room following mysterious paths known only to himself.',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,20,100,0,20),(90001,'Maintenance Droid','$rid=3$',1,0,8,2,7,4,3,7,5,0,'inventory',1,1,1,0,'<grunt>|Huh?|<stomp>',70,'Sturdy and durable, maintenance bots are designed to perform heavy duty tasks while supervised by a human operator.',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,150,100,0,60),(90002,'Security Guard','$rid=3$',1,0,5,8,4,4,3,7,5,110,'inventory',0,1,1,0,'Jeeez! Seems like I`ve been standing here forever...|Move along guys, nothing to see here.|<sigh>|Could this day get any longer?|What time is it anyway?',40,'Security guard looks like he\'s been standing here for a very long time.',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,100,100,0,120);

--
-- Table structure for table `tbl_Players`
--

DROP TABLE IF EXISTS `tbl_Players`;

CREATE TABLE `tbl_Players` (
  `name` varchar(50) NOT NULL,
  `room` varchar(50) NOT NULL,
  `lvl` int(11) NOT NULL,
  `exp` int(11) NOT NULL,
  `str` int(11) NOT NULL,
  `per` int(11) NOT NULL,
  `endu` int(11) NOT NULL,
  `cha` int(11) NOT NULL,
  `inte` int(11) NOT NULL,
  `agi` int(11) NOT NULL,
  `luc` int(11) NOT NULL,
  `cred` int(11) NOT NULL,
  `inv` varchar(200) NOT NULL,
  `pwd` varchar(50) NOT NULL,
  `clo_head` int(11) NOT NULL,
  `clo_larm` int(11) NOT NULL,
  `clo_rarm` int(11) NOT NULL,
  `clo_lhand` int(11) NOT NULL,
  `clo_rhand` int(11) NOT NULL,
  `clo_chest` int(11) NOT NULL,
  `clo_lleg` int(11) NOT NULL,
  `clo_rleg` int(11) NOT NULL,
  `clo_feet` int(11) NOT NULL,
  `imp_head` int(11) NOT NULL,
  `imp_larm` int(11) NOT NULL,
  `imp_rarm` int(11) NOT NULL,
  `imp_lhand` int(11) NOT NULL,
  `imp_rhand` int(11) NOT NULL,
  `imp_chest` int(11) NOT NULL,
  `imp_lleg` int(11) NOT NULL,
  `imp_rleg` int(11) NOT NULL,
  `imp_feet` int(11) NOT NULL,
  `hp` int(11) NOT NULL,
  `charge` int(11) NOT NULL,
  `isInCombat` tinyint(1) NOT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tbl_Players`
--

INSERT INTO `tbl_Players` VALUES ('Player1','$rid=1$',1,0,6,4,8,7,5,5,6,1332,'200001,200001,200002','Password',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,100,0),('Player2','$rid=3$',1,0,6,4,8,7,5,5,6,1332,'200001,200001,200002,200001','Password',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,100,0),('Player3','$rid=2$',1,0,6,4,8,7,5,5,6,1332,'','Password',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,100,0);

--
-- All done
--
