# -*- coding:utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request    
from AppAllInfo.items import *
from AppAllInfo.settings import APP_NAME
import codecs  
class bitfinex_news_spider(scrapy.Spider):
    name = "bittrex_news_spider"
    allowed_domains = ["support.bittrex.com"]
    urls = [
        #"http://www.wandoujia.com/tag/视频",
        #"http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"

        "https://support.bittrex.com/hc/en-us/sections/200142394-Announcements"
       # "https://www.feixiaohao.com/currencies/bitcoin/"
    ]
    #urls.extend([ "https://support.binance.com/hc/zh-cn/sections/115000106672?page=%d#articles" % x for x in range(2,4) ])
    start_urls = urls
#rules = [Rule(LinkExtractor(allow=['/apps/.+']), 'parse')]
    def parse(self, response):
    	page = Selector(response)
    	#for link in page.xpath("//a/@href"):
        #    href=link.extract()

        #    if href.startswith("/hc/en-us/articles/"):
        #        print "++++++++++++++++++++++",href
        #    	yield Request("https://support.bitfinex.com" +href, callback=self.parse_new_page)
        linklist = [link for link in  page.xpath("//a/@href") if link.extract().startswith("/hc/en-us/articles/")]
        href=linklist[0].extract()

            #if href.startswith("/hc/zh-cn/articles"):
        print "++++++++++++++++++++++",href
        yield Request("https://support.bittrex.com" +href, callback=self.parse_new_page)






    def parse_new_page(self, response):
        #for sel in response.xpath('//ul/li'):
         #   title = sel.xpath('a/text()').extract()
          #  link = sel.xpath('a/@href').extract()
           # desc = sel.xpath('text()').extract()
            #print title, link, desc
        item = BittrexNewsItem()
        sel = Selector(response)
        title = sel.css('''body > div.layout > main > div > div > div:nth-child(2) > div.column.column--sm-8 > article > header > h1''').extract()
        content = sel.css('''body > div.layout > main > div > div > div:nth-child(2) > div.column.column--sm-8 > article > div.article__body.markdown''').extract()



        print title,content

        item["url"] = response.url
        item['title'] = self.process_item(title)
        item['content'] = self.process_item(content)




        yield item
    def process_item(self,item):
    	return item and item[0].strip() or ""
    def process_name(self,item):
    	return item and item[1].strip() or ""
