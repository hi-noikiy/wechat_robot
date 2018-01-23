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
            sql = "update ccxt_exchanges set enable = 'False',update_time='{0}' where exchanges_name in {1}".format(now_time,str(tuple(disable_exchanges)))
        elif len(disable_exchanges) == 1:
            sql = "update ccxt_exchanges set enable = 'False',update_time='{0}' where exchanges_name={1}".format(now_time,disable_exchanges[0])
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
        sql = "select id,market_id,base,quote,symbol,exchanges,add_time from ccxt_markets where " \
              "is_delete='False' and enable='True' and symbol='{0}'".format(symbol)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        symbol_list = []
        for i in result:
            symbol_list.append(dict(id=i['id'],market_id=i['market_id'],base=i['base'],quote=i['quote'],
                                    symbol=i['symbol'],exchanges=i['exchanges'],add_time=i['add_time']))
        return symbol_list





