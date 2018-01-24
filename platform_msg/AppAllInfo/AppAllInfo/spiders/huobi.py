# -*- coding:utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
from AppAllInfo.items import *
from AppAllInfo.settings import APP_NAME
import codecs  
class huobi_pider(scrapy.Spider):
    name = "huobi_spider"
    allowed_domains = ["www.huobi.com"]
    urls = [
        #"http://www.wandoujia.com/tag/视频",
        #"http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"

        "https://www.huobi.com/p/content/notice"
       # "https://www.feixiaohao.com/currencies/bitcoin/"
    ]
    #urls.extend([ "https://www.huobi.com/p/content/notice?page=%d" % x for x in range(2,25) ])
    start_urls = urls
#rules = [Rule(LinkExtractor(allow=['/apps/.+']), 'parse')]
    def parse(self, response):
    	page = Selector(response)
    	#for link in page.xpath("//a/@href"):
        #    href=link.extract()

        #    if href.startswith("/p/content/notice/getNotice"):
        #        print "++++++++++++++++++++++",href
        #    	yield Request("https://www.huobi.com" +href, callback=self.parse_new_page)
        linklist = [link for link in  page.xpath("//a/@href") if link.extract().startswith("/p/content/notice/getNotice")]
        href=linklist[0].extract()

            #if href.startswith("/hc/zh-cn/articles"):
        print "++++++++++++++++++++++",href
        yield Request("https://www.huobi.com" +href, callback=self.parse_new_page)





    def parse_new_page(self, response):
        #for sel in response.xpath('//ul/li'):
         #   title = sel.xpath('a/text()').extract()
          #  link = sel.xpath('a/@href').extract()
           # desc = sel.xpath('text()').extract()
            #print title, link, desc
        item = HuobiItem()
        sel = Selector(response)
        title =  sel.css('#doc_body > div > div > div.main_wrap > ul > li > div > h1').extract() #sel.xpath('//*[@id="doc_body"]/div/div/div[2]/ul/li/div/h1/text()').extract()[0].strip()
        content =  sel.css('#doc_body > div > div > div.main_wrap > ul').extract()
        print title

        item["url"] =  response.url
        item['title'] = self.process_item(title)
        item['content'] = self.process_item(content)




        yield item
    def process_item(self,item):
    	return item and item[0].strip() or ""
    def process_name(self,item):
    	return item and item[1].strip() or ""
