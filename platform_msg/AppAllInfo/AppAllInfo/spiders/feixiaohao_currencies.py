# -*- coding:utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request    
from AppAllInfo.items import *
from AppAllInfo.settings import APP_NAME
import codecs  
class feixiaohao_currencies(scrapy.Spider):
    name = "feixiaohao_currencies_spider"
    allowed_domains = ["www.feixiaohao.com"]
    urls = [
        #"http://www.wandoujia.com/tag/视频",
        #"http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"

        "http://www.feixiaohao.com/currencies"
       # "https://www.feixiaohao.com/currencies/bitcoin/"
    ]
    urls.extend([ "http://www.feixiaohao.com/list_%d.html" % x for x in range(2,17) ])
    start_urls = urls
#rules = [Rule(LinkExtractor(allow=['/apps/.+']), 'parse')]
    def parse(self, response):
    	page = Selector(response)
    	for link in page.xpath("//a/@href"):
            href=link.extract()

            if href.startswith("/currencies/"):
            	yield Request("http://www.feixiaohao.com" +href, callback=self.parse_curr_page)





    def parse_curr_page(self, response):
        #for sel in response.xpath('//ul/li'):
         #   title = sel.xpath('a/text()').extract()
          #  link = sel.xpath('a/@href').extract()
           # desc = sel.xpath('text()').extract()
            #print title, link, desc
        item = FeiXiaoHaoItem()
        sel = Selector(response)
        name = sel.xpath('//*[@id="baseInfo"]/div[1]/div[1]/h1/node()').extract()[2].strip()
        chineseName = sel.xpath('//*[@id="baseInfo"]/div[1]/div[1]/h1/node()').extract()[-1].strip()
        engName = sel.xpath('//*[@id="baseInfo"]/div[2]/ul/li[1]/span[2]/text()').extract()[0]
        cnyPrice = sel.xpath('//*[@id="baseInfo"]/div[1]/div[1]/div[1]/text()').extract()[0]
        usdtPrice =  sel.xpath('//*[@id="baseInfo"]/div[1]/div[1]/div[3]/span[1]/text()').extract()[0].replace(u'\u2248', '')
        btcPrice =  sel.xpath('//*[@id="baseInfo"]/div[1]/div[1]/div[3]/span[2]/text()').extract()[0].replace(u'\u2248', '')
        upMarkets = sel.xpath('//*[@id="baseInfo"]/div[2]/ul/li[3]/span[2]/a/text()').extract()[0].strip().replace("家","")
        releaseTime = sel.xpath('//*[@id="baseInfo"]/div[2]/ul/li[4]/span[2]/text()').extract()[0]
        whitePaper = sel.xpath('//*[@id="baseInfo"]/div[2]/ul/li[5]/span[2]/a/@href').extract()[0]
        site = repr(sel.xpath('//*[@id="baseInfo"]/div[2]/ul/li[6]/span[2]/a/@href').extract())
        blockite =  repr(sel.xpath('//*[@id="baseInfo"]/div[2]/ul/li[7]/span[2]/a/@href').extract())
        concept = sel.xpath('//*[@id="baseInfo"]/div[2]/ul/li[8]/span[2]/a/text()').extract()[0]


        print name,chineseName
       
        item['name'] = name
        item['chineseName'] = chineseName
        item['engName'] = engName
        item['cnyPrice'] = cnyPrice
        item['usdtPrice'] = usdtPrice
        item['btcPrice'] = btcPrice
        item['upMarkets'] = upMarkets
        item['releaseTime'] = releaseTime
        item['whitePaper'] = whitePaper
        item['site'] =site
        item['blockite'] = blockite
        item['concept'] = "" #concept



        yield item
    def process_item(self,item):
    	return item and item[0].strip() or ""
    def process_name(self,item):
    	return item and item[1].strip() or ""