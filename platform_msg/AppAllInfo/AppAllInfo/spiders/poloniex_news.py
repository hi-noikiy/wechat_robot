# -*- coding:utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request    
from AppAllInfo.items import *
from AppAllInfo.settings import APP_NAME
import codecs  
class poloniex_news_spider(scrapy.Spider):
    name = "poloniex_news_spider"
    allowed_domains = ["www.zb.com"]
    urls = [
        #"http://www.wandoujia.com/tag/视频",
        #"http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"

        "https://www.zb.com/i/blog?type=livenews"
       # "https://www.feixiaohao.com/currencies/bitcoin/"
    ]
    #urls.extend([ "https://support.binance.com/hc/zh-cn/sections/115000106672?page=%d#articles" % x for x in range(2,4) ])
    start_urls = urls
#rules = [Rule(LinkExtractor(allow=['/apps/.+']), 'parse')]
    def parse(self, response):
    	page = Selector(response)
    	for link in page.xpath("//a/@href"):
            href=link.extract()

            if href.startswith("/i/blog"):
                print "++++++++++++++++++++++",href
            	yield Request("https://www.zb.com" +href, callback=self.parse_new_page)





    def parse_new_page(self, response):
        #for sel in response.xpath('//ul/li'):
         #   title = sel.xpath('a/text()').extract()
          #  link = sel.xpath('a/@href').extract()
           # desc = sel.xpath('text()').extract()
            #print title, link, desc
        item = ZBNewsItem()
        sel = Selector(response)
        title = sel.css("body > div.ch-body > div.envor-content > section.envor-section > div > div > div.col-lg-9.col-md-9.col-lg-pulla-3.col-md-pulla-3.page-right > h2").extract()
        content = sel.css('''body > section.container > div.container-group4.pt65.clearfix.bg-color-F9F9F9 > div > div > main > div > div.bd.p30 > div.news-article.lh-16em.color-666666.ls-10.fs-14''').extract()



        print title,content

        item["url"] = response.url
        item['title'] = self.process_item(title)
        item['content'] = self.process_item(content)




        yield item
    def process_item(self,item):
    	return item and item[0].strip() or ""
    def process_name(self,item):
    	return item and item[1].strip() or ""
