# -*- coding:utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
from AppAllInfo.items import *
from AppAllInfo.settings import APP_NAME
import codecs
import datetime
class okex_spider(scrapy.Spider):
    name = "okex_spider"
    allowed_domains = ["support.okex.com"]
    urls = [
        #"http://www.wandoujia.com/tag/视频",
        #"http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"

        "https://support.okex.com/hc/zh-cn/sections/115000447632-%E5%85%AC%E5%91%8A%E4%B8%AD%E5%BF%83"
       # "https://www.feixiaohao.com/currencies/bitcoin/"
    ]
    #urls.extend([ "https://support.okex.com/hc/zh-cn/sections/115000447632-%E5%85%AC%E5%91%8A%E4%B8%AD%E5%BF%83?page={0}#articles".format(x) for x in range(2,5) ])
    start_urls = urls
#rules = [Rule(LinkExtractor(allow=['/apps/.+']), 'parse')]
    def parse(self, response):
    	page = Selector(response)
    	#for link in page.xpath("//a/@href"):
        #    href=link.extract()

        #    if href.startswith("/hc/zh-cn/articles"):
        #        print "++++++++++++++++++++++",href
        #    	yield Request("https://support.okex.com" +href, callback=self.parse_new_page)
        linklist = [link for link in  page.xpath("//a/@href") if link.extract().startswith("/hc/zh-cn/articles")]
        href=linklist[0].extract()

            #if href.startswith("/hc/zh-cn/articles"):
        print "++++++++++++++++++++++",href
        yield Request("https://support.okex.com" +href, callback=self.parse_new_page)






    def parse_new_page(self, response):
        #for sel in response.xpath('//ul/li'):
         #   title = sel.xpath('a/text()').extract()
          #  link = sel.xpath('a/@href').extract()
           # desc = sel.xpath('text()').extract()
            #print title, link, desc
        item = OkexItem()
        sel = Selector(response)
       
        title =  sel.css("#article-container > article > header > h1").extract()#sel.xpath('//*[@id="article-container"]/article/header/h1/@title').extract()[0].strip()

        #upDate = sel.css("#article-container > article > section.article-info > div > div.article-body > p:nth-child(9)")#sel.xpath('//*[@id="article-container"]/article/section[1]/div/div[1]/p[3]/text()[4]').extract()[0]
        content_raw = sel.css("#article-container > article > section.article-info > div > div.article-body").extract()




        print title,content_raw
        item["url"] = response.url
        item['title'] = title
        item['content'] = content_raw




        yield item
    def process_item(self,item):
    	return item and item[0].strip() or ""
    def process_name(self,item):
    	return item and item[1].strip() or ""
