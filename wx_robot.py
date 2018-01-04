#coding=utf-8
# author = 'xuxin'

import itchat
from itchat.content import *
import ccxt
import datetime
import time
import traceback
from ccxt.base.errors import ExchangeError,ExchangeNotAvailable,RequestTimeout
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
print sys.getdefaultencoding()
itchat.auto_login(hotReload=True)

white_list = [u'币发群001']


@itchat.msg_register(TEXT, isGroupChat=True)
# @itchat.msg_register(TEXT)
def text_reply(msg):
    # print msg['Text']
    # print msg['ToUserName']
    # print msg['FromUserName']
    #print chardet.detect(text)
    text = msg['Text']
    chatroom_name = msg.User.NickName
    if chatroom_name in white_list and text.encode('utf-8').isalpha() and len(text)> 0 and len(text) <10:
        text = '{0}/USDT'.format(text.upper())
        try:
            gateio = ccxt.gateio()
            result = gateio.fetch_ticker(text)
            current_price = result['last']
            change = result['change']
            high24hr = result['high']
            low24hr = result['low']
            quoto_volume  = result['baseVolume']
            if quoto_volume > 10000:
                quoto_volume = u"{0:.2f}万".format(quoto_volume/10000)
                print quoto_volume
            url = 'https://gate.io/'
            time1 = datetime.datetime.strptime(result['datetime'], '%Y-%m-%dT%H:%M:%S.%fZ')
            timenow = (time1 + datetime.timedelta(hours=8))
            timestr = timenow.strftime('%Y-%m-%d %H:%M:%S')
            send_msg = u"gateio {0}\n当前价格: {1} 美元\n涨幅: {2:.2f}%\n24H最高价: {3}美元\n24H最低价: {4}美元\n" \
                       u"24H成交量: {5}\n更多详细信息: {6}\n[{7}]".format(text,current_price,change,high24hr,low24hr,
                                                                  quoto_volume,url,timestr)
            # print msg['FromUserName']
            print send_msg
            return send_msg
        except ExchangeError,e:
            return u"gateio 未发现: {0}".format(text)
        except ExchangeNotAvailable,e:
            print e.message
            return '服务器忙,请重试!'
        except RequestTimeout,e:
            return '查询超时，请重试!'
        except Exception,e:
            print traceback.format_exc()
            return '查询失败，请重试!'

itchat.run()