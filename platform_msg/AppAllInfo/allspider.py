import scrapy
from scrapy.crawler import CrawlerProcess

from AppAllInfo.spiders import binance_spider
process = CrawlerProcess()
platform_dict = {"binance":"binance_spider","okex":"okex_spider","zb":"zb_notices_spider","bigone":"bigone_spider","bitfinex":"bitfinex_news_spider",
                     "coinegg":"coinegg_news_spider","huobi":"huobi_spider","btctrade":"btctrade_news_spider","cex":"cex_notices_spider",
                     "bcex":"bcex_news_spider","coolcoin":"coolcoin_news_spider"}

for spider in platform_dict.values():
    print " scrapy crawl "+spider   
#process.start() 
