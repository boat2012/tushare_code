#!/usr/bin/python
# -*- coding:utf-8 -*-
# check the current sotck price whether touch the target high or low price

__author__ = 'zhenghz'
import tushare as ts
import ConfigParser
from sendwx import sendwx
from cncurrency import cncurrency
import logging
import sys
reload(sys)
sys.setdefaultencoding("utf8")

def main():
    logging.basicConfig(format="%(asctime)s -  %(message)s",filename="check_stock.log",level=logging.DEBUG)
    Config = ConfigParser.ConfigParser()
    Config.read("stock.ini")
    logging.debug("开始获取股票价格")
    df = ts.get_today_all()
    for stockid in Config.sections():
        high = float(Config.get(stockid,"high"))
        low = float(Config.get(stockid,"low"))
        has = Config.getboolean(stockid,"has")
        activate = Config.getboolean(stockid,"activate")
        #activate=True
        action = has and u"卖出" or u"买入"
        if activate:
            trade = df.loc[df["code"]==stockid].iloc[0]["trade"]
            #trade=25.44
            print trade
            if high!=0 and trade >= high:
                title = u"股票%s提醒" % action
                highcn = cncurrency(high)
                tradecn = cncurrency(trade)
                desp = u"你持有的股票%s已经达到%sxxxxxxx高于预期价格%sxxxxxxx请尽快%s" % (stockid,tradecn,highcn,action)
                sendwx(title,desp)
                activate=False
                logging.debug(title+":"+desp)
            if low!=0 and trade <= low:
                title = "股票%s提醒" % action
                lowcn = cncurrency(low)
                tradecn = cncurrency(trade)
                desp = "你持有的股票%s已经达到%sxxxxxxxxx低于预期价格%sxxxxxxxx请尽快%s" % (stockid,tradecn,lowcn,action)
                # print title,desp
                sendwx(title,desp)
                activate=False
                logging.debug(title+":"+desp)
            if not activate:
                cfgfile = open("stock.ini",'w')
                Config.set(stockid,"activate",activate)
                Config.write(cfgfile)
                cfgfile.close()
                logging.debug(stockid+"状态改变成失效")


if __name__ == '__main__':
    main()
