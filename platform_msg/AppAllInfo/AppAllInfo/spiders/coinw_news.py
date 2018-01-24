# -*- coding:utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request    
from AppAllInfo.items import *
from AppAllInfo.settings import APP_NAME
import codecs  
class coinw_news_spider(scrapy.Spider):
    name = "coinw_news_spider"
    allowed_domains = ["www.coinw.com"]
    urls = [
        #"http://www.wandoujia.com/tag/视频",
        #"http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"

        "https://www.coinw.com/newService/ourService.html?id=1"
       # "https://www.feixiaohao.com/currencies/bitcoin/"
    ]
    #urls.extend([ "https://support.binance.com/hc/zh-cn/sections/115000106672?page=%d#articles" % x for x in range(2,4) ])
    start_urls = urls
#rules = [Rule(LinkExtractor(allow=['/apps/.+']), 'parse')]
    def parse(self, response):
    	page = Selector(response)
        item = CoinwNewsItem()
    	for link,title in zip(page.xpath('''//a[contains(@href, "/newService")]/@href'''),page.xpath('''//a[contains(@href, "/newService")]/text()''')):
            
            href=link.extract()
            title_text = title.extract()
            
            print "++++++++++++++++++++++",href
            print "++++++++++++++++++++",title_text
            item['title'] = title_text
            request = Request("https://www.coinw.com" +href, callback=self.parse_new_page)
            request.meta['item'] = item
            yield request





    def parse_new_page(self, response):
        #for sel in response.xpath('//ul/li'):
         #   title = sel.xpath('a/text()').extract()
          #  link = sel.xpath('a/@href').extract()
           # desc = sel.xpath('text()').extract()
            #print title, link, desc
        sel = Selector(response)
        item = response.meta['item']
        #title = sel.xpath("/html/body/section[2]/div[2]/div/div/main/div/div[2]/div[1]/h3/text()").extract()
        content = sel.css('''body > section.container > div.container-group4.pt65.clearfix.bg-color-F9F9F9 > div > div > main > div > div.bd.p30 > div.news-article.lh-16em.color-666666.ls-10.fs-14''').extract()



        print item['title'],content

        item["url"] = response.url
        #item['title'] = self.process_item(title)
        item['content'] = self.process_item(content)




        yield item
    def process_item(self,item):
    	return item and item[0].strip() or ""
    def process_name(self,item):
    	return item and item[1].strip() or ""
