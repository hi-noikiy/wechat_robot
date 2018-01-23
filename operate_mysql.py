#coding=utf-8

import datetime
from mysql import connector
import ConfigParser

class OperateMysql():
    def __init__(self):
        self.conn = None
        self.cursor = None

    def get_connect(self):
        '''

        :return:
        '''
        config = ConfigParser.ConfigParser()
        config.read('setting.cfg')
        mysql_config = {
            'host':config.get('mysql','host'),
            'user':config.get('mysql','user'),
            'password':config.get('mysql','password'),
            'port':config.get('mysql','port'),
            'database':config.get('mysql','database'),
            'charset':config.get('mysql','charset')
        }
        try:
            self.conn = connector.connect(**mysql_config)
            self.cursor = self.conn.cursor()
        except connector.Error as e:
            print 'connect fails!{}'.format(e)

    def close_connect(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def save_exchanges(self, exchanges_list):
        '''
        保存交易所
        :return:
        '''
        # self.get_connect()
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # del_history_sql = "update ccxt_exchanges set update_time = '{0}',is_delete='True' where is_delete='False'".format(now_time)
        # self.cursor.execute(del_history_sql)
        for exchanges in exchanges_list:
            save_sql = "insert into ccxt_exchanges(exchanges_name, add_time)values('{0}','{1}')".format(exchanges,now_time)
            self.cursor.execute(save_sql)
        self.conn.commit()
        # self.close_connect()

    def disable_exchanges(self, disable_exchanges):
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if len(disable_exchanges) > 1:
            sql = "update ccxt_exchanges set is_delete = 'True',update_time='{0}' where exchanges_name in {1}".format(now_time,str(tuple(disable_exchanges)))
        elif len(disable_exchanges) == 1:
            sql = "update ccxt_exchanges set is_delete = 'True',update_time='{0}' where exchanges_name={1}".format(now_time,disable_exchanges[0])
        self.cursor.execute(sql)
        self.conn.commit()


    def save_markets(self, exchanges, markets):
        '''
        保存币市场
        :return:
        '''
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        del_history_sql = "update ccxt_markets set update_time = '{0}',is_delete='True' where is_delete='False' and exchanges='{1}'".format(now_time,exchanges)
        self.cursor.execute(del_history_sql)
        for market in markets:
            if isinstance(markets, dict):
                market = markets[market]
            save_sql = "insert into ccxt_markets(market_id, base, quote, symbol, exchanges, add_time)values ('{0}','{1}','{2}','{3}'," \
                  "'{4}','{5}')".format(market['id'],market['base'],market['quote'],market['symbol'],exchanges,now_time)
            self.cursor.execute(save_sql)
        self.conn.commit()
        # self.close_connect()

    def get_symbol_exchanges(self, symbol):
        '''
        查询币所在交易所
        :param symbol:
        :return:
        '''
        #从币安，gateio，货币查询
        sql = "select a.id,a.market_id,a.base,a.quote,a.symbol,a.exchanges,a.add_time from ccxt_markets a left JOIN " \
              "ccxt_exchanges b on exchanges_name = exchanges where base='{0}' and quote in('btc','usdt') and b.`enable`='True' " \
              "and a.is_delete = 'False' and b.is_delete = 'False'".format(symbol)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        if not result: #从币安,gateio，火币没查询到，从其他平台查询
            sql = "select a.id,a.market_id,a.base,a.quote,a.symbol,a.exchanges,a.add_time from ccxt_markets a left JOIN " \
                  "ccxt_exchanges b on exchanges_name = exchanges where base='{0}' and quote in('btc','usdt') and b.`enable`='False' " \
                  "and a.is_delete = 'False' and b.is_delete = 'False'".format(
                symbol)
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        symbol_list = []
        num = 0
        for i in result:
            if num > 5:
                break
            symbol_list.append(dict(id=i[0],market_id=i[1],base=[2],quote=i[3],
                                    symbol=i[4],exchanges=i[5],add_time=i[6]))
            num += 1
        return symbol_list





