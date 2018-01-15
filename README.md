# Simple-wikicrawler
Use Scrapy to crawl wikipedia entries, and store the items in MySQL

环境： Miniconda3, python3.6, mysql-5.7.20

框架、模块： Scrapy1.5, pymysql

数据库操作

use wiki_entries

建表
``` 
CREATE TABLE `wiki_EN` (
  `sequence` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `url` varchar(80) NOT NULL DEFAULT '',
  `names` varchar(100) NOT NULL DEFAULT '',
  `summary` text,
  `info` text,
  `content` text,
  `uptime` varchar(30) NOT NULL DEFAULT '',
  `refer` text,
  `label` varchar(500) DEFAULT '',
  PRIMARY KEY (`sequence`)
) ENGINE=InnoDB AUTO_INCREMENT=10660 DEFAULT CHARSET=utf8;
``` 
wiki_EN为英文维基百科， wiki_ZH为中文维基百科

两张表分别存储对应网站的爬虫结果



