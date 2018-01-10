# Simple-wikicrawler
A simple crawler which is used to attain wiki entries.

20180110  update: 添加Mysql存数据

环境： python3.6, mysql-5.7.20

python操作数据库的模块： pymysql最新

数据库名：testdb

建表的语句：
``` 
CREATE TABLE wiki_1(
url VARCHAR(2000) NOT NULL,
names VARCHAR(2000),
summary VARCHAR(2000),
info VARCHAR(2000),
content VARCHAR(2000),
uptime VARCHAR(2000),
refer VARCHAR(2000),
label VARCHAR(2000),
PRIMARY KEY (url)
);
``` 

报错：
``` 
2018-01-10 21:47:33 [scrapy.core.scraper] DEBUG: Scraped from <200 https://en.wikipedia.org/wiki/Aechmea_%27Black_Jack%27>
{'content': {},
 'info': '',
 'label': ['Bromeliaceae cultivar', 'Aechmea stubs'],
 'name': "Aechmea 'Black Jack'",
 'refer': [],
 'summary': [],
 'uptime': '25 May 2015,23:48',
 'url': 'https://en.wikipedia.org/wiki/Aechmea_%27Black_Jack%27'}
[]
!!!mysql connect success
Insert error: (1064, "You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '),'',{},'25 May 2015,23:48',(),('Bromeliaceae cultivar','Aechmea stubs'))' at line 1")
``` 
关于mysql insert error 1064 [这篇文章](https://www.inmotionhosting.com/support/website/database-troubleshooting/error-1064)讲得很清楚....但是我还是没有改出来....

