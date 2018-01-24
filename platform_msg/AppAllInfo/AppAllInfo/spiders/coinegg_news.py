# -*- coding:utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request    
from AppAllInfo.items import *
from AppAllInfo.settings import APP_NAME
import codecs  
import re
class coinegg_news_spider(scrapy.Spider):
    name = "coinegg_news_spider"
    allowed_domains = ["www.coinegg.com"]
    urls = [
        #"http://www.wandoujia.com/tag/视频",
        #"http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"

        "https://www.coinegg.com/gonggao/?lang=zh_CN"
       # "https://www.feixiaohao.com/currencies/bitcoin/"
    ]
    #urls.extend([ "https://support.binance.com/hc/zh-cn/sections/115000106672?page=%d#articles" % x for x in range(2,4) ])
    start_urls = urls
#rules = [Rule(LinkExtractor(allow=['/apps/.+']), 'parse')]
    def parse(self, response):
    	page = Selector(response)
        #for link in page.xpath("//a/@href"):
        #    href=link.extract()

        #    if href.startswith("/gonggao"):
        #        print "++++++++++++++++++++++",href
        #        yield Request("https://www.coinegg.com" +href, callback=self.parse_new_page)
        linklist = [link for link in  page.xpath("//a/@href") if re.compile(r"/gonggao/[0-9]+\.html").findall(link.extract())]
        href=linklist[0].extract()

            #if href.startswith("/hc/zh-cn/articles"):
        print "++++++++++++++++++++++",href
        yield Request("https://www.coinegg.com" +href, callback=self.parse_new_page)







    def parse_new_page(self, response):
        #for sel in response.xpath('//ul/li'):
         #   title = sel.xpath('a/text()').extract()
          #  link = sel.xpath('a/@href').extract()
           # desc = sel.xpath('text()').extract()
            #print title, link, desc
        sel = Selector(response)
        item = CoineggNewsItem()
        title = sel.css("body > div.body > div.right.gonggao > p.p1").extract()
        content = sel.css('''body > div.body > div.right.gonggao > div.gonggao-con''').extract()



        print title,content

        item["url"] = response.url
        item['title'] = self.process_item(title)
        item['content'] = self.process_item(content)




        yield item
    def process_item(self,item):
    	return item and item[0].strip() or ""
    def process_name(self,item):
    	return item and item[1].strip() or ""
