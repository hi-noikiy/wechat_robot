#coding:utf-8
import dataset
import ConfigParser
import os
import sys
import json

def strip_tags(html):
    """
    Python中过滤HTML标签的函数
    >>> str_text=strip_tags("<font color=red>hello</font>")
    >>> print str_text
    hello
    """
    from HTMLParser import HTMLParser
    html = html.strip()
    html = html.strip("\n")
    result = []
    parser = HTMLParser()
    parser.handle_data = result.append
    parser.feed(html)
    parser.close()
    return ''.join(result).strip()

def get_platform_msg(platform_name):
    cfg = ConfigParser.ConfigParser()
    #DIR_BASE = os.path.split( os.path.realpath( sys.argv[0] ) )[0]
    # parent_dir = os.path.dirname(DIR_BASE)
    cfg.read(os.path.join("../",'setting.cfg'))
    platform_dict = json.loads(cfg.get('platform', 'platform_dict'))
    mysql_host = cfg.get('mysql', 'host')
    mysql_user = cfg.get('mysql', 'user')
    mysql_password = cfg.get('mysql', 'password')
    mysql_port = cfg.get('mysql', 'port')
    mysql_database = cfg.get('mysql', 'database')
    mysql_charset = cfg.get('mysql', 'charset')
    db = dataset.connect('mysql://{0}:{1}@{2}/{3}?charset={4}'.format(mysql_user,mysql_password,mysql_host,mysql_database,mysql_charset))

    result = db.query("SELECT url,title,content FROM  "+platform_dict[platform_name] + " order by id desc limit 1")
    for row in result:
        return (row['url'],strip_tags(row['title']),strip_tags(row['content']))




if __name__ == '__main__':
   #send_msg_tmp = platform_msg.get_platform_msg(text)
   #send_msg = send_msg_tmp[1]+ "  \n详情:\n"+ send_msg_tmp[0]
   print  get_platform_msg(u"gateio")[2]
