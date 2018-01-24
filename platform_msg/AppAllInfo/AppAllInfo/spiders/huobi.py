# -*- coding:utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
from AppAllInfo.items import *
from AppAllInfo.settings import APP_NAME
import codecs  
import json
class huobi_spider(scrapy.Spider):
    name = "huobi_spider"
    allowed_domains = ["www.huobi.pro"]
    urls = [
        #"http://www.wandoujia.com/tag/视频",
        #"http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"

        "https://www.huobi.com/p/api/contents/pro/list_notice?r=ha95rykjf1bctben7undygb9&limit=10&language=zh-cn"
       # "https://www.feixiaohao.com/currencies/bitcoin/"
    ]
    #urls.extend([ "https://www.huobi.com/p/content/notice?page=%d" % x for x in range(2,25) ])
    start_urls = urls
#rules = [Rule(LinkExtractor(allow=['/apps/.+']), 'parse')]
    def parse(self, response):
    	#page = Selector(response)
        noticelist = json.loads(response.body_as_unicode())
    	#for link in page.xpath("//a/@href"):
        #    href=link.extract()

        #    if href.startswith("/p/content/notice/getNotice"):
        #        print "++++++++++++++++++++++",href
        #    	yield Request("https://www.huobi.com" +href, callback=self.parse_new_page)
        #linklist = [link for link in  page.css("#notice > ul > li:nth-child(2) > a") if link.extract().startswith("/zh-cn/notice_detail/")]
       # href=linklist[0].extract()
        noticeid = noticelist["data"]["items"][0]["id"]

            #if href.startswith("/hc/zh-cn/articles"):
        #print "++++++++++++++++++++++",href
        #yield Request("https://www.huobi.pro/zh-cn/notice_detail/?id=" +str(noticeid), callback=self.parse_new_page)
        item = HuobiItem()
        sel = Selector(response)
        title =  noticelist["data"]["items"][0]["title"] #asel.xpath('//*[@id="doc_body"]/div/div/div[2]/ul/li/div/h1/text()').extract()[0].strip()
        content =  noticelist["data"]["items"][0]["content"]
        print title

        item["url"] = "https://www.huobi.pro/zh-cn/notice_detail/?id=" +str(noticeid)
        item['title'] = title
        item['content'] = content




        yield item





    def parse_new_page(self, response):
        #for sel in response.xpath('//ul/li'):
         #   title = sel.xpath('a/text()').extract()
          #  link = sel.xpath('a/@href').extract()
           # desc = sel.xpath('text()').extract()
            #print title, link, desc
        item = HuobiItem()
        sel = Selector(response)
        title =  sel.css('#notice_title').extract() #sel.xpath('//*[@id="doc_body"]/div/div/div[2]/ul/li/div/h1/text()').extract()[0].strip()
        content =  sel.css('#notice_content').extract()
        print title

        item["url"] =  response.url
        item['title'] = self.process_item(title)
        item['content'] = self.process_item(content)




        yield item
    def process_item(self,item):
    	return item and item[0].strip() or ""
    def process_name(self,item):
    	return item and item[1].strip() or ""
