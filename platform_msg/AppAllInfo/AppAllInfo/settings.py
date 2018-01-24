# -*- coding: utf-8 -*-

# Scrapy settings for scrapy_project project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'AppAllInfo'
APP_NAME = u'appname'

SPIDER_MODULES = ['AppAllInfo.spiders']
NEWSPIDER_MODULE = 'AppAllInfo.spiders'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scrapy_project (+http://www.yourdomain.com)'
DOWNLOAD_DELAY = 2
RANDOMIZE_DOWNLOAD_DELAY = True
USER_AGENT = 'Opera/9.80 (X11; U; Linux i686; en-US; rv:1.9.2.3) Presto/2.2.15 Version/10.10'
COOKIES_ENABLED = False

# 广度优先搜索
SCHEDULER_ORDER = 'BFO'
CONCURRENT_REQUESTS_PER_SPIDER = 50
DEPTH_PRIORITY = 0
DEPTH_LIMIT = 5 #设置爬虫深度


MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "appinfo"
MONGODB_COLLECTION = "anzhi"

DB_HOST = '10.0.0.85'
DB_DBNAME = 'wechat_robot'
DB_USER = 'root'
DB_PASSWD = 'root'

ITEM_PIPELINES = {  
   #'AppAllInfo.pipelines.AppAllInfoFilePipeline':300
     # 'AppAllInfo.pipelines.AppAllInfoMongoPipeline':300
     #'AppAllInfo.pipelines.MySQLStorePipeline':300
   'AppAllInfo.pipelines.MysqlPipeline':300
}  
