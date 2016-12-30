#!/usr/bin/python
# -*- coding:utf-8 -*-
# check the current sotck price whether touch the target high or low price

__author__ = 'zhenghz'
import tushare as ts
import ConfigParser
from sendwx import sendwx
from cncurrency import cncurrency

def main():
    Config = ConfigParser.ConfigParser()
    Config.read("stock.ini")
    #df = ts.get_today_all()
    for stockid in Config.sections():
        high = float(Config.get(stockid,"high"))
        low = float(Config.get(stockid,"low"))
        has = Config.getboolean(stockid,"has")
        activate = Config.getboolean(stockid,"activate")
        print type(high),high,low,has,activate
        activate=True
        if activate:
            #trade = df.loc[df["code"]==stockid].iloc[0]["trade"]
            trade=15.44
            print trade
            if high!=0 and trade >= high:
                title = u"股票卖出提醒"
                highcn = cncurrency(high)
                tradecn = cncurrency(trade)
                desp = u"你持有的股票%s已经达到%s，高于预期价格%s，请尽快卖出" % (stockid,tradecn,highcn)
                sendwx(title,desp)
                activate=False
            if low!=0 and trade <= low:
                title = "股票卖出提醒"
                lowcn = cncurrency(low)
                tradecn = cncurrency(trade)
                desp = "你持有的股票%s已经达到%sxxxxxxxx低于预期价格%sxxxxxxx请尽快卖出" % (stockid,tradecn,lowcn)
                print title,desp
                sendwx(title,desp)
                activate=False
            if not activate:
                cfgfile = open("stock.ini",'w')
                Config.set(stockid,"activate",activate)
                Config.write(cfgfile)
                cfgfile.close()


if __name__ == '__main__':
    main()
