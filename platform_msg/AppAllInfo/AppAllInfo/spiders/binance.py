# -*- coding:utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request    
from AppAllInfo.items import *
from AppAllInfo.settings import APP_NAME
import codecs  
class binance_pider(scrapy.Spider):
    name = "binance_spider"
    allowed_domains = ["support.binance.com"]
    urls = [
        #"http://www.wandoujia.com/tag/视频",
        #"http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"

        "https://support.binance.com/hc/zh-cn/sections/115000106672-%E6%96%B0%E5%B8%81%E4%B8%8A%E7%BA%BF"
       # "https://www.feixiaohao.com/currencies/bitcoin/"
    ]
    #urls.extend([ "https://support.binance.com/hc/zh-cn/sections/115000106672?page=%d#articles" % x for x in range(2,4) ])
    start_urls = urls
#rules = [Rule(LinkExtractor(allow=['/apps/.+']), 'parse')]
    def parse(self, response):
    	page = Selector(response)
    	linklist = [link for link in  page.xpath("//a/@href") if link.extract().startswith("/hc/zh-cn/articles")]
        href=linklist[0].extract()

            #if href.startswith("/hc/zh-cn/articles"):
        print "++++++++++++++++++++++",href
        yield Request("https://support.binance.com" +href, callback=self.parse_new_page)





    def parse_new_page(self, response):
        #for sel in response.xpath('//ul/li'):
         #   title = sel.xpath('a/text()').extract()
          #  link = sel.xpath('a/@href').extract()
           # desc = sel.xpath('text()').extract()
            #print title, link, desc
        item = BinanceNewItem()
        sel = Selector(response)
        title = sel.css("#article-container > article > header > h1").extract()
        content = sel.css("#article-container > article > section.article-info > div > div.article-body").extract()



        print title,content

        item["url"] = response.url
        item['title'] = self.process_item(title)
        item['content'] = self.process_item(content)




        yield item
    def process_item(self,item):
    	return item and item[0].strip() or ""
    def process_name(self,item):
    	return item and item[1].strip() or ""
