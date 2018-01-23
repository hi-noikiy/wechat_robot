#coding=utf-8
# author = 'xuxin'

import itchat
from itchat.content import *
import ccxt
import datetime
import time
import traceback
from ccxt.base.errors import ExchangeError,ExchangeNotAvailable,RequestTimeout
from operate_mysql import OperateMysql
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import traceback

RETRY_NUM = 3   #查询货币信息重试次数

# itchat.auto_login(hotReload=True)
white_list = [u'bicom独立纵队']

class SymbolInfo():
    def __init__(self):
        self.retry = 0
        self.send_msg = ''

    def save_exchanges(self):
        exchanges_list = ccxt.exchanges
        # p = OperateMysql()
        # p.get_connect()
        # p.save_exchanges(exchanges_list)
        # p.close_connect()
        return exchanges_list

    def disable_exchanges(self, disable_exchanges):
        p = OperateMysql()
        p.get_connect()
        p.disable_exchanges(disable_exchanges)
        p.close_connect()

    def save_markets(self, exchanges):
        ''''
        '''
        flag = True  #判断执行是否成功
        try:
            ex_object = eval("ccxt.%s"%exchanges)()
            markets = ex_object.fetch_markets()
            p = OperateMysql()
            p.get_connect()
            p.save_markets(exchanges,markets)
            p.close_connect()
        except Exception,e:
            # print traceback.format_exc()
            print exchanges,e.message
            flag = False
        finally:
            return flag

    def get_symbol_info(self, exchanges, symbol):
        '''
        :param exchanges:交易所名称
        :param symbol:币名称
        :param retry:重试次数
        :return:
        '''
        try:
            ex_object = eval('ccxt.%s'%exchanges)()
            print ex_object.fetch_markets()
            result = ex_object.fetch_ticker(symbol)
            print result
            self.format_info(exchanges, symbol, result)
        except ExchangeError, e:
            self.send_msg = u"{0} 未发现: {1}".format(exchanges, symbol)
            print self.send_msg
        except ExchangeNotAvailable, e:
            self.send_msg = '服务器忙,请重试!'
            print self.send_msg
            if self.retry < RETRY_NUM:
                self.retry += 1
                self.get_symbol_info(exchanges, symbol)
        except RequestTimeout, e:
            self.send_msg = '查询超时，请重试!'
            print self.send_msg
            if self.retry < RETRY_NUM:
                self.retry += 1
                self.get_symbol_info(exchanges, symbol)
        except Exception, e:
            print traceback.format_exc()
            self.send_msg = '查询失败，请重试!'
            print self.send_msg
            if self.retry < RETRY_NUM:
                self.retry += 1
                self.get_symbol_info(exchanges, symbol)

    def format_info(self, exchanges, symbol, result):
        print '-----------------------'
        print exchanges,symbol,result
        print '=========================='
        current_price = result['last'] or result['close']  #最新价格
        change = result['change']  #涨幅
        high24hr = result['high']    #24小时最高价格
        low24hr = result['low']   #24小时最低价格
        quoto_volume = result['baseVolume']   #24小时成交量
        if quoto_volume > 10000:
            quoto_volume = u"{0:.2f}万".format(quoto_volume / 10000)
        url = 'https://gate.io/'
        time1 = datetime.datetime.strptime(result['datetime'], '%Y-%m-%dT%H:%M:%S.%fZ')
        timenow = (time1 + datetime.timedelta(hours=8))
        timestr = timenow.strftime('%Y-%m-%d %H:%M:%S')
        if exchanges == 'huobipro':
            pass
        self.send_msg = u"{8} {0}\n当前价格: {1} \n涨幅: {2:.2f}%\n24H最高价: {3} \n24H最低价: {4} \n" \
                        u"24H成交量: {5}\n更多详细信息: {6}\n[{7}]".format(symbol, current_price, change, high24hr, low24hr,
                                                                  quoto_volume, url, timestr,exchanges)

    def get_huobi_info(self, symbol):
        huobi = ccxt.huobi()
        print huobi.fetch_markets()
        print 'line 80'
        # print huobi.fetch_tickers()
        print 'line 83'
        result = huobi.fetch_ticker(symbol)
        print result

@itchat.msg_register(TEXT, isGroupChat=True)
# @itchat.msg_register(TEXT)
def run(msg):
    text = msg['Text']
    chatroom_name = msg.User.NickName
    if chatroom_name in white_list and text.encode('utf-8').isalpha() and len(text) > 0 and len(text) < 10:
        p = OperateMysql()
        p.get_connect()
        symbol_list = p.get_symbol_exchanges(text)
        p.close_connect()
        s = SymbolInfo()
        send_msg = []
        for i in symbol_list:
            s.get_symbol_info(i['exchanges'],i['symbol'])
            send_msg.append(s.send_msg)
        if send_msg:
            return "\n-----------------------------\n".join(send_msg)

def init_data():
    '''
    初始化数据
    :return:
    '''
    p = SymbolInfo()
    exchanges_list = p.save_exchanges()
    disable_exchanges = []
    for exchanges in exchanges_list:
        flag = p.save_markets(exchanges)
        if not flag:
            disable_exchanges.append(exchanges)
    p.disable_exchanges(disable_exchanges)

def test():
    text = 'doge'
    p = OperateMysql()
    p.get_connect()
    symbol_list = p.get_symbol_exchanges(text)
    p.close_connect()
    s = SymbolInfo()
    send_msg = []
    for i in symbol_list:
        s.get_symbol_info(i['exchanges'], i['symbol'])
        send_msg.append(s.send_msg)
    if send_msg:
        print  "\n-----------------------------\n".join(send_msg)

if __name__ == '__main__':
    # init_data()
    # itchat.run()
    test()



