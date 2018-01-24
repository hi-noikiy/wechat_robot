# -*- coding:utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request    

from AppAllInfo.items import *
from AppAllInfo.settings import APP_NAME
import codecs  
class bishijie_spider(scrapy.Spider):
    name = "bishijie_spider"
    allowed_domains = ["http://m.bishijie.com"]
    urls = [
        #"http://www.wandoujia.com/tag/视频",
        #"http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"

        "http://m.bishijie.com/kuaixun"
       # "https://www.feixiaohao.com/currencies/bitcoin/"
    ]
    #urls.extend([ "https://support.okex.com/hc/zh-cn/sections/115000447632-%E5%85%AC%E5%91%8A%E4%B8%AD%E5%BF%83?page={0}#articles".format(x) for x in range(2,4) ])
    start_urls = urls
#rules = [Rule(LinkExtractor(allow=['/apps/.+']), 'parse')]






    def parse(self, response):
        #for sel in response.xpath('//ul/li'):
         #   title = sel.xpath('a/text()').extract()
          #  link = sel.xpath('a/@href').extract()
           # desc = sel.xpath('text()').extract()
            #print title, link, desc
        item = BiShiJieItem()
        sel = Selector(response)
        content_today =  sel.xpath('//*[@id="kuaixun_list"]').extract()

        #content_yestoday = sel.css("#kuaixun_list > div:nth-child(2)").extract()




        print content_today

        item["url"] = response.url
        item['content_today'] = content_today
        #item['content_yestoday'] = content_yestoday





        yield item
    def process_item(self,item):
    	return item and item[0].strip() or ""
    def process_name(self,item):
    	return item and item[1].strip() or ""