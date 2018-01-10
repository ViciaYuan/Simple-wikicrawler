# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
#import json
import pymysql
from scrapy.conf import settings
#i = 0

class FilePipeline(object):
    #def __init__(self):
        #self.filename = open("entries.json","w")


    def process_item(self, item, spider):
        '''global i
        i = i + 1
        jsontext = json.dumps(dict(item), ensure_ascii=False) + ",\n" 
        self.filename.write(jsontext)'''
        
        host = settings['MYSQL_HOSTS']  
        user = settings['MYSQL_USER']  
        psd = settings['MYSQL_PASSWORD']  
        db = settings['MYSQL_DB']  
        c = settings['CHARSET']  
        port = settings['MYSQL_PORT']  
        
        #数据库连接  
        con = pymysql.connect(host=host,user=user,passwd=psd,db=db,charset=c,port=port)   
        #操作的游标
        cue = con.cursor()  
        
        print("!!!mysql connect success")
  
        try:    
            cue.execute("insert into wiki_1 (url,names,summary,info,content,uptime,refer,label) values (%s,%s,%s,%s,%s,%s,%s,%s)",
                [ item["url"], item["name"], item["summary"], item["info"], item["content"], item["uptime"], item["refer"], item["label"] ])   
            print("!!!insert success")#测试语句
            #mysql insert error1064原因之一是表的列名是reserved words，比如name，所以表里改用names
   
        except Exception as e:  
            print('Insert error:',e)  
            con.rollback()  
        else:  
            con.commit()  
        
        con.close()         
        return item


'''    def close_spider(self, spider):
        global i
        self.filename.write("\n共" + str(i) + "字条")
        self.filename.close()'''
