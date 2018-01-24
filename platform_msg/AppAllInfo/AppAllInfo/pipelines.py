# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import pymongo
from AppAllInfo import settings
from scrapy import log
#from scrapy.exceptions import DropItem
#from pybloomfilter import BloomFilter
from scrapy import signals
import json
import codecs
from twisted.enterprise import adbapi
from datetime import datetime
from hashlib import md5
import MySQLdb
import MySQLdb.cursors

import dataset
class AppAllInfoFilePipeline(object):
  def __init__(self):  
      #self.bf = BloomFilter(10000000, 0.01, 'filter.bloom')
      self.file = codecs.open( "test.json", mode='w', encoding='utf-8')
  
  def process_item(self, item, spider):

        line = json.dumps(dict(item), ensure_ascii=False) + "\n"  
        self.file.write(line)
      
  	    #return item  
  def spider_closed(self, spider):  
        self.file.close()



class AppAllInfoMongoPipeline(object):
  def __init__(self):  
        connection = pymongo.MongoClient(
            settings.MONGODB_SERVER,
            settings.MONGODB_PORT
        )
        db = connection[settings.MONGODB_DB]
        self.collection = db[settings.MONGODB_COLLECTION]
  
  def process_item(self, item, spider):  
        for data in item:
            if not data:
                raise DropItem("Missing data!")
        self.collection.update({'url': item['url']}, dict(item), upsert=True)
        log.msg("Question added to MongoDB database!",
                level=log.DEBUG, spider=spider)
        return item
      
  	    #return item  
  def spider_closed(self, spider):  
        self.file.close()


class MysqlPipeline(object):
    '''保存到数据库中对应的class
       1、在settings.py文件中配置
       2、在自己实现的爬虫类中yield item,会自动执行'''    

    def __init__(self,dbpool):
        self.dbpool=dbpool
        ''' 这里注释中采用写死在代码中的方式连接线程池，可以从settings配置文件中读取，更加灵活
            self.dbpool=adbapi.ConnectionPool('MySQLdb',
                                          host='127.0.0.1',
                                          db='crawlpicturesdb',
                                          user='root',
                                          passwd='123456',
                                          cursorclass=MySQLdb.cursors.DictCursor,
                                          charset='utf8',
                                          use_unicode=False)'''     
        self.db = dataset.connect('mysql://root:123456@localhost/coinbase?charset=utf8' ,engine_kwargs={ "encoding":'utf8'})   
        
    @classmethod
    def from_settings(cls,settings):
        '''1、@classmethod声明一个类方法，而对于平常我们见到的则叫做实例方法。 
           2、类方法的第一个参数cls（class的缩写，指这个类本身），而实例方法的第一个参数是self，表示该类的一个实例
           3、可以通过类来调用，就像C.f()，相当于java中的静态方法'''
        dbparams=dict(
            host=settings['DB_HOST'],#读取settings中的配置
            db=settings['DB_DBNAME'],
            user=settings['DB_USER'],
            passwd=settings['DB_PASSWD'],
            charset='utf8',#编码要加上，否则可能出现中文乱码问题
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=False,
        )
        dbpool=adbapi.ConnectionPool('MySQLdb',**dbparams)#**表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        return cls(dbpool)#相当于dbpool付给了这个类，self中可以得到

    #pipeline默认调用
    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._do_upinsert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        d.addBoth(lambda _: item)
        #db = dataset.connect('mysql://root:123456@localhost/database' ,engine_kwargs={ "encoding":'utf8'})
        #table = self.db[spider.name]
        #if type(item['url'])  == list:
         #   item['url'] = ''.join(item['url'])
        #item["urlmd5id"] = self._get_urlmd5id(item)
        #table.upsert(dict(item),["urlmd5id"])
        return d
    
    #写入数据库中
    def _conditional_insert(self,tx,item):
        #print "item======================= " , item[u'field1']
        sql="insert into test values(1,1,1)"
        #params=(item["name"],item["url"])
        #tx.execute(sql,params)
        tx.execute(sql)
        pass

    def _do_upinsert(self, conn, item, spider):
        urlmd5id = self._get_urlmd5id(item)
        now = datetime.utcnow().replace(microsecond=0).isoformat(' ')

        item["urlmd5id"] = urlmd5id
        item["updated"] = now       
        table = self.db[spider.name]
        if not  table.exists:
            table.upsert(item, ["urlmd5id(100)"])


        conn.execute("select 1 from  "+spider.name+" where urlmd5id = %s", (urlmd5id,))
        #print "error"
        ret = conn.fetchone()
        #ret = None
        if ret is not None:
            itemtmp =[x  for x in item.keys() if x != "urlmd5id" and x != "updated" ]
            itemkeys = ",".join([x+"=%s" for x in itemtmp])
            sql = "update "+ spider.name + " set " + itemkeys + ",updated = %s  where urlmd5id = %s"
            itemvalues = tuple([eval("item['%s']" % x) for x in itemtmp] + [now, urlmd5id])
            print "update sql:", sql
            print "itemvallues:",itemvalues
            conn.execute(sql , itemvalues)
        else:
            itemtmp =[x for x in item.keys() if x != "urlmd5id" and x != "updated" ]
            itemkeys = ",".join([x for x in itemtmp])+",updated,urlmd5id"
            valueshold = ",".join(['%s' for x in itemtmp])+",%s,%s"
            sql = "insert into " + spider.name + " (" + itemkeys + ") values(" + valueshold + ")"
            print "insert sql:",sql
            #print "itemvallues:",itemvalues
            itemvalues = tuple([eval("item['%s']" % x) for x in itemtmp] + [now,urlmd5id]) 
            print "itemvallues:",itemvalues
            conn.execute(sql, itemvalues)
            
    
    #错误处理方法
    def _handle_error(self, failue, item, spider):
        print '--------------database operation exception!!-----------------'
        print '-------------------------------------------------------------'
        print failue
    def _get_urlmd5id(self, item):
        #url进行md5处理，为避免重复采集设计
        return md5(item['url']).hexdigest()

